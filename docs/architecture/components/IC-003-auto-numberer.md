# IC-003 — AutoNumberer

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.9) first decided this interface

## Purpose

The six steps `auto_number_document` (IC-000 §1) sequences to renumber a document and report what changed. A
registry of independently addressable functions, not one coherent class-shaped interface — each is one step of
UC-002's own Main Success Scenario, called directly by `IC-000 §1`, not chained to each other.

## 1 `compute_numbering`

Computes fresh numbering by document position and heading depth. Skips every heading `mark_protected_headings`
(`IC-001 §3`) marks — `# Appendix`/`# Rationale` and their own nested subsections alike are never numbered (HLD
§3.1's two addenda; UC-002's own Technical Interpretation step 1 already excludes them, unchanged since
`parse_markdown_structure` started including them in `headings`).

`compute_numbering(parsed: ParsedStructure) -> Numbering`

```yaml
calls:
  - "IC-001 §3"
called_from:
  - "IC-000 §1"
```

## 2 `build_id_map`

Builds the old→new id map, keyed by pseudo-number and title.

`build_id_map(parsed: ParsedStructure, numbering: Numbering) -> IdMap`

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

`find_surviving_references(parsed: ParsedStructure, id_map: IdMap) -> SurvivingReferences`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 4 `rewrite_headings`

Applies computed numbering to headings/figures. Only ever asked to number what `compute_numbering` (§1) actually
produced a number for — `# Appendix`/`# Rationale` headings, having no entry in `Numbering`, are left as-is.

`rewrite_headings(parsed: ParsedStructure, numbering: Numbering) -> string`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 5 `rewrite_references`

Rewrites the surviving reference set found by §3 into the numbered document from §4.

`rewrite_references(numbered_document: string, surviving_refs: SurvivingReferences, id_map: IdMap) -> string`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

## 6 `format_report`

Formats the change report, human-readable or machine-consumable (§3.5).

`format_report(rewritten_document: string, mode: "human_readable" | "machine_consumable") -> NumberingReport`

```yaml
calls: []
called_from:
  - "IC-000 §1"
```

# Rationale

No genuinely competing shape was weighed for any of these six — each follows directly from UC-002's own
Technical Interpretation, already immutable and already reviewed (HLD §3.9).
