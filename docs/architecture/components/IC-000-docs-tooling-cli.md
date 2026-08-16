# IC-000 — Docs Tooling CLI

**Kind:** system interface (entry point)

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.2) first decided this is a CLI, and whose four use cases produced these four functions

## Purpose

The system's own entry point (Design Directory And HLD §4.4) — one function per CLI command, one command per
use case in scope. This is the project's first Feature, so this document doesn't exist prior to it; a later
Feature adding a new command extends this same document with a new numbered function rather than creating a
competing one (Design Directory And HLD §4.4/§3.2's ownership rule).

## 1 `auto_number_document`

CLI entry for UC-002 (Auto-Number Document Sections).

`auto_number_document(document: path, invoked_by: "architect" | "assistant") -> (document, report)`

```yaml
calls:
  - "IC-001 §1"
  - "IC-003 §1"
  - "IC-003 §2"
  - "IC-003 §3"
  - "IC-003 §4"
  - "IC-003 §5"
  - "IC-003 §6"
called_from: []
```

```yaml
pseudocode: |
  FUNCTION IC-000 §1:
    parsed <-- [IC-001 §1: parse_markdown_structure - document]
    numbering <-- [IC-003 §1: compute_numbering - parsed]
    id_map <-- [IC-003 §2: build_id_map - parsed, numbering]
      ON FAILURE (duplicate_identity): RAISE duplicate_identity
    surviving_refs <-- [IC-003 §3: find_surviving_references - parsed, id_map]
    numbered_doc <-- [IC-003 §4: rewrite_headings - parsed, numbering]
    rewritten_doc <-- [IC-003 §5: rewrite_references - numbered_doc, surviving_refs, id_map]
    IF invoked_by IS architect:
      report <-- [IC-003 §6: format_report - rewritten_doc, human_readable]
    ELSE:
      report <-- [IC-003 §6: format_report - rewritten_doc, machine_consumable]
    RETURN rewritten_doc, report
used_by_steps:
  - "UC-002 steps 1-8"
used_by_behaviors:
  - "SB-001 (behaviors not yet derived)"
```

## 2 `index_path`

CLI entry for UC-003 (Index A Path).

`index_path(path: path, recursive: bool, depth: int?) -> report`

```yaml
calls:
  - "IC-004 §1"
  - "IC-004 §2"
  - "IC-001 §1"
  - "IC-004 §3"
  - "IC-004 §4"
  - "IC-005 §1"
  - "IC-005 §2"
  - "IC-005 §3"
  - "IC-005 §4"
called_from: []
```

```yaml
pseudocode: |
  FUNCTION IC-000 §2:
    units <-- [IC-004 §1: resolve_index_units - path, recursive, depth]
    FOR EACH unit IN units:
      documents <-- [IC-004 §2: resolve_documents_in_unit - unit]
      FOR EACH document IN documents:
        structure <-- [IC-001 §1: parse_markdown_structure - document]
        words <-- [IC-004 §3: extract_words - structure]
        todos <-- [IC-004 §4: extract_todos - document]
        [IC-005 §1: write_index_files - document, structure, words, todos]
      existing_entries <-- [IC-005 §2: list_index_entries - unit]
      stale_entries <-- [IC-005 §3: find_stale_entries - existing_entries, documents]
      FOR EACH entry IN stale_entries:
        [IC-005 §4: remove_index_entries - entry]
    RETURN report
used_by_steps:
  - "UC-003 steps 1-6"
used_by_behaviors:
  - "SB-002 (behaviors not yet derived)"
```

## 3 `search_documentation`

CLI entry for UC-005 (Search Documentation).

`search_documentation(query: string, scope: string, mode: "list" | "details") -> results`

```yaml
calls:
  - "IC-002 §1"
  - "IC-002 §2"
  - "IC-007 §1"
  - "IC-005 §5"
  - "IC-007 §2"
  - "IC-007 §3"
  - "IC-007 §4"
called_from: []
```

```yaml
pseudocode: |
  FUNCTION IC-000 §3:
    IF scope IS chained:
      resolved_scope <-- [IC-002 §2: resolve_chained_scope - scope]
    ELSE:
      resolved_scope <-- [IC-002 §1: resolve_scope_single - scope]
    reduced_query <-- [IC-007 §1: reduce_query - query]
    matching_index <-- [IC-005 §5: load_word_index - resolved_scope, reduced_query]
    scores <-- [IC-007 §2: score_nodes - matching_index, reduced_query]
    IF mode IS details:
      top_results <-- [IC-007 §3: select_top_n - scores]
      previews <-- [IC-007 §4: preview_content - top_results]
      RETURN top_results, previews
    ELSE:
      RETURN scores
used_by_steps:
  - "UC-005 steps 1-5"
used_by_behaviors:
  - "SB-003 (behaviors not yet derived)"
```

## 4 `extract_content`

CLI entry for UC-006 (Extract Document Content).

`extract_content(reference: Reference, scope_hint: string?) -> content`

```yaml
calls:
  - "IC-002 §1"
  - "IC-008 §1"
  - "IC-008 §2"
  - "IC-008 §3"
  - "IC-008 §4"
called_from: []
```

```yaml
pseudocode: |
  FUNCTION IC-000 §4:
    resolved_scope <-- [IC-002 §1: resolve_scope_single - scope_hint]
    matches <-- [IC-008 §1: resolve_document - reference, resolved_scope]
    IF matches IS empty:
      RETURN empty_result
    IF matches HAS more than one:
      RETURN candidate_list: matches
    document = matches[0]
    target_range <-- [IC-008 §2: resolve_target_range - reference, document]
      ON FAILURE (section_not_found):
        closest <-- [IC-008 §3: find_closest_section - reference, document]
        RETURN failure, closest
    content <-- [IC-008 §4: read_source_text - document, target_range]
    RETURN content
used_by_steps:
  - "UC-006 steps 1-4"
used_by_behaviors:
  - "SB-004 (behaviors not yet derived)"
```

# Rationale

Each function's own bound pseudocode is a direct binding of its use case's already-immutable Technical
Interpretation, substituting the real components §5 of the HLD decided (Design Feature Instructions §4.3) — not
re-derived or reinterpreted here. `IC-000 §3`'s `IF scope IS chained` branch is the one place a function
here makes a runtime choice between two Key Decisions (`IC-002 §1`/`§2`, HLD §3.3) rather than calling a fixed
sequence — both addresses are listed in `calls:` since either may be reached, `calls:` being a declared
superset, not one concrete walk (Internal Component Template's own convention).
