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

Raises `section_not_found` when the referenced section doesn't exist (UC-006 Extension 3a). Out-of-bounds line
ranges are clamped to actual bounds, not an error (§3.7).

```yaml
calls:
  - "IC-005 §6"
called_from:
  - "IC-000 §4"
```

## 3 `find_closest_section`

Finds the nearest matching section on a `section_not_found` failure from §2, so the caller gets a pointer
rather than a bare error (UC-006 Extension 3a).

`find_closest_section(reference: Reference, document: path) -> Heading`

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
