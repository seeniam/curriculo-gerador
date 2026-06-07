from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LEGACY_DIR = BASE_DIR / "legacy"
OUTPUT_DIR = BASE_DIR / "output"

INVALID_FILENAME_CHARS = r'<>:"/\|?*'


def sanitize_filename(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = "".join("-" if char in INVALID_FILENAME_CHARS else char for char in ascii_value)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s*-\s*", " - ", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    return cleaned.strip(" .-") or "vaga"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value)
    return slug.strip("-") or "vaga"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem} - {index}{path.suffix}")
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"Could not create a unique filename for {path.name}")


def build_resume_filename(job_title: str, company: str) -> str:
    title = sanitize_filename(job_title or "Curriculo personalizado")
    company_name = sanitize_filename(company)
    parts = ["Curriculo", title]
    if company_name and company_name != "vaga":
        parts.append(company_name)
    parts.append("Neemias")
    return sanitize_filename(" - ".join(parts)) + ".pdf"


def save_job_description(job_title: str, company: str, description: str) -> Path:
    if not description or not description.strip():
        raise ValueError("A descricao da vaga e obrigatoria.")

    LEGACY_DIR.mkdir(parents=True, exist_ok=True)
    title = sanitize_filename(job_title or "Vaga personalizada")
    company_name = sanitize_filename(company)
    slug_source = f"{title} {company_name}".strip()
    job_path = unique_path(LEGACY_DIR / f"vaga-{slugify(slug_source)}.md")

    content = [
        f"# {title}",
        "",
    ]
    if company_name and company_name != "vaga":
        content.extend([f"Empresa: {company_name}", ""])
    content.extend(["## Descricao da vaga", "", description.strip(), ""])

    job_path.write_text("\n".join(content), encoding="utf-8")
    return job_path


def generate_resume_from_description(job_title: str, company: str, description: str) -> dict[str, str]:
    job_path = save_job_description(job_title, company, description)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    requested_pdf_name = build_resume_filename(job_title, company)
    pdf_path = unique_path(OUTPUT_DIR / requested_pdf_name)

    command = [
        sys.executable,
        "gerador_de_cv.py",
        "--job",
        str(job_path.relative_to(BASE_DIR)),
        "--one-page",
        "--pdf-only",
        "--no-portfolio",
        "--output-name",
        pdf_path.name,
    ]

    result = subprocess.run(
        command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Falha ao gerar curriculo.")

    if not pdf_path.exists():
        raise RuntimeError("A pipeline terminou, mas o PDF final nao foi encontrado.")

    return {
        "job_file": str(job_path),
        "pdf_file": str(pdf_path),
        "pdf_name": pdf_path.name,
        "stdout": result.stdout.strip(),
    }
