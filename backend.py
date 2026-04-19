import os
import json
import random
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)
client = anthropic.Anthropic()


def extract_text(file):
    name = file.filename.lower()
    if name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return file.read().decode("utf-8", errors="ignore")


def get_random_chunk(text, chunk_size=8000):
    """Return a random portion of the document so Claude focuses on different sections."""
    words = text.split()
    if len(words) <= chunk_size // 5:
        return text  # short doc — use all of it
    start = random.randint(0, max(0, len(words) - chunk_size // 5))
    chunk = " ".join(words[start: start + chunk_size // 5])
    # Always include a random earlier section too for variety
    if start > 100:
        prefix_start = random.randint(0, start - 1)
        prefix = " ".join(words[prefix_start: prefix_start + 200])
        return prefix + "\n...\n" + chunk
    return chunk


QUESTION_STYLES = [
    ("What is", "definition"),
    ("Which of the following best describes", "conceptual"),
    ("According to the document, why", "reasoning"),
    ("What happens when", "cause-effect"),
    ("How does X differ from Y", "comparison"),
    ("Which example best illustrates", "application"),
    ("What is the main purpose of", "purpose"),
    ("Based on the document, what would happen if", "inference"),
]


@app.route("/api/generate-quiz", methods=["POST"])
def generate_quiz():
    topic      = request.form.get("topic", "General Knowledge")
    difficulty = request.form.get("difficulty", "medium")
    count      = int(request.form.get("questionCount", 10))
    files      = request.files.getlist("files")

    doc_text = ""
    for f in files:
        doc_text += f"\n\n--- {f.filename} ---\n" + extract_text(f)

    if not doc_text.strip():
        return jsonify({"error": "No readable text found in uploaded files."}), 400

    # Pick a random section of the document to focus on
    doc_section = get_random_chunk(doc_text, chunk_size=12000)

    # Pick random question styles for this session
    styles = random.sample(QUESTION_STYLES, min(5, len(QUESTION_STYLES)))
    style_desc = ", ".join(f'"{s[0]}..." ({s[1]})' for s in styles)

    seed = random.randint(10000, 99999)

    prompt = f"""You are a quiz generator. Session ID: {seed}.

Using ONLY the document section below, generate exactly {count} multiple-choice questions about: {topic}
Difficulty: {difficulty}

IMPORTANT — to ensure variety, use these question starter styles this session:
{style_desc}

Rules:
- Each question must have exactly 4 options (A, B, C, D)
- Exactly one correct answer (index 0–3)
- Every question must be answerable from the document text below
- Do NOT ask about topics not mentioned in the document
- Make questions genuinely different from each other — cover different facts/concepts
- Return ONLY raw JSON, no markdown fences, no explanation

JSON format:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct": 0,
      "topic": "sub-topic from document"
    }}
  ]
}}

DOCUMENT SECTION:
{doc_section}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)
    return jsonify(result)


if __name__ == "__main__":
    print("\n  QuizCraft backend running at  →  http://localhost:5000\n")
    app.run(port=5000, debug=False)
