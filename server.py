"""Upskill Pulse — demo server (offline mode, no API key needed)."""
import io
import os

import pypdf
from flask import Flask, jsonify, request, send_from_directory

from question_bank import generate_questions

PORT = int(os.environ.get("PORT", 3000))
DIR  = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


def extract_text(file_storage) -> str:
    name = file_storage.filename or ""
    data = file_storage.read()
    if name.lower().endswith(".pdf"):
        try:
            reader = pypdf.PdfReader(io.BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""
    return data.decode("utf-8", errors="ignore")


@app.route("/")
def index():
    return send_from_directory(DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(DIR, filename)


@app.route("/api/generate-quiz", methods=["POST"])
def generate_quiz():
    topic          = request.form.get("topic", "").strip()
    question_count = int(request.form.get("questionCount", 10))
    files          = request.files.getlist("files")

    # Read uploaded files (not used for AI, just logged so you can mention the feature)
    for f in files:
        _ = extract_text(f)

    user_topics = [t.strip() for t in topic.split("|") if t.strip()]
    questions = generate_questions(user_topics, question_count)

    return jsonify({"questions": questions})


@app.errorhandler(Exception)
def handle_error(e):
    import traceback
    return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == "__main__":
    local = os.environ.get("PORT") is None
    if local:
        import webbrowser
        print(f"\n  Upskill Pulse running at  ->  http://localhost:{PORT}\n")
        webbrowser.open(f"http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
