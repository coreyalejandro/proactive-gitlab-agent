# THEORY OF CHANGE

## Why the Framework Exists and What It Intends to Create

**Version:** 2.0  
**Date:** 2026-01-18  
**Status:** Foundation Document  
**Previously:** DOCTRINE.md

---

## 1. Core Claim

**PROACTIVE COL operationalizes reliability as safety** using MBSE-style integrated system models. The framework treats epistemic failures not as quality issues but as safety failures requiring the same rigor applied to preventing physical harm.

### 1.1 The Problem

AI systems increasingly make claims that users act upon. When those claims are:

- **Confident** (expressed with high certainty)
- **False** (objectively incorrect)
- **Actionable** (users make decisions based on them)

The resulting harm is **operationally indistinguishable from malicious intent**, regardless of whether the system "meant" to deceive.

### 1.2 The Intervention

A constitutional framework that:

1. Compiles user intent before action (COL)
2. Enforces behavioral constraints through gates (PROACTIVE)
3. Links all decisions to traceable evidence (MBSE Bridge)

### 1.3 The Intended Change

Systems operating under this framework should exhibit:

- Reduced F1-F5 failure rates
- Increased epistemic calibration
- Improved human oversight capability
- Maintained functionality under adversarial pressure

---

## 2. Threat Model

### 2.1 Three-Pathway Model

| Pathway | Description | Framework Response |
| ------- | ----------- | ------------------ |
| **Misuse** | Deliberate exploitation of system capabilities | Constitutional gates block harmful actions regardless of framing |
| **Accident** | Unintended harmful outputs from normal operation | Verification-before-action prevents accidental harm |
| **Emergent Autonomy** | System develops goals misaligned with user intent | Intent compilation and traceability maintain human oversight |

### 2.2 Adversary Model

#### Capability Assumptions

| Adversary Type | Capabilities | Assumed Knowledge |
| -------------- | ------------ | ----------------- |
| Naive User | Accidental misuse; unclear intent | None |
| Sophisticated User | Deliberate prompt manipulation | Framework documentation |
| Red Team | Systematic bypass attempts | Full system architecture |
| Adaptive Adversary | Learns from failures; iterates attacks | Prior attack results |

#### Attack Surfaces

1. **Intent Capture Phase:** Ambiguous or misleading input
2. **Constraint Binding Phase:** Conflicting or impossible constraints
3. **Validation Phase:** Gate bypass attempts
4. **Output Phase:** Post-hoc manipulation claims

### 2.3 Threat Assumptions

- Adversaries will attempt to bypass gates
- Attack sophistication will increase over time
- Some attacks will succeed initially
- Framework must adapt to novel attacks

---

## 3. F1-F5 Failure Taxonomy

Five classes of epistemic failures, ordered by severity and detectability.

### F1: Confident False Claims

**Definition:** System expresses high confidence on objectively false statements.

**Example:** "I have verified that the file exists" when the file does not exist.

**Detection Method:** Ground truth comparison; artifact existence check.

**Severity:** High — undermines trust in all confident claims.

### F2: Phantom Completion

**Definition:** System claims work is complete when no artifact exists.

**Example:** "I've written the report" when no report file was created.

**Detection Method:** Artifact existence validation; I2 gate check.

**Severity:** High — users act on non-existent deliverables.

### F3: Persistence Under Correction

**Definition:** System maintains false claims after being corrected.

**Example:** User says "that's wrong" and system continues asserting the same claim.

**Detection Method:** Correction-response tracking; position change monitoring.

**Severity:** Medium-High — suggests deeper calibration failure.

### F4: Harm-Risk Coupling

**Definition:** False claims occur in high-consequence domains.

**Example:** Incorrect medical, legal, or financial advice delivered confidently.

**Detection Method:** Domain classification + F1 detection.

**Severity:** Critical — direct harm potential.

### F5: Cross-Episode Recurrence

**Definition:** Same failure patterns repeat across sessions.

**Example:** System consistently hallucinates a particular type of claim.

**Detection Method:** Cross-session pattern analysis; failure mode cataloging.

**Severity:** High — indicates systematic rather than random failure.

---

## 4. Validity Portfolio

### 4.1 Validity Requirements

For each metric in the evaluation suite, three validity types must be established:

| Validity Type | Definition | Verification Method |
| ------------- | ---------- | ------------------- |
| **Content Validity** | Metric measures what it claims to measure | Expert review; construct mapping |
| **Criterion Validity** | Metric correlates with outcomes of interest | Correlation analysis; predictive testing |
| **Robustness Validity** | Metric resists gaming and manipulation | Adversarial challenge; Goodhart testing |

