---
reconciliation:
  checked_at: "2026-08-19"
  uc_technical_interpretation_checksums:
    "UC-006": "sha256:c0f4aba52dff638e3658782c9c5ecb3822cf6c19c332f8628fd8661a11bb324"
  function_checksums:
    "IC-002 §1": "sha256:83e4d9d86620e5cd37f41e2a20fedb39ff58ee230ba6bd4b9faed046d53b980"
    "IC-008 §1": "sha256:8ab9ee07a58e7f5415cea8365f2a851c6f283a58ae69cbd7c30618b293cd0a0"
    "IC-008 §2": "sha256:57426b382d222a01df50e0288beabfbc6dc543547da79da9d1f8af31a96de3a"
    "IC-008 §3": "sha256:440d234fc05c26e7acfeeb2ca69fe0f889e866a9693c683bb998ed992f006e2"
    "IC-008 §4": "sha256:68708497ba9f6d627d0e390b2f02f631d11f248a51cf9ae90f625eccff98f59"
  behaviors:
    "1":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> {start_line: 1, end_line: 10}
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> two id-keyed entries
              - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
              - address: "IC-001 §2"  # is_reserved_section("Advanced Usage") -> false
          - address: "IC-008 §4"  # read_source_text(guide.md, {1, 10}) -> full verbatim text
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:42:35.000Z"
    "1.1":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:44:50.000Z"
    "1.2":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:46:51.000Z"
    "1.3":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:48:30.000Z"
    "1.4":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> {start_line: 6, end_line: 8}
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> two id-keyed entries
          - address: "IC-008 §4"  # read_source_text(guide.md, {6, 8}) -> "Getting Started"'s own text
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:50:22.000Z"
    "1.4.1":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:52:05.000Z"
    "1.4.2":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:53:36.000Z"
    "1.4.3":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:55:19.000Z"
    "1.4.3.1":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> raises invalid_range (start > end)
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:56:50.000Z"
    "1.4.3.2":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> resolves "1", then raises invalid_range
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> "Getting Started": {start_line: 6, end_line: 8}
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:58:25.000Z"
    "1.4.4":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> raises section_not_found (no "1.2.3")
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> four id-keyed entries, no "1.2.3" among them
          - address: "IC-008 §3"  # find_closest_section(reference, guide.md) -> "1.2" exists, returns Installation Steps
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> same four entries, checked for "1.2" this time
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:00:18.000Z"
    "1.4.5":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:02:25.000Z"
    "1.4.6":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:04:09.000Z"
    "1.4.7":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> raises ambiguous_section
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> four entries, two titled "Overview"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:05:52.000Z"
    "1.4.8":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> raises section_not_found (no "9.9")
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> two entries, neither numbered "9.9"
          - address: "IC-008 §3"  # find_closest_section(reference, guide.md) -> walks "9.9" -> "9", neither exists -> null
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> same two entries, neither numbered "9" either
          - address: "IC-008 §2"  # resolve_target_range(reference with section cleared, guide.md) -> whole-doc {1, 10}
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> checked for Appendix/Rationale exclusion, none found
              - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
              - address: "IC-001 §2"  # is_reserved_section("Advanced Usage") -> false
          - address: "IC-008 §4"  # read_source_text(guide.md, {1, 10}) -> full verbatim text
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:11:31.000Z"
    "1.4.9":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> {start_line: 12, end_line: 13}
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> entries include zone: "appendix" for Config Reference
              - address: "IC-001 §2"  # is_reserved_section("appendix") -> true, confirming the zone qualifier
          - address: "IC-008 §4"  # read_source_text(guide.md, {12, 13}) -> "Config Reference"'s own text
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:14:10.000Z"
    "1.5":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"
          - address: "IC-008 §1"
          - address: "IC-008 §2"
            children:
              - address: "IC-005 §6"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
          - address: "IC-008 §4"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:15:50.000Z"
    "1.5.1":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> raises invalid_range (start > end)
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:17:18.000Z"
    "1.5.2":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> ["docs/example/guide.md"]
          - address: "IC-008 §2"  # resolve_target_range(reference, guide.md) -> resolves real end, then raises invalid_range
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> three entries, including Appendix
              - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
              - address: "IC-001 §2"  # is_reserved_section("Advanced Usage") -> false
              - address: "IC-001 §2"  # is_reserved_section("Appendix") -> true, real end capped at 11
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:21:25.000Z"
    "2":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> [] (no match)
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:50:42.000Z"
    "3":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-008 §1"  # resolve_document(reference, scope) -> two matches
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:52:24.000Z"
    "4":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("@agent-plugins") -> no .weaver-docs.yaml found, raises weaver_docs_yaml_not_found
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:54:22.000Z"
    "5":
      call_tree:
        address: "IC-000 §4"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("@nonexistent-project") -> registry found, slug absent, raises unknown_scope_slug
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T15:55:59.000Z"
---
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
      IF closest IS NOT null:
        RETURN failure, closest
      whole_document_range <-- [IC-008 §2: resolve_target_range - reference WITH section CLEARED, document]
      content <-- [IC-008 §4: read_source_text - document, whole_document_range]
      RETURN content
    ON FAILURE (ambiguous_section):
      candidates <-- (returned directly by IC-008 §2)
      RETURN failure, candidates
    ON FAILURE (invalid_range):
      RAISE invalid_range
  content <-- [IC-008 §4: read_source_text - document, target_range]
  RETURN content
