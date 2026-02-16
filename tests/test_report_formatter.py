"""Tests for PROACTIVE Report Formatter module."""

import pytest

from proactive.mr_analyzer import MRAnalysisResult, Claim
from proactive.validator import Violation
from proactive.report_formatter import format_review_comment


class TestFormatReviewComment:
    """Test GitLab review comment formatting."""

    def test_blocked_review_has_violation_header(self):
        result = MRAnalysisResult(
            violations=[
                Violation(
                    violation_id="V-0001",
                    invariant="I2",
                    severity="ERROR",
                    location={"file": "MR_DESCRIPTION", "line": 1},
                    message="Phantom completion detected",
                )
            ],
            claims_found=[],
            trust_score=0.0,
        )
        comment = format_review_comment(result)
        assert "BLOCKED" in comment
        assert "I2" in comment
        assert "Phantom completion" in comment

    def test_approved_review_has_pass_header(self):
        result = MRAnalysisResult(violations=[], claims_found=[], trust_score=1.0)
        comment = format_review_comment(result)
        assert "APPROVED" in comment

    def test_includes_trust_score(self):
        result = MRAnalysisResult(violations=[], claims_found=[], trust_score=0.85)
        comment = format_review_comment(result)
        assert "85" in comment

    def test_flagged_review_for_warnings(self):
        result = MRAnalysisResult(
            violations=[
                Violation(
                    violation_id="V-0001",
                    invariant="I5",
                    severity="WARNING",
                    location={"file": "MR_DESCRIPTION", "line": 1},
                    message="Hedging with certainty",
                )
            ],
            claims_found=[],
            trust_score=0.5,
        )
        comment = format_review_comment(result)
        assert "FLAGGED" in comment

    def test_includes_suggested_fix(self):
        result = MRAnalysisResult(
            violations=[
                Violation(
                    violation_id="V-0001",
                    invariant="I1",
                    severity="ERROR",
                    location={"file": "MR_DESCRIPTION", "line": 1},
                    message="Absolute claim",
                    suggested_fix="Add epistemic tag",
                )
            ],
        )
        comment = format_review_comment(result)
        assert "Add epistemic tag" in comment

    def test_includes_claims_section(self):
        result = MRAnalysisResult(
            violations=[],
            claims_found=[
                Claim(text="All tests pass", claim_type="completion", source="description"),
            ],
            trust_score=1.0,
        )
        comment = format_review_comment(result)
        assert "Claims Analyzed" in comment
        assert "completion" in comment

    def test_includes_footer(self):
        result = MRAnalysisResult()
        comment = format_review_comment(result)
        assert "PROACTIVE" in comment
        assert "Constitutional AI" in comment
