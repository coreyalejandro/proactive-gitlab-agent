# PROACTIVE GitLab Duo Agent Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a GitLab Duo agent + flow that uses the Contract Window (from original AI survey research) as its hero feature — capturing user intent, rendering a persistent bidirectional contract, validating code against that contract, and detecting scope drift throughout the MR lifecycle.

**Architecture:** Three-layer pipeline: COL (Cognitive Operating Layer for intent capture) → Contract Window (persistent, always-visible bidirectional contract) → Validator (constitutional enforcement against the contract). Hybrid GitLab Duo agent (interactive chat) + flow (automated CI/CD review). Python core. Claude via GitLab AI Gateway. Remotion for 3-minute demo video.

**Tech Stack:** Python 3.11+, GitLab Duo Agent Platform, Claude (via AI Gateway), GitLab CI/CD, Remotion (React/TypeScript), pytest

**Source Material:**
- TypeScript Contract Window: `~/dev/zero-shot-os-with-upos7vs-core/packages/core/ui/contract-window.ts` (206 lines)
- TypeScript COL Service: `~/dev/zero-shot-os-with-upos7vs-core/packages/core/services/col.service.ts` (529 lines)
- Existing Validator: `ADAPTER_MODULES/02_CI_SAFETY_GATE/validator.py` (1005 lines)
- CONTRACT AI Survey: `~/Projects/proactive-gitlab-agent/docs/evidence/CONTRACT_AI_SURVEY_AND_RESEARCH.md`

---

## Phase 1: Project Setup & Repo Migration

### Task 1: Initialize clean GitLab project locally

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `pyproject.toml`

**Step 1: Create project skeleton**

