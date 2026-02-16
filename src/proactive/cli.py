"""
PROACTIVE CLI
Entry point for running constitutional reviews on merge request data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from proactive.mr_analyzer import MRContext, analyze_mr
from proactive.report_formatter import format_review_comment


__all__ = ["run_review", "main"]


def run_review(mr_data_path: str) -> int:
    """Run a PROACTIVE review on MR data from a JSON file.

    Args:
        mr_data_path: Path to a JSON file containing MR context.

    Returns:
        0 if the MR is approved, 1 if blocked.
    """
    path = Path(mr_data_path)
    data = json.loads(path.read_text(encoding="utf-8"))

    context = MRContext(
        title=data.get("title", ""),
        description=data.get("description", ""),
        diff=data.get("diff", ""),
        test_artifacts_exist=data.get("test_artifacts_exist", False),
        comments=data.get("comments", []),
        linked_issues=data.get("linked_issues", []),
    )

    result = analyze_mr(context)
    review = format_review_comment(result)

    print(review)

    report = {
        "verdict": result.verdict,
        "trust_score": result.trust_score,
        "violations_count": len(result.violations),
        "claims_count": len(result.claims_found),
        "violations": [
            {
                "invariant": v.invariant,
                "severity": v.severity,
                "message": v.message,
            }
            for v in result.violations
        ],
    }
    print(json.dumps(report, indent=2))

    return 0 if result.verdict != "BLOCKED" else 1


def main() -> None:
    """CLI entry point with argparse."""
    import argparse

    parser = argparse.ArgumentParser(description="PROACTIVE CLI")
    subparsers = parser.add_subparsers(dest="command")

    review_parser = subparsers.add_parser("review", help="Review an MR")
    review_parser.add_argument("--mr-data", required=True, help="Path to MR data JSON")
    review_parser.add_argument(
        "--format", default="text", choices=["text", "json", "gitlab"]
    )
    review_parser.add_argument("--strict", default="true")

    args = parser.parse_args()

    if args.command == "review":
        exit_code = run_review(args.mr_data)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
