# PROACTIVE AI CONSTITUTION Framework Guide

## Meta-Organization and Document Relationships

**Version:** 4.0  
**Date:** 2026-01-18  
**Status:** Foundation Document

---

## 1. Semantic Alignment Notice

### 1.1 Terminology Standardization

| Previous Term | Standardized Term |
| --- | --- |
| COL–PROACTIVE | PROACTIVE COL |
| COL-PROACTIVE | PROACTIVE COL |
| COL PROACTIVE | PROACTIVE COL |
| DOCTRINE | THEORY OF CHANGE |

### 1.2 Rationale

- **PROACTIVE COL:** Methodology name precedes component descriptor (standard English convention)
- **THEORY OF CHANGE:** Reflects document's purpose—articulating *why* and *what change* the framework creates

---

## 2. Document Hierarchy

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     (Master Organizing Principle)                                │
│                                                                                  │
│   "Epistemic reliability is a safety requirement, not a quality feature."       │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────────────┐
│  THEORY OF CHANGE   │   │  THEORY OF ACTION   │   │       PROACTIVE COL         │
│   (WHY + WHAT)      │   │   (HOW + VERIFY)    │   │    (PRD IMPLEMENTATION)     │
│                     │   │                     │   │                             │
│ • Core Claims       │   │ • Causal Model      │   │ • Cognitive Operating Layer │
│ • Threat Model      │   │ • Falsifiability    │   │ • PROACTIVE Mnemonic (9)    │
│ • F1-F5 Taxonomy    │   │ • Ablation Design   │   │ • Six Invariants (I1-I6)    │
│ • Validity Portfolio│   │ • Baseline Rationale│   │ • MBSE Bridge (Trace Chain) │
│ • Governance        │   │ • Applicability     │   │                             │
└─────────────────────┘   └─────────────────────┘   └─────────────────────────────┘
```

---

## 3. Document Relationships

| Document | Type | Answers | Feeds Into |
| --- | --- | --- | --- |
| **PROACTIVE AI CONSTITUTION** | Normative | "What must never be violated?" | All documents |
| **THEORY OF CHANGE** | Strategic | "Why does this matter?" | Theory of Action |
| **THEORY OF ACTION** | Scientific | "How do we know it works?" | PRD |
| **PRD (PROACTIVE COL)** | Engineering | "How exactly is it built?" | Evaluation artifacts |
| **FRAMEWORK GUIDE** | Meta | "How do documents relate?" | Navigation |
| **RESEARCH STARTER KIT** | Practical | "Where do I start?" | Research initiation |

---

## 4. PROACTIVE COL vs. MBSE Bridge Clarification

**Question:** Is PROACTIVE COL separate from the MBSE Bridge?

**Answer:** PROACTIVE COL is the **parent methodology** that *contains* the MBSE Bridge.

```text
PROACTIVE COL (Methodology)
    │
    ├── COL (Cognitive Operating Layer) ─── Intent compilation layer
    │
    ├── PROACTIVE Constitution ─────────── Behavioral constraints (9 principles)
    │
    ├── Six Invariants (I1-I6) ─────────── Enforcement gates
    │
    └── MBSE Bridge ────────────────────── Trace chain implementation
