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

# Appendix

## Technical Interpretation

```
FUNCTION extract_content(reference, scope_hint):
  resolved_scope <-- [resolve_scope - scope_hint]
  matches <-- [resolve_document - reference, resolved_scope]
  IF matches IS empty:
    RETURN empty_result
  IF matches HAS more than one:
    RETURN candidate_list: matches
  document = matches[0]
  target_range <-- [resolve_target_range - reference, document]
    ON FAILURE (section_not_found):
      closest <-- [find_closest_section - reference, document]
      RETURN failure, closest
  content <-- [read_source_text - document, target_range]
  RETURN content
```

One operation: the actor crosses the system boundary once per invocation, regardless of which of the four
reference shapes (whole document, `§section`, line range, or `§section` plus range) it resolves to.
`[resolve_document]`'s cardinality naturally covers Extensions 2a (empty → `matches IS empty`) and 2b (multiple
→ `matches HAS more than one`) as its own two outcomes, not additional branches layered on top.
`[resolve_target_range]` is deliberately a separate call from `[read_source_text]` — MSS step 4's own
constraint ("never reconstructed from index data") is a property of `[read_source_text]` specifically: it reads
the *source* file at a range something else already resolved, rather than being asked to derive content from
index data itself. Extension 3a (`§section` not found) is `[resolve_target_range]`'s one exceptional condition,
caught here to look up the closest match rather than left to propagate as a bare failure.

[SB-004 — Extract Document Content](../../design/doc-search-and-retrieval/specific-behaviors/SB-004-extract-document-content.md) - the operation above
