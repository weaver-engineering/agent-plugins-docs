# SB-003 — Search Documentation

## Context
* [UC-005 — Search Documentation](../../../analysis/use-cases/UC-005-search-documentation.md) - the use case this file's behaviors realize
* [IC-000 — Docs Tooling CLI](../../../architecture/components/IC-000-docs-tooling-cli.md) - §3, the bound entry point below
* Specific Behaviors (@docs/workflows/feature-workflow/specific-behaviors.md) - the convention this document follows

**Realizes:** UC-005 steps 1-5

**Bound Pseudocode (UC-005):**

```
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
entry state (Given) from UC-005's own Preconditions/Extensions, trace each through the bound pseudocode above,
and present each resulting behavior for a quick sanity check. Given/When/Then and Call Tree aren't recorded yet.
