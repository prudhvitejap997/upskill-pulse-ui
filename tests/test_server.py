"""Tests for server.py — Flask routes, file upload, Groq fallback."""
import sys, os, io, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch
import server


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    with server.app.test_client() as c:
        yield c


# ─────────────────────────────────────────────
# Static routes
# ─────────────────────────────────────────────
class TestStaticRoutes:
    def test_index_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_index_returns_html(self, client):
        resp = client.get("/")
        assert b"<!DOCTYPE html>" in resp.data or b"<!doctype html>" in resp.data

    def test_index_contains_app_name(self, client):
        resp = client.get("/")
        assert b"Upskill Pulse" in resp.data


# ─────────────────────────────────────────────
# /api/generate-quiz — offline fallback
# ─────────────────────────────────────────────
class TestGenerateQuizOffline:
    """Force Groq to fail so the offline bank is exercised."""

    def test_offline_fallback_returns_questions(self, client):
        with patch.object(server, "call_groq", side_effect=Exception("forced")):
            resp = client.post("/api/generate-quiz", data={
                "topic":         "Python",
                "difficulty":    "easy",
                "questionCount": "3",
            })
            assert resp.status_code == 200
            data = resp.get_json()
            assert "questions" in data
            assert data["source"] == "offline"
            assert len(data["questions"]) == 3

    def test_offline_questions_have_required_fields(self, client):
        with patch.object(server, "call_groq", side_effect=Exception("forced")):
            resp = client.post("/api/generate-quiz", data={
                "topic":         "JavaScript",
                "difficulty":    "medium",
                "questionCount": "5",
            })
            data = resp.get_json()
            for q in data["questions"]:
                assert "question" in q
                assert "options"  in q
                assert "correct"  in q
                assert "topic"    in q
                assert "type"     in q

    def test_offline_respects_requested_count(self, client):
        with patch.object(server, "call_groq", side_effect=Exception("forced")):
            resp = client.post("/api/generate-quiz", data={
                "topic":         "Python",
                "difficulty":    "easy",
                "questionCount": "7",
            })
            data = resp.get_json()
            assert len(data["questions"]) == 7

    def test_multiple_topics_pipe_separated(self, client):
        with patch.object(server, "call_groq", side_effect=Exception("forced")):
            resp = client.post("/api/generate-quiz", data={
                "topic":         "Python | React",
                "difficulty":    "medium",
                "questionCount": "4",
            })
            assert resp.status_code == 200
            data = resp.get_json()
            assert len(data["questions"]) == 4


# ─────────────────────────────────────────────
# /api/generate-quiz — Groq success path
# ─────────────────────────────────────────────
class TestGenerateQuizGroq:
    FAKE_GROQ_RESPONSE = [
        {
            "question": "What does `len([1,2,3])` return?",
            "options":  ["2", "3", "4", "TypeError"],
            "correct":  1,
            "topic":    "Python",
            "type":     "Code Output",
        }
    ]

    def test_groq_success_returns_ai_questions(self, client):
        with patch.object(server, "call_groq", return_value=self.FAKE_GROQ_RESPONSE):
            resp = client.post("/api/generate-quiz", data={
                "topic":         "Python",
                "difficulty":    "easy",
                "questionCount": "1",
            })
            assert resp.status_code == 200
            data = resp.get_json()
            assert data["source"] == "groq"
            assert len(data["questions"]) == 1
            assert data["questions"][0]["question"].startswith("What does")


# ─────────────────────────────────────────────
# File upload + text extraction
# ─────────────────────────────────────────────
class TestFileUpload:
    def test_upload_with_file_works(self, client):
        """POST with an actual file attachment — should parse and still return questions."""
        data = {
            "topic":         "Python",
            "difficulty":    "easy",
            "questionCount": "2",
            "files":         (io.BytesIO(b"Lists are mutable in Python."), "notes.txt"),
        }
        with patch.object(server, "call_groq", side_effect=Exception("forced")):
            resp = client.post("/api/generate-quiz",
                data=data,
                content_type="multipart/form-data",
            )
            assert resp.status_code == 200
            payload = resp.get_json()
            assert "questions" in payload
            assert len(payload["questions"]) == 2

    def test_extract_text_from_txt(self):
        """extract_text should decode plain TXT content correctly."""
        from werkzeug.datastructures import FileStorage
        fs = FileStorage(
            stream=io.BytesIO(b"hello world"),
            filename="note.txt",
            content_type="text/plain",
        )
        out = server.extract_text(fs)
        assert "hello world" in out

    def test_extract_text_from_corrupt_pdf_returns_empty(self):
        """A non-PDF byte stream sent as .pdf should not crash — returns empty string."""
        from werkzeug.datastructures import FileStorage
        fs = FileStorage(
            stream=io.BytesIO(b"not-a-real-pdf"),
            filename="broken.pdf",
            content_type="application/pdf",
        )
        out = server.extract_text(fs)
        assert out == ""


# ─────────────────────────────────────────────
# User-message builder
# ─────────────────────────────────────────────
class TestBuildUserMessage:
    def test_includes_topic_and_difficulty(self):
        msg = server.build_user_message("Python", "easy", 5, None)
        assert "Python"  in msg
        assert "easy"    in msg
        assert "5"       in msg

    def test_no_content_uses_no_files_branch(self):
        msg = server.build_user_message("React", "medium", 10, None)
        assert "React" in msg
        # no study material header
        assert "Study material" not in msg

    def test_with_content_includes_material_header(self):
        msg = server.build_user_message("Python", "hard", 10, "Lists are mutable.")
        assert "Study material" in msg
        assert "Lists are mutable." in msg

    def test_long_content_is_truncated(self):
        content = "Z" * 40000
        msg = server.build_user_message("Python", "easy", 5, content)
        # Content is truncated to 30k chars; full 40k would appear verbatim otherwise
        assert msg.count("Z") <= 30000
        assert msg.count("Z") >= 1000  # sanity: content still included
