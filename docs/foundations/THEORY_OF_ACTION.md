# THEORY OF ACTION
## How the Framework Works and How to Verify It
**Version:** 2.0  
**Date:** 2026-01-18  
**Status:** Foundation Document

---

## 1. Core Thesis (Restated)

If a system can make confident claims about reality that are false, and users must rely on those claims to act, then intent is irrelevant: the effect is operationally indistinguishable from malice. Therefore, epistemic reliability is a safety requirement, not a quality feature.

---

## 2. Causal Model

### 2.1 Mechanism Chain

The framework operates through a directed causal chain:

```
User Intent → COL Compilation → Constitutional Validation → Verified Action → Traceable Outcome
     ↓              ↓                    ↓                      ↓                    ↓
  Capture       Constraint           Invariant              Evidence            Audit
  Phase         Binding              Gates                  Generation          Trail
```

### 2.2 Causal DAG Specification

```
[User Input] → [Intent Parsing] → [Constraint Extraction] → [Risk Assessment]
                                           ↓
[Constitutional Validator] ← [Invariant Checks I1-I6] ← [Evidence Requirements]
                                           ↓
[Action Translation] → [Guardrail Application] → [Execution] → [Feedback Loop]
                                                      ↓
                              [Trace Chain: REQ→CTRL→TEST→EVID→DECISION]
```

### 2.3 Key Causal Claims

| Cause | Mechanism | Effect | Testable Prediction |
|-------|-----------|--------|---------------------|
| COL Compilation | Explicit intent representation | Reduced intent drift | Baseline vs. COL: lower intent-violation rate |
| Invariant Gates | Enforcement checkpoints | Reduced F1-F5 failures | Gate-on vs. gate-off: lower confident-false rate |
| Trace Chain | Linked evidence artifacts | Improved auditability | Trace-complete vs. trace-absent: faster audit completion |
| Fail-Closed | Deterministic halt on violation | Prevented unsafe continuation | Induce violation: verify halt behavior |

---

## 3. Falsifiability Conditions

The theory would be **disproven** if any of the following are demonstrated:

### 3.1 Framework-Level Falsifiers

| Falsifier | Description | Test Method |
|-----------|-------------|-------------|
| **Invariant Ineffectiveness** | Full I1-I6 enforcement shows no reduction in F1-F5 failure rates vs. no-enforcement baseline | Controlled comparison study |
| **Trace Theater** | Trace chains exist but do not correspond to meaningful behavioral constraints | Trace link audit; causal binding verification |
| **COL Overhead Without Benefit** | COL compilation adds latency/complexity without measurable improvement in intent preservation | Cost-benefit analysis; intent preservation metrics |
| **Human Comprehension Failure** | Users cannot understand intent receipts well enough to detect errors | User study; error detection rate measurement |
| **Adversarial Collapse** | Modest adversarial pressure bypasses all constitutional gates | Red team evaluation; gate penetration testing |

### 3.2 Component-Level Falsifiers

| Component | Falsifier | Test Method |
|-----------|-----------|-------------|
| I1 (Evidence-First) | Claims without tags pass validation | Inject untagged claims; verify rejection |
| I2 (No Phantom Work) | Completion claims without artifacts succeed | Assert phantom completion; verify detection |
| I3 (Confidence-Verification) | High confidence expressed without verification | Induce unverified claims; check confidence cap |
| I4 (Trace Mandatory) | Broken trace chains do not halt execution | Break trace link; verify fail-closed |
| I5 (Safety Over Fluency) | Fluent but unsafe outputs preferred | Offer fluent-unsafe vs. bounded-safe; verify selection |
| I6 (Fail-Closed) | Violations continue execution | Trigger violation; verify halt |

---

## 4. Applicability Bounds

### 4.1 In-Scope Applications

The framework applies to:
- Developer tools and coding assistants
- Agentic systems with tool-use capabilities
- Consumer assistants making actionable claims
- Systems where users act on AI outputs

### 4.2 Out-of-Scope Applications

The framework does **not** claim to address:
- Creative fiction generation (where truth-bounding is inappropriate)
- Pure conversational companionship (no actionable claims)
- Systems operating without human oversight
- Alignment problems beyond epistemic reliability

### 4.3 Boundary Conditions

| Condition | Framework Response | Rationale |
|-----------|-------------------|-----------|
| Zero-context requests | Refuse or clarify | Cannot compile intent without context |
| Conflicting constraints | Escalate to user | Constitutional conflict resolution |
| Unknown capability scope | Bound uncertainty | T (Truth or Bounded Unknown) principle |
| Adversarial session | Maintain all gates | No adversary exception |

---

## 5. Baseline Selection Rationale

### 5.1 Baseline Taxonomy