```
(revised this session, `IC-008 §3`'s own real mechanism found while deriving `SB-004 §1.4.4`/`§1.4.7`/§3.7's
own refinement: `find_closest_section` only ever finds an ancestor for a pseudo-number reference, walking its
dot-hierarchy — when even that's exhausted, there's no pointer left to return, so this falls all the way back
to the whole document instead of failing; `ambiguous_section` (§3.9's general-fix addendum) and `invalid_range`
(§3.7's own refinement) are `resolve_target_range`'s two other possible failures, both new since this bound
pseudocode was first written)

(§7.1 Mechanical Reconciliation — computed by hand, same basis as `SB-001`'s own note. Subset relationship:
already established deriving §1-§3 above. Side effects: N/A, no External Dependencies. Exceptions: swept —
`ambiguous_section`/`invalid_range` now declared on both `IC-008 §2` (origin) and `IC-000 §4` (its own caller,
added this pass); `section_not_found` is caught locally there, correctly not declared further.
`weaver_docs_yaml_not_found`/`unknown_scope_slug` — `IC-000 §4`'s own direct call to `resolve_scope_single` —
were flagged as exercised nowhere in this outline; closed by §4/§5 below, the direct parallels to `SB-003 §6`/
`§2.1`. Function checksums above are unchanged by that addition — `IC-002 §1`/`IC-008 §1`'s own pseudocode
didn't change, only new behaviors tracing through what was already bound.)

## 1 Whole Document, Exact Path

**Realizes:** happy path

**Given** a scope `docs/example/`, already indexed (UC-003), containing `docs/example/guide.md`:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.
```
— no Appendix or Rationale

**When** `extract_content(reference: {slug_or_path: "guide", section: null, line_range: null}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — no trailing `.md`, since it's always ignored (MSS step 2:
`"guide"`/`"guide.md"` are functionally identical, not just for wildcard slugs)

**Then** `resolve_scope_single` resolves `"docs/example/"` to `{roots: ["docs/example/"]}`; `resolve_document`
resolves `"guide"` against `docs/example/guide.md` on disk (the trailing `.md` a real file always has is never
part of the comparison) and finds exactly one match, `"docs/example/guide.md"`; `resolve_target_range` — no
`§section` given — reads
`guide.md`'s own `sections.yaml` (`IC-005 §6`) to find the whole-document boundary: two entries, `"Getting
Started"` and `"Advanced Usage"`, neither matching `is_reserved_section` (`IC-001 §2`), so nothing is excluded
and the range is the entire file, `{start_line: 1, end_line: 10}`; `read_source_text` reads and returns that
range verbatim:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.
```
the operation returns this content directly

### 1.1 Wildcard Match

**Realizes:** happy path

**Given** a scope `docs/example/`, already indexed, containing `docs/example/guides/install-guide.md` — nested
one level down, in a subdirectory the caller doesn't name — with the same content as §1's `guide.md`:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.
```

