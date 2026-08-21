# IC-007 — Searcher

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.8, §3.9) first decided this interface

## Purpose

Reduces a query, scores `IndexStore`'s matching sections, and produces either the full ranked list or a
details-mode preview. A registry of the four steps `search_documentation` (IC-000 §3) sequences, not one
coherent class-shaped interface.

## 1 `reduce_query`

Reduces the query string via `WordReducer`, so it's mechanically the same reduction the index itself was
built with.

`reduce_query(query: string) -> Words`

```yaml
calls:
  - "IC-006 §1"
called_from:
  - "IC-000 §3"
```

## 2 `score_nodes`

Scores document- and section-level relevance together, via a selectable algorithm (`--calc`, §3.8) — one call
producing both levels, since swapping the algorithm affects both together (UC-005 MSS steps 3-4).

`score_nodes(matching_index: MatchingIndex, reduced_query: Words) -> Scores`

```yaml
calls: []
called_from:
  - "IC-000 §3"
```

## 3 `select_top_n`

Selects the top `--max-results` results (default `20`, §3.8).

`select_top_n(scores: Scores) -> TopResults`

```yaml
calls: []
called_from:
  - "IC-000 §3"
```

## 4 `preview_content`

Produces the first `--preview-lines` lines (default `5`, §3.8) of each result's content, for details mode. A
document-level result (`section: null`) previews the *whole document* — every section and subsection in
document order — excluding any `# Appendix`/`# Rationale` content (HLD §3.9 addendum: the range runs from line
1 up to, but not including, the first heading `is_reserved_section` matches, or end of file if none; needs
`read_section_index` to know where each heading falls, and `is_reserved_section` to know which of them to
exclude). A section-level result previews that section specifically, including its own subsections (already
within its own `start_line`/`end_line`), capped by the section's own content length.

`preview_content(top_results: TopResults) -> Previews`

```yaml
calls:
  - "IC-005 §6"
  - "IC-001 §2"
called_from:
  - "IC-000 §3"
```

# Rationale

No genuinely competing shape was weighed for any of these four — each follows directly from UC-005's own
Technical Interpretation, corrected during review to narrow `load_word_index` by a reduced query rather than
loading the whole scoped tree (HLD §3.9, and the PR #17 review comment that prompted the correction).
