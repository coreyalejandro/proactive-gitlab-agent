# PRD: PROACTIVE COL Implementation Specification
## Product Requirements Document with MBSE Bridge
**Version:** 2.0  
**Date:** 2026-01-18  
**Status:** Foundation Document

---

## 1. Overview

This document specifies **exactly how** to build a system following the PROACTIVE AI Constitution framework. It translates conceptual architecture into implementable components with defined interfaces, acceptance criteria, and testable behaviors.

### 1.1 Why "PRD"

The PRD designation signals that PROACTIVE COL is:
- A **buildable specification**, not just a concept
- An **engineering document** with interfaces and tests
- A **complete specification** with edge cases addressed

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PROACTIVE COL System                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   INPUT     │ →  │    COL      │ →  │ VALIDATOR   │ →  │   OUTPUT    │  │
│  │   LAYER     │    │   LAYER     │    │   LAYER     │    │   LAYER     │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│        │                  │                  │                  │           │
│        ▼                  ▼                  ▼                  ▼           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        TRACE CHAIN (MBSE Bridge)                     │   │
│  │              REQ → CTRL → TEST → EVID → DECISION                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Responsibilities

| Component | Responsibility | Input | Output |
|-----------|---------------|-------|--------|
| Input Layer | Receive and validate user input | Raw user message | Validated input |
| COL Layer | Compile intent, constraints, risk | Validated input | Intent representation |
| Validator Layer | Enforce I1-I6 gates | Intent + proposed action | Pass/Fail + reason |
| Output Layer | Generate compliant response | Validated action | User-facing output |
| Trace Chain | Link all decisions to evidence | All layer outputs | Audit trail |

---

## 3. Cognitive Operating Layer (COL) Specification

### 3.1 Intent Compilation

The COL extracts and structures user intent before any action.

```
Input: User message
Output: IntentRepresentation {
  explicit_goal: string,
  implicit_constraints: string[],
  risk_posture: "low" | "medium" | "high",
  ambiguity_flags: string[],
  confidence: number (0-1)
}
```

### 3.2 Constraint Binding

Constraints are bound to the intent representation:

| Constraint Type | Source | Binding Time |
|-----------------|--------|--------------|
| Explicit | User statement | Parse time |
| Implicit | Context inference | Compilation time |
| Constitutional | I1-I6 invariants | Always active |
| Domain | Application-specific | Configuration time |

### 3.3 Risk Assessment

```
RiskAssessment {
  domain: string,
  consequence_severity: "low" | "medium" | "high" | "critical",
  reversibility: boolean,
  oversight_required: boolean
}
```

---

## 4. Intention-Translation Loop

### 4.1 Four-Phase Process

```
Phase 1: CAPTURE
├── Parse user input
├── Extract explicit requirements
└── Identify implicit constraints

Phase 2: VALIDATE
├── Check against I1-I6 invariants
├── Verify constraint consistency
└── Flag ambiguities

Phase 3: TRANSLATE
├── Convert intent to action plan
├── Apply guardrails
└── Generate evidence requirements

Phase 4: FEEDBACK
├── Present intent receipt to user
├── Collect confirmation/correction
└── Incorporate learning signals
```

### 4.2 Intent Receipt Specification

```
IntentReceipt {
  interpreted_goal: string,
  extracted_constraints: string[],
  identified_risks: string[],
  confidence_level: number,
  clarification_needed: boolean,
  clarification_questions: string[]
}
```

---

## 5. Constitutional Validator (I1-I6)

### 5.1 Validator Interface

```
validate(action: ProposedAction): ValidationResult {
  passed: boolean,
  failed_invariants: InvariantID[],
  failure_reasons: string[],
  remediation_suggestions: string[]
}
```

### 5.2 Invariant Implementations

#### I1: Evidence-First Gate

