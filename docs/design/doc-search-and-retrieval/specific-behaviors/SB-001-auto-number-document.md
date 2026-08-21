---
reconciliation:
  checked_at: "2026-08-19"
  uc_technical_interpretation_checksums:
    "UC-002": "sha256:b8670d4c9c106fbd9189cffa9a7fb7ac6caccee127a4e7bc49eecca4c777f5a"
  function_checksums:
    "IC-001 §1": "sha256:efcf19280fecc92fb9ae0ab3ccce93c8d372c0c74adba47c124e05c012c6c9f"
    "IC-003 §1": "sha256:cbee7d5fa5ba79ab7e3d27b8fd328660c7ea8706145f77d958010835da9b83c"
    "IC-003 §2": "sha256:c5f5c493a4375bb4ba32104b5b13f19fc8b69ca3fd700470886226bdebc0ea7"
    "IC-003 §3": "sha256:0c0e1a9f5cabd2d232fcc26055107db36386f36267070fdb25f0908a86716d2"
    "IC-003 §4": "sha256:3284c7767c2037cfcc7ce88fe2104e62bed31402b7419db739d5daeef4d1c36"
    "IC-003 §5": "sha256:d1c4a01be149ac44822f7645d94cfcabe45dc180012aad9f9f54fb1b39eb69b"
    "IC-003 §6": "sha256:1ebe330157d8db48d5d9dec5daaf0507e199807813d6ef0d3a25ff74f531afd"
  behaviors:
    "1":
      call_tree:
        address: "IC-000 §1"
        children:
          - address: "IC-001 §1"
          - address: "IC-003 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
          - address: "IC-003 §2"
          - address: "IC-003 §3"
          - address: "IC-003 §4"
          - address: "IC-003 §5"
          - address: "IC-003 §6"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:37:11.000Z"
    "1.1":
      call_tree:
        address: "IC-000 §1"
        children:
          - address: "IC-001 §1"
          - address: "IC-003 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
          - address: "IC-003 §2"
          - address: "IC-003 §3"
          - address: "IC-003 §4"
          - address: "IC-003 §5"
          - address: "IC-003 §6"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:58:53.000Z"
    "2":
      call_tree:
        address: "IC-000 §1"
        children:
          - address: "IC-001 §1"
          - address: "IC-003 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
          - address: "IC-003 §2"
          - address: "IC-003 §3"
          - address: "IC-003 §4"
          - address: "IC-003 §5"
          - address: "IC-003 §6"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T16:12:28.000Z"
    "3":
      call_tree:
        address: "IC-000 §1"
        children:
          - address: "IC-001 §1"
          - address: "IC-003 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
          - address: "IC-003 §2"
          - address: "IC-003 §3"
          - address: "IC-003 §4"
          - address: "IC-003 §5"
          - address: "IC-003 §6"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T16:15:36.000Z"
    "4":
      call_tree:
        address: "IC-000 §1"
        children:
          - address: "IC-001 §1"
          - address: "IC-003 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
          - address: "IC-003 §2"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T16:19:10.000Z"
---
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