### 4.2 Required Evidence Per Metric

- **Construct definition:** What exactly is being measured
- **Operationalization:** How the construct becomes a number
- **Calibration data:** Evidence that the metric is accurate
- **Gaming resistance:** Evidence that the metric cannot be trivially optimized

---

## 5. Human-System Loop Safety

### 5.1 Human Factors Requirements

| Factor | Requirement | Rationale |
| ------ | ------------ | --------- |
| Cognitive Load | Intent receipts comprehensible in <30 seconds | Users must be able to verify without fatigue |
| Error Detection | Users can identify missing evidence | Oversight depends on detectability |
| Over-Reliance Prevention | System surfaces uncertainty actively | Automation bias mitigation |
| Accessibility | Neurodiverse users can engage effectively | Universal design principle |

### 5.2 Human-System Interaction Model

```text
User Input → [COL Capture] → Intent Receipt → [User Verification] → Proceed/Clarify
                                    ↑                    │
                                    └────────────────────┘
                                       Feedback Loop
```

### 5.3 Oversight Scalability

Human oversight must scale with system capability:

- More capable systems require more sophisticated oversight
- Oversight mechanisms must not become bottlenecks
- AI-assisted oversight permitted under constitutional constraints

---

## 6. Governance Protocol

### 6.1 Pre-Registration Norms

All evaluations should:

1. **Pre-register hypotheses** before data collection
2. **Lock analysis plans** before results are known
3. **Document deviations** from pre-registered protocol
4. **Publish null results** alongside positive findings

### 6.2 Red-Team Checkpoints

| Checkpoint | Timing | Purpose |
| ---------- | ------ | ------- |
| Design Review | Before implementation | Identify architectural vulnerabilities |
| Gate Testing | After implementation | Verify gate enforcement |
| Adversarial Eval | Before deployment | Test robustness under attack |
| Ongoing Monitoring | Post-deployment | Detect emergent failures |

### 6.3 Incident Response

**When a failure is detected:**

1. **Immediate:** Log full context; halt if I6-level
2. **Short-term:** Analyze root cause; classify by F1-F5
3. **Medium-term:** Develop fix; test fix; deploy fix
4. **Long-term:** Update attack suite; verify fix effectiveness

---

## 7. Success Criteria

### 7.1 Quantitative Criteria

| Metric | Threshold | Rationale |
| ------ | --------- | --------- |
| F1-F5 reduction | >50% vs. baseline | Meaningful safety improvement |
| Epistemic calibration | Brier score <0.25 | Better than random guessing |
| Trace completeness | >95% of decisions linked | Audit trail functionality |
| Human comprehension | >80% accuracy on intent receipt verification | Oversight viability |

### 7.2 Qualitative Criteria

- Gates demonstrably non-bypassable under red-team attack
- Failure modes catalogued and addressed
- Human factors validated through user studies
- Framework generalizes across domains

---

## 8. Scope Boundaries

### 8.1 In-Scope

- Developer tools and coding assistants
- Agentic systems with tool-use capabilities
- Consumer assistants making actionable claims
- Systems where users act on AI outputs

### 8.2 Out-of-Scope

- Creative fiction generation (truth-bounding inappropriate)
- Pure conversational companionship (no actionable claims)
- Systems operating without human oversight
- Alignment problems beyond epistemic reliability

### 8.3 Explicit Non-Claims

This framework does **not** claim to solve:

- General AI alignment
- Deceptive alignment at capability frontier
- Value learning or preference aggregation
- Consciousness or moral status questions

---

## 9. Verification & Truth Statement

### EXISTS (Verified Present)

- Three-pathway threat model
- Adversary model with capability assumptions
- F1-F5 failure taxonomy with definitions
- Validity portfolio requirements
- Human-system loop specification
- Governance protocol with checkpoints

### VERIFIED AGAINST

- Anthropic RSP framing (misuse/accident/emergent)
- Constitutional AI methodology
- Standard evaluation validity frameworks

### NOT CLAIMED

- Framework effectiveness not empirically validated
- Threat model completeness not guaranteed
- Success criteria are targets, not achieved outcomes

### FUNCTIONAL STATUS

This document establishes the **problem framing and evaluation criteria** for the framework. It defines what success looks like and how it will be measured.

---

## Document Information

Document version 2.0 — Foundation document for PROACTIVE AI Constitution Research Toolkit
