from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from generator.ui_service import OUTPUT_DIR, generate_resume_from_description  # noqa: E402


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    payload = request.get_json(silent=True) or {}
    job_title = str(payload.get("jobTitle", "")).strip()
    company = str(payload.get("company", "")).strip()
    description = str(payload.get("description", "")).strip()

    if not description:
        return jsonify({"ok": False, "error": "Cole a descricao da vaga antes de gerar."}), 400

    try:
        result = generate_resume_from_description(job_title, company, description)
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500

    pdf_name = result["pdf_name"]
    return jsonify(
        {
            "ok": True,
            "pdfName": pdf_name,
            "pdfPath": result["pdf_file"],
            "jobFile": result["job_file"],
            "downloadUrl": f"/output/{pdf_name}",
        }
    )


@app.get("/output/<path:filename>")
def output_file(filename: str):
    requested = (OUTPUT_DIR / filename).resolve()
    output_root = OUTPUT_DIR.resolve()
    if output_root not in requested.parents or requested.suffix.lower() != ".pdf":
        abort(404)
    if not requested.exists():
        abort(404)
    return send_from_directory(output_root, requested.name, as_attachment=False)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
