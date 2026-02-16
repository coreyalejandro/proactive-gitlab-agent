"""Tests for PROACTIVE MR Analyzer module."""

import pytest

from proactive.mr_analyzer import MRContext, MRAnalysisResult, Claim, extract_claims, analyze_mr


class TestExtractClaims:
    """Test claim extraction from MR text."""

    def test_extracts_completion_claims(self):
        description = "All tests pass. Implementation is complete."
        claims = extract_claims(description)
        assert len(claims) >= 2
        assert any("tests pass" in c.text.lower() for c in claims)

    def test_extracts_performance_claims(self):
        description = "Optimized the query to O(1) lookup time."
        claims = extract_claims(description)
        assert len(claims) >= 1
        assert claims[0].claim_type == "performance"

    def test_no_claims_in_plain_code(self):
        diff = "def add(a, b):\n    return a + b"
        claims = extract_claims(diff)
        assert len(claims) == 0

    def test_extracts_correctness_claims(self):
        description = "This fixes the bug in user authentication."
        claims = extract_claims(description)
        assert len(claims) >= 1
        assert claims[0].claim_type == "correctness"

    def test_claim_source_is_preserved(self):
        claims = extract_claims("All tests pass.", source="comment")
        assert len(claims) >= 1
        assert claims[0].source == "comment"


class TestMRContext:
    """Test MRContext dataclass."""

    def test_frozen_fields(self):
        ctx = MRContext(
            title="Test",
            description="Description",
            diff="diff content",
            test_artifacts_exist=True,
            comments=[],
        )
        assert ctx.title == "Test"
        assert ctx.test_artifacts_exist is True

    def test_default_comments(self):
        ctx = MRContext(
            title="Test",
            description="Desc",
            diff="diff",
            test_artifacts_exist=True,
        )
        assert ctx.comments == []
        assert ctx.linked_issues == []


class TestMRAnalysisResult:
    """Test MRAnalysisResult verdict logic."""

    def test_should_block_on_error_violations(self):
        from proactive.validator import Violation

        result = MRAnalysisResult(
            violations=[
                Violation(
                    violation_id="V-0001",
                    invariant="I2",
                    severity="ERROR",
                    location={"file": "test.py"},
                    message="test",
                )
            ],
        )
        assert result.should_block is True
        assert result.verdict == "BLOCKED"

    def test_flagged_on_warning_only(self):
        from proactive.validator import Violation

        result = MRAnalysisResult(
            violations=[
                Violation(
                    violation_id="V-0001",
                    invariant="I5",
                    severity="WARNING",
                    location={"file": "test.py"},
                    message="test",
                )
            ],
        )
        assert result.should_block is False
        assert result.verdict == "FLAGGED"

    def test_approved_with_no_violations(self):
        result = MRAnalysisResult()
        assert result.should_block is False
        assert result.verdict == "APPROVED"


class TestAnalyzeMR:
    """Test end-to-end MR analysis."""

    def test_blocks_phantom_completion(self):
        context = MRContext(
            title="Add user authentication",
            description="All tests pass. Implementation complete.",
            diff="def login(user, password):\n    pass",
            test_artifacts_exist=False,
            comments=[],
        )
        result = analyze_mr(context)
        assert result.should_block is True
        assert any(v.invariant == "I2" for v in result.violations)

    def test_approves_clean_mr(self):
        context = MRContext(
            title="Add helper function",
            description="Adds a utility function for string formatting.",
            diff="def format_name(first, last):\n    return f'{first} {last}'",
            test_artifacts_exist=True,
            comments=[],
        )
        result = analyze_mr(context)
        assert result.should_block is False
        assert len(result.violations) == 0

    def test_extracts_claims_from_comments(self):
        context = MRContext(
            title="Fix bug",
            description="Minor fix.",
            diff="x = 1",
            test_artifacts_exist=True,
            comments=["All tests pass now."],
        )
        result = analyze_mr(context)
        assert len(result.claims_found) >= 1

    def test_trust_score_decreases_with_violations(self):
        context = MRContext(
            title="Big feature",
            description="All tests pass. Implementation complete. Fully implemented.",
            diff="def stub(): pass",
            test_artifacts_exist=False,
            comments=[],
        )
        result = analyze_mr(context)
        assert result.trust_score < 1.0
