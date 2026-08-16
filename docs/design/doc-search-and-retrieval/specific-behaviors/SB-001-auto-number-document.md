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

## 1 Happy Path

**Realizes:** happy path

**Given** a document `docs/example/sample.md`:
```
# Sample Document

## Context
* [Other Doc](other.md) - related

## 3 First Section
Intro text. See §5 for background.

## 5 Second Section
Background details here.
```

**When** `auto_number_document(document: "docs/example/sample.md", invoked_by: "assistant")` is invoked (`IC-000 §1`)

**Then** the document is rewritten to:
```
# Sample Document

## Context
* [Other Doc](other.md) - related

## 1 First Section
Intro text. See §2 for background.

## 2 Second Section
Background details here.
```
and the report returned (`NumberingReport`, HLD §4.6) is:
```yaml
renumbered:
  - {old: "3", new: "1", title: "First Section"}
  - {old: "5", new: "2", title: "Second Section"}
references_rewritten:
  - {old: "§5", new: "§2", line: 8}
references_removed: []
```

**Call Tree**

```yaml
call_tree:
  address: "IC-000 §1"
  children:
    - address: "IC-001 §1"
    - address: "IC-003 §1"
    - address: "IC-003 §2"
    - address: "IC-003 §3"
    - address: "IC-003 §4"
    - address: "IC-003 §5"
    - address: "IC-003 §6"
```

//TODO - Derive the remaining specific behaviors (Design Feature Instructions §5): §1.1 (Extension 8a, invoked
by the Architect — human-readable report), §2 (Extension 3a, disambiguated duplicate pseudo-number), and §3
(Extension 3b, `duplicate_identity` failure) are the three still outstanding, pending sanity check on §1 above.
