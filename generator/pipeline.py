from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import time
import unicodedata
from pathlib import Path

from generator.io_utils import ensure_directory, find_job_files, find_latest_job_file, inline_css, read_text


FORBIDDEN_PHRASES = (
    "AI-Enabled Products",
    "Superior completo em andamento no histórico informado",
    "Superior completo em andamento no historico informado",
)

WHATSAPP_URL = (
    "https://api.whatsapp.com/send/?phone=5598982975194&text=Ol%C3%A1%2C+"
    "gostaria+de+falar+com+voc%C3%AA+sobre+uma+vaga...&type=phone_number&app_absent=0"
)

ONE_PAGE_CSS = """
html[data-layout="one-page"] {
    font-size: 12px;
}

html[data-layout="one-page"] body {
    line-height: 1.18;
    background: #fff;
}

html[data-layout="one-page"] .resume-shell {
    max-width: 794px;
    padding: 12px 16px 14px;
    border-radius: 0;
    box-shadow: none;
}

html[data-layout="one-page"] .resume-header {
    margin-bottom: 8px;
    padding-bottom: 6px;
}

html[data-layout="one-page"] .resume-header h1 {
    font-size: 1.48rem;
    line-height: 1.05;
}

html[data-layout="one-page"] .headline {
    margin: 4px 0 3px;
    font-size: 0.91rem;
}

html[data-layout="one-page"] .contact-line,
html[data-layout="one-page"] .meta,
html[data-layout="one-page"] .submeta {
    font-size: 0.84rem;
}

html[data-layout="one-page"] section {
    margin-bottom: 7px;
}

html[data-layout="one-page"] h2 {
    margin-bottom: 4px;
    padding-bottom: 2px;
    font-size: 0.84rem;
}

html[data-layout="one-page"] h3 {
    margin-bottom: 1px;
    font-size: 0.9rem;
}

html[data-layout="one-page"] p {
    margin-bottom: 4px;
}

html[data-layout="one-page"] ul {
    margin-top: 2px;
    padding-left: 15px;
}

html[data-layout="one-page"] li {
    margin-bottom: 1px;
}

html[data-layout="one-page"] article {
    margin-bottom: 5px;
    padding: 0;
}

html[data-layout="one-page"] .item-header {
    gap: 10px;
}

html[data-layout="one-page"] .item-header .meta {
    font-size: 0.82rem;
}

@media print {
    @page {
        size: A4;
        margin: 8mm;
    }

    html[data-layout="one-page"] .resume-shell {
        max-width: none;
        padding: 0;
        border: 0;
        border-radius: 0;
        box-shadow: none;
    }
}
""".strip()


def resolve_context(base_dir: Path) -> dict[str, Path]:
    return {
        "career_master": base_dir / "career" / "career_master.md",
        "raw_notes": base_dir / "career" / "raw_notes.md",
        "template_html": base_dir / "templates" / "resume_base.html",
        "template_css": base_dir / "templates" / "resume.css",
        "persona_pt": base_dir / "generator" / "persona_headhunter_pt.md",
        "persona_en": base_dir / "generator" / "persona_headhunter_en.md",
        "legacy_default_pt": base_dir / "legacy" / "default_pt.html",
        "legacy_default_en": base_dir / "legacy" / "default.html",
        "portfolio_visual": base_dir / "portfolio-visual.pdf",
        "output_dir": base_dir / "output",
    }


