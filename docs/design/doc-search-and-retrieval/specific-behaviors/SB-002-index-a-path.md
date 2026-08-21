---
reconciliation:
  checked_at: "2026-08-19"
  uc_technical_interpretation_checksums:
    "UC-003": "sha256:d017965a306e9e8a2d3de729f03e888af585692a58f4c137c9476f9c672d52c"
  function_checksums:
    "IC-001 §1": "sha256:efcf19280fecc92fb9ae0ab3ccce93c8d372c0c74adba47c124e05c012c6c9f"
    "IC-004 §1": "sha256:38bf6333416923660329b225a98bd901c0a40ceacf5c2548f072879ffb4fdba"
    "IC-004 §2": "sha256:67d34bb0711429491359486f53d3f2da91198603f936636148edc7415f9fe7a"
    "IC-004 §3": "sha256:ecccd428b229e2252fd5c6d2d4936a65e4243b5f9cadeaf5ed1e28f274f68d3"
    "IC-004 §4": "sha256:e641b3548aac632cbc0993b7200d612f7b94642891a17396cfbcf56712f7b41"
    "IC-005 §1": "sha256:1a745552cd763a4ae908f207f84f0fd355c2c2bd9db71e878afab64277e3ac7"
    "IC-005 §2": "sha256:7951e17e78f08deda6f5e0ec45056b0192daa64d44d31bf7d4312667a9eb95b"
    "IC-005 §3": "sha256:e224e38061d8d34b974bcccb27be1b2665fd4a51f351bfb6ad0100ea2555596"
    "IC-005 §4": "sha256:80f5ca5241050d854534f72e608c9e3ba61252edc1769e56bc6e7cb881d17d9"
  behaviors:
    "1":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"  # resolve_index_units(path, recursive, depth) -> one unit: docs/example/
          - address: "IC-004 §2"  # resolve_documents_in_unit(unit) -> [guide.md]
          - address: "IC-001 §1"  # parse_markdown_structure(guide.md) -> ParsedStructure
          - address: "IC-004 §3"  # extract_words(structure) -> WordIndex
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started]) -> {} (nothing reserved)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
              - address: "IC-006 §1"  # reduce_words(document root text) -> [example, guide]
              - address: "IC-006 §1"  # reduce_words("Getting Started" text) -> [install, tool, run, "//todo" x6]
          - address: "IC-004 §4"  # extract_todos(guide.md) -> six TodoEntry, one per marker spelling
          - address: "IC-005 §1"  # write_index_files(...) -> all three files written
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started]) -> {} (second call, for sections.yaml's own zone field)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
          - address: "IC-005 §2"  # list_index_entries(unit) -> [guide.md entry]
          - address: "IC-005 §3"  # find_stale_entries(entries, documents) -> []
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "1.1":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"
          - address: "IC-004 §2"
          - address: "IC-001 §1"
          - address: "IC-004 §3"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
              - address: "IC-006 §1"
              - address: "IC-006 §1"
          - address: "IC-004 §4"
          - address: "IC-005 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
          - address: "IC-005 §2"
          - address: "IC-005 §3"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "1.2":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"
          - address: "IC-004 §2"
          - address: "IC-001 §1"
          - address: "IC-004 §3"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
              - address: "IC-006 §1"
              - address: "IC-006 §1"
          - address: "IC-004 §4"
          - address: "IC-005 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
          - address: "IC-005 §2"
          - address: "IC-005 §3"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "1.3":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"
          - address: "IC-004 §2"
          - address: "IC-001 §1"
          - address: "IC-004 §3"
            children:
              - address: "IC-001 §3"
              - address: "IC-006 §1"
          - address: "IC-004 §4"
          - address: "IC-005 §1"
            children:
              - address: "IC-001 §3"
          - address: "IC-005 §2"
          - address: "IC-005 §3"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "2":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"  # resolve_index_units(docs/guides/, recursive=true, depth=null) -> two units
          - address: "IC-004 §2"  # resolve_documents_in_unit(docs/guides/) -> [intro.md]
          - address: "IC-001 §1"  # parse_markdown_structure(intro.md)
          - address: "IC-004 §3"  # extract_words(intro.md structure)
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Overview]) -> {} (nothing reserved)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Overview") -> false
              - address: "IC-006 §1"  # reduce_words(intro.md root text) -> [getting, started]
              - address: "IC-006 §1"  # reduce_words("Overview" text) -> [read, guide, first]
          - address: "IC-004 §4"  # extract_todos(intro.md) -> []
          - address: "IC-005 §1"  # write_index_files(intro.md, ...) -> sections+words written
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Overview]) -> {} (second call, for sections.yaml's own zone field)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Overview") -> false
          - address: "IC-005 §2"  # list_index_entries(docs/guides/) -> [intro.md entry]
          - address: "IC-005 §3"  # find_stale_entries(...) -> []
          - address: "IC-004 §2"  # resolve_documents_in_unit(docs/guides/advanced/) -> [tips.md]
          - address: "IC-001 §1"  # parse_markdown_structure(tips.md)
          - address: "IC-004 §3"  # extract_words(tips.md structure)
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Performance]) -> {} (nothing reserved)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Performance") -> false
              - address: "IC-006 §1"  # reduce_words(tips.md root text) -> [advanced, tips]
              - address: "IC-006 §1"  # reduce_words("Performance" text) -> [tune, settings, speed]
          - address: "IC-004 §4"  # extract_todos(tips.md) -> []
          - address: "IC-005 §1"  # write_index_files(tips.md, ...) -> sections+words written
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Performance]) -> {} (second call, for sections.yaml's own zone field)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Performance") -> false
          - address: "IC-005 §2"  # list_index_entries(docs/guides/advanced/) -> [tips.md entry]
          - address: "IC-005 §3"  # find_stale_entries(...) -> []
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T13:55:54.000Z"
    "3":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"  # resolve_index_units(docs/example/, recursive=false, depth=null) -> one unit
          - address: "IC-004 §2"  # resolve_documents_in_unit(unit) -> [guide.md] (old.md no longer on disk)
          - address: "IC-001 §1"  # parse_markdown_structure(guide.md) -> one heading
          - address: "IC-004 §3"  # extract_words(structure) -> WordIndex
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started]) -> {} (nothing reserved)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
              - address: "IC-006 §1"  # reduce_words(document root text) -> [example, guide]
              - address: "IC-006 §1"  # reduce_words("Getting Started" text) -> [install, tool, run]
          - address: "IC-004 §4"  # extract_todos(guide.md) -> []
          - address: "IC-005 §1"  # write_index_files(guide.md, ...) -> sections+words written
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started]) -> {} (second call, for sections.yaml's own zone field)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
          - address: "IC-005 §2"  # list_index_entries(unit) -> [guide.md entry, old.md entry]
          - address: "IC-005 §3"  # find_stale_entries(...) -> [old.md entry only; guide.md's own entry survives]
          - address: "IC-005 §4"  # remove_index_entries(old.md entry) -> deletes old's three files, guide's own two untouched
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "4.1":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"
          - address: "IC-004 §2"
          - address: "IC-001 §1"
          - address: "IC-004 §3"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
              - address: "IC-006 §1"
              - address: "IC-006 §1"
          - address: "IC-004 §4"
          - address: "IC-005 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
          - address: "IC-005 §2"
          - address: "IC-005 §3"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "4.2":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"
          - address: "IC-004 §2"
          - address: "IC-001 §1"
          - address: "IC-004 §3"
            children:
              - address: "IC-001 §3"
              - address: "IC-006 §1"
          - address: "IC-004 §4"
          - address: "IC-005 §1"
            children:
              - address: "IC-001 §3"
          - address: "IC-005 §2"
          - address: "IC-005 §3"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "5.1":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"  # resolve_index_units(path, recursive, depth) -> one unit: docs/example/
          - address: "IC-004 §2"  # resolve_documents_in_unit(unit) -> [guide.md]
          - address: "IC-001 §1"  # parse_markdown_structure(guide.md) -> two headings
          - address: "IC-004 §3"  # extract_words(structure) -> WordIndex
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started, Appendix]) -> [Appendix's id]
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
                  - address: "IC-001 §2"  # is_reserved_section("Appendix") -> true, opens a zone (nothing nested to extend it here)
              - address: "IC-006 §1"  # reduce_words(document root text) -> [example, guide]
              - address: "IC-006 §1"  # reduce_words("Getting Started" text) -> [install, tool, run]
          - address: "IC-004 §4"  # extract_todos(guide.md) -> []
          - address: "IC-005 §1"  # write_index_files(...) -> sections (both headings) + words (body only) written
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started, Appendix]) -> [Appendix's id] (second call, for sections.yaml's own zone field)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
                  - address: "IC-001 §2"  # is_reserved_section("Appendix") -> true
          - address: "IC-005 §2"  # list_index_entries(unit) -> [guide.md entry]
          - address: "IC-005 §3"  # find_stale_entries(entries, documents) -> []
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "5.2":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"
          - address: "IC-004 §2"
          - address: "IC-001 §1"
          - address: "IC-004 §3"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
              - address: "IC-006 §1"
              - address: "IC-006 §1"
          - address: "IC-004 §4"
          - address: "IC-005 §1"
            children:
              - address: "IC-001 §3"
                children:
                  - address: "IC-001 §2"
                  - address: "IC-001 §2"
          - address: "IC-005 §2"
          - address: "IC-005 §3"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
    "5.3":
      call_tree:
        address: "IC-000 §2"
        children:
          - address: "IC-004 §1"  # resolve_index_units(path, recursive, depth) -> one unit: docs/example/
          - address: "IC-004 §2"  # resolve_documents_in_unit(unit) -> [guide.md]
          - address: "IC-001 §1"  # parse_markdown_structure(guide.md) -> three headings
          - address: "IC-004 §3"  # extract_words(structure) -> WordIndex
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started, Appendix, Config Reference]) -> [Appendix's id, Config Reference's id]
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
                  - address: "IC-001 §2"  # is_reserved_section("Appendix") -> true, opens a zone at depth 1
              - address: "IC-006 §1"  # reduce_words(document root text) -> [example, guide]
              - address: "IC-006 §1"  # reduce_words("Getting Started" text) -> [install, tool, run]
          - address: "IC-004 §4"  # extract_todos(guide.md) -> []
          - address: "IC-005 §1"  # write_index_files(...) -> sections (all three headings) + words (body only) written
            children:
              - address: "IC-001 §3"  # mark_protected_headings([Getting Started, Appendix, Config Reference]) -> [Appendix's id, Config Reference's id] (second call, for sections.yaml's own zone field)
                children:
                  - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
                  - address: "IC-001 §2"  # is_reserved_section("Appendix") -> true, opens a zone at depth 1
          - address: "IC-005 §2"  # list_index_entries(unit) -> [guide.md entry]
          - address: "IC-005 §3"  # find_stale_entries(entries, documents) -> []
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:28:45.000Z"
---
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