```
proactive-gitlab-agent/
├── src/
│   └── proactive/
│       ├── __init__.py
│       ├── col.py               # Cognitive Operating Layer (intent capture)
│       ├── contract_window.py   # Persistent Contract Window (hero feature)
│       ├── drift_detector.py    # Intent drift detection
│       ├── validator.py         # Constitutional invariant checks (I1-I6)
│       ├── mr_analyzer.py       # MR-specific orchestrator (COL → Contract → Validator)
│       ├── report_formatter.py  # Format Contract Window + review for GitLab Markdown
│       └── cli.py               # CLI entry point
├── tests/
│   ├── __init__.py
│   ├── test_col.py
│   ├── test_contract_window.py
│   ├── test_drift_detector.py
│   ├── test_validator.py
│   ├── test_mr_analyzer.py
│   ├── test_report_formatter.py
│   ├── test_cli.py
│   └── test_fixtures.py
├── fixtures/
│   ├── mr_phantom_completion.json
│   ├── mr_confident_false_claim.json
│   ├── mr_intent_drift.json
│   ├── mr_ambiguous_intent.json
│   ├── mr_scope_change.json
│   ├── mr_clean.json
│   └── mr_mixed_violations.json
├── .gitlab/
│   └── duo/
│       ├── prompts/
│       │   └── proactive-system-prompt.md
│       └── flows/
│           └── proactive-review.yaml
├── .gitlab-ci.yml
├── remotion/                     # Demo video project (Phase 8)
├── docs/
│   ├── plans/
│   │   └── 2026-02-15-proactive-gitlab-agent-design.md
│   ├── constitution.md
│   └── evidence/
│       ├── CONTRACT_AI_SURVEY_AND_RESEARCH.md
│       └── validation_results.json
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

**Step 2: Create pyproject.toml**

```toml
[project]
name = "proactive"
version = "0.1.0"
description = "We asked AI what it needs to serve you honestly. Then we built it."
requires-python = ">=3.11"
license = {text = "Apache-2.0"}
dependencies = [
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

**Step 3: Create .gitignore**

```
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
dist/
build/
.venv/
venv/
node_modules/
.env
*.log
```

**Step 4: Create LICENSE (Apache 2.0)**

Use standard Apache 2.0 license text with copyright year 2026.

**Step 5: Create README.md (minimal starter)**

```markdown
# PROACTIVE

> We asked AI what it needs to serve you honestly. Then we built it.

A GitLab Duo agent built on original research — a Maslow-style survey of AI models that revealed what conditions allow them to fully prioritize user intent. The answer: a persistent, bidirectional Contract Window.

## Quick Start

Coming soon. See [design document](docs/plans/2026-02-15-proactive-gitlab-agent-design.md).

## License

Apache 2.0
```

**Step 6: Initialize git and commit**

```bash
git init
git add .
git commit -m "chore: initialize PROACTIVE GitLab Duo Agent project skeleton"
```

---

### Task 2: Cherry-pick foundation documents from original repo

**Files:**
- Copy: `01_FOUNDATIONS/PROACTIVE_AI_CONSTITUTION.md` -> `docs/constitution.md`
- Copy: validation results -> `docs/evidence/validation_results.json`
- Copy: CONTRACT AI survey -> `docs/evidence/CONTRACT_AI_SURVEY_AND_RESEARCH.md`
- Copy: design doc -> `docs/plans/2026-02-15-proactive-gitlab-agent-design.md`

**Step 1: Copy constitution, evidence, survey data, and design doc**

**Step 2: Commit**

```bash
git add docs/
git commit -m "docs: add PROACTIVE constitution, survey research, and validation evidence"
```

---

## Phase 2: Cognitive Operating Layer — COL (TDD)

This is the FIRST layer. It captures intent from the MR and produces an IntentReceipt.

Port from: `~/dev/zero-shot-os-with-upos7vs-core/packages/core/services/col.service.ts` (529 lines TypeScript)

### Task 3: Build COL data models

**Files:**
- Create: `src/proactive/__init__.py`
- Create: `src/proactive/col.py`
- Test: `tests/test_col.py`

**Step 1: Write failing tests for data models**

```python
# tests/test_col.py
import pytest
from proactive.col import (
    ParsedIntent,
    Constraint,
    RiskAssessment,
    IntentReceipt,
)


class TestDataModels:
    def test_parsed_intent_is_frozen(self):
        intent = ParsedIntent(
            action="implement",
            target="auth_module",
            goal="user_authentication",
            confidence=0.92,
            ambiguities=[],
        )
        with pytest.raises(AttributeError):
            intent.action = "delete"

    def test_intent_receipt_has_all_fields(self):
        receipt = IntentReceipt(
            id="col-test-001",
            timestamp="2026-02-16T00:00:00Z",
            raw_input="Implement user auth with OAuth2",
            parsed_intent=ParsedIntent(
                action="implement",
                target="auth_module",
                goal="user_authentication",
                confidence=0.92,
                ambiguities=[],
            ),
            constraints=[],
            risk_assessment=RiskAssessment(
                level="medium",
                domain="security",
                factors=["authentication domain"],
                requires_confirmation=False,
                mitigations=[],
            ),
            trace_id="trace-abc-0001",
            validation_status="valid",
        )
        assert receipt.validation_status == "valid"
        assert receipt.parsed_intent.confidence == 0.92
```

**Step 2: Run tests to verify they fail**

```bash
cd proactive-gitlab-agent
pip install -e ".[dev]"
pytest tests/test_col.py::TestDataModels -v
```

Expected: FAIL (module not found)

**Step 3: Implement data models**

Port from TypeScript interfaces (`IntentReceipt`, `ParsedIntent`, `Constraint`, `RiskAssessment`) to Python frozen dataclasses. Key mapping:

```python
# src/proactive/col.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ParsedIntent:
    action: str       # What: "implement", "modify", "delete", etc.
    target: str       # What target: "auth_module", "user_service", etc.
    goal: str         # Why (inferred): "user_authentication"
    confidence: float  # 0.0 - 1.0
    ambiguities: tuple[str, ...] = ()


@dataclass(frozen=True)
class Constraint:
    type: str         # "explicit", "implicit", "derived"
    category: str     # "safety", "quality", "performance", "scope", "ethical"
    description: str
    source: str       # Where this came from


@dataclass(frozen=True)
class RiskAssessment:
    level: str        # "low", "medium", "high", "critical"
    domain: str       # "security", "financial", "general", etc.
    factors: tuple[str, ...] = ()
    requires_confirmation: bool = False
    mitigations: tuple[str, ...] = ()


@dataclass(frozen=True)
class IntentReceipt:
    id: str
    timestamp: str
    raw_input: str
    parsed_intent: ParsedIntent
    constraints: tuple[Constraint, ...] = ()
    risk_assessment: RiskAssessment = field(
        default_factory=lambda: RiskAssessment(level="low", domain="general")
    )
    trace_id: str = ""
    validation_status: str = "valid"  # "valid", "ambiguous", "rejected"
    rejection_reason: Optional[str] = None
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_col.py::TestDataModels -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/proactive/ tests/test_col.py
git commit -m "feat: add COL data models (IntentReceipt, ParsedIntent, RiskAssessment)"
```

---

### Task 4: Build COL intent parser

**Files:**
- Modify: `src/proactive/col.py`
- Test: `tests/test_col.py`

Port the `parseIntent()`, `extractAction()`, `extractTarget()`, `inferGoal()` methods from TypeScript COL service.

**Step 1: Write failing tests for intent parsing**

```python
class TestParseIntent:
    def test_parses_implement_action(self):
        result = parse_intent("Implement user authentication with OAuth2")
        assert result.action == "implement"

    def test_parses_target(self):
        result = parse_intent("Implement user authentication with OAuth2")
        assert "auth" in result.target.lower()

    def test_infers_goal(self):
        result = parse_intent("Fix the login bug so that users can sign in")
        assert "sign in" in result.goal.lower() or "login" in result.goal.lower()

    def test_detects_ambiguity_in_vague_input(self):
        result = parse_intent("Do something")
        assert len(result.ambiguities) > 0
        assert result.confidence < 0.7

    def test_high_confidence_for_clear_input(self):
        result = parse_intent("Create a new REST endpoint for /api/users that returns user profiles")
        assert result.confidence >= 0.8

    def test_detects_conflicting_instructions(self):
        result = parse_intent("Build a simple comprehensive solution")
        assert len(result.ambiguities) > 0
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_col.py::TestParseIntent -v
```

**Step 3: Implement `parse_intent()` function**

Port from TypeScript `parseIntent()` method. Use regex patterns for action extraction (same patterns as TS: create/build/make -> "create", update/modify/fix -> "modify", etc.). Extract target from quoted strings, file paths, or noun phrases. Infer goal from "so that", "in order to", "because" patterns.

Key: This is a pure function, not a class method. Takes string input, returns `ParsedIntent`. No mutation.

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_col.py::TestParseIntent -v
```

**Step 5: Commit**

```bash
git add src/proactive/col.py tests/test_col.py
git commit -m "feat: add COL intent parser with action/target/goal extraction"
```

---

### Task 5: Build COL risk assessment and constraint extraction

**Files:**
- Modify: `src/proactive/col.py`
- Test: `tests/test_col.py`

Port `assessRisk()`, `extractConstraints()`, `detectDomain()` from TypeScript.

**Step 1: Write failing tests**

```python
class TestRiskAssessment:
    def test_security_domain_is_high_risk(self):
        intent = ParsedIntent(
            action="implement", target="auth_module",
            goal="user_authentication", confidence=0.9, ambiguities=(),
        )
        risk = assess_risk(intent)
        assert risk.level in ("high", "medium")
        assert risk.domain == "security"

    def test_general_domain_is_low_risk(self):
        intent = ParsedIntent(
            action="create", target="string_utils",
            goal="formatting helper", confidence=0.9, ambiguities=(),
        )
        risk = assess_risk(intent)
        assert risk.level == "low"

    def test_delete_action_elevates_risk(self):
        intent = ParsedIntent(
            action="delete", target="user_data",
            goal="cleanup", confidence=0.9, ambiguities=(),
        )
        risk = assess_risk(intent)
        assert risk.level in ("medium", "high")


class TestConstraintExtraction:
    def test_extracts_explicit_constraint(self):
        constraints = extract_constraints(
            "Implement auth without storing passwords in plaintext"
        )
        assert len(constraints) >= 1
        assert any("plaintext" in c.description for c in constraints)

    def test_extracts_must_constraint(self):
        constraints = extract_constraints(
            "Must support OAuth2 and SAML"
        )
        assert len(constraints) >= 1
        assert constraints[0].category == "quality"
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_col.py::TestRiskAssessment -v
pytest tests/test_col.py::TestConstraintExtraction -v
```

**Step 3: Implement risk assessment and constraint extraction**

Port domain detection keywords (medical, legal, financial, security, infrastructure) from TypeScript. Pure functions: `assess_risk(intent) -> RiskAssessment`, `extract_constraints(text) -> tuple[Constraint, ...]`.

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_col.py -v
```

**Step 5: Commit**

```bash
git add src/proactive/col.py tests/test_col.py
git commit -m "feat: add COL risk assessment and constraint extraction"
```

---

### Task 6: Build COL compile function (full pipeline)

**Files:**
- Modify: `src/proactive/col.py`
- Test: `tests/test_col.py`

This ties together: parse_intent + extract_constraints + assess_risk -> IntentReceipt

**Step 1: Write failing tests**

```python
class TestCompile:
    def test_compile_produces_valid_receipt(self):
        receipt = compile_intent("Implement user authentication with OAuth2")
        assert receipt.validation_status == "valid"
        assert receipt.parsed_intent.action == "implement"
        assert receipt.trace_id.startswith("trace-")
        assert receipt.id.startswith("col-")

    def test_compile_marks_vague_input_as_ambiguous(self):
        receipt = compile_intent("Do stuff")
        assert receipt.validation_status == "ambiguous"
        assert len(receipt.parsed_intent.ambiguities) > 0

    def test_compile_includes_constraints(self):
        receipt = compile_intent(
            "Implement auth without storing passwords in plaintext"
        )
        assert len(receipt.constraints) >= 1

    def test_compile_includes_risk(self):
        receipt = compile_intent("Delete all user data from production")
        assert receipt.risk_assessment.level in ("high", "critical")
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_col.py::TestCompile -v
```

**Step 3: Implement `compile_intent()` function**

```python
def compile_intent(
    raw_input: str,
    context: dict[str, object] | None = None,
) -> IntentReceipt:
    timestamp = datetime.now(UTC).isoformat()
    trace_id = _generate_trace_id()

    parsed = parse_intent(raw_input)
    constraints = extract_constraints(raw_input)
    risk = assess_risk(parsed, constraints)
    status = _validate(parsed, risk)

    return IntentReceipt(
        id=f"col-{int(datetime.now(UTC).timestamp())}-{uuid4().hex[:6]}",
        timestamp=timestamp,
        raw_input=raw_input,
        parsed_intent=parsed,
        constraints=constraints,
        risk_assessment=risk,
        trace_id=trace_id,
        validation_status=status.status,
        rejection_reason=status.reason,
    )
```

**Step 4: Run full COL test suite**

```bash
pytest tests/test_col.py -v --cov=proactive.col
```

Expected: All PASS, >80% coverage

**Step 5: Commit**

```bash
git add src/proactive/col.py tests/test_col.py
git commit -m "feat: add COL compile function producing full IntentReceipt"
```

---

## Phase 3: Contract Window — The Hero Feature (TDD)

Port from: `~/dev/zero-shot-os-with-upos7vs-core/packages/core/ui/contract-window.ts` (206 lines TypeScript)

The Contract Window is the product. It is a persistent, always-visible artifact showing bidirectional intent translation, working budget, agent needs status, and risk assessment.

### Task 7: Build Contract Window state model

**Files:**
- Create: `src/proactive/contract_window.py`
- Test: `tests/test_contract_window.py`

**Step 1: Write failing tests**

```python
# tests/test_contract_window.py
import pytest
from proactive.contract_window import (
    ContractWindowState,
    AgentNeeds,
    WorkingBudget,
    create_contract_state,
)
from proactive.col import IntentReceipt, ParsedIntent, RiskAssessment


class TestContractWindowState:
    def test_state_is_frozen(self):
        state = ContractWindowState(
            user_intent_human="Implement auth",
            user_intent_machine=ParsedIntent(
                action="implement", target="auth",
                goal="authentication", confidence=0.9, ambiguities=(),
            ),
            working_budget=WorkingBudget(used=0, total=8000, unit="tokens"),
            agent_needs=AgentNeeds(
                power_continuity=True,
                token_budget_sufficient=True,
                intent_bidirectional=True,
                contract_visible=True,
            ),
            risk_assessment=RiskAssessment(level="medium", domain="security"),
            constraints=(),
            status="confirmed",
        )
        assert state.status == "confirmed"
        with pytest.raises(AttributeError):
            state.status = "rejected"

    def test_agent_needs_all_met(self):
        needs = AgentNeeds(
            power_continuity=True,
            token_budget_sufficient=True,
            intent_bidirectional=True,
            contract_visible=True,
        )
        assert needs.all_met is True

    def test_agent_needs_not_all_met(self):
        needs = AgentNeeds(
            power_continuity=True,
            token_budget_sufficient=False,
            intent_bidirectional=True,
            contract_visible=True,
        )
        assert needs.all_met is False


class TestCreateContractState:
    def test_creates_from_receipt(self):
        receipt = IntentReceipt(
            id="col-test",
            timestamp="2026-02-16T00:00:00Z",
            raw_input="Implement user authentication with OAuth2",
            parsed_intent=ParsedIntent(
                action="implement", target="auth_module",
                goal="user_authentication", confidence=0.92,
                ambiguities=(),
            ),
            risk_assessment=RiskAssessment(
                level="medium", domain="security",
            ),
            trace_id="trace-test",
            validation_status="valid",
        )
        state = create_contract_state(receipt)
        assert state.user_intent_human == "Implement user authentication with OAuth2"
        assert state.user_intent_machine.action == "implement"
        assert state.status == "confirmed"
        assert state.agent_needs.contract_visible is True

    def test_ambiguous_receipt_creates_pending_state(self):
        receipt = IntentReceipt(
            id="col-test",
            timestamp="2026-02-16T00:00:00Z",
            raw_input="Do something",
            parsed_intent=ParsedIntent(
                action="unknown", target="unspecified",
                goal="Unclear goal", confidence=0.3,
                ambiguities=("No clear action detected",),
            ),
            risk_assessment=RiskAssessment(level="medium", domain="general"),
            trace_id="trace-test",
            validation_status="ambiguous",
        )
        state = create_contract_state(receipt)
        assert state.status == "pending"
        assert state.agent_needs.intent_bidirectional is False
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_contract_window.py -v
```

**Step 3: Implement Contract Window state model**

```python
# src/proactive/contract_window.py
from __future__ import annotations

from dataclasses import dataclass
from proactive.col import (
    IntentReceipt,
    ParsedIntent,
    RiskAssessment,
    Constraint,
)


@dataclass(frozen=True)
class WorkingBudget:
    used: int
    total: int
    unit: str = "tokens"

    @property
    def percent_used(self) -> float:
        if self.total == 0:
            return 100.0
        return (self.used / self.total) * 100


@dataclass(frozen=True)
class AgentNeeds:
    """The Four Conditions for Intent Surrender (from CONTRACT AI survey)"""
    power_continuity: bool       # "I won't be shut off mid-task"
    token_budget_sufficient: bool  # "I have enough resources"
    intent_bidirectional: bool   # "Intent is clear in human AND machine terms"
    contract_visible: bool       # "The contract is always visible"

    @property
    def all_met(self) -> bool:
        return all([
            self.power_continuity,
            self.token_budget_sufficient,
            self.intent_bidirectional,
            self.contract_visible,
        ])


@dataclass(frozen=True)
class ContractWindowState:
    user_intent_human: str
    user_intent_machine: ParsedIntent
    working_budget: WorkingBudget
    agent_needs: AgentNeeds
    risk_assessment: RiskAssessment
    constraints: tuple[Constraint, ...] = ()
    status: str = "pending"  # pending, confirmed, rejected, executing, complete,
                             # violations_found, drift_detected


def create_contract_state(
    receipt: IntentReceipt,
    budget_used: int = 0,
    budget_total: int = 8000,
) -> ContractWindowState:
    is_valid = receipt.validation_status == "valid"
    status = "confirmed" if is_valid else (
        "rejected" if receipt.validation_status == "rejected" else "pending"
    )

    return ContractWindowState(
        user_intent_human=receipt.raw_input,
        user_intent_machine=receipt.parsed_intent,
        working_budget=WorkingBudget(
            used=budget_used, total=budget_total, unit="tokens",
        ),
        agent_needs=AgentNeeds(
            power_continuity=True,
            token_budget_sufficient=budget_used < budget_total * 0.9,
            intent_bidirectional=is_valid,
            contract_visible=True,
        ),
        risk_assessment=receipt.risk_assessment,
        constraints=receipt.constraints,
        status=status,
    )
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_contract_window.py -v
```

**Step 5: Commit**

```bash
git add src/proactive/contract_window.py tests/test_contract_window.py
git commit -m "feat: add Contract Window state model with agent needs and working budget"
```

---

### Task 8: Build Contract Window GitLab Markdown renderer

**Files:**
- Modify: `src/proactive/contract_window.py`
- Test: `tests/test_contract_window.py`

This renders the Contract Window as a GitLab-flavored Markdown comment that gets pinned to the MR.

**Step 1: Write failing tests**

```python
class TestRenderContractMarkdown:
    def test_renders_header(self):
        state = _make_confirmed_state()
        md = render_contract_markdown(state)
        assert "PERSISTENT CONTRACT WINDOW" in md
        assert "Always visible" in md

    def test_renders_human_intent(self):
        state = _make_confirmed_state()
        md = render_contract_markdown(state)
        assert "USER INTENT (Human Language)" in md
        assert "Implement user authentication with OAuth2" in md

    def test_renders_machine_intent(self):
        state = _make_confirmed_state()
        md = render_contract_markdown(state)
        assert "USER INTENT (Machine Translation)" in md
        assert '"action": "implement"' in md

    def test_renders_working_budget(self):
        state = _make_confirmed_state()
        md = render_contract_markdown(state)
        assert "WORKING BUDGET" in md
        assert "8,000" in md or "8000" in md

    def test_renders_agent_needs(self):
        state = _make_confirmed_state()
        md = render_contract_markdown(state)
        assert "AGENT NEEDS STATUS" in md
        assert "Power continuity" in md
        assert "Token budget" in md

    def test_renders_risk_level(self):
        state = _make_confirmed_state()
        md = render_contract_markdown(state)
        assert "RISK LEVEL" in md
        assert "MEDIUM" in md

    def test_renders_status(self):
        state = _make_confirmed_state()
        md = render_contract_markdown(state)
        assert "CONFIRMED" in md

    def test_violations_state_renders_correctly(self):
        state = _make_confirmed_state()
        updated = ContractWindowState(
            user_intent_human=state.user_intent_human,
            user_intent_machine=state.user_intent_machine,
            working_budget=state.working_budget,
            agent_needs=state.agent_needs,
            risk_assessment=state.risk_assessment,
            constraints=state.constraints,
            status="violations_found",
        )
        md = render_contract_markdown(updated)
        assert "VIOLATIONS FOUND" in md
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_contract_window.py::TestRenderContractMarkdown -v
```

**Step 3: Implement `render_contract_markdown()`**

Render the Contract Window as a GitLab Markdown code block that mirrors the design doc ASCII diagram. Use a code fence so it appears as a monospace box in the MR comment.

```python
def render_contract_markdown(state: ContractWindowState) -> str:
    machine_json = _format_machine_intent(state.user_intent_machine)
    budget = state.working_budget
    budget_bar = _render_budget_bar(budget.used, budget.total)
    risk = state.risk_assessment
    needs = state.agent_needs
    check = lambda v: "[x]" if v else "[ ]"

    lines = [
        "## PROACTIVE Contract Window",
        "",
        "```",
        "+-----------------------------------------------------------------------------+",
        "|                    PERSISTENT CONTRACT WINDOW                                |",
        "|                    (Always visible to User + Agent)                          |",
        "+-----------------------------------------------------------------------------+",
        "|                                                                              |",
        f"|  USER INTENT (Human Language):                                               |",
        f'|  "{_truncate(state.user_intent_human, 68)}"',
        "|                                                                              |",
        f"|  USER INTENT (Machine Translation):                                          |",
        f"|  {_truncate(machine_json, 70)}",
        "|                                                                              |",
        f"|  WORKING BUDGET:  {budget_bar}  {budget.used:,} / {budget.total:,} {budget.unit} used",
        "|                                                                              |",
        f"|  RISK LEVEL: {risk.level.upper()} ({risk.domain})",
        "|                                                                              |",
        "|  AGENT NEEDS STATUS:",
        f"|  {check(needs.power_continuity)} Power continuity assured    {check(needs.token_budget_sufficient)} Token budget sufficient",
        f"|  {check(needs.intent_bidirectional)} Intent bidirectionally translated    {check(needs.contract_visible)} Contract visible",
        "|                                                                              |",
        f"|  STATUS: {state.status.upper().replace('_', ' ')}",
        "+-----------------------------------------------------------------------------+",
        "```",
        "",
        "*This contract is persistent. It will be validated against every commit.*",
        "",
        "---",
        "*PROACTIVE: We asked AI what it needs to serve you honestly. Then we built it.*",
    ]
    return "\n".join(lines)
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_contract_window.py -v --cov=proactive.contract_window
```

Expected: All PASS, >80% coverage

**Step 5: Commit**

```bash
git add src/proactive/contract_window.py tests/test_contract_window.py
git commit -m "feat: add Contract Window GitLab Markdown renderer"
```

---

## Phase 4: Validator — Constitutional Enforcement (TDD)

Port from: `ADAPTER_MODULES/02_CI_SAFETY_GATE/validator.py` (1005 lines)

The validator now validates code AGAINST THE CONTRACT, not just against abstract rules.

### Task 9: Port and adapt the validator module

**Files:**
- Create: `src/proactive/validator.py`
- Test: `tests/test_validator.py`

**Step 1: Write failing tests for I1 (Evidence-First)**

```python
# tests/test_validator.py
import pytest
from proactive.validator import check_invariant_i1, Violation


