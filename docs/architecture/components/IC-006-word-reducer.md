# IC-006 — WordReducer

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.10) first decided this interface

## Purpose

The documentation standard's own §4 tokenization/stemming/stopword reduction, in exactly one place — called
directly by both `PathIndexer` (building the index) and `Searcher` (reducing a query), so the two are
mechanically guaranteed to stay consistent rather than independently asserting equivalence (§3.10).

## 1 `reduce_words`

Reduces any given text to its significant word tokens.

`reduce_words(text: string) -> words`

Case-folds; keeps `-`, `_`, `.`, `:`, `/` inside a token; treats every other character as a break, except `@`,
which starts a verbatim `@{repo-slug}/{path}[/§M.N]` token; reduces plurals/possessives to their root; drops
stopwords (`stopwords.yaml`).

```yaml
calls: []
called_from:
  - "IC-004 §3"
  - "IC-007 §1"
```

# Rationale

Extracted from what were originally two independent implementations inside `extract_words` and `reduce_query` —
see the HLD's own `# Rationale` (§3.10) for why that was a real bug risk, not just a style preference.