(§7.1 Mechanical Reconciliation — computed by hand, same basis as `SB-001`'s own note. Subset relationship:
already established deriving §1-§5.3 above. Side effects: N/A, no External Dependencies. Exceptions: swept —
this operation's own call graph raises nothing at all, every behavior here is a happy path.)

## 1 Happy Path

**Realizes:** happy path

**Given** a directory `docs/example/`, never previously indexed (no existing `.index/` entries), containing
exactly one document `docs/example/guide.md`:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

//TODO - add troubleshooting section (WVR-77)
//TO-DO - clarify install steps
//TO_DO - mention prerequisites
#TODO - add screenshots (WVR-80)
#TO-DO - link the FAQ
#to_do - note supported platforms
```
(deliberately exercising every recognized marker spelling in one fixture — `//`/`#` prefix, `TODO`/`TO-DO`/
`TO_DO` separator, case-insensitive, each one starting its own line)

**When** `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`)

**Then** `parse_markdown_structure` (`IC-001 §1`) is called on `guide.md` and returns one heading, `Getting
Started` (`pseudo_number: "1"`, `start_line: 6`, `end_line: 14`), no figures; `extract_words` (`IC-004 §3`) is
called with that structure and returns:
```yaml
document: {example: 1, guide: 1}
sections:
  "Getting Started": {install: 1, tool: 1, run: 1, "//todo": 6}
```
(`the`/`and`/`it` dropped as stopwords; each marker line's own description text stays excluded from indexed
prose per documentation-standards.md §4, but the marker pattern itself is canonicalized to one `"//todo"` token
per occurrence regardless of which of the six spellings was used — HLD §3.10 addendum, elicited directly from
the architect — so all six lines contribute to a single count of `6`); `extract_todos` (`IC-004 §4`)
is called on `guide.md` and returns:
```yaml
- {text: "add troubleshooting section (WVR-77)", section: "Getting Started", line: 9, ref: "WVR-77"}
- {text: "clarify install steps", section: "Getting Started", line: 10, ref: null}
- {text: "mention prerequisites", section: "Getting Started", line: 11, ref: null}
- {text: "add screenshots (WVR-80)", section: "Getting Started", line: 12, ref: "WVR-80"}
- {text: "link the FAQ", section: "Getting Started", line: 13, ref: null}
- {text: "note supported platforms", section: "Getting Started", line: 14, ref: null}
```
(all six recognized regardless of `//`/`#`, `TODO`/`TO-DO`/`TO_DO`, or case — the last one, `#to_do`, is
all-lowercase); `write_index_files` (`IC-005 §1`) is called with all four and writes
`docs/example/.index/guide.sections.yaml`, `guide.words.yaml`, and `guide.todo.yaml` (all three have content,
none omitted); `list_index_entries` (`IC-005 §2`) is called for the unit and returns the just-written `guide.md`
entry; `find_stale_entries` (`IC-005 §3`) is called with that entry against `documents:
["docs/example/guide.md"]` and returns `[]` (the document is still current, so nothing is stale — no
`remove_index_entries` call follows); the operation returns:
```yaml
indexed:
  - {document: "docs/example/guide.md", sections_written: true, words_written: true, todos_written: true}
removed: []
```

