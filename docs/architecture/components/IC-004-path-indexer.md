# IC-004 — PathIndexer

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.9) first decided this interface

## Purpose

Walks a path into independent per-directory units and extracts each unit's own indexable content — words and
TODOs — from its documents. Deliberately unit-scoped throughout (§5's own note, HLD): recursion is this same
per-unit work repeated, never one combined pass spanning a whole recursed tree.

## 1 `resolve_index_units`

Resolves `path`/`recursive`/`depth` to independent per-directory units — a single unit for a single file or a
non-recursive directory, one unit per directory encountered when `recursive` is set.

`resolve_index_units(path: path, recursive: bool, depth: int?) -> units`

```yaml
calls: []
called_from:
  - "IC-000 §2"
```

## 2 `resolve_documents_in_unit`

Resolves one unit's own immediate `.md` documents — never documents belonging to any other unit.

`resolve_documents_in_unit(unit: Unit) -> documents`

```yaml
calls: []
called_from:
  - "IC-000 §2"
```

## 3 `extract_words`

Extracts significant words per node (the document itself, plus each section/figure), via `WordReducer`.

`extract_words(structure: ParsedStructure) -> words`

Calls `WordReducer.reduce_words` per node's own text, then records the result against that node (documentation
standard §4).

```yaml
calls:
  - "IC-006 §1"
called_from:
  - "IC-000 §2"
```

## 4 `extract_todos`

Extracts every `//TODO`-style marker, with its text, containing section, line, and any task reference found
within it.

`extract_todos(document: path) -> todos`

```yaml
calls: []
called_from:
  - "IC-000 §2"
```

# Rationale

No genuinely competing shape was weighed for any of these four — each follows directly from UC-003's own
Technical Interpretation, corrected during review to be unit-scoped throughout (HLD §3.9, and the PR #17
review comment that prompted the correction).
