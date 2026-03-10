import glob
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""


def find_job_files(base_dir: Path) -> list[Path]:
    search_roots = [
        base_dir / "jobs",
        base_dir,
        base_dir / "legacy",
    ]
    patterns = ("vaga*.md", "job*.md")

    matches: list[Path] = []
    for root in search_roots:
        if not root.exists():
            continue
        for pattern in patterns:
            matches.extend(Path(p) for p in glob.glob(str(root / pattern)))

    unique_matches = sorted(set(matches), key=lambda path: path.stat().st_mtime, reverse=True)
    return unique_matches


def find_latest_job_file(base_dir: Path) -> Path | None:
    matches = find_job_files(base_dir)
    if not matches:
        return None

    return matches[0]


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def inline_css(template_html: str, css_text: str) -> str:
    return template_html.replace("{{INLINE_CSS}}", css_text)