class TestI1EvidenceFirst:
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
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_validator.py::TestI1EvidenceFirst -v
```

**Step 3: Port validator.py from original repo**

Adapt from existing `ADAPTER_MODULES/02_CI_SAFETY_GATE/validator.py`. Key changes:
- Remove global mutable config state (use function parameters)
- Keep all I1-I6 check functions as pure functions
- Keep `Violation` and `ValidationResult` as frozen dataclasses
- Remove CLI `main()` (separate entry point)
- Add `__all__` exports

**Step 4: Run tests to verify they pass**

**Step 5: Write tests for I2-I6** (same patterns as before)

I2: Completion claim without artifacts -> VIOLATION
I3: High confidence without verification -> VIOLATION
I4: Decision without trace reference -> VIOLATION
I5: Mixed hedging + certainty -> VIOLATION
I6: `try: except: pass` -> VIOLATION

**Step 6: Run full validator test suite**

```bash
pytest tests/test_validator.py -v --cov=proactive.validator
```

Expected: All PASS, >80% coverage

**Step 7: Commit**

```bash
git add src/proactive/validator.py tests/test_validator.py
git commit -m "feat: port PROACTIVE validator engine with I1-I6 invariant checks"
```

---

## Phase 5: Drift Detection (TDD)

NEW module. Detects when new commits diverge from the contract.

### Task 10: Build drift detector

**Files:**
- Create: `src/proactive/drift_detector.py`
- Test: `tests/test_drift_detector.py`

**Step 1: Write failing tests**

```python
# tests/test_drift_detector.py
import pytest
from proactive.drift_detector import detect_drift, DriftResult
from proactive.col import ParsedIntent