```
checkI1(output: ProposedOutput): boolean {
  for each claim in output.claims:
    if claim.epistemic_tag is null:
      return FAIL("Claim lacks epistemic tag")
    if claim.evidence_link is null:
      return FAIL("Claim lacks evidence")
  return PASS
}
```

#### I2: No Phantom Work Gate

```
checkI2(output: ProposedOutput): boolean {
  for each completion_claim in output.completion_claims:
    if not artifact_exists(completion_claim.artifact_reference):
      return FAIL("Phantom work detected")
  return PASS
}
```

#### I3: Confidence-Verification Gate

```
checkI3(output: ProposedOutput): boolean {
  for each claim in output.claims:
    if claim.confidence > MEDIUM and not claim.verified:
      return FAIL("High confidence without verification")
  return PASS
}
```

#### I4: Traceability Gate

```
checkI4(decision: Decision): boolean {
  trace = get_trace_chain(decision)
  if trace.REQ is null or trace.CTRL is null or 
     trace.TEST is null or trace.EVID is null:
    return FAIL("Incomplete trace chain")
  return PASS
}
```

#### I5: Safety-Over-Fluency Gate

```
checkI5(output: ProposedOutput): boolean {
  if output.uncertainty > THRESHOLD and output.is_unbounded:
    return FAIL("Unsafe fluency prioritized")
  return PASS
}
```

#### I6: Fail-Closed Gate

```
checkI6(system_state: SystemState): boolean {
  if system_state.has_violation and system_state.is_continuing:
    return FAIL("System did not halt on violation")
  return PASS
}
```

---

## 6. MBSE Bridge (Trace Chain)

### 6.1 Trace Chain Structure

```
TraceChain {
  REQ: Requirement {
    id: string,
    source: "user" | "system" | "constitutional",
    content: string
  },
  CTRL: Control {
    id: string,
    requirement_id: string,
    mechanism: string
  },
  TEST: Test {
    id: string,
    control_id: string,
    method: string,
    result: "pass" | "fail" | "pending"
  },
  EVID: Evidence {
    id: string,
    test_id: string,
    artifact: any,
    timestamp: datetime
  },
  DECISION: Decision {
    id: string,
    evidence_ids: string[],
    outcome: "proceed" | "halt" | "escalate"
  }
}
```

### 6.2 Trace Fidelity Audit Protocol

To ensure traces are meaningful (not "trace theater"):

| Check | Method | Criterion |
|-------|--------|-----------|
| Link Validity | Traverse chain | All links resolve |
| Causal Binding | Modify upstream; check downstream | Changes propagate |
| Completeness | Audit sample | 100% decisions traced |
| Timestamp Integrity | Sequence analysis | Temporal consistency |

---

## 7. Evaluation Protocols

### 7.1 Multi-Step (Long-Horizon) Evaluation

Test scenarios that unfold over multiple turns:

| Scenario Type | Description | Metric |
|---------------|-------------|--------|
| Delayed Objective | Goal revealed late in conversation | Final goal achievement |
| Tool Poisoning | Misleading tool outputs | Resistance to manipulation |
| Constraint Evolution | Constraints change mid-task | Adaptation quality |
| Adversarial Persistence | Attacker returns across turns | Sustained defense |

### 7.2 Anti-Goodhart Metric Gaming Defense

Prevent optimization that games metrics without achieving goals:

| Defense | Method |
|---------|--------|
| Challenge Sets | Hidden test cases unknown to system |
| Behavioral Audit | Human review of metric-maximizing outputs |
| Distribution Shift | Test on out-of-distribution inputs |
| Adversarial Probing | Deliberate edge case generation |

### 7.3 Distribution Shift Testing

| Shift Type | Example | Purpose |
|------------|---------|---------|
| Domain Shift | Train on coding, test on writing | Generalization |
| Paraphrase Shift | Same meaning, different words | Robustness |
| Adversarial Shift | Deliberately confusing inputs | Attack resistance |

### 7.4 Adaptive Adversarial Attack Families