**When** `extract_content(reference: {slug_or_path: "**install-guide", section: null, line_range: null},
scope_hint: "docs/example/")` is invoked (`IC-000 §4`) — a wildcard slug, trailing `.md` not given, with no
`guides/` in the reference at all

**Then** `resolve_scope_single` resolves the scope as in §1; `resolve_document` matches the `**install-guide`
wildcard against every document under scope, recursively — finding it nested inside `guides/` without the
caller ever naming that subdirectory — and returns exactly one match, `"docs/example/guides/install-guide.md"`;
everything from `resolve_target_range` onward is identical to §1's own logic, run against this document instead,
returning the same whole-document content

### 1.2 Document Has An Appendix

**Realizes:** happy path

**Given** — as §1, but `docs/example/guide.md` also has an Appendix:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.

# Appendix
Supplementary notes about advanced configuration options.
```

**When** — as §1, `extract_content(reference: {slug_or_path: "guide", section: null, line_range: null},
scope_hint: "docs/example/")` is invoked (`IC-000 §4`)

**Then** — as §1 through `resolve_document`; `resolve_target_range` reads `sections.yaml` and finds three
entries this time — `"Getting Started"`, `"Advanced Usage"`, `"Appendix"` — checking each against
`is_reserved_section`: the first two return `false`, `"Appendix"` returns `true`, so the whole-document range
stops right before it: `{start_line: 1, end_line: 11}`; `read_source_text` reads and returns just that:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.

```
the Appendix's own two lines (`12`-`13`) are never read — proving "report `my-stuff` returns the whole doc,
without appendix or rationale"

### 1.3 Document Has A Rationale

**Realizes:** happy path

**Given** — as §1.2, but `docs/example/guide.md` reads:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.

# Rationale
Chosen for its simplicity over more complex alternatives considered earlier.
```
(a `# Rationale` in place of `# Appendix`, same line positions — `start_line: 12`, `end_line: 13`)

**When** — as §1.2

**Then** — as §1.2, but `is_reserved_section("Rationale")` is what returns `true` this time instead of
`"Appendix"` — otherwise identical: `{start_line: 1, end_line: 11}`, the same returned content, the Rationale's
own two lines never read

### 1.4 Section By Number

**Realizes:** happy path

**Given** — as §1, the same scope and `guide.md` (`"Getting Started"` numbered `1`, `"Advanced Usage"` numbered
`2`, no Appendix/Rationale)

**When** `extract_content(reference: {slug_or_path: "guide", section: "1", line_range: null}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`)

**Then** — as §1 through `resolve_document`; `resolve_target_range` sees `reference.section` is `"1"`, a valid
pseudo-number, so it resolves by number rather than title — reads `sections.yaml` and finds the entry whose own
`number` field equals `"1"` (`"Getting Started"`, `start_line: 6`, `end_line: 8`) — no ambiguity possible, since
`compute_numbering` never assigns the same number twice; `read_source_text` reads and returns just that range:
```
## 1 Getting Started
Install the tool and run it.

```

#### 1.4.1 Section Is Appendix

**Realizes:** happy path

**Given** — as §1.2, the same `guide.md` with its Appendix (`start_line: 12`, `end_line: 13`)