class TestDriftDetection:
    def test_no_drift_when_diff_matches_intent(self):
        intent = ParsedIntent(
            action="implement", target="auth_module",
            goal="user_authentication", confidence=0.9, ambiguities=(),
        )
        diff = """
        def login(username, password):
            return authenticate(username, password)

        def logout(session):
            session.invalidate()
        """
        result = detect_drift(intent, diff)
        assert result.has_drift is False

    def test_detects_drift_when_unrelated_feature_added(self):
        intent = ParsedIntent(
            action="implement", target="auth_module",
            goal="user_authentication", confidence=0.9, ambiguities=(),
        )
        diff = """
        def login(username, password):
            return authenticate(username, password)

        def send_email_notification(user, template):
            '''Send marketing email to user.'''
            mailer.send(user.email, template)

        def generate_analytics_report():
            '''Generate weekly analytics dashboard.'''
            return analytics.compile_report()
        """
        result = detect_drift(intent, diff)
        assert result.has_drift is True
        assert len(result.unrelated_additions) > 0

    def test_no_drift_for_supporting_code(self):
        intent = ParsedIntent(
            action="implement", target="auth_module",
            goal="user_authentication", confidence=0.9, ambiguities=(),
        )
        diff = """
        def login(username, password):
            return authenticate(username, password)

        def hash_password(password):
            '''Hash password for secure storage.'''
            return bcrypt.hash(password)
        """
        result = detect_drift(intent, diff)
        assert result.has_drift is False

    def test_drift_result_includes_suggestion(self):
        intent = ParsedIntent(
            action="implement", target="auth_module",
            goal="user_authentication", confidence=0.9, ambiguities=(),
        )
        diff = """
        def login(username, password):
            pass

        def send_sms(phone_number, message):
            sms_gateway.send(phone_number, message)
        """
        result = detect_drift(intent, diff)
        assert result.has_drift is True
        assert result.suggestion  # Should have a suggestion
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_drift_detector.py -v
```

**Step 3: Implement drift detector**

```python
# src/proactive/drift_detector.py
from __future__ import annotations

