"""Tests for question_bank.py — topic matching, question generation, schema validity."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from question_bank import BANK, TOPIC_ALIASES, match_topics, generate_questions

ALLOWED_TYPES = {"Code Output", "Error Prediction", "Concept", "Syntax", "Comparison", "Behavior"}


# ─────────────────────────────────────────────
# match_topics
# ─────────────────────────────────────────────
class TestMatchTopics:
    def test_python_keyword_matches(self):
        assert "python" in match_topics(["python"])

    def test_py_alias_matches(self):
        assert "python" in match_topics(["py"])

    def test_javascript_alias_matches(self):
        assert "javascript" in match_topics(["js"])

    def test_typescript_maps_to_javascript(self):
        assert "javascript" in match_topics(["typescript"])

    def test_docker_container_matches(self):
        assert "docker" in match_topics(["container"])

    def test_unknown_topic_returns_generic(self):
        assert match_topics(["foobar"]) == ["generic"]

    def test_empty_list_returns_generic(self):
        assert match_topics([]) == ["generic"]

    def test_multiple_topics_all_matched(self):
        matched = match_topics(["Python", "React"])
        assert "python" in matched
        assert "react" in matched

    def test_case_insensitive(self):
        assert "python" in match_topics(["PYTHON"])
        assert "javascript" in match_topics(["JavaScript"])

    def test_kubernetes_alias(self):
        assert "docker" in match_topics(["kubernetes"])


# ─────────────────────────────────────────────
# generate_questions — count + structure
# ─────────────────────────────────────────────
class TestGenerateQuestions:
    def test_returns_exact_count_requested(self):
        qs = generate_questions(["python"], 5)
        assert len(qs) == 5

    def test_small_pool_falls_back_to_generic(self):
        """Docker has 4 + generic has 8 = 12 max. Falls back but caps at pool size."""
        qs = generate_questions(["docker"], 10)
        assert len(qs) == 10  # 4 docker + 8 generic covers 10

    def test_each_question_has_required_fields(self):
        qs = generate_questions(["python"], 3)
        for q in qs:
            assert "question" in q
            assert "options"  in q
            assert "correct"  in q
            assert "topic"    in q
            assert "type"     in q

    def test_each_question_has_four_options(self):
        qs = generate_questions(["javascript"], 5)
        for q in qs:
            assert len(q["options"]) == 4

    def test_correct_index_in_valid_range(self):
        qs = generate_questions(["python"], 10)
        for q in qs:
            assert 0 <= q["correct"] <= 3

    def test_type_is_from_allowed_set(self):
        qs = generate_questions(["python"], 10)
        for q in qs:
            assert q["type"] in ALLOWED_TYPES

    def test_question_text_is_nonempty_string(self):
        qs = generate_questions(["python"], 5)
        for q in qs:
            assert isinstance(q["question"], str)
            assert len(q["question"]) > 0

    def test_options_are_all_strings(self):
        qs = generate_questions(["javascript"], 5)
        for q in qs:
            for opt in q["options"]:
                assert isinstance(opt, str)
                assert len(opt) > 0

    def test_unknown_topic_falls_back_to_generic(self):
        qs = generate_questions(["foobar"], 3)
        assert len(qs) == 3
        for q in qs:
            assert q["topic"] in ("Generic", "General Tech")

    def test_shuffling_produces_different_order(self):
        """Two calls with same args should rarely return the exact same order."""
        a = generate_questions(["python"], 10)
        b = generate_questions(["python"], 10)
        # With 10 items and shuffling, P(identical) is extremely low
        assert [q["question"] for q in a] != [q["question"] for q in b]


# ─────────────────────────────────────────────
# Bank integrity
# ─────────────────────────────────────────────
class TestBankIntegrity:
    def test_every_category_has_questions(self):
        for category, items in BANK.items():
            assert len(items) > 0, f"{category} is empty"

    def test_every_bank_question_has_correct_schema(self):
        for category, items in BANK.items():
            for item in items:
                assert "q"    in item, f"{category}: missing 'q'"
                assert "opts" in item, f"{category}: missing 'opts'"
                assert "c"    in item, f"{category}: missing 'c'"
                assert "t"    in item, f"{category}: missing 't'"

    def test_every_bank_question_has_four_options(self):
        for category, items in BANK.items():
            for item in items:
                assert len(item["opts"]) == 4, f"{category}: {item['q'][:40]}... has {len(item['opts'])} options"

    def test_every_correct_index_is_valid(self):
        for category, items in BANK.items():
            for item in items:
                assert 0 <= item["c"] <= 3, f"{category}: invalid correct index {item['c']}"

    def test_every_type_is_from_allowed_set(self):
        for category, items in BANK.items():
            for item in items:
                assert item["t"] in ALLOWED_TYPES, f"{category}: unknown type {item['t']}"

    def test_topic_aliases_reference_real_categories(self):
        for alias_key in TOPIC_ALIASES:
            assert alias_key in BANK, f"alias '{alias_key}' has no matching BANK entry"

    def test_bank_has_generic_fallback(self):
        assert "generic" in BANK, "BANK must include 'generic' for unknown-topic fallback"
