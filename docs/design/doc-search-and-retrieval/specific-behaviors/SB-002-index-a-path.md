# SB-002 — Index A Path

## Context
* [UC-003 — Index A Path](../../../analysis/use-cases/UC-003-index-a-path.md) - the use case this file's behaviors realize
* [IC-000 — Docs Tooling CLI](../../../architecture/components/IC-000-docs-tooling-cli.md) - §2, the bound entry point below
* Specific Behaviors (@docs/workflows/feature-workflow/specific-behaviors.md) - the convention this document follows

**Realizes:** UC-003 steps 1-6

**Bound Pseudocode (UC-003):**

```
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
```

```yaml
reconciliation:
  checked_at: null
  uc_technical_interpretation_checksums: {}
  function_checksums: {}
  reviewed_by: null
  reviewed_at: null
```

//TODO - Derive this operation's specific behaviors (Design Feature Instructions §5): establish every valid
entry state (Given) from UC-003's own Preconditions/Extensions, trace each through the bound pseudocode above,
and present each resulting behavior for a quick sanity check. Given/When/Then and Call Tree aren't recorded yet.
