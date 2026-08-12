# UC-006 — Extract Document Content

**Actor:** [The Architect's Assistant](../user-personas/architects-assistant.md) — though, as with
[UC-005](UC-005-search-documentation.md), any agent needing content may invoke it in practice.
**Scope:** Reads raw source `.md` content using `.index/` data only to locate it; doesn't compute relevance
(that's [UC-005](UC-005-search-documentation.md)) and doesn't index anything itself
(see [UC-003](UC-003-index-a-path.md)).

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [UC-005 — Search Documentation](UC-005-search-documentation.md) - typical pointer source
* [UC-003 — Index A Path](UC-003-index-a-path.md) - produces the sections.yaml this relies on for line ranges
* [The Architect's Assistant](../user-personas/architects-assistant.md) - primary actor
* @docs/standards/documentation-standards.md/§4 - Indexing (the data this locates content via)

## 1 Goal

Given a reference — exact or wildcard-slug — return the corresponding raw content: whole document, a section,
an explicit line range, or a line range within a section, without the caller needing an exact path in hand.

## 2 Trigger

A caller (typically holding a [UC-005](UC-005-search-documentation.md) result, but not required to) needs
actual content at a known or approximately-known location.

## 3 Preconditions

* `.index/` `sections.yaml` exists for the scope (from [UC-003](UC-003-index-a-path.md)) if a `§section`
  reference is used.
* An exact reference or a `**{slug}` wildcard is given.

## 4 Main Success Scenario

1. Resolve scope: `@{scope}` — a single project (`@{slug}`, `-docs` suffix optional), `@docs` for
   `weaver-engineering/docs`, or `@all` for every weaver-engineering docs repo, but not the chained
   multi-project form ([UC-005](UC-005-search-documentation.md)'s job, not this one's, since extraction
   already knows where it's going) — optionally narrowed further by `/{path}`. Defaults to cwd if omitted.
2. Resolve the target document: an exact file path, or a `**{slug}` wildcard matched within the resolved
   scope/path (a trailing `.md` on `{slug}` is ignored — every document is one).
3. Resolve target content within the matched document: the whole document (nothing further given),
   `§{section}`, an explicit `[{start}-{end}]` line range, or `§{section}[{start}-{end}]` (a line range within
   that section).
4. Read and return the raw text directly from the source `.md` file at the resolved range — never reconstructed
   from index data.

## 5 Postconditions

* Returned content is verbatim source text.
* A wildcard matching nothing succeeds with an empty result.
* A wildcard matching more than one document fails, returning the candidate list for the caller to retry with
  an exact path.
* A `§section` reference not present in an otherwise-successfully-matched document fails, but includes a
  pointer to the closest matching section rather than a bare error.

## 6 Extensions

* **2a.** `**{slug}` matches nothing → succeeds with an empty result, not an error.
* **2b.** `**{slug}` matches more than one document → fails, returning the candidate list.
* **3a.** `§{section}` doesn't exist in the matched document → fails, with a pointer to the closest matching
  section.

## 7 Open Design Questions

* A line range (`[{start}-{end}]`, alone or combined with `§{section}`) that extends beyond the document's or
  section's actual bounds — not yet specified.
