# UC-003 — Index A Path

**Actor:** [The Architect's Assistant](../user-personas/architects-assistant.md) — typically invoked as part
of larger delegated work (e.g. [UC-001](UC-001-discuss-concept-and-document.md) step 7), but may also be
invoked directly by [The Architect](../user-personas/architect.md), including on early-stage outline documents
that are still full of `//TODO`s.
**Scope:** Indexes structure, words, and TODOs for whatever path it's given; doesn't number anything itself
(see [UC-002](UC-002-auto-number-document-sections.md)) — indexing works whether or not numbering has been
applied.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [UC-001 — Discuss A Project Concept And Document It](UC-001-discuss-concept-and-document.md) - a caller
* [UC-002 — Auto-Number Document Sections](UC-002-auto-number-document-sections.md) - numbers feed the `number` attribute when present
* [The Architect's Assistant](../user-personas/architects-assistant.md) - primary actor
* @docs/standards/documentation-standards.md/§4 - Indexing (the rule this implements)

## 1 Goal

Keep `.index/<slug>.sections.yaml`, `.index/<slug>.words.yaml`, and `.index/<slug>.todo.yaml` accurate for a
given path, reflecting exactly what's currently in the document(s) — structure, words, and outstanding TODOs —
supporting full-text search and section-level extraction without a full-document read.

## 2 Trigger

Invoked against a path (a file or a directory) whose content has changed, or that has never been indexed —
including documents with no numbering at all.

## 3 Preconditions

* The given path is a single `.md` file, or a directory.
* Indexing doesn't require numbering — sections are found from markdown headings and pseudo-numbered figures
  regardless of whether [UC-002](UC-002-auto-number-document-sections.md) has run.

## 4 Main Success Scenario

1. Resolve the given path: a single file, or a directory. Directory scope defaults to non-recursive — only
   that directory's immediate `.md` files; recursing the full tree, optionally depth-limited, is opt-in.
2. For each document found: parse its headings (excluding Context/Appendix/Rationale) and pseudo-numbered
   figures, computing each entry's title, type, `start_line`, `end_line`, and a `number` attribute where one is
   present.
3. Extract significant words per node (the document itself, plus each section/figure), per the tokenization,
   stemming, and stopword rules in the documentation standard.
4. Extract every `//TODO`-style marker in the document, with its text, containing section, line, and any task
   reference found within it.
5. Write `.index/<slug>.sections.yaml`, `.words.yaml`, and `.todo.yaml` for each document — each written only
   if it has content to hold; none are written empty.
6. Remove `.index/` entries — including individual files that no longer have content to justify them — for any
   source document under the given path whose corresponding content is gone.

## 5 Postconditions

* Each index file exists only if there's content to justify it: no sections → no `.sections.yaml`; no
  significant words after stopword removal → no `.words.yaml`; no `//TODO` markers → no `.todo.yaml`. Nothing
  is written empty.
* Where content that previously justified a file is now gone (e.g. the last TODO was resolved), the
  now-unjustified file is removed, not left stale.
* All still-justified index files accurately reflect current content for every document under the given path.
* Stale index entries for deleted source documents are gone entirely.

## 6 Extensions

* **5a.** A document has no `//TODO` markers → no `.todo.yaml` is written for it (or an existing one is
  removed, if it previously had TODOs that are now gone).

## 7 Open Design Questions

* Exact CLI flags (path vs. recurse vs. depth syntax) are a design-phase concern, deliberately out of scope
  here.