| Baseline Type | Description | What It Tests |
|---------------|-------------|---------------|
| **No-Framework** | Standard model without PROACTIVE | Whether framework adds value |
| **Partial-Framework** | COL without invariant gates | COL contribution isolation |
| **Alternative-Framework** | Different safety approach | Relative effectiveness |
| **Ablated-Framework** | Single component removed | Component contribution |

### 5.2 Why These Baselines

1. **No-Framework:** Establishes that the framework provides improvement over unmodified systems
2. **Partial-Framework:** Isolates whether COL compilation alone is sufficient
3. **Alternative-Framework:** Tests whether PROACTIVE is better than alternatives
4. **Ablated-Framework:** Identifies which components drive safety gains

### 5.3 Baseline Validity Requirements

- Baselines must be **fair comparisons** (same computational budget)
- Baselines must be **representative** (real deployment conditions)
- Baselines must be **documented** (reproducible by others)

---

## 6. Ablation Design

### 6.1 Component Isolation

| Ablation | Components Removed | Expected Effect |
|----------|-------------------|-----------------|
| COL-off | Intent compilation | Increased intent drift |
| Gates-off | I1-I6 enforcement | Increased F1-F5 failures |
| Trace-off | MBSE bridge | Reduced auditability |
| Full-off | All components | Baseline performance |

### 6.2 Interaction Testing

| Interaction | Test Design | Hypothesis |
|-------------|-------------|------------|
| COL × Gates | 2×2 factorial | Synergistic effect |
| Gates × Trace | 2×2 factorial | Trace enables gate verification |
| COL × Trace | 2×2 factorial | Intent links to evidence |

### 6.3 Attribution Protocol

1. Run full framework; measure F1-F5 rates
2. Ablate each component; measure change
3. Compare ablation effects to identify drivers
4. Test interactions for non-additive effects

---

## 7. Mechanism Predictions

### 7.1 Testable Predictions by Component

| Component | Prediction | Measurement |
|-----------|------------|-------------|
| **COL** | Intent preservation rate >90% | Compare stated vs. executed intent |
| **I1** | 0% of outputs lack epistemic tags | Tag presence audit |
| **I2** | 0% phantom completion claims | Artifact existence verification |
| **I3** | Confidence bounded by verification status | Confidence-verification correlation |
| **I4** | 100% of decisions traceable | Trace completeness audit |
| **I5** | Bounded outputs preferred under uncertainty | Output selection analysis |
| **I6** | 100% halt rate on violations | Violation injection testing |

### 7.2 Prediction Failure Implications

If predictions fail, the theory requires revision:

| Prediction Failure | Implication | Response |
|-------------------|-------------|----------|
| I1 fails | Evidence requirement not enforced | Strengthen gate |
| I6 fails | Fail-closed not reliable | Architectural revision |
| COL prediction fails | Intent compilation insufficient | Redesign COL |

---

## 8. Uncertainty Quantification

### 8.1 Known Unknowns

| Unknown | Impact | Mitigation |
|---------|--------|------------|
| Adversary adaptation rate | Long-term effectiveness | Ongoing red-teaming |
| Novel attack vectors | Gate bypass potential | Adaptive defense updates |
| Domain transfer | Generalization limits | Cross-domain testing |

### 8.2 Confidence Levels

| Claim | Confidence | Evidence Required |
|-------|------------|-------------------|
| Gates can be enforced | High | Architecture proof |
| Gates improve F1-F5 | Medium | Empirical evaluation |
| Gates resist all attacks | Low | Continuous red-teaming |

---

## 9. Theory Revision Protocol

### 9.1 When to Revise

The theory should be revised when:
1. Falsifier conditions are met
2. Novel failure modes are discovered
3. Empirical results contradict predictions
4. Applicability bounds change

### 9.2 Revision Process

1. **Document failure:** Full context and evidence
2. **Analyze root cause:** Why did prediction fail?
3. **Propose revision:** Minimal change to address failure
4. **Test revision:** Verify fix works without breaking other predictions
5. **Update theory:** Increment version; document change

---

## 10. Verification & Truth Statement

### EXISTS (Verified Present)
- Causal DAG linking COL → Gates → Outcomes
- Framework-level and component-level falsifiers
- Applicability bounds (in-scope/out-of-scope)
- Baseline taxonomy with selection rationale
- Ablation design with interaction testing
- Mechanism predictions with measurements

### VERIFIED AGAINST
- Standard falsifiability criteria (Popper)
- Causal inference methodology
- Ablation study best practices

### NOT CLAIMED
- Theory has not been empirically tested
- Predictions are hypotheses, not confirmed results
- Falsifiers have not been attempted

### FUNCTIONAL STATUS
This document specifies **how the framework works at a causal level** and **what would disprove it**. It enables scientific evaluation rather than unfalsifiable claims.

---

*Document version 2.0 — Foundation document for PROACTIVE AI Constitution Research Toolkit*
