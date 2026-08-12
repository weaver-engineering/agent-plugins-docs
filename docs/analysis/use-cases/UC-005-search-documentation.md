# UC-005 — Search Documentation

**Actor:** [The Architect's Assistant](../user-personas/architects-assistant.md) — though in practice any agent
needing context may invoke it, not only this specific persona; it's the closest fit we have, and its
constraints (no persistent memory, needs machine-consumable output) are exactly why search matters.
**Scope:** Ranks and previews existing `.index/` content; doesn't read source documents directly (that's
[UC-006](UC-006-extract-document-content.md)'s job) and doesn't decide relevance algorithms beyond making one
selectable.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [UC-003 — Index A Path](UC-003-index-a-path.md) - produces what this reads
* [UC-006 — Extract Document Content](UC-006-extract-document-content.md) - consumes this use case's pointer output
* [The Architect's Assistant](../user-personas/architects-assistant.md) - primary actor
* @docs/standards/documentation-standards.md/§4 - Indexing (the data this searches)

## 1 Goal

Given a query and a scope, return documents/sections ranked by relevance, either as bare pointers for the
caller to choose from, or as top-N results with content previews — without requiring a full-document read.

## 2 Trigger

An agent (typically the Assistant) needs context on a subject and doesn't know which document or section
covers it.

## 3 Preconditions

* `.index/` content exists for the target scope (produced by [UC-003](UC-003-index-a-path.md)).
* A query string is given; a scope path is optional, defaulting to cwd.

## 4 Main Success Scenario

1. Resolve scope: a filesystem path (defaulting to cwd), or an `@{slug}` specifier — a single project's docs
   repo (`-docs` suffix optional), `@{slug}@{slug}` chaining multiple, `@docs` for `weaver-engineering/docs`,
   or `@all` for every weaver-engineering docs repo.
2. Load every `.words.yaml` under that scope into a single tree.
3. Score each node (document and section) against the query using a selectable algorithm — default: match
   count normalized by the node's total word count, so a small section entirely about the term outranks a
   large document that mentions it once. Multi-word queries combine per-term scores (summed, not requiring
   every term present), so results degrade gracefully rather than requiring an exact match on every word.
4. Produce a document-level score alongside each section's, via the same selectable algorithm — swapping the
   algorithm consistently affects both levels together, since one component computes both.
5. Return results in one of two forms: the full ranked list as bare pointers (document/section references
   only — exact-match compatible with [UC-006](UC-006-extract-document-content.md)'s input, so a caller can
   hand one straight to extraction), or, in "details" mode, the top N results with the first X lines of each
   matched node's content as a preview.

## 5 Postconditions

* Results are ranked by relevance under whichever algorithm was selected (or the default).
* Every returned pointer is directly usable as [UC-006](UC-006-extract-document-content.md) input, with no
  translation step.
* No source document is read in full — only indexed content and, in details mode, bounded previews.

## 6 Extensions

* **3a.** Query matches nothing in scope → empty result set, not an error.
* **3b.** `@all` or a multi-project `@{slug}@{slug}` spans repos with no shared relevance baseline (e.g. very
  different doc sizes/densities) → cross-repo score comparability isn't addressed here.

## 7 Open Design Questions

* Exact algorithm-selection syntax (e.g. a `--calc` flag), and N/X defaults for details mode, are design-phase
  concerns.
* That document-level rollup is computed by the same component as section-level scoring (not a separate fixed
  mechanism) is a deliberate allocation, worth carrying into design.