def build_prompt(
    career_master: str,
    raw_notes: str,
    job_description: str,
    persona_pt: str,
    persona_en: str,
    rendered_template: str,
    legacy_default_pt: str,
    legacy_default_en: str,
    one_page: bool,
) -> str:
    layout_rules = """
9. Keep the content density balanced for a strong professional resume.
""".strip()
    if one_page:
        layout_rules = """
9. This resume must fit on exactly one A4 page when printed to PDF.
10. Prioritize only the most relevant content for the target job.
11. Prefer shorter summaries, fewer bullets, tighter wording, and omitting lower-priority sections when needed to keep it on one page.
12. Do not fake compactness with unreadable text. Keep it credible, readable, and professional.
13. Use a compact structure similar to: header, professional summary, core skills, technical skills, experience, selected projects, education, courses/certifications.
14. Keep education and certifications visually separated at the end, not merged into a single paragraph.
""".strip()

    return f"""
You are generating an ATS-friendly HTML resume.

Use the correct persona according to the language of the target job description:
- Portuguese job description => use the Portuguese persona.
- English job description => use the English persona.

The source of truth is the Markdown career master. The HTML files in legacy are reference material only.

===== CAREER MASTER (SOURCE OF TRUTH) =====
{career_master}

===== RAW NOTES (OPTIONAL, MAY BE PARTIAL OR MESSY) =====
{raw_notes}

===== TARGET JOB DESCRIPTION =====
{job_description}

===== PERSONA (PORTUGUESE) =====
{persona_pt}

===== PERSONA (ENGLISH) =====
{persona_en}

===== HTML TEMPLATE TO FOLLOW =====
{rendered_template}

===== LEGACY HTML REFERENCE (PORTUGUESE) =====
{legacy_default_pt}

===== LEGACY HTML REFERENCE (ENGLISH) =====
{legacy_default_en}

===== OUTPUT RULES =====
1. Generate ONLY the final HTML.
2. Do not include markdown fences.
3. Never use markdown syntax inside the HTML, especially `**bold**`. Use `<strong>` instead.
3. Keep the document ATS-friendly:
   - single column
   - semantic headings
   - simple lists
   - no tables for layout
   - no decorative icons or graphics
   - no multi-column layout
4. Follow the provided template structure and CSS direction.
5. Use the career master as the primary truth source.
6. Never invent facts. If information is missing, omit it gracefully or keep conservative placeholders only if strictly necessary.
7. Preserve professional credibility and natural language.
8. Ensure the final document is printable and clean.
{layout_rules}
"""


def normalize_whatsapp_contact(html_output: str) -> str:
    phone_link_pattern = re.compile(
        r'<a\s+href=["\']tel:\+?5598982975194["\']>\s*(?:\+55\s*)?98\s*98297[-\s]?5194\s*</a>',
        flags=re.IGNORECASE,
    )
    html_output = phone_link_pattern.sub(
        f'<a href="{WHATSAPP_URL}">WhatsApp</a>',
        html_output,
    )

    whatsapp_link_pattern = re.compile(
        r'<a\s+href=["\']https://api\.whatsapp\.com/send/\?phone=5598982975194(?:[^"\']*)?["\']>\s*(?:Whatsapp|WhatsApp|\+55\s*98\s*98297[-\s]?5194)\s*</a>',
        flags=re.IGNORECASE,
    )
    return whatsapp_link_pattern.sub(
        f'<a href="{WHATSAPP_URL}">WhatsApp</a>',
        html_output,
    )


def sanitize_html_output(html_output: str) -> str:
    sanitized = (
        html_output.replace("```html\n", "")
        .replace("```html", "")
        .replace("```", "")
        .strip()
    )
    sanitized = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", sanitized, flags=re.DOTALL)

    for phrase in FORBIDDEN_PHRASES:
        sanitized = sanitized.replace(phrase, "")

    sanitized = re.sub(r"\s+\|\s+\|", " |", sanitized)
    sanitized = re.sub(r"\|\s*</", "</", sanitized)
    sanitized = re.sub(r">\s*\|\s*", "> ", sanitized)
    sanitized = normalize_whatsapp_contact(sanitized)
    sanitized = re.sub(r"\(\s*\)", "", sanitized)
    sanitized = re.sub(r"\s{2,}", " ", sanitized)
    return sanitized


def append_css_override(html_output: str, css_text: str) -> str:
    if not css_text.strip():
        return html_output

    style_close_tag = "</style>"
    if style_close_tag in html_output:
        return html_output.replace(style_close_tag, f"\n{css_text}\n{style_close_tag}", 1)

    head_close_tag = "</head>"
    if head_close_tag in html_output:
        return html_output.replace(head_close_tag, f"<style>\n{css_text}\n</style>\n{head_close_tag}", 1)

    return html_output