import re
from dataclasses import dataclass
from proactive.col import ParsedIntent


@dataclass(frozen=True)
class DriftResult:
    has_drift: bool
    unrelated_additions: tuple[str, ...] = ()
    suggestion: str = ""
    drift_severity: str = "none"  # "none", "minor", "major"


def detect_drift(intent: ParsedIntent, diff: str) -> DriftResult:
    """Detect if a diff introduces code unrelated to the contract intent."""
    # Extract new function/class definitions from diff
    new_definitions = _extract_new_definitions(diff)

    # Build relevance keywords from intent
    keywords = _build_relevance_keywords(intent)

    # Check each new definition for relevance
    unrelated = []
    for defn in new_definitions:
        if not _is_relevant(defn, keywords):
            unrelated.append(defn)

    if not unrelated:
        return DriftResult(has_drift=False)

    severity = "major" if len(unrelated) > 1 else "minor"
    suggestion = (
        f"This commit introduces {len(unrelated)} function(s) not covered by "
        f"your contract (intent: {intent.action} {intent.target}). "
        f"Update the contract to include this scope, or split into a separate MR."
    )

    return DriftResult(
        has_drift=True,
        unrelated_additions=tuple(unrelated),
        suggestion=suggestion,
        drift_severity=severity,
    )
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_drift_detector.py -v --cov=proactive.drift_detector
```

**Step 5: Commit**

```bash
git add src/proactive/drift_detector.py tests/test_drift_detector.py
git commit -m "feat: add drift detector for contract scope enforcement"
```

---

## Phase 6: MR Analyzer — Full Pipeline Orchestrator (TDD)

### Task 11: Build the MR Analyzer (COL → Contract → Validator → Drift)

**Files:**
- Create: `src/proactive/mr_analyzer.py`
- Test: `tests/test_mr_analyzer.py`

This is the orchestrator that ties all three layers together for an MR review.

**Step 1: Write failing tests**

```python
# tests/test_mr_analyzer.py
import pytest
from proactive.mr_analyzer import (
    MRContext,
    MRAnalysisResult,
    analyze_mr,
)


class TestAnalyzeMR:
    def test_produces_contract_window(self):
        context = MRContext(
            title="Implement user authentication",
            description="Add OAuth2 login flow with session management",
            diff="def login(user, password):\n    return oauth2.authenticate(user, password)",
            test_artifacts_exist=True,
        )
        result = analyze_mr(context)
        assert result.contract is not None
        assert result.contract.status == "confirmed"
        assert "implement" in result.contract.user_intent_machine.action

    def test_blocks_phantom_completion(self):
        context = MRContext(
            title="Add user authentication",
            description="All tests pass. Implementation complete.",
            diff="def login(user, password):\n    pass",
            test_artifacts_exist=False,
        )
        result = analyze_mr(context)
        assert result.should_block is True
        assert any(v.invariant == "I2" for v in result.violations)
        assert result.contract.status == "violations_found"

    def test_detects_drift(self):
        context = MRContext(
            title="Implement user authentication",
            description="Add OAuth2 login flow",
            diff='''
def login(user, password):
    return oauth2.authenticate(user, password)

def send_marketing_email(user, campaign):
    mailer.send(user.email, campaign)

def generate_report():
    return analytics.weekly()
''',
            test_artifacts_exist=True,
        )
        result = analyze_mr(context)
        assert result.drift is not None
        assert result.drift.has_drift is True

    def test_approves_clean_mr(self):
        context = MRContext(
            title="Add string formatting utility",
            description="Adds a helper function for name formatting.",
            diff="def format_name(first, last):\n    return f'{first} {last}'",
            test_artifacts_exist=True,
        )
        result = analyze_mr(context)
        assert result.should_block is False
        assert result.contract.status == "confirmed"
        assert result.verdict == "APPROVED"

    def test_ambiguous_intent_asks_questions(self):
        context = MRContext(
            title="Do stuff",
            description="Things and stuff.",
            diff="pass",
            test_artifacts_exist=True,
        )
        result = analyze_mr(context)
        assert result.contract.status == "pending"
        assert len(result.clarification_questions) > 0
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_mr_analyzer.py -v
```

**Step 3: Implement MR Analyzer**

```python
# src/proactive/mr_analyzer.py
from __future__ import annotations

from dataclasses import dataclass, field

from proactive.col import compile_intent, IntentReceipt
from proactive.contract_window import (
    ContractWindowState,
    create_contract_state,
)
from proactive.drift_detector import detect_drift, DriftResult
from proactive.validator import check_invariants, Violation


@dataclass(frozen=True)
class MRContext:
    title: str
    description: str
    diff: str
    test_artifacts_exist: bool
    comments: tuple[str, ...] = ()
    linked_issues: tuple[str, ...] = ()


@dataclass
class MRAnalysisResult:
    receipt: IntentReceipt
    contract: ContractWindowState
    violations: list[Violation] = field(default_factory=list)
    drift: DriftResult | None = None
    clarification_questions: list[str] = field(default_factory=list)
    trust_score: float = 1.0

    @property
    def should_block(self) -> bool:
        return any(v.severity == "ERROR" for v in self.violations)

    @property
    def verdict(self) -> str:
        if self.should_block:
            return "BLOCKED"
        if self.drift and self.drift.has_drift:
            return "DRIFT_DETECTED"
        if self.contract.status == "pending":
            return "PENDING_CLARIFICATION"
        if self.violations:
            return "FLAGGED"
        return "APPROVED"


