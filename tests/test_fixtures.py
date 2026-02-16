"""Integration tests using MR fixture files."""

import json

import pytest
from pathlib import Path

from proactive.mr_analyzer import MRContext, analyze_mr


FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"


def load_fixture(name: str) -> MRContext:
    """Load an MR fixture file into an MRContext."""
    data = json.loads((FIXTURE_DIR / name).read_text())
    return MRContext(
        title=data["title"],
        description=data["description"],
        diff=data["diff"],
        test_artifacts_exist=data["test_artifacts_exist"],
        comments=data.get("comments", []),
    )


class TestFixtures:
    """Integration tests: each fixture exercises a specific failure mode."""

    def test_phantom_completion_is_blocked(self):
        ctx = load_fixture("mr_phantom_completion.json")
        result = analyze_mr(ctx)
        assert result.should_block is True
        assert any(v.invariant == "I2" for v in result.violations)

    def test_confident_false_claim_is_flagged(self):
        ctx = load_fixture("mr_confident_false_claim.json")
        result = analyze_mr(ctx)
        assert any(v.invariant == "I1" for v in result.violations)

    def test_clean_mr_is_approved(self):
        ctx = load_fixture("mr_clean.json")
        result = analyze_mr(ctx)
        assert result.verdict == "APPROVED"
        assert len(result.violations) == 0

    def test_mixed_violations_is_blocked(self):
        ctx = load_fixture("mr_mixed_violations.json")
        result = analyze_mr(ctx)
        assert result.should_block is True
        invariants_hit = {v.invariant for v in result.violations}
        assert "I2" in invariants_hit  # phantom completion
        assert "I1" in invariants_hit  # absolute claims

    def test_source_fabrication_has_no_code_violations(self):
        """Source fabrication is flagged by I1 for absolute-sounding claims,
        but the fixture itself has no absolute language - it's a subtle case
        that would need LLM-based verification to catch fully."""
        ctx = load_fixture("mr_source_fabrication.json")
        result = analyze_mr(ctx)
        # This fixture is clean from a regex perspective;
        # real source fabrication detection would need LLM augmentation
        assert result.verdict in ("APPROVED", "FLAGGED")


class TestFixturesCLI:
    """Test fixtures through the CLI entry point."""

    def test_clean_fixture_via_cli(self):
        from proactive.cli import run_review

        exit_code = run_review(str(FIXTURE_DIR / "mr_clean.json"))
        assert exit_code == 0

    def test_phantom_fixture_via_cli(self):
        from proactive.cli import run_review

        exit_code = run_review(str(FIXTURE_DIR / "mr_phantom_completion.json"))
        assert exit_code == 1

    def test_mixed_fixture_via_cli(self):
        from proactive.cli import run_review

        exit_code = run_review(str(FIXTURE_DIR / "mr_mixed_violations.json"))
        assert exit_code == 1
