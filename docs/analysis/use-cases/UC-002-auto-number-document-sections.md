# UC-002 — Auto-Number Document Sections

**Actor:** [The Architect's Assistant](../user-personas/architects-assistant.md) — typically invoked as part of
larger delegated work (e.g. [UC-001](UC-001-discuss-concept-and-document.md) step 5), but may also be invoked
directly by [The Architect](../user-personas/architect.md), e.g. after manually reordering sections.
**Scope:** Numbers and re-links what's already in the document; doesn't decide document structure or content,
and never touches external (`@{repo-slug}/{path}`) references.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [UC-001 — Discuss A Project Concept And Document It](UC-001-discuss-concept-and-document.md) - its main caller
* [The Architect's Assistant](../user-personas/architects-assistant.md) - primary actor
* @docs/standards/documentation-standards.md/§3 - Document Shape (the numbering convention this implements)
* @docs/standards/documentation-standards.md/§6 - Cross-References (the reference-rewrite rule this implements)

## 1 Goal

Keep a document's section/figure numbering, and every same-document reference to it, correct and in sync with
the documentation standard — without the author maintaining numbers by hand.

## 2 Trigger

Invoked against a document whose headings/figures are unnumbered, partially numbered, or need renumbering after
restructuring (sections added, removed, or reordered).

## 3 Preconditions

* The document follows the general shape (Title, optional Context, then body headings) — may have zero, some,
  or all headings/figures pre-numbered or pseudo-numbered.
* A pseudo-number matches `^\d+(\.\d+)*\.?$` (headings) or `^\d+(\.\d+)*\.[a-zA-Z]\.?$` (figures); anything
  else, however number-like, is ordinary title text with no special meaning — not even as an opt-in signal.
* The first section (or first subsection within a parent) defaults to hidden id `0` unless it carries a valid
  pseudo-number, which opts it into visible numbering from `1`. Every later sibling always gets a visible
  number regardless of whether the author typed one.

## 4 Main Success Scenario

1. Parse the document once: every eligible heading (excluding Context/Appendix/Rationale, never numbered), any
   pseudo-numbers the author typed (including on brand-new headings/figures, so a same-edit reference to
   something just added resolves correctly rather than reading as dangling), every fenced code block and
   whether it carries a pseudo-number (marking it a figure), and every `§M.N(.O)?` token or markdown-link
   anchor anywhere in the doc.
2. Compute fresh numbering by document position and heading depth.
3. Build an old→new id map, keyed by pseudo-number *and* title (so two headings sharing a pseudo-number but
   differing in title resolve distinctly; two sharing both number and title are a genuinely broken source
   document — not this tool's problem to resolve).
4. Remove any `§`-reference or link anchor whose old id has no entry in the map — evaluated against the
   original, unmodified document, before anything else changes, so a dangling reference can never later be
   mistaken for a match once renumbering is underway.
5. Rewrite each numbered heading/figure to its computed id.
6. Rewrite the surviving references/anchors using the map.
7. Leave `@{repo-slug}/{path}[/§M.N]` external references and any non-reference `A.B.C`-shaped text untouched
   throughout.
8. Report every change made — renumbered items, references rewritten, references removed — in a form usable by
   whichever actor invoked it: human-readable when the Architect invokes it directly, machine-consumable when
   the Assistant or another tool invokes it as part of a pipeline, per the Assistant's own goal of producing
   output other tools can reliably consume. The exact interface — flags, schema, format — is a design-phase
   decision, not specified here.

## 5 Postconditions

* All eligible headings/figures carry correct, freshly-computed numbers (or remain hidden `0` where intended).
* All surviving same-document references and anchors point at the new numbering; dangling ones are gone, not
  misdirected.
* External references and non-reference number-like text are unchanged.
* A change report exists, in a form consumable by whichever actor invoked the tool.

## 6 Extensions

* **3a.** Two headings/figures share the same pseudo-number but have different titles → not ambiguous; the
  title disambiguates them for the tool's own mapping.
* **3b.** Two headings/figures share both the same pseudo-number *and* the same title → genuinely duplicate
  identity; the source document itself is broken, not something numbering resolves.
* **8a.** Invoked directly by the Architect rather than the Assistant → the change report defaults to
  human-readable rather than machine-consumable.

## 7 Open Design Questions

* Exact CLI flags, exit codes, and report format(s) — including whether/how JSON is used — are a design-phase
  concern, deliberately out of scope here.
