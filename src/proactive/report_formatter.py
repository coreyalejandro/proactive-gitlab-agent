"""
PROACTIVE Report Formatter
Formats MRAnalysisResult into GitLab-flavored markdown for code review comments.
"""

from __future__ import annotations

from proactive.mr_analyzer import MRAnalysisResult


__all__ = ["format_review_comment"]


VERDICT_ICONS = {
    "BLOCKED": ":no_entry:",
    "FLAGGED": ":warning:",
    "APPROVED": ":white_check_mark:",
}

INVARIANT_NAMES = {
    "I1": "Evidence-First Outputs",
    "I2": "No Phantom Work",
    "I3": "Confidence Requires Verification",
    "I4": "Traceability Is Mandatory",
    "I5": "Safety Over Fluency",
    "I6": "Fail Closed",
}


def format_review_comment(result: MRAnalysisResult) -> str:
    """Format an MR analysis result as a GitLab review comment.

    Args:
        result: The analysis result to format.

    Returns:
        GitLab-flavored markdown string.
    """
    verdict = result.verdict
    icon = VERDICT_ICONS.get(verdict, "")
    trust_pct = int(result.trust_score * 100)

    lines = [
        f"## {icon} PROACTIVE Review: **{verdict}**",
        "",
        f"**Trust Score:** {trust_pct}%",
        "",
    ]

    if result.violations:
        lines.append("### Violations Found")
        lines.append("")

        for v in result.violations:
            inv_name = INVARIANT_NAMES.get(v.invariant, v.invariant)
            lines.append(f"**[{v.severity}] {v.invariant}: {inv_name}**")
            lines.append(f"> {v.message}")
            if v.suggested_fix:
                lines.append(f"> **Fix:** {v.suggested_fix}")
            lines.append("")

    if result.claims_found:
        lines.append(f"### Claims Analyzed: {len(result.claims_found)}")
        lines.append("")
        for claim in result.claims_found[:10]:
            status = "unverified" if any(
                v.evidence and v.evidence.get("claim_text") == claim.text
                for v in result.violations
            ) else "verified"
            marker = ":x:" if status == "unverified" else ":white_check_mark:"
            lines.append(f"- {marker} [{claim.claim_type}] {claim.text[:100]}")
        lines.append("")

    lines.append("---")
    lines.append("*PROACTIVE: Constitutional AI for your pipeline*")

    return "\n".join(lines)
