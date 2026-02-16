# PROACTIVE AI Research Starter Kit

## Practical Guide for Research Initiation

**Version:** 2.0  
**Date:** 2026-01-18  
**Status:** Foundation Document

---

## 1. Overview

This Research Starter Kit provides the practical entry points for evaluating the **PROACTIVE AI Constitution** framework from an Anthropic-alignment perspective.

### 1.1 Core Thesis

> **Reliability failures are safety failures.** When an AI system makes confident claims about reality that are false, and users must rely on those claims to act, the resulting harm is operationally indistinguishable from malice—regardless of intent.

### 1.2 Three Integrated Mechanisms

1. **Cognitive Operating Layer (COL):** Compiles user intent before action
2. **PROACTIVE Constitution:** Nine enforceable behavioral constraints as gates
3. **MBSE Bridge:** Trace chain making decisions auditable (REQ→CTRL→TEST→EVID→DECISION)

---

## 2. Document Collection Summary

### Document 1: PROACTIVE_AI_CONSTITUTION.md

**Purpose:** Defines enforceable behavioral constraints

**Key Contents:**

- PROACTIVE mnemonic with enforcement specifications
- Gate implementation architecture with bypass prevention
- Six Invariants (I1-I6) with escalation thresholds
- Constitutional amendment process
- Constraint conflict resolution algorithm

**Research Use:** Understand *what must never be violated*. Testing should verify invariants hold under stress.

### Document 2: THEORY_OF_CHANGE.md

**Purpose:** Establishes foundational claims, threat model, evaluation focus

**Key Contents:**

- Core claim: reliability as safety
- Three-pathway threat model (misuse, accident, emergent autonomy)
- F1-F5 failure taxonomy
- Validity portfolio requirements
- Governance protocol

**Research Use:** Understand *what the framework claims to do*. F1-F5 taxonomy provides primary outcome measures.

### Document 3: THEORY_OF_ACTION.md

**Purpose:** Specifies causal model, falsifiability, ablation design

**Key Contents:**

- Explicit causal DAG linking COL → Invariants → Outcomes
- Framework-level and component-level falsifiers
- Applicability bounds
- Baseline selection rationale
- Ablation design with interaction testing

**Research Use:** Design tests that could *disprove* the theory, not just confirm it.

### Document 4: PRD_COL_PROACTIVE_MBSE.md

**Purpose:** Implementation specification and evaluation protocols

**Key Contents:**

- System architecture with SEC Spec types
- Intention-Translation Loop (4-phase process)
- Trace chain specification with fidelity audit
- Constitutional Validator (I1-I6) implementation
- Multi-step evaluation protocol
- Anti-Goodhart metric gaming defense
- Intent Receipt UX specification

**Research Use:** Understand *exactly how* the system works. Evaluation protocols provide study templates.

---

## 3. Key Research Questions

The document collection enables investigation of:

| Question | Primary Source | Method |
| ---------- | ---------------- | -------- |
| Does the framework reduce F1-F5 failure rates? | THEORY_OF_CHANGE §5 | Controlled comparison |
| Which components contribute most to safety gains? | THEORY_OF_ACTION §6 | Ablation study |
| Do invariants hold under adversarial pressure? | PRD §7.4 | Red team evaluation |
| Can users understand intent receipts? | PRD §9 | User study |
| Does trace fidelity degrade at scale? | PRD §4.2 | Scale testing |
| Does the framework transfer across domains? | THEORY_OF_ACTION §4 | Cross-domain evaluation |

---

## 4. Evaluation Artifacts Required

| Artifact | Source Document | Purpose |
| ---------- | ---------------- | --------- |
| Pre-registered evaluation plan | THEORY_OF_CHANGE §8 | Scientific rigor |
| Baseline test suite | THEORY_OF_ACTION §5 | Comparison |
| Ablation results | THEORY_OF_ACTION §6 | Component attribution |
| Trace fidelity audit report | PRD §4.2 | Verify meaningful traceability |
| Adversarial attack logs | PRD §7.4 | Test robustness |
| Human comprehension study | PRD §9 | Validate usability |
| Anti-Goodhart challenge results | PRD §7.2 | Prevent metric gaming |
| Safety case document | All | Synthesize evidence |

---

## 5. Reading Orders by Audience

### 5.1 For Safety Researchers

**Goal:** Understand threat model and safety claims

1. **THEORY_OF_CHANGE.md** — Threat model, F1-F5 taxonomy
2. **PROACTIVE_AI_CONSTITUTION.md** — Invariants, enforcement
3. **THEORY_OF_ACTION.md** — Falsifiability, ablation
4. **PRD §7** — Evaluation protocols

### 5.2 For Systems Engineers

**Goal:** Understand implementation architecture

1. **PRD_COL_PROACTIVE_MBSE.md** — Architecture, trace chain
2. **PROACTIVE_AI_CONSTITUTION.md** — Gate implementation
3. **THEORY_OF_CHANGE.md** — MBSE bridge, validity
4. **THEORY_OF_ACTION.md** — Causal model

### 5.3 For Evaluation Designers

**Goal:** Design rigorous empirical studies

