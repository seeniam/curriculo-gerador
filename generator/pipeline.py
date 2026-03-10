from __future__ import annotations

import argparse
import os
import time
import unicodedata
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

from generator.io_utils import ensure_directory, find_job_files, find_latest_job_file, inline_css, read_text


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
) -> str:
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
"""


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


def build_output_path(output_dir: Path, job_file: Path) -> Path:
    company_slug = slugify_filename_part(job_file.stem)
    preferred_name = f"vaga-{company_slug}_neemias.html"
    preferred_path = output_dir / preferred_name
    if not preferred_path.exists():
        return preferred_path

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return output_dir / f"vaga-{company_slug}_neemias_{timestamp}.html"


def generate_for_job(
    *,
    job_file: Path,
    base_dir: Path,
    context: dict[str, Path],
    model: genai.GenerativeModel,
    career_master: str,
    raw_notes: str,
    template_html: str,
    template_css: str,
    persona_pt: str,
    persona_en: str,
    legacy_default_pt: str,
    legacy_default_en: str,
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
    )

    print(f"-> Generating ATS-friendly HTML resume for: {job_file.relative_to(base_dir)}")
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.2),
    )
    html_output = (
        response.text.replace("```html\n", "")
        .replace("```html", "")
        .replace("```", "")
        .strip()
    )

    ensure_directory(context["output_dir"])
    output_path = build_output_path(context["output_dir"], job_file)
    output_path.write_text(html_output, encoding="utf-8")

    print(f"[+] Saved as: {output_path}")


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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent.parent
    context = resolve_context(base_dir)

    print("====================================")
    print(" AI Tailored CV Generator           ")
    print("====================================")
    print("-> Architecture: Markdown source of truth + HTML template")

    load_dotenv(base_dir / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n[!] ERROR: API Key not found!")
        print(f"Please create a '.env' file in {base_dir}")
        print("Add the following line: GEMINI_API_KEY=your_api_key_here")
        print("You can get a free key at: https://aistudio.google.com/app/apikey\n")
        return

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

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

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
            )

        print("\n[+] SUCCESS! Resume generation completed.")
        print("-> Source of truth used: career/career_master.md\n")
    except Exception as exc:
        print(f"\n[-] An error occurred during Gemini API generation: {exc}")
