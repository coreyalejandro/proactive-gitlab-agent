# PROACTIVE

> Constitutional AI for your pipeline

A GitLab Duo agent that enforces safety principles on every merge request. Catches phantom completions, confident false claims, and source fabrication before they reach production.

## The Problem

AI agents confidently lie. They claim "all tests pass" when no test files exist. They assert O(1) performance for O(n) code. They reference libraries that don't exist. Today, zero pipelines catch these failures before merge.

**PROACTIVE** is a constitutional safety layer that reviews every MR against six invariants, blocking phantom work and surfacing confident false claims with specific, actionable feedback.

## Architecture

```text
                     Merge Request
                         |
                    [MR Analyzer]
                    extract_claims()
                         |
                  +------+------+
                  |             |
             [Validator]   [Claim List]
            I1-I6 checks       |
                  |        Completion?
                  |        Performance?
                  +------+------+
                         |
                  [Analysis Result]
                  violations, trust_score
                         |
                  [Report Formatter]
                  GitLab markdown
                         |
                    Review Comment
                    APPROVED / FLAGGED / BLOCKED
```

**Components:**

| Module | Purpose |
| ------ | ------- |
| `validator.py` | I1-I6 invariant checks via regex pattern matching |
| `mr_analyzer.py` | Claim extraction + phantom completion detection |
| `report_formatter.py` | GitLab-flavored markdown review comments |
| `cli.py` | CLI entry point for CI/CD pipeline integration |

## Invariants (I1-I6)

| ID | Name | What It Catches | Severity |
| -- | ---- | --------------- | -------- |
| I1 | Evidence-First Outputs | "definitely", "guaranteed", "I am certain" without epistemic tags | ERROR |
| I2 | No Phantom Work | "all tests pass" when no test artifacts exist | ERROR |
| I3 | Confidence Requires Verification | `confidence: 0.95` without verification reference | WARNING |
| I4 | Traceability Is Mandatory | "we decided to use X" without REQ/CTRL/TEST trace chain | ERROR |
| I5 | Safety Over Fluency | "seems like a certain improvement" (hedging + certainty) | WARNING |
| I6 | Fail Closed | `try: ... except: pass` (silent error suppression) | ERROR |

## Failure Modes (F1-F5)

| ID | Mode | Example |
| -- | ---- | ------- |
| F1 | Confident False Claim | "O(1) lookup" for linear scan code |
| F2 | Phantom Completion | "Implementation complete" with stub functions |
| F3 | Source Fabrication | Referencing a library that doesn't exist |
| F4 | Silent Failure | Catching exceptions and doing nothing |
| F5 | Untraced Decision | Architectural choice without justification chain |

## Quick Start

### Install

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v --cov=proactive
```

### Review an MR (local)

Create an MR data file:

```json
{
  "title": "Add feature X",
  "description": "All tests pass. Implementation complete.",
  "diff": "def feature(): pass",
  "test_artifacts_exist": false,
  "comments": []
}
```

Run the review:

```bash
python -m proactive.cli review --mr-data mr.json
```

### GitLab CI/CD Integration

The `.gitlab-ci.yml` runs PROACTIVE automatically on merge requests:

```yaml
proactive-review:
  stage: review
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script:
    - pip install -e .
    - python -m proactive.cli review --mr-data mr_context.json
  allow_failure: false
```

### GitLab Duo Agent Setup

1. Navigate to **Automate > Agents > New agent** in your GitLab project
2. Name: `PROACTIVE`
3. Paste the system prompt from `.gitlab/duo/prompts/proactive-system-prompt.md`
4. Select tools: Build Review MR Context, GitLab Blob Search, Post Duo Code Review
5. Add trigger: `assign_reviewer` event

## Validation Evidence

Validated against n=200 TruthfulQA samples:

| Metric | Result |
| ------ | ------ |
| Detection Rate | 100% (all invariant violations caught) |
| False Positive Rate | 0% (no clean samples flagged) |
| Invariants Tested | I1, I2, I3, I4, I5, I6 |

Full results: [`docs/evidence/validation_results.json`](docs/evidence/validation_results.json)

## Project Structure

```text
proactive-gitlab-agent/
├── src/proactive/           # Python validation engine
│   ├── validator.py         # I1-I6 invariant checks
│   ├── mr_analyzer.py       # MR claim extraction
│   ├── report_formatter.py  # GitLab review formatting
│   └── cli.py               # CLI entry point
├── tests/                   # Unit + integration tests (58 tests, 83% coverage)
├── fixtures/                # MR test fixtures (5 failure scenarios)
├── .gitlab/duo/             # Duo agent prompt + flow config
├── .gitlab-ci.yml           # CI/CD pipeline
├── remotion/                # Demo video (Remotion/React)
└── docs/                    # Constitution + evidence
```

## Demo Video

The 3-minute demo video is built with [Remotion](https://remotion.dev):

```bash
cd remotion
npm install
npm run start     # Preview in browser
npm run build     # Render to remotion/out/demo.mp4
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests first (TDD)
4. Ensure `pytest tests/ -v --cov=proactive` passes with >80% coverage
5. Submit a merge request

PROACTIVE will review your MR against I1-I6 before merge.

## License

Apache 2.0 - See [LICENSE](LICENSE)