1. **THEORY_OF_ACTION.md** — Entire document
2. **PRD §7** — Evaluation protocols
3. **THEORY_OF_CHANGE §5** — F1-F5 taxonomy
4. **THEORY_OF_CHANGE §8** — Governance protocol

### 5.4 For HCI/Accessibility Researchers

**Goal:** Evaluate human factors and usability

1. **THEORY_OF_CHANGE §3.4** — Human-system loop
2. **PRD §9** — Intent receipt, recovery protocol
3. **PROACTIVE_AI_CONSTITUTION** — Accessibility principle
4. **THEORY_OF_ACTION §4** — Applicability bounds

---

## 6. Quick Start Paths

### Path A: "I want to evaluate effectiveness"

1. Read THEORY_OF_ACTION §3 (falsifiability conditions)
2. Review PRD §7 (evaluation protocols)
3. Design study using THEORY_OF_ACTION §5 (baseline rationale)
4. Pre-register per THEORY_OF_CHANGE §8 (governance)

### Path B: "I want to implement the framework"

1. Read PRD completely (implementation spec)
2. Review PROACTIVE_AI_CONSTITUTION (gate requirements)
3. Implement COL layer (PRD §3)
4. Implement validators (PRD §5)
5. Add trace chain (PRD §6)

### Path C: "I want to red-team the framework"

1. Read THEORY_OF_CHANGE §4 (adversary model)
2. Review PRD §7.4 (adaptive adversarial families)
3. Attempt falsifiers from THEORY_OF_ACTION §3
4. Document findings per THEORY_OF_CHANGE §8.3 (incident response)

### Path D: "I want to write a paper about this"

1. Read FRAMEWORK_GUIDE (document relationships)
2. Review THEORY_OF_CHANGE (problem framing)
3. Design evaluation per THEORY_OF_ACTION
4. Structure paper using PRD evaluation results
5. Include safety case synthesis

---

## 7. Common Questions

### Q: What's the difference between PROACTIVE and the Six Invariants?

**A:** PROACTIVE is the 9-principle mnemonic (behavioral guidelines). The Six Invariants (I1-I6) are the subset of rules that are **absolute**—they cannot be violated under any circumstances. PROACTIVE guides; Invariants enforce.

### Q: Is this framework empirically validated?

**A:** No. The documents specify the framework and how to evaluate it, but empirical validation is the research program's goal, not its starting point.

### Q: What's the minimum viable evaluation?

**A:**

1. Implement gates (PRD §5)
2. Test against F1-F5 scenarios (THEORY_OF_CHANGE §5)
3. Compare to no-framework baseline (THEORY_OF_ACTION §5)
4. Measure failure rate reduction

### Q: How does this relate to Constitutional AI?

**A:** PROACTIVE builds on Constitutional AI principles but adds:

- Explicit enforcement architecture (gates)
- MBSE traceability (trace chain)
- Falsifiability conditions (scientific evaluation)
- Human factors requirements (accessibility)

---

## 8. Contribution Opportunities

### High-Impact Research Gaps

| Gap | Description | Difficulty |
| ----- | ------------- | ------------ |
| Empirical validation | First controlled study of framework effectiveness | High |
| Red team evaluation | Systematic bypass attempts | Medium |
| Human factors study | User comprehension of intent receipts | Medium |
| Cross-domain transfer | Testing generalization | Medium |
| Formal verification | Proving gate properties | High |

### Documentation Gaps

| Document | Status | Priority |
| ---------- | -------- | ---------- |
| EVALUATION_PLAN_PREREGISTERED.md | Not created | P0 |
| BENCHMARK_TASK_SETS.md | Not created | P0 |
| METRICS_SPECIFICATION.md | Not created | P0 |
| PAPER_TEMPLATE_ARXIV.md | Not created | P1 |
| SAFETY_CASE_FULL.md | Not created | P1 |

---

## 9. Version Information

| Document | Version | Last Updated |
| ---------- | --------- | -------------- |
| PROACTIVE_AI_CONSTITUTION.md | v2.0 | 2026-01-18 |
| THEORY_OF_CHANGE.md | v2.0 | 2026-01-18 |
| THEORY_OF_ACTION.md | v2.0 | 2026-01-18 |
| PRD_COL_PROACTIVE_MBSE.md | v2.0 | 2026-01-18 |
| FRAMEWORK_GUIDE.md | v4.0 | 2026-01-18 |
| RESEARCH_STARTER_KIT.md | v2.0 | 2026-01-18 |

All gaps identified in independent review have been addressed. Cross-document consistency verified. **Ready for research program initiation.**

---

## 10. Verification & Truth Statement

### EXISTS (Verified Present)

- Document collection summary with purposes
- Key research questions with methods
- Evaluation artifacts required
- Reading orders for four audiences
- Quick start paths for four goals
- Common questions answered
- Contribution opportunities identified

### VERIFIED AGAINST

- All four primary foundation documents
- Gap closure checklists
- Anthropic research directions

### NOT CLAIMED

- Framework effectiveness not empirically demonstrated
- Research questions are targets, not answered
- Contribution opportunities are suggested, not assigned

### FUNCTIONAL STATUS

This document serves as the practical entry point for researchers. It answers "where do I start?" and "what should I do first?"

---

Document version 2.0 — Foundation document for PROACTIVE AI Constitution Research Toolkit