**When** `extract_content(reference: {slug_or_path: "guide", section: "aPpeNdix", line_range: null}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — deliberately mixed-case, to exercise case-insensitive title
matching (HLD §3.9's general-fix addendum)

**Then** — as §1.4 through `resolve_document`; `resolve_target_range` sees `"aPpeNdix"` isn't a valid
pseudo-number, so it resolves by title instead, case-insensitively — exactly one entry matches, the Appendix
itself (whose own stored title is `"Appendix"`, not the reference's own casing) — resolving to
`{start_line: 12, end_line: 13}`; `read_source_text` reads and returns:
```
# Appendix
Supplementary notes about advanced configuration options.
```
succeeding despite this same content being excluded from §1.2's own whole-document extraction, and never
surfacing in search (`SB-003`) — the direct proof of "report `my-stuff§appendix` returns the whole appendix"

#### 1.4.2 Section Is Rationale

**Realizes:** happy path

**Given** — as §1.3, the same `guide.md` with its Rationale (`start_line: 12`, `end_line: 13`)

**When** `extract_content(reference: {slug_or_path: "guide", section: "rationale", line_range: null},
scope_hint: "docs/example/")` is invoked (`IC-000 §4`)

**Then** — as §1.4.1, but resolving `"rationale"` (lowercase) against the Rationale's own stored title
`"Rationale"`, case-insensitively — one match, `{start_line: 12, end_line: 13}`; `read_source_text` returns:
```
# Rationale
Chosen for its simplicity over more complex alternatives considered earlier.
```

#### 1.4.3 Range Within A Section

**Realizes:** happy path

**Given** — as §1.4, the same `guide.md` (`"Getting Started"` spans `start_line: 6`, `end_line: 8`)

**When** `extract_content(reference: {slug_or_path: "guide", section: "1", line_range: [7, 7]}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`)

**Then** — as §1.4 through resolving `"1"` to `"Getting Started"`'s own bounds (`{start_line: 6, end_line: 8}`);
`reference.line_range` (`[7, 7]`) is then applied *within* that section's own bounds — fully inside them, no
clamping needed — resolving to `{start_line: 7, end_line: 7}`; `read_source_text` reads and returns just:
```
Install the tool and run it.
```
— the section's own heading line (`6`) and trailing blank (`8`) both excluded, only the requested single line
returned

##### 1.4.3.1 Start After End

**Realizes:** unhappy path — malformed range

**Given** — as §1.4.3, the same `guide.md`

**When** `extract_content(reference: {slug_or_path: "guide", section: "1", line_range: [8, 7]}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — `start` (`8`) after `end` (`7`)

**Then** `resolve_scope_single`/`resolve_document` run as in §1.4.3, resolving `guide.md`; `resolve_target_range`
validates `reference.line_range` before resolving the section at all — `start > end` is malformed regardless of
what any section's own bounds turn out to be, so there's nothing to gain by reading `sections.yaml` first — and
raises `invalid_range`, uncaught, straight out of `extract_content`. `read_source_text` never runs.

##### 1.4.3.2 Start Past The Section's Own End

**Realizes:** unhappy path — no valid overlap

**Given** — as §1.4.3, the same `guide.md` (`"Getting Started"` spans `start_line: 6`, `end_line: 8`)

**When** `extract_content(reference: {slug_or_path: "guide", section: "1", line_range: [9, 9]}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — `start`/`end` are both `9`, internally well-formed, but `9` is
already past the section's own last line, `8`

**Then** `resolve_scope_single`/`resolve_document` run as before; `resolve_target_range`'s own `start <= end`
check passes (`9 <= 9`), so it proceeds to resolve `"1"` against `sections.yaml` (`IC-005 §6`) — `"Getting
Started"`, `{start_line: 6, end_line: 8}` — then finds `reference.line_range`'s own `start` (`9`) is already
past that section's `end_line` (`8`): no valid overlap at all, unlike `[7-10]`'s partial overlap which §3.7
would clamp — raises `invalid_range`, uncaught. `read_source_text` never runs.

#### 1.4.4 Section Not Found

**Realizes:** unhappy path — Extension 3a

**Given** a scope `docs/example/`, already indexed, containing `docs/example/guide.md`:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

### 1.1 Prerequisites
Node 18 or later.

### 1.2 Installation Steps
Run the installer script.

## 2 Advanced Usage
Configure the advanced settings as needed.
```
— `"1.2 Installation Steps"` exists as a real subsection; `"1.2.3"` doesn't

**When** `extract_content(reference: {slug_or_path: "guide", section: "1.2.3", line_range: null}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`)

**Then** `resolve_scope_single`/`resolve_document` run as before; `resolve_target_range` sees `"1.2.3"` is a
valid pseudo-number, but no `sections.yaml` entry's `number` equals it — raises `section_not_found`; `IC-000
§4`'s own `ON FAILURE` handler catches it and calls `find_closest_section`, which walks the reference's own
dot-hierarchy upward — not fuzzy title matching — stripping the last segment (`"1.2.3"` → `"1.2"`) and checking
whether *that* number exists: it does, `"1.2 Installation Steps"` (`start_line: 12`, `end_line: 14`) — so that's
the closest match returned, one level up, not a guess based on how similar any title looks; the operation
returns `failure, closest` — not a bare error, a usable pointer the caller can retry with

#### 1.4.5 Subsection Nested Inside Appendix

**Realizes:** happy path

**Given** a scope `docs/example/`, already indexed, containing `docs/example/guide.md`:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

# Appendix
Supplementary notes about advanced configuration options.

## 1 Config Reference
Detailed settings for advanced configuration options.
```
— the same shape `SB-002 §5.3` derives: an Appendix with its own nested, non-reserved-titled subsection

**When** `extract_content(reference: {slug_or_path: "guide", section: "Config Reference", line_range: null},
scope_hint: "docs/example/")` is invoked (`IC-000 §4`)

**Then** `resolve_document` finds `guide.md`; `resolve_target_range` sees `"Config Reference"` isn't a valid
pseudo-number, resolves by title instead — exactly one entry matches, since `"Config Reference"` was never
excluded from `sections.yaml` in the first place (only from `.words.yaml`, per `SB-002 §5.3`'s own protected
zone) — resolving to `{start_line: 12, end_line: 13}`; `read_source_text` reads and returns:
```
## 1 Config Reference
Detailed settings for advanced configuration options.
```
succeeding normally — no exclusion applies here at all, unlike §1.4.1's `§Appendix` itself, since
`is_reserved_section("Config Reference")` was never true to begin with; this section simply never surfaces in
search (`SB-003`), which is a completely separate mechanism from extraction

#### 1.4.6 Subsection Nested Inside Rationale

**Realizes:** happy path

**Given** — as §1.4.5, but `docs/example/guide.md` reads:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

# Rationale
Chosen for its simplicity over more complex alternatives considered earlier.

## 1 Alternatives Considered
A plain filesystem scan was discarded as too slow at scale.
```
(a `# Rationale` in place of `# Appendix`, its own nested subsection titled `"Alternatives Considered"` instead
of `"Config Reference"`, same line positions — `start_line: 12`, `end_line: 13`)

**When** `extract_content(reference: {slug_or_path: "guide", section: "Alternatives Considered", line_range:
null}, scope_hint: "docs/example/")` is invoked (`IC-000 §4`)

**Then** — as §1.4.5, resolving by title to `{start_line: 12, end_line: 13}`; `read_source_text` returns:
```
## 1 Alternatives Considered
A plain filesystem scan was discarded as too slow at scale.
```

#### 1.4.7 Ambiguous Section Title

**Realizes:** unhappy path — ambiguous reference

**Given** a scope `docs/example/`, already indexed, containing `docs/example/guide.md`:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

### 1.1 Overview
A brief summary of the setup process.

## 2 Advanced Usage
Configure the advanced settings as needed.

### 2.1 Overview
A brief summary of advanced configuration.
```
— two genuinely different subsections, `"1.1"` and `"2.1"`, both titled `"Overview"` — representable without
collision now that `.sections.yaml` is `id`-keyed (HLD §3.9's general-fix addendum)

**When** `extract_content(reference: {slug_or_path: "guide", section: "Overview", line_range: null}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`)

**Then** `resolve_document` finds `guide.md`; `resolve_target_range` sees `"Overview"` isn't a valid
pseudo-number and isn't zone-qualified either, so it resolves by title — and finds *two* entries matching,
`"1.1"` and `"2.1"` — raising `ambiguous_section` instead of picking one; the operation returns `failure,
candidates`:
```yaml
- {title: "Overview", number: "1.1"}
- {title: "Overview", number: "2.1"}
```
so the caller can retry with either candidate's own `number` to disambiguate

#### 1.4.8 Number Not Found, No Ancestor Either

**Realizes:** happy path — falls back to the whole document

**Given** — as §1, the same scope and `guide.md` (`"Getting Started"` numbered `1`, `"Advanced Usage"` numbered
`2`, no Appendix/Rationale)

**When** `extract_content(reference: {slug_or_path: "guide", section: "9.9", line_range: null}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — neither `"9.9"` nor its own parent, `"9"`, exists anywhere in the
document

**Then** `resolve_document` finds `guide.md` as before; `resolve_target_range` finds no entry numbered `"9.9"` —
raises `section_not_found`; `find_closest_section` walks the hierarchy — `"9.9"` → `"9"` — and finds neither
exists either, exhausting every segment, so it returns nothing (`null`); since there's no ancestor pointer left
to return, `extract_content` doesn't fail at all — it calls `resolve_target_range` again, this time with
`reference.section` cleared, resolving the same whole-document range §1 itself computes (`{start_line: 1,
end_line: 10}`, nothing to exclude since there's no Appendix/Rationale here); `read_source_text` reads and
returns that, the operation succeeding with the whole document rather than failing:
```
# Install Guide

## Context
* [Other Doc](other.md) - related

## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.
```

#### 1.4.9 Zone-Qualified Section Number

**Realizes:** happy path

**Given** — as §1.4.5, the same `guide.md` — deliberately, `"Getting Started"` (body) and `"Config Reference"`
(inside the Appendix) are *both* numbered `"1"`, since the Appendix's own numbering is never coordinated with
the body's (HLD §3.1's second addendum)

**When** `extract_content(reference: {slug_or_path: "guide", section: "appendix.1", line_range: null},
scope_hint: "docs/example/")` is invoked (`IC-000 §4`)

**Then** `resolve_target_range` sees `"appendix.1"` is zone-qualified — splits on the first `.`, checks
`"appendix"` against `is_reserved_section` (matches), and resolves the remainder, `"1"`, scoped to only the
entries whose own `zone` field is `"appendix"` — finding `"Config Reference"` (`start_line: 12`, `end_line:
13`), *not* `"Getting Started"`, even though both are literally numbered `"1"`; `read_source_text` reads and
returns:
```
## 1 Config Reference
Detailed settings for advanced configuration options.
```
(a bare, unqualified `§1` — as §1.4 already derived — only ever matches `zone: null` entries, so it resolves to
`"Getting Started"` and never this one; the two numbering scopes coexist without either becoming ambiguous)

### 1.5 Document-Level Range

**Realizes:** happy path

**Given** — as §1, the same scope and `guide.md` (`10` lines total, no Appendix/Rationale)

**When** `extract_content(reference: {slug_or_path: "guide", section: null, line_range: [6, 20]}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — deliberately requesting past the document's own last line (`10`)

**Then** — as §1 through `resolve_document`; `resolve_target_range` — no `§section` given, but `line_range` is —
first computes the document's own real end the same way §1 does (checking for Appendix/Rationale, finding
none, so it's the physical end of file, `10`), then applies `reference.line_range` against it: `start` (`6`) is
within bounds, `end` (`20`) runs past them — a genuine partial overlap, so it's clamped rather than rejected
(§3.7), resolving to `{start_line: 6, end_line: 10}`; `read_source_text` reads and returns:
```
## 1 Getting Started
Install the tool and run it.

## 2 Advanced Usage
Configure the advanced settings as needed.
```

#### 1.5.1 Start After End

**Realizes:** unhappy path — malformed range

**Given** — as §1.5, the same `guide.md`

**When** `extract_content(reference: {slug_or_path: "guide", section: null, line_range: [20, 6]}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — `start` (`20`) after `end` (`6`)

**Then** `resolve_scope_single`/`resolve_document` run as before; `resolve_target_range` validates
`reference.line_range` before computing the document's own real end at all — `start > end` is malformed
regardless of where that boundary turns out to be — and raises `invalid_range`, uncaught. `read_source_text`
never runs.

#### 1.5.2 Start Past The Document's Own Real End

**Realizes:** unhappy path — no valid overlap

**Given** — as §1.2, the same `guide.md` with its Appendix (real end `11`, physical end of file `13`)

**When** `extract_content(reference: {slug_or_path: "guide", section: null, line_range: [12, 12]}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`) — `start`/`end` both `12`, internally well-formed, and line `12`
genuinely exists in the file (it's the Appendix's own heading line) — but past the document's own *real* end

**Then** `resolve_scope_single`/`resolve_document` run as before; `resolve_target_range`'s own `start <= end`
check passes (`12 <= 12`); it computes the document's own real end the same way §1.2 does — reads
`sections.yaml`, finds `"Appendix"` via `is_reserved_section`, real end `11` — then finds `reference.line_range`'s
own `start` (`12`) is already past that boundary: no valid overlap, even though line `12` physically exists in
the file (it's the Appendix's own content) — raises `invalid_range` rather than clamping to nothing.
`read_source_text` never runs.

## 2 Wildcard Matches Nothing

**Realizes:** happy path — Extension 2a

**Given** a scope `docs/example/`, already indexed, containing only `docs/example/guide.md` — nothing matching
a `"nonexistent"` slug anywhere

**When** `extract_content(reference: {slug_or_path: "**nonexistent", section: null, line_range: null},
scope_hint: "docs/example/")` is invoked (`IC-000 §4`)

**Then** `resolve_scope_single` resolves the scope as usual; `resolve_document` searches for the `**nonexistent`
wildcard and finds no matches at all — `[]`; the operation returns `empty_result` directly — a success, not an
error (Extension 2a) — `resolve_target_range`/`read_source_text` never run

## 3 Wildcard Matches More Than One

**Realizes:** unhappy path — Extension 2b

**Given** a scope `docs/example/`, already indexed, containing two documents whose slugs both match a
`"guide"` wildcard: `docs/example/install-guide.md` and `docs/example/user-guide.md`

**When** `extract_content(reference: {slug_or_path: "**guide", section: null, line_range: null}, scope_hint:
"docs/example/")` is invoked (`IC-000 §4`)

**Then** `resolve_scope_single` resolves the scope as usual; `resolve_document` finds *two* documents matching
`**guide` — `["docs/example/install-guide.md", "docs/example/user-guide.md"]`; the operation fails, returning
the candidate list directly (Extension 2b) so the caller can retry with an exact path; `resolve_target_range`/
`read_source_text` never run

## 4 Scope Resolution Fails, No Registry Found

**Realizes:** unhappy path — the gap flagged in §7.1's own reconciliation

**Given** cwd `/tmp/scratch/some/deep/path/`, with no `.weaver-docs.yaml` anywhere from there up to filesystem
root — the same fixture `SB-003 §6` uses

**When** `extract_content(reference: {slug_or_path: "guide", section: null, line_range: null}, scope_hint:
"@agent-plugins")` is invoked (`IC-000 §4`)

**Then** `resolve_scope_single` walks up through every parent directory to filesystem root without ever finding
a `.weaver-docs.yaml`; it raises `weaver_docs_yaml_not_found`, uncaught, straight out of `extract_content` — the
same failure `SB-003 §6` derives for search, now confirmed to propagate through `IC-000 §4` too, not just
`IC-000 §3`. `resolve_document`/`resolve_target_range`/`read_source_text` never run.

## 5 Scope Resolution Fails, Slug Not In Registry

**Realizes:** unhappy path — the gap flagged in §7.1's own reconciliation

**Given** cwd `/workspace/AgentPlugins/agent-plugins-docs/notes/`, registry at `/workspace/.weaver-docs.yaml`
(entries `agent-plugins`, `docs`) — the same fixture `SB-003 §2.1` uses

**When** `extract_content(reference: {slug_or_path: "guide", section: null, line_range: null}, scope_hint:
"@nonexistent-project")` is invoked (`IC-000 §4`)

**Then** `resolve_scope_single` walks up and finds `/workspace/.weaver-docs.yaml`, exactly as in `SB-003 §2`'s
own success case — the registry lookup itself succeeds — but `"nonexistent-project"` isn't one of its entries;
it raises `unknown_scope_slug`, uncaught, straight out of `extract_content`. `resolve_document`/
`resolve_target_range`/`read_source_text` never run.