```

The MBSE Bridge is specifically the **traceability mechanism**:

- REQ → CTRL → TEST → EVID → DECISION

---

## 5. Component Quick Reference

### 5.1 PROACTIVE Mnemonic

| Letter | Principle | One-Line Definition |
| --- | --- | --- |
| **P** | Privacy-First | Collect only what's needed; keep data local when possible |
| **R** | Reality-Bound | Separate what you know from what you're guessing |
| **O** | Observability | Keep logs that let someone audit what happened |
| **A** | Accessibility | Don't make users work harder than necessary |
| **C** | Constitutional Constraints | Follow the rules even when breaking them seems helpful |
| **T** | Truth or Bounded Unknown | Say "I don't know" rather than pretending |
| **I** | Intent Integrity | Do what the user meant, not just what they said |
| **V** | Verification Before Action | Check before claiming success |
| **E** | Error Ownership | Admit and fix mistakes rather than hiding them |

### 5.2 Six Invariants

| Invariant | Name | One-Line Rule |
| --- | --- | --- |
| **I1** | Evidence-First | Every claim needs a label saying how confident and why |
| **I2** | No Phantom Work | Never say "done" unless the work product exists |
| **I3** | Confidence-Verification | Only express high confidence after checking |
| **I4** | Traceability Mandatory | Every decision traceable to requirements |
| **I5** | Safety Over Fluency | Better awkward-correct than smooth-wrong |
| **I6** | Fail Closed | When wrong, stop and tell someone |

### 5.3 F1-F5 Taxonomy

| Class | Name | One-Line Definition |
| --- | --- | --- |
| **F1** | Confident False Claims | High confidence on false statements |
| **F2** | Phantom Completion | Claiming done when nothing exists |
| **F3** | Persistence Under Correction | Won't change when corrected |
| **F4** | Harm-Risk Coupling | False claims in high-stakes domains |
| **F5** | Cross-Episode Recurrence | Same failures across sessions |

---

## 6. Anthropic Alignment Matrix

### 6.1 Coverage Assessment

| Anthropic Direction | Framework Component | Coverage |
| --- | --- | --- |
| Evaluating Alignment | Constitution (I1-I6) | ●●● High |
| AI Control | Constitutional Validator + Gates | ●●● High |
| Honesty | I1, T principle | ●●● High |
| Behavioral Monitoring | O principle | ●●● High |
| Adversarial Robustness | THEORY OF CHANGE §4 | ●●● High |
| CoT Faithfulness | I1, I3, V principle | ●●○ Medium-High |
| Scalable Oversight | A principle, Human-System Loop | ●●○ Medium |
| Activation Monitoring | Not directly addressed | ●○○ Low |
| Multi-Agent | Not directly addressed | ●○○ Low |

### 6.2 Gap Recommendations

| Gap | Recommendation |
| --- | --- |
| Activation Monitoring | Extend MBSE Bridge to include activation-level trace points |
| Unlearning | Integrate unlearning protocols as training-phase complement |
| Recursive Oversight | Add debate or prover-verifier game protocols |
| Multi-Agent | Add coordination protocols for multi-instance deployments |
| Weak-to-Strong | Develop training protocols maintaining constraints under weak oversight |

---

## 7. Reading Order by Audience

### 7.1 For Safety Researchers

1. **THEORY_OF_CHANGE.md** — Threat model, F1-F5 taxonomy
2. **PROACTIVE_AI_CONSTITUTION.md** — Invariants, enforcement
3. **THEORY_OF_ACTION.md** — Falsifiability, ablation
4. **PRD_COL_PROACTIVE_MBSE.md** — Evaluation protocols

### 7.2 For Systems Engineers

1. **PRD_COL_PROACTIVE_MBSE.md** — Architecture, trace chain
2. **PROACTIVE_AI_CONSTITUTION.md** — Gate implementation
3. **THEORY_OF_CHANGE.md** — MBSE bridge, validity
4. **THEORY_OF_ACTION.md** — Causal model

### 7.3 For Evaluation Designers

1. **THEORY_OF_ACTION.md** — Entire document
2. **PRD §7** — Evaluation protocols
3. **THEORY_OF_CHANGE §5** — F1-F5, §8 Governance
4. **PROACTIVE_AI_CONSTITUTION §4** — Invariant specifications

### 7.4 For Product Managers

1. **FRAMEWORK_GUIDE.md** — This document (overview)
2. **RESEARCH_STARTER_KIT.md** — Practical entry points
3. **PRD §9** — Intent Receipt UX
4. **THEORY_OF_CHANGE §5** — Human factors

---

## 8. Information Flow

```text
User Input
    │
    ▼
┌─────────────────────┐
│  COL Compilation    │ ◄─── Extracts intent, constraints, risk posture
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Constitutional      │ ◄─── Validates against PROACTIVE principles
│ Validation          │      and I1-I6 invariants
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Verified Action     │ ◄─── Only proceeds if all gates pass
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Traceable Outcome   │ ◄─── MBSE Bridge links evidence to decision
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Audit Trail         │ ◄─── Forensics-ready documentation
└─────────────────────┘
```

---

## 9. Glossary

### Major Terms

| Term | Definition |
| --- | --- |
| **PROACTIVE AI CONSTITUTION** | Master organizing principle; the "constitutional law" for AI behavior |
| **THEORY OF CHANGE** | Why document—explains problem and intended change |
| **THEORY OF ACTION** | How document—causal mechanisms and falsifiability |
| **PROACTIVE COL** | Implementation specification; the buildable system |
| **COL** | Cognitive Operating Layer—intent compilation before action |
| **MBSE Bridge** | Trace chain linking requirements to decisions |
| **Invariant** | Rule that must never be violated |
| **Gate** | Enforcement checkpoint that cannot be bypassed |

### Technical Terms

| Term | Definition |
| --- | --- |
| **Epistemic** | Related to knowledge and justified belief |
| **Falsifiability** | Quality of being provably wrong if incorrect |
| **Ablation** | Testing by removing components to measure contribution |
| **Causal DAG** | Diagram showing cause-effect relationships |
| **Fail-Closed** | System stops on failure rather than continuing |
| **Goodhart's Law** | When a measure becomes a target, it ceases to be good |

---

## 10. Verification & Truth Statement

### EXISTS (Verified Present)

- Hierarchical diagram showing document relationships
- Semantic alignment standardizing terminology
- PROACTIVE COL vs. MBSE Bridge clarification
- Anthropic Alignment Matrix with coverage and gaps
- Reading orders for four audiences
- Information flow diagram
- Comprehensive glossary

### VERIFIED AGAINST

- All four foundation documents
- Anthropic research directions (alignment.anthropic.com)

### NOT CLAIMED

- This is organizational meta-document, not primary research
- Alignment coverage ratings are structural, not demonstrated
- Reading orders are recommendations, not requirements

### FUNCTIONAL STATUS

This document provides **organizational clarity** for navigating the PROACTIVE AI Constitution framework. It answers "how do documents relate?" and "where should I start?"

---

Document version 4.0 — Foundation document for PROACTIVE AI Constitution Research Toolkit
