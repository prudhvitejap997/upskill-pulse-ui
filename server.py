"""Upskill Pulse — server with Groq AI + offline fallback."""
import io
import json
import os

import pypdf
import requests
from flask import Flask, jsonify, request, send_from_directory

from question_bank import generate_questions as offline_questions

PORT = int(os.environ.get("PORT", 3000))
DIR  = os.path.dirname(os.path.abspath(__file__))

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

app = Flask(__name__)

SYSTEM_PROMPT = """You are a senior software engineer writing a technical quiz for experienced developers.

Return ONLY a valid JSON array — no markdown fences, no explanation — with this exact structure:
[
  {
    "question": "Full question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,
    "topic": "Specific subtopic from the material",
    "type": "Code Output"
  }
]

CRITICAL RULES — follow every one:
- "correct" is the 0-based index of the correct answer
- "type" MUST be exactly one of: "Code Output", "Error Prediction", "Concept", "Syntax", "Comparison", "Behavior"
- Generate exactly the requested number of questions
- Base ALL questions strictly on the provided study material — quote exact function names, class names, values, and behaviour from it
- NEVER ask about history, purpose, context, or "what is X used for" — those are not technical questions
- Every question must test PRECISION: exact return values, specific error types, exact syntax, subtle edge cases, real behavioural differences between similar constructs
- Rotate through question types — do not repeat the same type back-to-back
- Preferred patterns:
    * Code Output      → "What does this code return?" (include inline code)
    * Error Prediction → "Which of the following will raise an exception?"
    * Concept          → "Which statement about [function/class] is TRUE?"
    * Syntax           → "Which call signature is correct for [function]?"
    * Comparison       → "What is the difference between X and Y?"
    * Behavior         → "What happens when [edge case]?"
- Distractors must be technically plausible — wrong by a subtle detail, not obviously nonsense
- Difficulty mapping:
    easy   → correct usage of APIs, basic syntax, common return types
    medium → edge cases, subtle differences, less-known parameters, error conditions
    hard   → tricky interactions, non-obvious defaults, order-of-operations, corner cases a senior dev might get wrong"""


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


def build_user_message(topic, difficulty, question_count, content):
    if content:
        return (
            f"Topic: {topic}\n"
            f"Difficulty: {difficulty}\n"
            f"Number of questions: {question_count}\n\n"
            f"Study material (read carefully — every question must come from this):\n"
            f"{content[:30000]}\n\n"
            f"Generate {question_count} {difficulty}-difficulty TECHNICAL questions. "
            f"Each question must reference specific functions, classes, methods, syntax, "
            f"return values, or behaviours found in the material above. "
            f"Do NOT ask generic or conceptual questions."
        )
    return (
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n"
        f"Number of questions: {question_count}\n\n"
        f"Generate {question_count} {difficulty}-difficulty TECHNICAL questions about \"{topic}\" — "
        f"focus on exact syntax, API behaviour, edge cases, and code-level precision. "
        f"No conceptual or high-level questions."
    )


def call_groq(user_msg):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model":    GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_msg},
        ],
        "temperature": 0.4,
        "max_tokens":  4096,
    }
    resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=90)
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"]
    start = raw.find("[")
    end   = raw.rfind("]") + 1
    return json.loads(raw[start:end])


@app.route("/")
def index():
    return send_from_directory(DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(DIR, filename)


@app.route("/api/generate-quiz", methods=["POST"])
def generate_quiz():
    topic          = request.form.get("topic", "").strip()
    difficulty     = request.form.get("difficulty", "medium")
    question_count = int(request.form.get("questionCount", 10))
    files          = request.files.getlist("files")

    chunks = []
    for f in files:
        text = extract_text(f).strip()
        if text:
            chunks.append(f"=== {f.filename} ===\n{text}")
    content = "\n\n".join(chunks) if chunks else None

    user_msg  = build_user_message(topic, difficulty, question_count, content)
    user_tops = [t.strip() for t in topic.split("|") if t.strip()]

    try:
        questions = call_groq(user_msg)
        source = "groq"
    except Exception as e:
        print(f"[Groq failed: {e}] — falling back to offline bank")
        questions = offline_questions(user_tops, question_count)
        source = "offline"

    return jsonify({"questions": questions, "source": source})


@app.errorhandler(Exception)
def handle_error(e):
    import traceback
    return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == "__main__":
    local = os.environ.get("PORT") is None
    if local:
        import webbrowser
        print(f"\n  Upskill Pulse running at  ->  http://localhost:{PORT}\n")
        print(f"  Using Groq model: {GROQ_MODEL}\n")
        webbrowser.open(f"http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
