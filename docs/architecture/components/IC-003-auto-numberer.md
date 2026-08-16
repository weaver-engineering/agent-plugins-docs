# IC-003 — AutoNumberer

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.9) first decided this interface

## Purpose

The six steps `auto_number_document` (IC-000 §1) sequences to renumber a document and report what changed. A
registry of independently addressable functions, not one coherent class-shaped interface — each is one step of
UC-002's own Main Success Scenario, called directly by `IC-000 §1`, not chained to each other.

## 1 `compute_numbering`

Computes fresh numbering by document position and heading depth.

`compute_numbering(parsed: ParsedStructure) -> numbering`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 2 `build_id_map`

Builds the old→new id map, keyed by pseudo-number and title.

`build_id_map(parsed: ParsedStructure, numbering: Numbering) -> id_map`

Raises `duplicate_identity` when two headings/figures share both pseudo-number and title (UC-002 Extension 3b)
— a broken source document, not something numbering resolves.

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 3 `find_surviving_references`

Finds same-document references whose old id survives into `id_map`, evaluated against the original,
unmodified document (UC-002 MSS step 4) — a dangling reference is simply absent from the result, not flagged.

`find_surviving_references(parsed: ParsedStructure, id_map: IdMap) -> references`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 4 `rewrite_headings`

Applies computed numbering to headings/figures.

`rewrite_headings(parsed: ParsedStructure, numbering: Numbering) -> document`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 5 `rewrite_references`

Rewrites the surviving reference set found by §3 into the numbered document from §4.

`rewrite_references(numbered_document: document, surviving_refs: references, id_map: IdMap) -> document`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 6 `format_report`

Formats the change report, human-readable or machine-consumable (§3.5).

`format_report(rewritten_document: document, mode: "human_readable" | "machine_consumable") -> report`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

# Rationale

No genuinely competing shape was weighed for any of these six — each follows directly from UC-002's own
Technical Interpretation, already immutable and already reviewed (HLD §3.9).
