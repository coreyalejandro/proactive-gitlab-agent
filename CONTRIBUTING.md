# Contributing to PROACTIVE GitLab Duo Agent

## Document Standards

### Required Sections

Every document must include:

1. **Header Block**
   ```markdown
   # [DOCUMENT TITLE]
   ## [Subtitle]
   **Version:** X.Y
   **Date:** YYYY-MM-DD
   **Status:** Draft | Review | Foundation
   ```

2. **Verification & Truth Statement** (at end of every document)
   ```markdown
   ## Verification & Truth Statement

   ### EXISTS (Verified Present)
   - [List what this document actually contains — verified inventory]

   ### VERIFIED AGAINST
   - [List source documents/standards this was checked against]

   ### NOT CLAIMED
   - [Explicit non-claims — what this document does NOT assert]

   ### FUNCTIONAL STATUS
   [What role this document serves — its actual use]
   ```

   **Why this block is mandatory:** It enforces the PROACTIVE invariants on our own documentation:
   - EXISTS → I2 (No Phantom Work): can't claim content that isn't there
   - VERIFIED AGAINST → I1 (Evidence-First) + I4 (Traceability): claims traced to sources
   - NOT CLAIMED → I5 (Safety Over Fluency): bounded statements over confident narrative
   - FUNCTIONAL STATUS → I3 (Confidence-Verification): scopes what the document can be used for

   Every document in `docs/foundations/` follows this pattern. New documents must too.

### Naming Convention

- Use SCREAMING_SNAKE_CASE for document names
- Include version in document, not filename
- Keep filenames descriptive but concise

### Cross-References

When referencing other documents:
- Use relative paths: `docs/foundations/THEORY_OF_ACTION.md`
- Include section numbers: `THEORY_OF_ACTION.md §3.2`
- Link to specific claims when possible

## Review Process

1. Create document following template
2. Self-review against Verification & Truth Statement checklist
3. Cross-reference against source documents in `docs/foundations/`
4. Submit for peer review
5. Address feedback
6. Merge when approved

## Questions

Open an issue for:
- Clarification on document scope
- Template modifications
- Cross-reference conflicts
