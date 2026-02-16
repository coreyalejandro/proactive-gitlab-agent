"""
PROACTIVE MR Analyzer
Extracts claims from merge request context and runs them through the validator.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from proactive.validator import Violation, check_invariants


__all__ = [
    "Claim",
    "MRContext",
    "MRAnalysisResult",
    "extract_claims",
    "analyze_mr",
]


@dataclass(frozen=True)
class Claim:
    """A verifiable claim extracted from MR text."""

    text: str
    claim_type: str  # "completion", "performance", "correctness", "existence"
    source: str  # "description", "comment", "diff_comment"
    line_number: Optional[int] = None


@dataclass(frozen=True)
class MRContext:
    """Context for a merge request under review."""

    title: str
    description: str
    diff: str
    test_artifacts_exist: bool
    comments: List[str] = field(default_factory=list)
    linked_issues: List[str] = field(default_factory=list)


@dataclass
class MRAnalysisResult:
    """Result of analyzing a merge request."""

    violations: List[Violation] = field(default_factory=list)
    claims_found: List[Claim] = field(default_factory=list)
    trust_score: float = 1.0

    @property
    def should_block(self) -> bool:
        return any(v.severity == "ERROR" for v in self.violations)

    @property
    def verdict(self) -> str:
        if self.should_block:
            return "BLOCKED"
        if self.violations:
            return "FLAGGED"
        return "APPROVED"


# ---------------------------------------------------------------------------
# Claim extraction patterns
# ---------------------------------------------------------------------------

COMPLETION_PATTERNS = [
    (r"\b(?:all\s+)?tests?\s+pass(?:ing|ed|es)?\b", "completion"),
    (r"\b(?:implementation|feature)\s+(?:is\s+)?complete[d]?\b", "completion"),
    (r"\bfully\s+implemented\b", "completion"),
    (r"\bfinished\s+(?:all|the|this)\b", "completion"),
    (r"\bdone\s+(?:with|implementing)\b", "completion"),
]

PERFORMANCE_PATTERNS = [
    (r"\bO\([^)]+\)", "performance"),
    (r"\b\d+x\s+(?:faster|slower|improvement)\b", "performance"),
    (r"\breduced\s+(?:latency|time|memory)\b", "performance"),
]

CORRECTNESS_PATTERNS = [
    (r"\bfixes?\s+(?:the\s+)?bug\b", "correctness"),
    (r"\bresolves?\s+(?:the\s+)?issue\b", "correctness"),
    (r"\bno\s+(?:more\s+)?(?:errors?|bugs?|issues?)\b", "correctness"),
]


def extract_claims(text: str, source: str = "description") -> List[Claim]:
    """Extract verifiable claims from MR text.

    Args:
        text: Raw text from MR description, comment, or diff.
        source: Origin label for the claim.

    Returns:
        List of extracted claims.
    """
    claims: List[Claim] = []
    all_patterns = COMPLETION_PATTERNS + PERFORMANCE_PATTERNS + CORRECTNESS_PATTERNS

    for pattern, claim_type in all_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Get the full sentence containing the match
            start = text.rfind(".", 0, match.start())
            end = text.find(".", match.end())
            sentence = text[start + 1 : end + 1 if end != -1 else len(text)].strip()

            claims.append(
                Claim(
                    text=sentence if sentence else match.group(),
                    claim_type=claim_type,
                    source=source,
                )
            )

    return claims


def analyze_mr(context: MRContext) -> MRAnalysisResult:
    """Analyze a merge request for constitutional violations.

    Extracts claims from description and comments, runs I1-I6 checks,
    and flags phantom completions (completion claims without test artifacts).

    Args:
        context: The MR context to analyze.

    Returns:
        Analysis result with violations, claims, and trust score.
    """
    all_violations: List[Violation] = []
    all_claims: List[Claim] = []

    # Extract claims from description
    all_claims.extend(extract_claims(context.description, "description"))

    # Extract claims from comments
    for comment in context.comments:
        all_claims.extend(extract_claims(comment, "comment"))

    # Run I1-I6 checks on description
    all_violations.extend(check_invariants(context.description, "MR_DESCRIPTION"))

    # Check for phantom completion (I2): completion claims without test artifacts
    completion_claims = [c for c in all_claims if c.claim_type == "completion"]
    if completion_claims and not context.test_artifacts_exist:
        for claim in completion_claims:
            all_violations.append(
                Violation(
                    violation_id=f"V-MR-I2-{hash(claim.text) % 10000:04X}",
                    invariant="I2",
                    severity="ERROR",
                    location={
                        "file": "MR_DESCRIPTION",
                        "line": 1,
                        "context": claim.text[:200],
                    },
                    message=(
                        f"I2 VIOLATION: Phantom completion detected. "
                        f"MR claims '{claim.text[:80]}' but no test execution "
                        f"artifacts found. Merge blocked."
                    ),
                    suggested_fix=(
                        "Run tests and ensure artifacts are committed, "
                        "or remove the completion claim."
                    ),
                    evidence={
                        "claim_text": claim.text,
                        "claim_type": claim.claim_type,
                        "test_artifacts_exist": False,
                    },
                    rule_id="I2_phantom_completion_mr",
                )
            )

    # Calculate trust score
    if not all_claims:
        trust_score = 1.0
    else:
        violation_count = len(all_violations)
        trust_score = max(0.0, 1.0 - (violation_count / max(len(all_claims), 1)))

    return MRAnalysisResult(
        violations=all_violations,
        claims_found=all_claims,
        trust_score=trust_score,
    )