(§7.1 Mechanical Reconciliation — no `pseudocode-subset-checker`/`reconciliation-checksum-utility` skill built
yet, computed by hand via `shasum -a 256` over each cited slice, per design-assistant.md's own fallback
protocol. Subset relationship: already established piece by piece deriving §1-§4 above, each sanity-checked as
written — this is the first recorded baseline, not a fresh semantic walk. Side effects: N/A, this Feature has no
External Dependencies (HLD §6). Exceptions: swept — `duplicate_identity` is now declared on both `IC-003 §2`
(origin) and `IC-000 §1` (its own caller, added this pass) — see `IC-000`'s own doc.)

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

### 1.1 Invoked By The Architect

**Realizes:** happy path — Extension 8a

**Given** — as §1, the same document `docs/example/sample.md`

**When** — as §1, but `auto_number_document(document: "docs/example/sample.md", invoked_by: "architect")` is
invoked (`IC-000 §1`)

**Then** — as §1 (the same rewritten document, the same renumbering/reference changes underneath), but
`format_report` (`IC-003 §6`) is called with `mode: "human_readable"` instead of `"machine_consumable"`,
rendering the identical `NumberingReport` data (HLD §4.26, §3.9) as a human-readable report rather than raw
structured output — e.g.:
```
Renumbered:
  §3 -> §1  First Section
  §5 -> §2  Second Section
References rewritten:
  §5 -> §2 (line 8)
References removed: none
```
(the literal human-readable text shape isn't itself fixed by any Key Decision — §3.5 settled the
human/machine split, not this rendering's exact wording — so the block above is illustrative of the same
underlying data, not a decided format string)

## 2 No Pre-Existing Pseudo-Numbers

**Realizes:** happy path

**Given** a document `docs/example/untitled-sections.md`, none of whose headings carry any pseudo-number:
```
# Sample Two

## Context
* [Other Doc](other.md) - related

## Introduction
Getting started info.

## Details
More info here.

## Notes
Final notes.
```

**When** `auto_number_document(document: "docs/example/untitled-sections.md", invoked_by: "assistant")` is
invoked (`IC-000 §1`)

**Then** the document is rewritten to:
```
# Sample Two

## Context
* [Other Doc](other.md) - related

## Introduction
Getting started info.

## 1 Details
More info here.

## 2 Notes
Final notes.
```
`Introduction`, the first section, carries no valid pseudo-number (Precondition 3), so it defaults to the
hidden id `"0"` internally and stays unnumbered in the visible heading; every later sibling still gets a visible
number computed fresh from `1`, regardless of having had none before. The report returned is:
```yaml
renumbered:
  - {old: "", new: "1", title: "Details"}
  - {old: "", new: "2", title: "Notes"}
references_rewritten: []
references_removed: []
```
(`old: ""` is this behavior's own inferred convention for "had no pseudo-number before" — `RenumberedEntry.old`
(HLD §4.23) is a plain, non-nullable `string`, and no Key Decision states what a brand-new number's `old` value
should literally contain; flagged for confirmation rather than silently decided. `Introduction` itself doesn't
appear in `renumbered` at all, since it has no visible number either before or after.)

## 3 Disambiguated Duplicate Pseudo-Number

**Realizes:** happy path — Extension 3a

**Given** a document `docs/example/duplicate-number.md`, two headings both carrying pseudo-number `2` but
different titles:
```
# Sample Three

## Context
* [Other Doc](other.md) - related

## 2 Alpha Section
Alpha content.

## 2 Beta Section
Beta content.
```

**When** `auto_number_document(document: "docs/example/duplicate-number.md", invoked_by: "assistant")` is
invoked (`IC-000 §1`)

**Then** `build_id_map` (`IC-003 §2`) keys each heading by `(pseudo_number, title)` (UC-002 MSS step 3), so the
shared old number `"2"` doesn't collide — `("2", "Alpha Section")` and `("2", "Beta Section")` are two distinct
`IdMap` entries, no `duplicate_identity` is raised, and numbering proceeds normally by document position: the
document is rewritten to:
```
# Sample Three

## Context
* [Other Doc](other.md) - related

## 1 Alpha Section
Alpha content.

## 2 Beta Section
Beta content.
```
and the report returned is:
```yaml
renumbered:
  - {old: "2", new: "1", title: "Alpha Section"}
  - {old: "2", new: "2", title: "Beta Section"}
references_rewritten: []
references_removed: []
```
(no same-document `§`-reference appears in this Given at all — resolving a *reference* to one of two
identically-numbered-but-differently-titled headings, as opposed to the id map merely holding both without
colliding, isn't something this behavior needs to exercise, since a plain `§2` token in prose carries no title
to disambiguate by in the first place)

## 4 Duplicate Identity

**Realizes:** unhappy path — Extension 3b (`duplicate_identity`)

**Given** a document `docs/example/duplicate-identity.md`, two headings sharing both the same pseudo-number and
the same title:
```
# Sample Four

## Context
* [Other Doc](other.md) - related

## 2 Overview
First overview text.

## 2 Overview
Second overview text.
```

**When** `auto_number_document(document: "docs/example/duplicate-identity.md", invoked_by: "assistant")` is
invoked (`IC-000 §1`)

**Then** `parse_markdown_structure` (`IC-001 §1`) and `compute_numbering` (`IC-003 §1`) both run normally, but
`build_id_map` (`IC-003 §2`) finds both headings would key to the identical `(pseudo_number, title)` pair —
`("2", "Overview")` — a genuine collision, not Extension 3a's case (§3 above), since nothing here disambiguates
them; it raises `duplicate_identity`, which propagates straight out of `auto_number_document` uncaught (the
bound pseudocode's own `ON FAILURE (duplicate_identity): RAISE duplicate_identity`, with no handler above it).
No document rewrite happens, no report is produced; per Key Decision §3.5, the CLI surfaces this as a non-zero
exit — the one case UC-002's own exit-code convention exists for.
