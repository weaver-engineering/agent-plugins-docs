# SB-004 — Extract Document Content

## Context
* [UC-006 — Extract Document Content](../../../analysis/use-cases/UC-006-extract-document-content.md) - the use case this file's behaviors realize
* [IC-000 — Docs Tooling CLI](../../../architecture/components/IC-000-docs-tooling-cli.md) - §4, the bound entry point below
* Specific Behaviors (@docs/workflows/feature-workflow/specific-behaviors.md) - the convention this document follows

**Realizes:** UC-006 steps 1-4

**Bound Pseudocode (UC-006):**

```
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
entry state (Given) from UC-006's own Preconditions/Extensions, trace each through the bound pseudocode above,
and present each resulting behavior for a quick sanity check. Given/When/Then and Call Tree aren't recorded yet.