*(Flagging rather than silently deciding: this fixture's marker set — `TO_DO` as a third separator alongside
`todo`/`to-do`, and every marker required to start its own line — is drawn from the architect's own direct
correction, not from documentation-standards.md §4's currently-written text, which documents only `todo`/`to-do`
and says nothing about line position. That standards document itself likely needs a matching update; it isn't
something this design process edits directly, so it's noted here for the architect's own follow-up rather than
silently reconciled.)*

### 1.1 No TODO Markers At All

**Realizes:** happy path — Extension 5a

**Given** a directory `docs/example/`, never previously indexed, containing exactly one document
`docs/example/guide.md`:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it. Also see //TODO for details.
```
— the `//TODO`-looking text on line 7 is deliberately mid-line, not at line start, so the marker rule
(documentation-standards.md §4) excludes it; there is no genuine marker anywhere in this document

**When** — as §1, `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`)

**Then** `parse_markdown_structure` (`IC-001 §1`) returns the same one heading as §1 (`start_line: 6`,
`end_line: 7`); `extract_todos` (`IC-004 §4`) returns `[]` — the mid-line `//TODO` text never starts a line, so
nothing matches; `extract_words` (`IC-004 §3`) returns:
```yaml
document: {example: 1, guide: 1}
sections:
  "Getting Started": {install: 1, tool: 1, run: 1, "//todo": 1, details: 1}
```
(`the`/`and`/`it`/`also`/`see`/`for` dropped as stopwords; `reduce_words` recognizes the marker pattern itself
wherever it appears — line-start isn't a condition for this recognition, only for `extract_todos`'s own marker
list — so the mid-line `//TODO` still canonicalizes to one `"//todo"` token (HLD §3.10 addendum) even though it
isn't a genuine TODO marker for extraction purposes; `details` is the only other survivor of the surrounding
prose); `write_index_files` (`IC-005 §1`) is called and
writes `guide.sections.yaml` and `guide.words.yaml`, but **not** `guide.todo.yaml` — no TODO content justifies
one; `list_index_entries`/`find_stale_entries` behave as in §1 (no stale entries); the operation returns:
```yaml
indexed:
  - {document: "docs/example/guide.md", sections_written: true, words_written: true, todos_written: false}
removed: []
```

