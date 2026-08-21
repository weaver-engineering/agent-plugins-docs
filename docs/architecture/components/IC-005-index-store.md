# IC-005 — IndexStore

**Kind:** internally-owned data store

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.9, §3.4) first decided this interface

## Purpose

Reads and writes the persisted `.index/` file format — `sections.yaml`/`words.yaml`/`todo.yaml` — that
`PathIndexer` populates and `Searcher`/`ContentExtractor` read back. In-process filesystem I/O against files
this project itself manages, not a formal External Dependency (§3.4).

## 1 `write_index_files`

Persists `sections`/`words`/`todo` `.index/` files for one document; omits a file entirely when it has no
content to hold (UC-003 Extension 5a) rather than writing one empty. On a re-index, this is symmetric in both
directions: a file whose content is present gets written/overwritten, and a file whose content has become empty
since the previous index — content that used to justify it is now gone — gets actively deleted, not left
standing with stale content (UC-003's own Goal and Postconditions; confirmed while deriving `SB-002 §4.1`).
`sections.yaml` is written keyed by each heading/figure's own stable `id` (HLD §3.9's general-fix addendum,
found while deriving `SB-004`), `title` a field within each entry rather than the key — two headings sharing a
title no longer overwrite each other. Calls `mark_protected_headings` itself to populate each entry's own `zone`
field (§3.9's later addendum) — `null` for ordinary body content, `"appendix"`/`"rationale"` for anything inside
one — a second call to the same function `extract_words` already made, not a shared precomputed value passed
down from `IC-000 §2`: cheap, deterministic, and simpler than restructuring that orchestration to thread one
extra value through.

`write_index_files(document: path, structure: ParsedStructure, words: WordIndex, todos: Todos) -> void`

```yaml
calls:
  - "IC-001 §3"
called_from:
  - "IC-000 §2"
```

## 2 `list_index_entries`

Lists existing `.index/` entries for one unit.

`list_index_entries(unit: Unit) -> Entries`

```yaml
calls: []
called_from:
  - "IC-000 §2"
```

## 3 `find_stale_entries`

Finds entries in a unit with no corresponding current document (UC-003 MSS step 6), scoped to that unit only.

`find_stale_entries(existing_entries: Entries, documents: Documents) -> Entries`

```yaml
calls: []
called_from:
  - "IC-000 §2"
```

## 4 `remove_index_entries`

Deletes stale entries, including individual index files that no longer have content to justify them.

`remove_index_entries(entry: Entry) -> void`

```yaml
calls: []
called_from:
  - "IC-000 §2"
```

## 5 `load_word_index`

Reads `.words.yaml` content under a resolved scope, filtered to a reduced query: returns only nodes that
actually contain a matching word — a document's own root `WordCounts` as well as its sections (HLD §3.9
addendum), each with its own total word count (needed for relevance normalization) — not the whole scoped
tree. A root-level match is returned with `section: null` (HLD §4.34), the same convention `score_nodes`'s own
output already uses for a document-level score.

`load_word_index(scope: Scope, reduced_query: Words) -> MatchingIndex`

```yaml
calls: []
called_from:
  - "IC-000 §3"
```

## 6 `read_section_index`

Reads one document's own `sections.yaml` entries directly — added while binding `ContentExtractor` (§4.3):
resolving a `§section` reference to a line range, or finding the closest matching section on a miss, both need
one document's section boundaries, which is neither `load_word_index` (scoped to a query match, not a single
document) nor any function `PathIndexer` exposes. Also read by `preview_content` (`IC-007 §4`, HLD §3.9
addendum), to find where a document-level preview should stop excluding Appendix/Rationale. Returns `SectionIndex`
keyed by `id` (HLD §3.9's general-fix addendum) — a caller resolving by title or number now scans entries'
own `title`/`number` fields rather than doing a direct key lookup.

`read_section_index(document: path) -> SectionIndex`

```yaml
calls: []
called_from:
  - "IC-008 §2"
  - "IC-008 §3"
  - "IC-007 §4"
```

# Rationale

§1-§4 (write side) and §5-§6 (read side) stay one component, not two, per the HLD's own `# Rationale` on the
`IndexStore`/`PathIndexer` split (§5 component grouping): both sides are defined by the same persisted `.index/`
file format, not by which use case happens to call them.

§6 wasn't part of the original Ideation pass (§3.9) — it surfaced only once `ContentExtractor`'s own functions
needed real addresses to bind to (§4.3), which is exactly the kind of gap binding is meant to surface rather
than one Ideation could have anticipated in the abstract.