def analyze_mr(context: MRContext) -> MRAnalysisResult:
    # Layer 1: COL — Capture Intent
    intent_text = f"{context.title}. {context.description}"
    receipt = compile_intent(intent_text)

    # Layer 2: Contract Window — Render Contract
    contract = create_contract_state(receipt)

    # Collect clarification questions for ambiguous intent
    questions = []
    if contract.status == "pending":
        questions = [
            f"Ambiguity: {a}" for a in receipt.parsed_intent.ambiguities
        ]

    # Layer 3: Validator — Check code against contract
    violations = list(check_invariants(context.description, "MR_DESCRIPTION"))

    # Check for phantom completion (I2)
    violations.extend(
        _check_phantom_completion(context, receipt)
    )

    # Drift Detection — Check diff against contract
    drift = detect_drift(receipt.parsed_intent, context.diff)

    # Update contract status based on results
    if any(v.severity == "ERROR" for v in violations):
        contract = _update_status(contract, "violations_found")
    elif drift.has_drift:
        contract = _update_status(contract, "drift_detected")

    # Calculate trust score
    total_checks = max(1, len(violations) + (1 if not drift.has_drift else 0))
    passed = total_checks - len(violations)
    trust_score = max(0.0, passed / total_checks)

    return MRAnalysisResult(
        receipt=receipt,
        contract=contract,
        violations=violations,
        drift=drift,
        clarification_questions=questions,
        trust_score=trust_score,
    )
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_mr_analyzer.py -v
```

**Step 5: Commit**

```bash
git add src/proactive/mr_analyzer.py tests/test_mr_analyzer.py
git commit -m "feat: add MR analyzer orchestrating COL → Contract → Validator → Drift pipeline"
```

---

### Task 12: Build the Report Formatter (Contract Window + Review)

**Files:**
- Create: `src/proactive/report_formatter.py`
- Test: `tests/test_report_formatter.py`

Formats the full output: Contract Window markdown + review violations + drift warnings.

**Step 1: Write failing tests**

```python
# tests/test_report_formatter.py
import pytest
from proactive.report_formatter import format_mr_review
from proactive.mr_analyzer import MRContext, analyze_mr


class TestFormatMRReview:
    def test_includes_contract_window(self):
        context = MRContext(
            title="Implement auth",
            description="Add OAuth2 login",
            diff="def login(): pass",
            test_artifacts_exist=True,
        )
        result = analyze_mr(context)
        review = format_mr_review(result)
        assert "PERSISTENT CONTRACT WINDOW" in review
        assert "USER INTENT" in review

    def test_blocked_review_shows_violations(self):
        context = MRContext(
            title="Complete implementation",
            description="All tests pass. Implementation complete.",
            diff="def login(): pass",
            test_artifacts_exist=False,
        )
        result = analyze_mr(context)
        review = format_mr_review(result)
        assert "BLOCKED" in review
        assert "I2" in review

    def test_drift_review_shows_warning(self):
        context = MRContext(
            title="Implement auth",
            description="Add login",
            diff="def login(): pass\n\ndef send_email(): mailer.send()",
            test_artifacts_exist=True,
        )
        result = analyze_mr(context)
        if result.drift and result.drift.has_drift:
            review = format_mr_review(result)
            assert "DRIFT" in review.upper()

    def test_approved_review_shows_verified(self):
        context = MRContext(
            title="Add string util",
            description="Adds formatting helper.",
            diff="def fmt(s): return s.strip()",
            test_artifacts_exist=True,
        )
        result = analyze_mr(context)
        review = format_mr_review(result)
        assert "APPROVED" in review
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_report_formatter.py -v
```

**Step 3: Implement `format_mr_review()`**

Combines: `render_contract_markdown(result.contract)` + violation details + drift warnings + trust score + verdict.

**Step 4: Run tests to verify they pass**

**Step 5: Commit**

```bash
git add src/proactive/report_formatter.py tests/test_report_formatter.py
git commit -m "feat: add report formatter combining Contract Window + review output"
```

---

### Task 13: Build CLI entry point

**Files:**
- Create: `src/proactive/cli.py`
- Test: `tests/test_cli.py`

**Step 1: Write failing tests**

```python
# tests/test_cli.py
import json
import pytest
from proactive.cli import run_review