### 1.2 No Significant Words

**Realizes:** happy path

**Given** a directory `docs/example/`, never previously indexed, containing exactly one document
`docs/example/minimal.md`:
```
# The Of

## Context
* [Other Doc](other.md) - related

## 1 It Is
It is of the.
```
— deliberately no TODO markers of any spelling: per §3.10's addendum (§1.1 above), a marker's own canonical
`"//todo"` token would itself be a significant word, so a document with a marker can never actually reach a
truly empty `WordIndex` — this condition and Extension 5a's are coupled, not independent, once any marker is
present

**When** — as §1, `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`)

**Then** `parse_markdown_structure` (`IC-001 §1`) returns one heading, `It Is` (`start_line: 6`, `end_line: 7`);
`extract_todos` (`IC-004 §4`) returns `[]`; `extract_words` (`IC-004 §3`) returns:
```yaml
document: {}
sections:
  "It Is": {}
```
(the document's own title, `"The Of"`, and the section's own body text, `"It is of the."`, are both composed
entirely of stopwords — nothing survives anywhere in the document); `write_index_files` (`IC-005 §1`) is called
and writes only `docs/example/.index/minimal.sections.yaml` — the heading itself still justifies
`sections.yaml` — but **neither** `minimal.words.yaml` **nor** `minimal.todo.yaml`; `list_index_entries`/
`find_stale_entries` behave as in §1 (no stale entries); the operation returns:
```yaml
indexed:
  - {document: "docs/example/minimal.md", sections_written: true, words_written: false, todos_written: false}
removed: []
```

