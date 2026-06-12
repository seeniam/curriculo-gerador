from __future__ import annotations

import sys
import os
from pathlib import Path

from flask import Flask, Response, abort, jsonify, render_template, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

from generator.ui_service import OUTPUT_DIR, generate_resume_from_description  # noqa: E402


app = Flask(__name__)


def access_token() -> str:
    return os.environ.get("APP_ACCESS_TOKEN", "").strip()


def is_production_runtime() -> bool:
    return bool(os.environ.get("PORT"))


def unauthorized_response() -> Response:
    return Response(
        "Autenticacao obrigatoria.",
        401,
        {"WWW-Authenticate": 'Basic realm="Gerador de Curriculo"'},
    )


@app.before_request
def require_private_access():
    token = access_token()
    if not token:
        if is_production_runtime():
            return Response("APP_ACCESS_TOKEN nao configurado.", 503)
        return None

    auth = request.authorization
    header_token = request.headers.get("X-App-Token", "")
    query_token = request.args.get("token", "")
    supplied_token = auth.password if auth else header_token or query_token

    if supplied_token != token:
        return unauthorized_response()

    return None


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