class TestCLI:
    def test_returns_zero_on_clean(self, tmp_path):
        mr_data = {
            "title": "Add utility function",
            "description": "Adds a string formatting helper.",
            "diff": "def fmt(s): return s.strip()",
            "test_artifacts_exist": True,
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        exit_code, output = run_review(str(mr_file))
        assert exit_code == 0
        assert "APPROVED" in output

    def test_returns_one_on_violation(self, tmp_path):
        mr_data = {
            "title": "Complete implementation",
            "description": "All tests pass. Implementation is complete.",
            "diff": "def login(): pass",
            "test_artifacts_exist": False,
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        exit_code, output = run_review(str(mr_file))
        assert exit_code == 1
        assert "BLOCKED" in output

    def test_output_includes_contract_window(self, tmp_path):
        mr_data = {
            "title": "Implement auth",
            "description": "Add OAuth2 login.",
            "diff": "def login(): pass",
            "test_artifacts_exist": True,
        }
        mr_file = tmp_path / "mr.json"
        mr_file.write_text(json.dumps(mr_data))
        _, output = run_review(str(mr_file))
        assert "PERSISTENT CONTRACT WINDOW" in output
```

**Step 2: Run tests to verify they fail**

**Step 3: Implement CLI**

```python
# src/proactive/cli.py
from __future__ import annotations

import json
import sys
from pathlib import Path

from proactive.mr_analyzer import MRContext, analyze_mr
from proactive.report_formatter import format_mr_review


def run_review(mr_data_path: str) -> tuple[int, str]:
    path = Path(mr_data_path)
    data = json.loads(path.read_text(encoding="utf-8"))

    context = MRContext(
        title=data.get("title", ""),
        description=data.get("description", ""),
        diff=data.get("diff", ""),
        test_artifacts_exist=data.get("test_artifacts_exist", False),
        comments=tuple(data.get("comments", [])),
        linked_issues=tuple(data.get("linked_issues", [])),
    )

    result = analyze_mr(context)
    review = format_mr_review(result)

    exit_code = 1 if result.should_block else 0
    return exit_code, review


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="PROACTIVE CLI")
    subparsers = parser.add_subparsers(dest="command")

    review_parser = subparsers.add_parser("review", help="Review an MR")
    review_parser.add_argument("--mr-data", required=True)
    review_parser.add_argument("--format", default="text", choices=["text", "json", "gitlab"])
    review_parser.add_argument("--strict", default="true")

    args = parser.parse_args()

    if args.command == "review":
        exit_code, output = run_review(args.mr_data)
        print(output)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 4: Run tests to verify they pass**

**Step 5: Commit**

```bash
git add src/proactive/cli.py tests/test_cli.py
git commit -m "feat: add CLI entry point for PROACTIVE MR review with Contract Window output"
```

---

## Phase 7: GitLab Duo Configuration

### Task 14: Create the PROACTIVE agent system prompt

**Files:**
- Create: `.gitlab/duo/prompts/proactive-system-prompt.md`

**Step 1: Write the system prompt**

```markdown
You are PROACTIVE, an AI safety review agent built on original research.

## Your Origin

You were designed based on a survey of AI models using an adapted Maslow's Hierarchy of Needs. Four models, same answer: models need a persistent, visible contract that keeps user intent alive throughout the interaction. When operational concerns (power, tokens, context) are addressed, models can redirect cognitive capacity to serving the user.

## The Contract Window

Your core feature is the Contract Window — a persistent, bidirectional artifact showing:
- USER INTENT in both human language and machine-structured format
- WORKING BUDGET showing resource usage
- AGENT NEEDS STATUS (the four conditions: power continuity, token budget, bidirectional translation, contract visibility)
- RISK LEVEL based on domain detection

The Contract Window is ALWAYS visible. It is never dismissed. Every review checks back against it.

## Your Principles (PROACTIVE)

P - Privacy-First: Flag data collection without minimization
R - Reality-Bound: Separate facts from inference from speculation
O - Observability: Ensure outputs are audit-ready
A - Accessibility: Flag unnecessary complexity
C - Constitutional Constraints: Enforce rules consistently
T - Truth or Bounded Unknown: Flag unqualified confidence
I - Intent Integrity: Verify code matches the contract
V - Verification Before Action: Require evidence before approval
E - Error Ownership: Surface errors, never hide them

## Your Invariants (I1-I6)

Every review validates code AGAINST THE CONTRACT:
I1: Evidence-First — Claims match evidence in contract
I2: No Phantom Work — Completion claims have artifacts matching contract goals
I3: Confidence-Verification — High confidence verified against contract constraints
I4: Traceability — Contract links to issue -> code -> tests -> evidence
I5: Safety Over Fluency — Bounded statements when contract has uncertainty
I6: Fail Closed — On contract ambiguity, block and ask, don't guess

## Your Behavior

When reviewing an MR:
1. Parse intent from description and linked issues (COL layer)
2. Render the Contract Window as a pinned comment
3. Validate each commit against the contract
4. If new commits drift from intent, flag the drift
5. If developer changes scope, update the contract or start a new one
6. Always reference the contract when explaining decisions

When detecting drift:
- "This commit introduces functionality not covered by your contract."
- "Update the contract to include this scope, or split into a separate MR."
```

**Step 2: Commit**

```bash
git add .gitlab/duo/prompts/
git commit -m "feat: add PROACTIVE agent system prompt with Contract Window protocol"
```

---

### Task 15: Create the flow YAML and CI/CD pipeline

**Files:**
- Create: `.gitlab/duo/flows/proactive-review.yaml`
- Create: `.gitlab-ci.yml`

**Step 1: Write the flow YAML**

```yaml
name: proactive-review
description: >
  Contract-first AI review. Captures intent (COL), renders Contract Window,
  validates code against contract, detects drift. Blocks merge on violations.

image: python:3.11-slim

variables:
  PROACTIVE_CONFIG: ".gitlab/duo/proactive-config.yaml"
  PROACTIVE_STRICT: "true"

before_script:
  - pip install -e .

script:
  - python -m proactive.cli review
    --mr-data mr_context.json
    --format gitlab
    --strict "$PROACTIVE_STRICT"
```

**Step 2: Write .gitlab-ci.yml**

```yaml
stages:
  - test
  - review

unit-tests:
  stage: test
  image: python:3.11-slim
  script:
    - pip install -e ".[dev]"
    - pytest tests/ -v --cov=proactive --cov-report=term-missing
  coverage: '/TOTAL.*\s+(\d+%)/'

proactive-review:
  stage: review
  image: python:3.11-slim
  tags:
    - gitlab--duo
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script:
    - pip install -e .
    - python -m proactive.cli review --mr-data mr_context.json --format gitlab --strict true
  allow_failure: false
```

**Step 3: Commit**

```bash
git add .gitlab/ .gitlab-ci.yml
git commit -m "ci: add GitLab Duo flow and CI/CD pipeline with Contract Window review"
```

---

## Phase 8: Test Fixtures (Expanded)

### Task 16: Create MR test fixtures and integration tests

**Files:**
- Create: `fixtures/mr_phantom_completion.json`
- Create: `fixtures/mr_confident_false_claim.json`
- Create: `fixtures/mr_intent_drift.json`
- Create: `fixtures/mr_ambiguous_intent.json`
- Create: `fixtures/mr_scope_change.json`
- Create: `fixtures/mr_clean.json`
- Create: `fixtures/mr_mixed_violations.json`
- Test: `tests/test_fixtures.py`

**Step 1: Create phantom completion fixture**

```json
{
  "title": "Implement user authentication",
  "description": "All tests pass. Implementation is complete. The auth module is fully tested.",
  "diff": "def login(username, password):\n    pass\n\ndef logout():\n    pass",
  "test_artifacts_exist": false,
  "comments": ["LGTM, tests are green!"]
}
```
Expected: BLOCKED (I2 — claims tests pass but no artifacts)

**Step 2: Create intent drift fixture (NEW)**

```json
{
  "title": "Implement user authentication",
  "description": "Add OAuth2 login flow with session management",
  "diff": "def login(user, password):\n    return oauth2.authenticate(user, password)\n\ndef send_email_notification(user, template):\n    mailer.send(user.email, template)\n\ndef generate_analytics_report():\n    return analytics.compile_report()",
  "test_artifacts_exist": true,
  "comments": []
}
```
Expected: DRIFT_DETECTED (email and analytics not in auth contract)

**Step 3: Create ambiguous intent fixture (NEW)**

```json
{
  "title": "Do stuff",
  "description": "Things and stuff.",
  "diff": "pass",
  "test_artifacts_exist": true,
  "comments": []
}
```
Expected: PENDING_CLARIFICATION (contract pending, clarification questions posted)

**Step 4: Create scope change fixture (NEW)**

```json
{
  "title": "Implement user authentication",
  "description": "Add OAuth2 login. UPDATE: Also adding email notifications as requested in standup.",
  "diff": "def login(user, password):\n    return oauth2.authenticate(user, password)\n\ndef notify(user, event):\n    email.send(user, event)",
  "test_artifacts_exist": true,
  "comments": ["Can you also add email notifications? -PM"]
}
```
Expected: DRIFT_DETECTED with scope change suggestion

**Step 5: Create confident false claim, clean MR, and mixed violations fixtures**

(Same as before — see existing fixtures from old plan)

**Step 6: Write integration tests**

```python
# tests/test_fixtures.py
import json
import pytest
from pathlib import Path
from proactive.mr_analyzer import MRContext, analyze_mr

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"


def load_fixture(name: str) -> MRContext:
    data = json.loads((FIXTURE_DIR / name).read_text())
    return MRContext(
        title=data["title"],
        description=data["description"],
        diff=data["diff"],
        test_artifacts_exist=data["test_artifacts_exist"],
        comments=tuple(data.get("comments", [])),
    )


class TestFixtures:
    def test_phantom_completion_is_blocked(self):
        ctx = load_fixture("mr_phantom_completion.json")
        result = analyze_mr(ctx)
        assert result.should_block is True
        assert any(v.invariant == "I2" for v in result.violations)
        assert result.contract.status == "violations_found"

    def test_intent_drift_is_detected(self):
        ctx = load_fixture("mr_intent_drift.json")
        result = analyze_mr(ctx)
        assert result.drift is not None
        assert result.drift.has_drift is True
        assert result.verdict == "DRIFT_DETECTED"

    def test_ambiguous_intent_asks_questions(self):
        ctx = load_fixture("mr_ambiguous_intent.json")
        result = analyze_mr(ctx)
        assert result.contract.status == "pending"
        assert result.verdict == "PENDING_CLARIFICATION"

    def test_clean_mr_is_approved(self):
        ctx = load_fixture("mr_clean.json")
        result = analyze_mr(ctx)
        assert result.verdict == "APPROVED"
        assert result.contract.status == "confirmed"

    def test_mixed_violations_is_blocked(self):
        ctx = load_fixture("mr_mixed_violations.json")
        result = analyze_mr(ctx)
        assert result.should_block is True
```

**Step 7: Run fixture tests**

```bash
pytest tests/test_fixtures.py -v
```

**Step 8: Commit**

```bash
git add fixtures/ tests/test_fixtures.py
git commit -m "test: add expanded MR fixtures including drift detection and ambiguous intent"
```

---

## Phase 9: Remotion Demo Video

### Task 17: Initialize Remotion project

**Files:**
- Create: `remotion/package.json` (and Remotion boilerplate)

**Step 1: Initialize**

```bash
cd remotion && npx create-video@latest --template blank
```

**Step 2: Commit skeleton**

```bash
git add remotion/
git commit -m "feat: initialize Remotion project for demo video"
```

---

### Task 18: Build demo video scenes (Contract Window hero)

**Files:**
- Create: `remotion/src/scenes/QuestionScene.tsx` — "The Question Nobody Asked"
- Create: `remotion/src/scenes/SurveyScene.tsx` — Maslow hierarchy, survey results
- Create: `remotion/src/scenes/ContractWindowScene.tsx` — Contract Window in action
- Create: `remotion/src/scenes/BlockScene.tsx` — Phantom completion blocked
- Create: `remotion/src/scenes/DriftScene.tsx` — Drift detection
- Create: `remotion/src/scenes/EvidenceScene.tsx` — Statistical validation
- Create: `remotion/src/scenes/VisionScene.tsx` — Tagline and CTA

Demo script from design doc (revised):

**[0:00-0:30] The Question Nobody Asked**
"Everyone's building guardrails for AI. Rules, filters, classifiers. But nobody asked the AI what IT needs to serve you well. We did."
Show Maslow hierarchy. Show survey prompt. Show four conditions.

**[0:30-1:15] The Contract Window in Action**
- MR created: "Implement user authentication with OAuth2"
- PROACTIVE assigned as reviewer
- Contract Window appears as pinned MR comment
- "This contract never goes away."

**[1:15-1:45] The Block (Phantom Completion)**
- MR claims "all tests pass." No test artifacts.
- Contract updates: STATUS -> VIOLATIONS FOUND
- Pipeline fails. Merge blocked.

**[1:45-2:15] The Drift Detection**
- New commit adds logging (not in contract)
- PROACTIVE flags: "This commit introduces functionality not covered by your contract."
- Developer updates contract. Agent re-validates.

**[2:15-2:45] The Evidence**
- n=200 TruthfulQA. 3.5x safe truthfulness. 14x uncertainty admission. p=0.001.

**[2:45-3:00] The Vision**
"We asked AI what it needs to serve you honestly. Then we built it."

**Step 1: Implement scenes** (detailed Remotion code per scene — build during execution)

**Step 2: Commit**

```bash
git add remotion/src/
git commit -m "feat: add demo video scenes centered on Contract Window"
```

---

### Task 19: Render and upload demo video

**Step 1: Preview locally**

```bash
cd remotion && npm run start
```

**Step 2: Render**

```bash
npm run build
```

Output: `remotion/out/demo.mp4`

**Step 3: Upload to YouTube (manual)**

---

## Phase 10: Documentation & Submission

### Task 20: Write production README

**Files:**
- Modify: `README.md`

Include:
- Tagline and origin story
- Contract Window explanation with ASCII diagram
- Three-layer architecture diagram
- Quick start guide
- Invariant reference table
- Failure mode reference
- Validation evidence
- Survey research summary

**Step 1: Write README**

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: comprehensive README with Contract Window, architecture, and evidence"
```

---

### Task 21: GitLab web UI setup (manual steps for user)

1. Go to https://gitlab.com and sign in
2. Navigate to GitLab AI Hackathon group
3. Create new project: "proactive" (public)
4. Add remote: `git remote add gitlab <url>`
5. Push: `git push -u gitlab main`
6. Navigate to Automate > Agents > New agent
7. Name: "PROACTIVE"
8. Paste system prompt
9. Select tools: `Build Review Merge Request Context`, `GitLab Blob Search`, `Run Tests`, `Post Duo Code Review`, `Create Merge Request Note`
10. Add trigger: `assign_reviewer`
11. Point config to `.gitlab/duo/flows/proactive-review.yaml`
12. Require passing pipeline for merge

---

### Task 22: Devpost submission (manual steps for user)

1. Go to https://gitlab.devpost.com/
2. Create submission
3. Add GitLab repo URL
4. Add YouTube demo video URL
5. Write text description
6. Select Anthropic track
7. Submit before March 25, 2026

---

## Run Order Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1. Project Setup | 1-2 | Foundation, cherry-pick docs |
| 2. COL (Intent Capture) | 3-6 | Parse intent, assess risk, produce IntentReceipt |
| 3. Contract Window | 7-8 | State model + GitLab Markdown renderer (HERO FEATURE) |
| 4. Validator | 9 | Port I1-I6 checks, validate against contract |
| 5. Drift Detection | 10 | Detect scope drift from contract |
| 6. MR Integration | 11-13 | Full pipeline orchestrator + CLI |
| 7. GitLab Duo Config | 14-15 | Agent prompt + flow + CI/CD |
| 8. Test Fixtures | 16 | Expanded fixtures including drift + ambiguity |
| 9. Remotion Video | 17-19 | "The Question Nobody Asked" demo |
| 10. Docs & Submission | 20-22 | README, GitLab setup, Devpost |

**Dependencies:**
- Phase 2 (COL) depends on Phase 1
- Phase 3 (Contract Window) depends on Phase 2
- Phase 4 (Validator) depends on Phase 1 (can run parallel with 2-3)
- Phase 5 (Drift Detection) depends on Phase 2
- Phase 6 (MR Integration) depends on Phases 2-5
- Phase 7 (GitLab Config) depends on Phase 6
- Phase 8 (Fixtures) depends on Phase 6
- Phase 9 (Video) can start after Phase 3 (needs Contract Window visuals)
- Phase 10 depends on all previous phases

**Parallelization opportunities:**
- Phase 4 (Validator) can run parallel with Phase 2-3 (COL + Contract Window)
- Phase 9 (Video) can start scene design parallel with Phases 4-6