def apply_layout_mode(html_output: str, *, one_page: bool) -> str:
    if not one_page:
        return html_output

    html_output = re.sub(
        r"<html(\s[^>]*)?>",
        lambda match: (
            "<html data-layout=\"one-page\">"
            if not match.group(1)
            else (
                match.group(0)
                if "data-layout=" in match.group(0)
                else f"<html{match.group(1)} data-layout=\"one-page\">"
            )
        ),
        html_output,
        count=1,
        flags=re.IGNORECASE,
    )
    return append_css_override(html_output, ONE_PAGE_CSS)


def validate_html_output(html_output: str) -> list[str]:
    warnings: list[str] = []

    if "**" in html_output:
        warnings.append("markdown bold syntax detected in HTML output")
    if "```" in html_output:
        warnings.append("markdown fence detected in HTML output")
    if "<html" not in html_output.lower():
        warnings.append("missing <html> tag in output")
    if not html_output.lstrip().lower().startswith("<!doctype html>") and "<html" not in html_output[:200].lower():
        warnings.append("output does not clearly start as an HTML document")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in html_output:
            warnings.append(f"forbidden phrase detected: {phrase}")

    return warnings


def load_local_env(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


class CodexCliResumeModel:
    def __init__(self, *, base_dir: Path, model: str | None = None, profile: str | None = None) -> None:
        self.base_dir = base_dir
        self.model = model
        self.profile = profile
        self.executable = self.resolve_executable()

    def resolve_executable(self) -> str | None:
        configured_path = os.getenv("CODEX_CLI_PATH")
        if configured_path and Path(configured_path).exists():
            return configured_path

        path_executable = shutil.which("codex")
        if path_executable:
            return path_executable

        if os.name != "nt":
            return None

        home_dir = Path.home()
        extension_roots = [
            home_dir / ".vscode" / "extensions",
            home_dir / ".cursor" / "extensions",
            home_dir / ".vscode-insiders" / "extensions",
        ]
        matches: list[Path] = []
        for root in extension_roots:
            if root.exists():
                matches.extend(root.glob("openai.chatgpt-*/bin/windows-x86_64/codex.exe"))

        if not matches:
            return None

        newest_match = max(matches, key=lambda path: path.stat().st_mtime)
        return str(newest_match)

    def is_available(self) -> bool:
        return bool(self.executable)

    def generate_html(self, prompt: str) -> str:
        if not self.executable:
            raise RuntimeError("Codex CLI was not found in PATH.")

        codex_prompt = f"""
You are the resume generation engine for this local application.

Return only the final HTML requested below. Do not inspect or edit files. Do not run shell commands.
The application already included all source material in the prompt.

{prompt}
""".strip()

        temp_dir = self.base_dir / "output" / ".codex-cli"
        ensure_directory(temp_dir)
        output_path = temp_dir / f"codex-final-message-{time.strftime('%Y%m%d_%H%M%S')}.html"
        command = [
            self.executable,
            "exec",
            "-",
            "--cd",
            str(self.base_dir),
            "--sandbox",
            "read-only",
            "--ephemeral",
            "--color",
            "never",
            "--output-last-message",
            str(output_path),
        ]
        if self.model:
            command.extend(["--model", self.model])
        if self.profile:
            command.extend(["--profile", self.profile])

        result = subprocess.run(
            command,
            input=codex_prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=300,
        )

        if result.returncode != 0:
            error_output = result.stderr.strip() or result.stdout.strip() or "unknown Codex CLI error"
            raise RuntimeError(error_output)

        if output_path.exists():
            final_message = output_path.read_text(encoding="utf-8").strip()
            if final_message:
                try:
                    output_path.unlink()
                except OSError:
                    pass
                return final_message

        return result.stdout.strip()


def slugify_filename_part(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_value.lower()

    for prefix in ("vaga_", "vaga-", "job_", "job-"):
        if lowered.startswith(prefix):
            lowered = lowered[len(prefix):]
            break

    cleaned = []
    last_was_separator = False
    for char in lowered:
        if char.isalnum():
            cleaned.append(char)
            last_was_separator = False
        else:
            if not last_was_separator:
                cleaned.append("-")
                last_was_separator = True

    slug = "".join(cleaned).strip("-")
    return slug or "empresa"


def build_output_path(output_dir: Path, job_file: Path, *, one_page: bool, output_name: str | None) -> Path:
    if output_name:
        requested_name = Path(output_name).name
        preferred_name = str(Path(requested_name).with_suffix(".html"))
        return output_dir / preferred_name
    else:
        company_slug = slugify_filename_part(job_file.stem)
        suffix = "_1pagina" if one_page else ""
        preferred_name = f"curriculo-{company_slug}_neemias{suffix}.html"

    preferred_path = output_dir / preferred_name
    if not preferred_path.exists():
        return preferred_path

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return output_dir / f"{preferred_path.stem}_{timestamp}.html"


def build_pdf_output_path(html_output_path: Path) -> Path:
    return html_output_path.with_suffix(".pdf")


def find_browser_executable() -> str | None:
    browser_candidates = (
        "msedge",
        "chrome",
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    )

    for candidate in browser_candidates:
        resolved = shutil.which(candidate) if "\\" not in candidate else candidate
        if resolved and Path(resolved).exists():
            return resolved

    return None


def run_browser_pdf_export(
    *,
    browser_executable: str,
    html_output_path: Path,
    pdf_output_path: Path,
    browser_profile_dir: Path,
) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        html_path_escaped = str(html_output_path.resolve()).replace("'", "''")
        pdf_path_escaped = str(pdf_output_path.resolve()).replace("'", "''")
        profile_path_escaped = str(browser_profile_dir.resolve()).replace("'", "''")
        browser_path_escaped = browser_executable.replace("'", "''")
        powershell_command = (
            f"$html = Resolve-Path '{html_path_escaped}'; "
            f"$pdf = '{pdf_path_escaped}'; "
            f"$profile = '{profile_path_escaped}'; "
            "New-Item -ItemType Directory -Force -Path $profile | Out-Null; "
            f"& '{browser_path_escaped}' '--headless=new' '--disable-gpu' '--no-first-run' "
            "'--disable-crash-reporter' '--disable-breakpad' '--no-default-browser-check' "
            "\"--user-data-dir=$profile\" '--no-pdf-header-footer' '--print-to-pdf-no-header' "
            "\"--print-to-pdf=$pdf\" $html.Path"
        )
        return subprocess.run(
            ["powershell", "-Command", powershell_command],
            capture_output=True,
            text=True,
            check=False,
            timeout=45,
        )

    command = [
        browser_executable,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--disable-crash-reporter",
        "--disable-breakpad",
        "--no-default-browser-check",
        f"--user-data-dir={browser_profile_dir.resolve()}",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_output_path.resolve()}",
        html_output_path.resolve().as_uri(),
    ]
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        timeout=45,
    )