### 1.3 No Sections

**Realizes:** happy path

**Given** a directory `docs/example/`, never previously indexed, containing exactly one document
`docs/example/notes.md`:
```
# Install The Tool

Run the setup script and verify the install.

//TODO - add troubleshooting section (WVR-77)

## Context
* [Other Doc](other.md) - related
```
— all body content sits before `## Context`, in the document's own root/preamble; nothing follows `## Context`,
so there's no eligible heading anywhere

**When** — as §1, `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`)

**Then** `parse_markdown_structure` (`IC-001 §1`) returns `headings: []`, `figures: []`; `extract_todos`
(`IC-004 §4`) returns `[{text: "add troubleshooting section (WVR-77)", section: "Install The Tool", line: 5,
ref: "WVR-77"}]` (`section` is the document's own title, per documentation-standards.md §4, since the marker sits
before `## Context`); `extract_words` (`IC-004 §3`) returns:
```yaml
document: {install: 2, tool: 1, run: 1, setup: 1, script: 1, verify: 1, "//todo": 1}
sections: {}
```
(`the`/`and` dropped as stopwords; `install` appears twice — once in the title, once in the prose; the marker's
own canonical `"//todo"` token counts here too, at the document root, the same as it would inside any section);
`write_index_files` (`IC-005 §1`) is called and writes `docs/example/.index/notes.words.yaml` and
`notes.todo.yaml`, but **not** `notes.sections.yaml` — nothing structural justifies it; `list_index_entries`/
`find_stale_entries` behave as in §1 (no stale entries); the operation returns:
```yaml
indexed:
  - {document: "docs/example/notes.md", sections_written: false, words_written: true, todos_written: true}
removed: []
```

## 2 Recursive Across Multiple Units

**Realizes:** happy path

**Given** a directory tree, never previously indexed:
```
docs/guides/intro.md:
  # Getting Started

  ## Context
  * [Other Doc](other.md) - related

  ## 1 Overview
  Read this guide first.

docs/guides/advanced/tips.md:
  # Advanced Tips

  ## Context
  * [Other Doc](other.md) - related

  ## 1 Performance
  Tune the settings for speed.
```

**When** `index_path(path: "docs/guides/", recursive: true, depth: null)` is invoked (`IC-000 §2`)

**Then** `resolve_index_units` (`IC-004 §1`) is called once and returns two units — `{directory: "docs/guides/"}`
and `{directory: "docs/guides/advanced/"}` — one per directory encountered while recursing; everything from
`resolve_documents_in_unit` onward then runs once per unit, independently, each against only that unit's own
document:
* `docs/guides/` — `intro.md` parses to one heading, `Overview` (`start_line: 6`, `end_line: 7`); `extract_words`
  returns `document: {getting: 1, started: 1}`, `sections: {"Overview": {read: 1, guide: 1, first: 1}}`;
  `extract_todos` returns `[]`; `write_index_files` writes `docs/guides/.index/intro.sections.yaml` and
  `docs/guides/.index/intro.words.yaml` — this unit's own `.index/` subdirectory, not `intro.todo.yaml`;
  `list_index_entries`/`find_stale_entries` find nothing stale in this unit.
