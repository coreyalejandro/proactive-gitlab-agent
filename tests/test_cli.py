"""Tests for PROACTIVE CLI entry point."""

import json

import pytest

from proactive.cli import run_review


class TestRunReview:
    """Test the run_review function."""

    def test_returns_zero_on_clean(self, tmp_path):
        mr_data = {
            "title": "Add utility function",
            "description": "Adds a string formatting helper.",
            "diff": "def fmt(s): return s.strip()",
            "test_artifacts_exist": True,
            "comments": [],
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        exit_code = run_review(str(mr_file))
        assert exit_code == 0

    def test_returns_one_on_violation(self, tmp_path):
        mr_data = {
            "title": "Complete implementation",
            "description": "All tests pass. Implementation is complete.",
            "diff": "def login(): pass",
            "test_artifacts_exist": False,
            "comments": [],
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        exit_code = run_review(str(mr_file))
        assert exit_code == 1

    def test_outputs_review_comment(self, tmp_path, capsys):
        mr_data = {
            "title": "Fix bug",
            "description": "Minor string fix.",
            "diff": "x = 1",
            "test_artifacts_exist": True,
            "comments": [],
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        run_review(str(mr_file))
        captured = capsys.readouterr()
        assert "PROACTIVE Review" in captured.out
        assert "APPROVED" in captured.out

    def test_outputs_json_report(self, tmp_path, capsys):
        mr_data = {
            "title": "Add feature",
            "description": "New feature added.",
            "diff": "def feat(): pass",
            "test_artifacts_exist": True,
            "comments": [],
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        run_review(str(mr_file))
        captured = capsys.readouterr()
        # Should contain JSON report after the review comment
        assert '"verdict"' in captured.out

    def test_handles_missing_optional_fields(self, tmp_path):
        mr_data = {
            "title": "Minimal MR",
            "description": "Simple change.",
            "diff": "",
            "test_artifacts_exist": True,
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        exit_code = run_review(str(mr_file))
        assert exit_code == 0
