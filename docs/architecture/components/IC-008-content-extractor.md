# IC-008 — ContentExtractor

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.7, §3.9) first decided this interface

## Purpose

Resolves a document and a target range, then reads verbatim source text — the one place outside `IndexStore`
that reads `IndexStore`'s own persisted data directly (`sections.yaml`, via IC-005 §6), since resolving a
`§section` reference to a line range needs it.

## 1 `resolve_document`

Resolves an exact path or `**{slug}` wildcard match within a resolved scope. Its own cardinality covers UC-006
Extensions 2a (empty) and 2b (multiple) as its two outcomes, not additional branches layered on top.

`resolve_document(reference: Reference, resolved_scope: Scope) -> DocumentMatches`

```yaml
calls: []
called_from:
  - "IC-000 §4"
```

## 2 `resolve_target_range`

Resolves the whole document, a `§section`, an explicit line range, or a `§section` plus range, within the
matched document.

`resolve_target_range(reference: Reference, document: path) -> TargetRange`

A whole-document reference (no `§section` given) excludes any `# Appendix`/`# Rationale` content — the same
boundary `preview_content` (`IC-007 §4`) uses (HLD §3.9 addendum), found the same way: read the document's
section titles via `IC-005 §6`, check each against `is_reserved_section` (`IC-001 §2`). Either section is still
retrievable, just only by naming it explicitly (`§Appendix`/`§Rationale`), through the path below.

A `§{section}` reference resolves three ways (HLD §3.9's addenda). First, if it's zone-qualified —
`{appendix|rationale}.{number}`, case-insensitive on the zone name — split on the first `.`, resolve the
remainder as a number *scoped to entries whose own `zone` field matches* (§4.33): Appendix/Rationale subsections
keep whatever numbers their author typed, uncoordinated with the main body's, so `§rationale.1.2` and a body
`§1.2` can coexist without colliding. Otherwise, if it matches a valid pseudo-number pattern, against whichever
*unqualified* (`zone: null`) `SectionIndex` entry's own `number` field equals it — always unique within that
scope. Otherwise, as a title, case-insensitively, against entries' own `title` fields, zone or not: one match
resolves normally; zero raises `section_not_found` (Extension 3a); more than one raises `ambiguous_section`,
returning every matching entry as `SectionCandidates` (HLD §4.33.2) so the caller can retry with one candidate's
own `number`. Out-of-bounds line ranges are clamped to actual bounds (§3.7) — except where there's no valid
overlap at all (`start` after `end`, or `start` itself past the target's own real end), which raises
`invalid_range` instead (§3.7's own refinement).

```yaml
calls:
  - "IC-005 §6"
  - "IC-001 §2"
called_from:
  - "IC-000 §4"
```

## 3 `find_closest_section`

Finds the nearest existing *ancestor* of a `section_not_found` failure from §2 (HLD §3.7's later correction) —
only ever applies to a pseudo-number reference: strips the last dot-separated segment (`"1.2.3"` → `"1.2"`) and
checks whether that shorter number exists, repeating until one does or every segment is exhausted. Not fuzzy
title matching — a title-shaped reference that fails to match has no hierarchy to walk and gets no pointer at
all, straight `section_not_found`. Returns nothing (not a `Heading`) when even the top-level segment doesn't
exist — `IC-000 §4`'s own caller then falls back to the whole document instead of failing at all.

`find_closest_section(reference: Reference, document: path) -> Heading | null`

```yaml
calls:
  - "IC-005 §6"
called_from:
  - "IC-000 §4"
```

## 4 `read_source_text`

Reads verbatim source text directly from the source `.md` file at a resolved range — never reconstructed from
index data (UC-006 MSS step 4).

`read_source_text(document: path, target_range: TargetRange) -> string`

```yaml
calls: []
called_from:
  - "IC-000 §4"
```

# Rationale

No genuinely competing shape was weighed for any of these four — each follows directly from UC-006's own
Technical Interpretation (HLD §3.9). §2 and §3's `IC-005 §6` dependency wasn't visible until binding (§4.3) —
see `IC-005`'s own `# Rationale`.