* `docs/guides/advanced/` — `tips.md` parses to one heading, `Performance` (`start_line: 6`, `end_line: 7`);
  `extract_words` returns `document: {advanced: 1, tips: 1}`, `sections: {"Performance": {tune: 1, settings: 1,
  speed: 1}}` (`the`/`for` dropped as stopwords); `extract_todos` returns `[]`; `write_index_files` writes
  `docs/guides/advanced/.index/tips.sections.yaml` and `docs/guides/advanced/.index/tips.words.yaml` — this
  unit's own, separate `.index/` subdirectory, not `tips.todo.yaml`; `list_index_entries`/`find_stale_entries`
  find nothing stale in this unit either — independently of `docs/guides/.index/`'s own entries, never merged
  with them.

The operation returns:
```yaml
indexed:
  - {document: "docs/guides/intro.md", sections_written: true, words_written: true, todos_written: false}
  - {document: "docs/guides/advanced/tips.md", sections_written: true, words_written: true, todos_written: false}
removed: []
```

## 3 Stale Entry Removal

**Realizes:** happy path

**Given** a directory `docs/example/` containing exactly one currently-existing document,
`docs/example/guide.md`:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.
```
alongside a full `.index/` entry surviving from an earlier run for a *different* document that's since been
deleted: `docs/example/.index/old.sections.yaml`, `docs/example/.index/old.words.yaml`, and
`docs/example/.index/old.todo.yaml`, all for `docs/example/old.md` — deliberately mixed, not an empty
directory, so this behavior proves removal is scoped to exactly the stale entry, leaving the current document's
own index files untouched

**When** `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`)

**Then** `resolve_index_units` (`IC-004 §1`) returns one unit, `{directory: "docs/example/"}`;
`resolve_documents_in_unit` (`IC-004 §2`) returns `["docs/example/guide.md"]` — `old.md` is absent, since it no
longer exists on disk; the per-document loop runs once, for `guide.md` only: `parse_markdown_structure` returns
one heading, `Getting Started` (`start_line: 6`, `end_line: 7`); `extract_words` returns `document: {example: 1,
guide: 1}`, `sections: {"Getting Started": {install: 1, tool: 1, run: 1}}`; `extract_todos` returns `[]`;
`write_index_files` writes `docs/example/.index/guide.sections.yaml` and `guide.words.yaml` (not
`guide.todo.yaml`); `list_index_entries` (`IC-005 §2`), called *after* that write, now sees both entries in
`.index/` — `guide.md`'s just-written one and `old.md`'s surviving one; `find_stale_entries` (`IC-005 §3`)
compares them against `documents: ["docs/example/guide.md"]` and finds only `old.md` absent — `guide.md`'s own
entry is *not* stale, even though it was just (re)written this same pass; `remove_index_entries` (`IC-005 §4`)
is called once, for `old.md`'s entry only, deleting its three files — `guide.sections.yaml`/`guide.words.yaml`
are left exactly as this same pass just wrote them, never touched by the removal step; the operation returns:
```yaml
indexed:
  - {document: "docs/example/guide.md", sections_written: true, words_written: true, todos_written: false}
removed:
  - {document: "docs/example/old.md"}
