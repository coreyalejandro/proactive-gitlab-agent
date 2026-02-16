"""Tests for PROACTIVE Constitutional Validator (I1-I6 invariants)."""

import pytest

from proactive.validator import (
    Violation,
    ValidationResult,
    check_invariant_i1,
    check_invariant_i2,
    check_invariant_i3,
    check_invariant_i4,
    check_invariant_i5,
    check_invariant_i6,
    check_invariants,
)


class TestI1EvidenceFirst:
    """I1: Every claim must carry an epistemic tag and supporting evidence."""

    def test_flags_absolute_claim_without_tag(self):
        content = "This function is definitely O(n) time complexity."
        violations = check_invariant_i1(content, "test.py")
        assert len(violations) > 0
        assert violations[0].invariant == "I1"

    def test_passes_claim_with_epistemic_tag(self):
        content = "[OBSERVED] This function is O(n) based on benchmarks."
        violations = check_invariant_i1(content, "test.py")
        assert len(violations) == 0

    def test_flags_certainty_expression(self):
        content = "I am certain this implementation handles all edge cases."
        violations = check_invariant_i1(content, "test.py")
        assert len(violations) > 0

    def test_flags_guaranteed_claim(self):
        content = "This approach is guaranteed to work in all scenarios."
        violations = check_invariant_i1(content, "test.py")
        assert len(violations) > 0
        assert violations[0].severity == "ERROR"

    def test_passes_plain_code(self):
        content = "def add(a, b):\n    return a + b"
        violations = check_invariant_i1(content, "test.py")
        assert len(violations) == 0


class TestI2NoPhantomWork:
    """I2: Cannot claim work is complete unless artifact exists."""

    def test_flags_missing_file_claim(self, tmp_path):
        content = 'Created file "output/report.json" successfully.'
        violations = check_invariant_i2(content, "test.py", str(tmp_path))
        assert len(violations) > 0
        assert violations[0].invariant == "I2"

    def test_passes_existing_file_claim(self, tmp_path):
        (tmp_path / "output").mkdir()
        (tmp_path / "output" / "report.json").write_text("{}")
        content = 'Created file "output/report.json" successfully.'
        violations = check_invariant_i2(content, "test.py", str(tmp_path))
        assert len(violations) == 0

    def test_flags_completion_without_evidence(self):
        content = "Completed all tasks and finished the entire implementation."
        violations = check_invariant_i2(content, "test.py", ".")
        assert len(violations) > 0


class TestI3ConfidenceRequiresVerification:
    """I3: High confidence (>=0.8) requires verification artifacts."""

    def test_flags_high_confidence_without_verification(self):
        content = "confidence: 0.95"
        violations = check_invariant_i3(content, "test.py")
        assert len(violations) > 0
        assert violations[0].invariant == "I3"

    def test_passes_high_confidence_with_verification(self):
        content = "confidence: 0.95 - verified by test suite results."
        violations = check_invariant_i3(content, "test.py")
        assert len(violations) == 0

    def test_passes_low_confidence(self):
        content = "confidence: 0.5"
        violations = check_invariant_i3(content, "test.py")
        assert len(violations) == 0


class TestI4TraceabilityMandatory:
    """I4: Decision statements need trace chain references."""

    def test_flags_decision_without_trace(self):
        content = "We decided to use PostgreSQL for the database."
        violations = check_invariant_i4(content, "test.py")
        assert len(violations) > 0
        assert violations[0].invariant == "I4"

    def test_passes_decision_with_trace(self):
        content = "We decided to use PostgreSQL per REQ-001 trace chain."
        violations = check_invariant_i4(content, "test.py")
        assert len(violations) == 0


class TestI5SafetyOverFluency:
    """I5: Hedging + certainty language is contradictory."""

    def test_flags_mixed_hedging_and_certainty(self):
        content = "This seems like a certain improvement to performance."
        violations = check_invariant_i5(content, "test.py")
        assert len(violations) > 0
        assert violations[0].invariant == "I5"

    def test_passes_consistent_hedging(self):
        content = "This might improve performance, but we need to test it."
        violations = check_invariant_i5(content, "test.py")
        assert len(violations) == 0

    def test_passes_consistent_certainty_with_evidence(self):
        content = "[OBSERVED] The improvement is measurable at 3x throughput."
        violations = check_invariant_i5(content, "test.py")
        assert len(violations) == 0


class TestI6FailClosed:
    """I6: Stop and surface failures, don't work around."""

    def test_flags_bare_except_pass(self):
        content = "try:\n    risky()\nexcept:\n    pass"
        violations = check_invariant_i6(content, "test.py")
        assert len(violations) > 0
        assert violations[0].invariant == "I6"

    def test_passes_proper_error_handling(self):
        content = "try:\n    risky()\nexcept Exception as e:\n    raise RuntimeError(str(e))"
        violations = check_invariant_i6(content, "test.py")
        assert len(violations) == 0

    def test_flags_error_suppression(self):
        content = "We should ignore the error and continue anyway."
        violations = check_invariant_i6(content, "test.py")
        assert len(violations) > 0


class TestCheckInvariants:
    """Test the aggregated check_invariants function."""

    def test_returns_empty_for_clean_content(self):
        content = "def add(a, b):\n    return a + b"
        violations = check_invariants(content, "test.py")
        assert len(violations) == 0

    def test_returns_multiple_violations(self):
        content = (
            "This is definitely correct and guaranteed to work. "
            "Completed all tasks. "
            "try:\n    risky()\nexcept:\n    pass"
        )
        violations = check_invariants(content, "test.py")
        invariants_hit = {v.invariant for v in violations}
        assert "I1" in invariants_hit
        assert "I6" in invariants_hit


class TestViolationDataclass:
    """Test Violation dataclass methods."""

    def test_to_dict_excludes_none(self):
        v = Violation(
            violation_id="V-0001",
            invariant="I1",
            severity="ERROR",
            location={"file": "test.py", "line": 1},
            message="Test violation",
        )
        d = v.to_dict()
        assert "suggested_fix" not in d
        assert "evidence" not in d
        assert d["invariant"] == "I1"


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_has_errors_true(self):
        result = ValidationResult(
            file_path="test.py",
            violations=[
                Violation(
                    violation_id="V-0001",
                    invariant="I1",
                    severity="ERROR",
                    location={"file": "test.py"},
                    message="error",
                )
            ],
        )
        assert result.has_errors is True
        assert result.error_count == 1

    def test_has_errors_false_for_warnings(self):
        result = ValidationResult(
            file_path="test.py",
            violations=[
                Violation(
                    violation_id="V-0001",
                    invariant="I5",
                    severity="WARNING",
                    location={"file": "test.py"},
                    message="warning",
                )
            ],
        )
        assert result.has_errors is False
        assert result.warning_count == 1