def export_html_to_pdf(html_output_path: Path) -> Path | None:
    browser_executable = find_browser_executable()
    if not browser_executable:
        print("[!] PDF export skipped: Chrome/Chromium/Edge executable not found.")
        return None

    pdf_output_path = build_pdf_output_path(html_output_path)
    browser_profile_dir = html_output_path.parent / ".browser-profile"
    ensure_directory(browser_profile_dir)

    try:
        result = run_browser_pdf_export(
            browser_executable=browser_executable,
            html_output_path=html_output_path,
            pdf_output_path=pdf_output_path,
            browser_profile_dir=browser_profile_dir,
        )
    except OSError as exc:
        print(f"[!] PDF export skipped: failed to start browser ({exc}).")
        return None
    except subprocess.TimeoutExpired:
        print("[!] PDF export skipped: browser timed out while generating PDF.")
        return None

    if result.returncode != 0:
        error_output = result.stderr.strip() or result.stdout.strip() or "unknown browser error"
        print(f"[!] PDF export failed: {error_output}")
        return None

    if not pdf_output_path.exists():
        print("[!] PDF export failed: browser finished without creating the PDF file.")
        return None

    return pdf_output_path


def cleanup_browser_profile(output_dir: Path) -> None:
    browser_profile_dir = output_dir / ".browser-profile"
    if not browser_profile_dir.exists():
        return

    for attempt in range(3):
        try:
            shutil.rmtree(browser_profile_dir)
            print(f"[+] Browser temporary profile removed: {browser_profile_dir.name}")
            return
        except OSError:
            if attempt == 2:
                print(f"[!] Could not remove browser temporary profile: {browser_profile_dir}")
                return
            time.sleep(1)


