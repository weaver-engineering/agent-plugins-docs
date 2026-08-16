# SB-001 — Auto-Number A Document

## Context
* [UC-002 — Auto-Number Document Sections](../../../analysis/use-cases/UC-002-auto-number-document-sections.md) - the use case this file's behaviors realize
* [IC-000 — Docs Tooling CLI](../../../architecture/components/IC-000-docs-tooling-cli.md) - §1, the bound entry point below
* Specific Behaviors (@docs/workflows/feature-workflow/specific-behaviors.md) - the convention this document follows

**Realizes:** UC-002 steps 1-8

**Bound Pseudocode (UC-002):**

```
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
entry state (Given) from UC-002's own Preconditions/Extensions, trace each through the bound pseudocode above,
and present each resulting behavior for a quick sanity check. Given/When/Then and Call Tree aren't recorded yet.