```

## 4 Re-Index After Partial Content Loss

**Given** a document previously indexed with all three of its `.index/` files present, re-indexed after an edit
removed some, but not all, of what justified them

*(Resolved while deriving §4.1: `write_index_files` actively deletes a file it previously wrote that a re-index
no longer justifies, not merely skips writing a new one — now stated directly on `write_index_files`'s own
`IC-005 §1` document, not just assumed here.)*

### 4.1 Lost The Last TODO

**Realizes:** happy path

**Given** — as §4: `docs/example/guide.md` was previously indexed while it read:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

//TODO - add troubleshooting section (WVR-77)
```
producing `docs/example/.index/guide.sections.yaml`, `guide.words.yaml` (including the marker's own canonical
`"//todo"` token), and `guide.todo.yaml` (one entry) — the document has since been edited to resolve that TODO,
now reading:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.
```

**When** `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`) — a
re-index, not a first index

**Then** `parse_markdown_structure` returns the same one heading, now shorter (`start_line: 6`, `end_line: 7`,
no trailing TODO line); `extract_todos` returns `[]`; `extract_words` returns `document: {example: 1, guide: 1}`,
`sections: {"Getting Started": {install: 1, tool: 1, run: 1}}` — no `"//todo"` token this time, since no marker
survives to canonicalize; `write_index_files` (`IC-005 §1`) (re)writes `guide.sections.yaml`/`guide.words.yaml`
with this content, and **deletes the existing `guide.todo.yaml`** — this is the assumption flagged at §4 above,
now the concrete claim this behavior stands or falls on: `write_index_files` must actively retract a file it
previously wrote that a re-index no longer justifies, not merely skip writing a new one, or `docs/example/
.index/guide.todo.yaml` would wrongly keep reporting a TODO that's already resolved; `list_index_entries`/
`find_stale_entries` still find `guide.md` itself current, so no whole-document removal happens — this is a
per-file retraction inside `write_index_files`, distinct from `remove_index_entries`' own whole-entry removal
(§3). The operation returns:
```yaml
indexed:
  - {document: "docs/example/guide.md", sections_written: true, words_written: true, todos_written: false}
removed: []
```

### 4.2 Lost The Last Heading

**Realizes:** happy path

**Given** — as §4: `docs/example/guide.md` was previously indexed while it read:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.
```
producing `docs/example/.index/guide.sections.yaml` (one heading) and `guide.words.yaml`, no `guide.todo.yaml`
(no TODO, then or now) — the document has since been edited to fold that heading's prose into the root, leaving
no heading anywhere:
```
# Example Guide
Install the tool and run it.

## Context
* [Other Doc](other.md) - related
```

**When** `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`) — a
re-index, not a first index

**Then** `parse_markdown_structure` returns `headings: []`, `figures: []`; `extract_todos` returns `[]`
(unaffected — there was no TODO before and there's none now); `extract_words` returns `document: {example: 1,
guide: 1, install: 1, tool: 1, run: 1}`, `sections: {}` — the former section's words are now part of the
document root's own count, since that text moved there; `write_index_files` (re)writes `guide.words.yaml` with
this content, leaves `guide.todo.yaml` alone (still absent), and **deletes the existing `guide.sections.yaml`**
— the same retraction contract §4.1 confirmed on `IC-005 §1`, applying here to a different file, not a new
assumption. The operation returns:
```yaml
indexed:
  - {document: "docs/example/guide.md", sections_written: false, words_written: true, todos_written: false}
removed: []
```

*(losing `.words.yaml` alone was considered and dropped per the architect's own call: a document with no
significant words left is realistically a document with no content at all, which wouldn't plausibly still
justify its other two files either — not a distinct condition worth its own behavior.)*

## 5 Document With Appendix Or Rationale

**Given** a document containing a `# Appendix` and/or `# Rationale` section, indexed — resolved via Candidate A
(HLD §3.1 addendum): `parse_markdown_structure` includes the heading like any other, and `extract_words`
(`IC-004 §3`) skips it — and anything nested under it — via `mark_protected_headings` (`IC-001 §3`, §3.1's own
second correction: a protected *zone*, not a single excluded heading) — so `.sections.yaml` still carries it
(UC-006 can still locate and return it on request)

### 5.1 Appendix Present

**Realizes:** happy path

**Given** a directory `docs/example/`, never previously indexed, containing exactly one document
`docs/example/guide.md`:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