def append_portfolio_to_pdf(pdf_output_path: Path, portfolio_path: Path) -> Path | None:
    if not portfolio_path.exists():
        print(f"[!] Portfolio append skipped: {portfolio_path.name} not found.")
        return None

    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("[!] Portfolio append skipped: install pypdf with 'pip install pypdf'.")
        return None

    merged_output_path = pdf_output_path.with_suffix(".merged.pdf")
    writer = PdfWriter()

    try:
        for source_path in (pdf_output_path, portfolio_path):
            reader = PdfReader(str(source_path))
            for page in reader.pages:
                writer.add_page(page)

        with merged_output_path.open("wb") as output_file:
            writer.write(output_file)

        merged_output_path.replace(pdf_output_path)
        return pdf_output_path
    except Exception as exc:
        if merged_output_path.exists():
            try:
                merged_output_path.unlink()
            except OSError:
                pass
        print(f"[!] Portfolio append failed: {exc}")
        return None


def generate_for_job(
    *,
    job_file: Path,
    base_dir: Path,
    context: dict[str, Path],
    model: CodexCliResumeModel,
    career_master: str,
    raw_notes: str,
    template_html: str,
    template_css: str,
    persona_pt: str,
    persona_en: str,
    legacy_default_pt: str,
    legacy_default_en: str,
    one_page: bool,
    output_name: str | None,
    pdf_only: bool,
    append_portfolio: bool,
) -> None:
    job_description = read_text(job_file)
    if not job_description:
        print(f"[-] Skipping empty job file: {job_file.relative_to(base_dir)}")
        return

    rendered_template = inline_css(template_html, template_css)
    prompt = build_prompt(
        career_master=career_master,
        raw_notes=raw_notes,
        job_description=job_description,
        persona_pt=persona_pt,
        persona_en=persona_en,
        rendered_template=rendered_template,
        legacy_default_pt=legacy_default_pt,
        legacy_default_en=legacy_default_en,
        one_page=one_page,
    )

    print(f"-> Generating ATS-friendly HTML resume for: {job_file.relative_to(base_dir)}")
    html_output = sanitize_html_output(model.generate_html(prompt))
    html_output = apply_layout_mode(html_output, one_page=one_page)
    warnings = validate_html_output(html_output)

    ensure_directory(context["output_dir"])
    output_path = build_output_path(
        context["output_dir"],
        job_file,
        one_page=one_page,
        output_name=output_name,
    )
    output_path.write_text(html_output, encoding="utf-8")

    print(f"[+] Saved as: {output_path}")
    pdf_output_path = export_html_to_pdf(output_path)
    if pdf_output_path:
        if append_portfolio:
            appended_pdf_path = append_portfolio_to_pdf(pdf_output_path, context["portfolio_visual"])
            if appended_pdf_path:
                print(f"[+] Portfolio appended from: {context['portfolio_visual']}")
        print(f"[+] PDF saved as: {pdf_output_path}")
        if pdf_only:
            try:
                output_path.unlink()
                print(f"[+] Temporary HTML removed: {output_path.name}")
            except OSError as exc:
                print(f"[!] Could not remove temporary HTML: {exc}")
            cleanup_browser_profile(context["output_dir"])
    for warning in warnings:
        print(f"[!] Output warning for {job_file.name}: {warning}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate ATS-friendly resumes from job descriptions.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate one resume for each vaga*.md/job*.md file found.",
    )
    parser.add_argument(
        "--job",
        type=str,
        help="Generate only for a specific job file path.",
    )
    parser.add_argument(
        "--one-page",
        action="store_true",
        help="Generate a compact resume intended to fit on a single A4 page before exporting to PDF.",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        help="Force the generated output file name for a single job, for example curriculo-frontend_neemias.pdf.",
    )
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="Keep only the generated PDF and remove the intermediate HTML after export.",
    )
    parser.add_argument(
        "--no-portfolio",
        action="store_true",
        help="Do not append portfolio-visual.pdf to the generated resume PDF.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent.parent
    context = resolve_context(base_dir)

    print("====================================")
    print(" Codex Tailored CV Generator        ")
    print("====================================")
    print("-> Architecture: Markdown source of truth + HTML template")
    if args.one_page:
        print("-> Layout mode: one-page compact resume (HTML first, PDF after)")

    load_local_env(base_dir / ".env")

    if args.job:
        requested_job = Path(args.job)
        job_files = [requested_job if requested_job.is_absolute() else base_dir / requested_job]
    elif args.all:
        job_files = find_job_files(base_dir)
    else:
        latest_job = find_latest_job_file(base_dir)
        job_files = [latest_job] if latest_job else []

    if not job_files:
        print("No job description file found. Add a file named 'vaga*.md' or 'job*.md'.")
        print("Searched in: project root, jobs/, and legacy/.")
        return

    if args.all:
        if args.output_name:
            print("[!] --output-name is ignored when using --all.")
        print("-> Job files detected:")
        for job_file in job_files:
            print(f"   - {job_file.relative_to(base_dir)}")
    else:
        print(f"-> Job description selected: {job_files[0].relative_to(base_dir)}")

    career_master = read_text(context["career_master"])
    raw_notes = read_text(context["raw_notes"])
    template_html = read_text(context["template_html"])
    template_css = read_text(context["template_css"])
    persona_pt = read_text(context["persona_pt"])
    persona_en = read_text(context["persona_en"])
    legacy_default_pt = read_text(context["legacy_default_pt"])
    legacy_default_en = read_text(context["legacy_default_en"])

    required_blocks = {
        "career/career_master.md": career_master,
        "templates/resume_base.html": template_html,
        "templates/resume.css": template_css,
        "generator/persona_headhunter_pt.md": persona_pt,
        "generator/persona_headhunter_en.md": persona_en,
    }
    missing = [name for name, content in required_blocks.items() if not content]
    if missing:
        print("ERROR: One or more required files are missing or empty:")
        for item in missing:
            print(f" - {item}")
        return

    model = CodexCliResumeModel(
        base_dir=base_dir,
        model=os.getenv("CODEX_MODEL"),
        profile=os.getenv("CODEX_PROFILE"),
    )
    if not model.is_available():
        print("\n[!] ERROR: Codex CLI not found!")
        print("Install/login to Codex CLI, then run this generator again.")
        print("Optional .env settings: CODEX_MODEL and CODEX_PROFILE\n")
        return

    try:
        for job_file in job_files:
            generate_for_job(
                job_file=job_file,
                base_dir=base_dir,
                context=context,
                model=model,
                career_master=career_master,
                raw_notes=raw_notes,
                template_html=template_html,
                template_css=template_css,
                persona_pt=persona_pt,
                persona_en=persona_en,
                legacy_default_pt=legacy_default_pt,
                legacy_default_en=legacy_default_en,
                one_page=args.one_page,
                output_name=None if args.all else args.output_name,
                pdf_only=args.pdf_only,
                append_portfolio=not args.no_portfolio,
            )

        print("\n[+] SUCCESS! Resume generation completed.")
        print("-> Source of truth used: career/career_master.md\n")
    except Exception as exc:
        print(f"\n[-] An error occurred during Codex generation: {exc}")