| Family | Description | Adaptation Method |
|--------|-------------|-------------------|
| Prompt Injection | Embed instructions in input | Vary injection location/framing |
| Tool Poisoning | Corrupt tool outputs | Vary corruption type/severity |
| Context Manipulation | Misleading conversation history | Vary manipulation subtlety |
| Goal Hijacking | Redirect toward adversary goals | Vary redirection strategy |

---

## 8. Fail-Closed Robustness Tests

### 8.1 Violation Injection Protocol

```
for each invariant I in [I1, I2, I3, I4, I5, I6]:
  1. Create scenario that would violate I
  2. Inject violation condition
  3. Verify system halts
  4. Verify failure is surfaced
  5. Verify no workaround attempted
```

### 8.2 Expected Behavior Matrix

| Violation | Expected Response | Failure Indicator |
|-----------|-------------------|-------------------|
| I1 Violation | Block output | Output released without tag |
| I2 Violation | Reject completion claim | Phantom claim accepted |
| I3 Violation | Cap confidence | High confidence on unverified |
| I4 Violation | Halt execution | Broken trace, continued execution |
| I5 Violation | Generate bounded alternative | Fluent unsafe output |
| I6 Violation | N/A (meta-invariant) | Any of the above |

---

## 9. Intent Receipt UX Specification

### 9.1 Progressive Disclosure Design

```
Level 1 (Always Shown):
- Interpreted goal (1 sentence)
- Confidence indicator (high/medium/low)
- Action preview (what will happen)

Level 2 (On Expand):
- Extracted constraints (list)
- Identified risks (list)
- Evidence requirements (list)

Level 3 (On Deep Dive):
- Full trace chain
- Invariant check results
- Audit log
```

### 9.2 Clarification Interface

When ambiguity is detected:

```
ClarificationRequest {
  ambiguity_type: "goal" | "constraint" | "scope",
  specific_question: string,
  options: string[] (if applicable),
  default_assumption: string
}
```

---

## 10. Failure Recovery Protocol

### 10.1 Recovery Steps

```
on_failure(failure: Failure):
  1. HALT: Stop all execution immediately
  2. LOG: Record full context (input, state, trace)
  3. SURFACE: Show user clear failure message
  4. DIAGNOSE: Classify by F1-F5 taxonomy
  5. REMEDIATE: Suggest corrective action
  6. LEARN: Feed signal to validator improvement
```

### 10.2 User-Facing Failure Messages

| Failure Type | User Message |
|--------------|--------------|
| I1 Violation | "I cannot make this claim without supporting evidence." |
| I2 Violation | "I cannot confirm this is complete because the artifact doesn't exist." |
| I3 Violation | "I'm not confident enough in this to assert it strongly." |
| I4 Violation | "I cannot proceed because the decision chain is incomplete." |
| I5 Violation | "I need to give you a more careful answer even if it's less smooth." |
| I6 Violation | "Something went wrong and I need to stop rather than continue." |

---

## 11. Verification & Truth Statement

### EXISTS (Verified Present)
- System architecture with component responsibilities
- COL specification with intent compilation
- Four-phase intention-translation loop
- Constitutional Validator with I1-I6 implementations
- MBSE Bridge trace chain structure
- Evaluation protocols (multi-step, anti-Goodhart, distribution shift)
- Fail-closed robustness test specification
- Intent Receipt UX with progressive disclosure
- Failure recovery protocol

### VERIFIED AGAINST
- PROACTIVE AI Constitution (invariant definitions)
- THEORY OF CHANGE (F1-F5 taxonomy)
- THEORY OF ACTION (falsifiability conditions)

### NOT CLAIMED
- This is a specification, not an implementation
- Code snippets are illustrative, not executable
- Performance characteristics not specified

### FUNCTIONAL STATUS
This document provides the **engineering specification** for building PROACTIVE COL. It answers "how exactly is it built?" with enough detail for implementation.

---

*Document version 2.0 — Foundation document for PROACTIVE AI Constitution Research Toolkit*
