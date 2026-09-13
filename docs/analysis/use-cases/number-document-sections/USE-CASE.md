# number-document-sections — Number A Document's Sections

**Actor:** [The Architect](../../user-personas/architect.md) — primary. [The Agent](../../user-personas/agent.md)
is a supporting actor, invoking the same operation on the Architect's behalf as a step of
[document-a-concept](../document-a-concept/USE-CASE.md).
**Scope:** Numbers and re-links what is already in the document. It does not decide the document's structure or
content, and never touches external (`@{repo-slug}/{path}`) references — see §7.

## Context
* [Agent Plugins index](../../../agent-plugins.md) - root index for this repo
* [The Architect](../../user-personas/architect.md) - primary actor
* [The Agent](../../user-personas/agent.md) - supporting actor
* [document-a-concept](../document-a-concept/USE-CASE.md) - the use case whose authoring step invokes this one
* @docs/standards/documentation-standards.md/§3 - Document Shape, the numbering convention this satisfies
* @docs/standards/documentation-standards.md/§6 - Cross-References, the reference-rewrite rule this satisfies

## 1 Goal

Every section, subsection and figure in a document carries the number the documentation standard requires, and
every same-document reference to them still resolves — without the Architect maintaining any of it by hand.

Renumbering by hand is slow, and it is worse than slow: it is silently error-prone. A reference missed during a
restructure keeps pointing at a number that now names a different section, so the document stays readable while
saying something false. The Architect cannot tell the two apart by reading it back.

## 2 Trigger

A document's headings and figures are unnumbered, partially numbered, or need renumbering because sections were
added, removed or reordered.

## 3 Preconditions

* The document follows the general shape — Title, optional Context, then body headings — and may have zero, some
  or all of its headings and figures already numbered or pseudo-numbered.
* A pseudo-number matches `^\d+(\.\d+)*\.?$` (headings) or `^\d+(\.\d+)*\.[a-zA-Z]\.?$` (figures). Anything else,
  however number-like, is ordinary title text with no special meaning — not even as an opt-in signal.
* The first section, or the first subsection within a parent, defaults to the hidden id `0` unless it carries a
  valid pseudo-number, which opts it into visible numbering from `1`. Every later sibling is always numbered
  visibly, whether or not the author typed a number.

## 4 Main Success Scenario

1. The Architect invokes the numbering tool against a document — directly, or through The Agent as a step of
   larger delegated work.
2. The tool parses the document once, recording: every eligible heading (Context, Appendix and Rationale are
   never numbered), any pseudo-numbers the author typed — including on brand-new headings and figures, so a
   reference written in the same edit as its target resolves rather than reading as dangling — every fenced code
   block and whether it carries a pseudo-number, marking it a figure, and every `§M.N(.O)?` token or
   markdown-link anchor anywhere in the document.
3. The tool computes fresh numbering from document position and heading depth.
4. The tool builds an old-to-new id map keyed by pseudo-number *and* title, so two headings sharing a
   pseudo-number but differing in title resolve distinctly.
5. The tool removes any `§` reference or link anchor whose old id has no entry in that map — evaluated against
   the original, unmodified document, before anything else changes, so a dangling reference can never later be
   mistaken for a match once renumbering is under way.
6. The tool rewrites each numbered heading and figure to its computed id, then rewrites the surviving references
   and anchors through the map, leaving `@{repo-slug}/{path}[/§M.N]` external references and non-reference
   `A.B.C`-shaped text untouched throughout.
7. The tool reports every change it made — items renumbered, references rewritten, references removed — in a form
   usable by whoever invoked it: human-readable for the Architect, machine-consumable when The Agent invoked it
   as part of a pipeline.
8. The Architect (or The Agent, on their behalf) confirms from the report that the document's structure is what
   was intended, rather than re-reading the numbering itself.

## 5 Postconditions

* Every eligible heading and figure carries a correct, freshly computed number, or remains hidden `0` where
  intended.
* Every surviving same-document reference and anchor points at the new numbering; dangling ones are gone, not
  misdirected at whatever now occupies their old number.
* External references and non-reference number-like text are unchanged.
* A change report exists, in a form consumable by whichever actor invoked the tool.

## 6 Extensions

* **3a.** Two headings or figures share a pseudo-number but have different titles → not ambiguous; the title
  disambiguates them in the tool's own map.
* **3b.** Two headings or figures share both pseudo-number *and* title → a genuinely duplicate identity. The
  source document is broken in a way numbering cannot resolve; the tool reports it rather than guessing.
* **7a.** The Agent invoked the tool rather than the Architect → the change report defaults to machine-consumable
  rather than human-readable.

## 7 Open Design Questions (not resolved by this use case)

* Exact CLI flags, exit codes and report formats — including whether and how JSON is used — are a design-phase
  concern.
* Whether numbering is ever triggered by the document changing rather than by an actor invoking it is the same
  open question registration carries in
  [find-and-read-documentation §7](../find-and-read-documentation/USE-CASE.md), and is deliberately left open in
  the same way.
* This use case's Technical Interpretation has not yet been written — see
  [find-and-read-documentation §7](../find-and-read-documentation/USE-CASE.md) for why the whole set is
  outstanding.
