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

`reduce_query(query: string) -> reduced_query`

```yaml
calls:
  - "IC-006 §1"
called_from:
  - "IC-000 §3"
```

## 2 `score_nodes`

Scores document- and section-level relevance together, via a selectable algorithm (`--calc`, §3.8) — one call
producing both levels, since swapping the algorithm affects both together (UC-005 MSS steps 3-4).

`score_nodes(matching_index: MatchingIndex, reduced_query: Words) -> scores`

```yaml
calls: []
called_from:
  - "IC-000 §3"
```

## 3 `select_top_n`

Selects the top `--max-results` results (default `20`, §3.8).

`select_top_n(scores: Scores) -> top_results`

```yaml
calls: []
called_from:
  - "IC-000 §3"
```

## 4 `preview_content`

Produces the first `--preview-lines` lines (default `5`, §3.8) of each result's content, for details mode.

`preview_content(top_results: TopResults) -> previews`

```yaml
calls: []
called_from:
  - "IC-000 §3"
```

# Rationale

No genuinely competing shape was weighed for any of these four — each follows directly from UC-005's own
Technical Interpretation, corrected during review to narrow `load_word_index` by a reduced query rather than
loading the whole scoped tree (HLD §3.9, and the PR #17 review comment that prompted the correction).