# Appendix
Supplementary notes about advanced configuration options.
```

**When** — as §1, `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`)

**Then** `parse_markdown_structure` (`IC-001 §1`) returns two headings: `Getting Started` (`pseudo_number: "1"`,
`start_line: 6`, `end_line: 8`) and `Appendix` (`pseudo_number: null`, `start_line: 9`, `end_line: 10`);
`extract_todos` returns `[]`; `extract_words` (`IC-004 §3`) calls `mark_protected_headings` (`IC-001 §3`) once
with both headings, which walks them in order and returns `[Appendix's own id]` — `Getting Started`, at depth
`2`, comes before any protected heading opens a zone, so it's never marked; `Appendix`, at depth `1`, matches
`is_reserved_section` directly and opens one (there's nothing nested under it in this fixture — §5.3 below
covers a document whose Appendix has its own nested subsection). `extract_words` then returns:
```yaml
document: {example: 1, guide: 1}
sections:
  "Getting Started": {install: 1, tool: 1, run: 1}
```
— `Appendix` never gets a `sections` entry in `.words.yaml` at all: `extract_words` skips `reduce_words`
entirely for any marked heading, it isn't just filtered out afterward; `write_index_files` (`IC-005 §1`) writes
`docs/example/.index/guide.sections.yaml` with **both** headings — `Appendix` included, even though it's absent
from `guide.words.yaml` — and `guide.words.yaml`, not `guide.todo.yaml`. A later `extract_content` call (UC-006)
can still resolve `§Appendix` and return its content, via `sections.yaml`, even though a search (UC-005) would
never surface it. The operation returns:
```yaml
indexed:
  - {document: "docs/example/guide.md", sections_written: true, words_written: true, todos_written: false}
removed: []
```

### 5.2 Rationale Present

**Realizes:** happy path

**Given** — as §5.1, but `docs/example/guide.md` reads:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

# Rationale
Chosen for its simplicity over more complex alternatives considered earlier.
```
(a `# Rationale` section in place of `# Appendix`, same line positions — `start_line: 9`, `end_line: 10`)

**When** — as §5.1

**Then** — as §5.1, but the second heading's own title is `"Rationale"` instead of `"Appendix"` —
`is_reserved_section("Rationale")` also returns `true` (`IC-001 §2` checks both reserved names, not just one);
`sections.yaml` carries both `Getting Started` and `Rationale`; `words.yaml` is unchanged from §5.1
(`document: {example: 1, guide: 1}`, `sections: {"Getting Started": {install: 1, tool: 1, run: 1}}`) —
`Rationale` gets no `reduce_words` call either, the same exclusion as `Appendix`, regardless of which of the two
reserved names it is

### 5.3 Appendix With Its Own Subsection

**Realizes:** happy path

**Given** a directory `docs/example/`, never previously indexed, containing exactly one document
`docs/example/guide.md`:
```
# Example Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

# Appendix
Supplementary notes about advanced configuration options.

## 1 Config Reference
Detailed settings for advanced configuration options.
```
— the Appendix has its own nested subsection, `Config Reference`, whose own title isn't itself reserved

**When** — as §1, `index_path(path: "docs/example/", recursive: false, depth: null)` is invoked (`IC-000 §2`)

**Then** `parse_markdown_structure` returns three headings: `Getting Started` (depth `2`, `start_line: 6`,
`end_line: 8`), `Appendix` (depth `1`, `start_line: 9`, `end_line: 13`), and `Config Reference` (depth `2`,
`start_line: 12`, `end_line: 13`); `extract_words` calls `mark_protected_headings` once with all three —
walking in order: `Getting Started` (depth `2`) opens no zone; `Appendix` (depth `1`) matches
`is_reserved_section` and opens one at depth `1`; `Config Reference` (depth `2`, deeper than `1`) falls inside
that zone and is marked too — **without `mark_protected_headings` ever calling `is_reserved_section` on
`"Config Reference"` itself**, since once inside a zone every deeper heading is marked unconditionally.
`extract_words` returns:
```yaml
document: {example: 1, guide: 1}
sections:
  "Getting Started": {install: 1, tool: 1, run: 1}
```
— neither `Appendix` nor `Config Reference` gets a `.words.yaml` entry, proving the zone extends to genuine
nested substructure, not just the one heading that opens it; `write_index_files` writes
`docs/example/.index/guide.sections.yaml` with **all three** headings — `Config Reference` fully locatable and
extractable by its own title (`§Config Reference`), even though it's excluded from search — and
`guide.words.yaml`, not `guide.todo.yaml`. The operation returns:
```yaml
indexed:
  - {document: "docs/example/guide.md", sections_written: true, words_written: true, todos_written: false}
removed: []
```

(still only two `IC-006 §1` calls and two `IC-001 §2` calls — `mark_protected_headings` never calls
`is_reserved_section` for `Config Reference`, since it's already inside the zone `Appendix` opened)
