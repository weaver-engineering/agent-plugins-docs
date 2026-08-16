# Doc Search & Retrieval — High-Level Design

## Context
* [WVR-95](https://linear.app/weaver-engineering/issue/WVR-95) - the Feature this design realizes
* [UC-002 — Auto-Number Document Sections](../../analysis/use-cases/UC-002-auto-number-document-sections.md) - realized by this design
* [UC-003 — Index A Path](../../analysis/use-cases/UC-003-index-a-path.md) - realized by this design
* [UC-005 — Search Documentation](../../analysis/use-cases/UC-005-search-documentation.md) - realized by this design
* [UC-006 — Extract Document Content](../../analysis/use-cases/UC-006-extract-document-content.md) - realized by this design
* [Architecture Definition Document](../../architecture/architecture-definition-document.md) - §1 names this an MCP server (default for tools, not the bare-delivery exception), §4 names this Feature as the worked exemplar for the analysis/design/catalog document boundary
* Design Directory And HLD (@docs/workflows/feature-workflow/design-directory-and-hld.md) - the convention this document follows

## 1 Scope

This design covers the Doc Search & Retrieval MCP server: the four documentation tools already analysed as
standalone use cases —
[UC-002](../../analysis/use-cases/UC-002-auto-number-document-sections.md) (auto-numbering),
[UC-003](../../analysis/use-cases/UC-003-index-a-path.md) (indexing),
[UC-005](../../analysis/use-cases/UC-005-search-documentation.md) (search), and
[UC-006](../../analysis/use-cases/UC-006-extract-document-content.md) (extraction) — bundled and hosted
together as one MCP server rather than shipped as four bare tools, per the Architecture Definition Document's
§1 default-to-MCP model.

It explicitly excludes: why these four capabilities exist and what each does (already-written analysis, linked
above, immutable once its Technical Interpretation is derived below — not re-opened by this design); the
capability catalog entry itself (`docs/architecture/capability-catalog.md`, already present, not duplicated
here); and the mechanics of achieving parity between Claude Code and OpenCode for any given capability
(`docs/design/cross-platform-capability-parity.md`, WVR-94, a separate placeholder document this design does
not resolve).

## 2 Solution Overview

*(Not yet populated — depends on Solution Shape (Design Feature Instructions §2.3 / §4), which decides which of
§5's new candidates actually earn a standing Internal Component document versus staying Chunk-private, per
Design Directory And HLD §4.3. Gap Analysis (§3, below) is done; this section fills in once Ideation has run.)*

## 3 Key Decisions

### 3.1 `parse_markdown_structure` Interface

UC-002's and UC-003's parsing needs are met by a single shared component, `parse_markdown_structure(document)`,
returning every field either caller could want in one call — headings, figures, pseudo-numbers, references, and
start/end lines. UC-002 (`auto_number_document`) reads `pseudo_numbers` and `references`; UC-003
(`index_path`)'s `parse_structure` step reads `start_end_lines`. Neither caller narrows the interface to only
its own fields.

### 3.2 Delivery Surface: CLI Now, MCP Later

This Feature ships as a command-line tool now, not an MCP tool — the ADD's own MCP-hosting default (§1) is
about how this capability is eventually *published*, not something this design phase builds today. Every
operation's core logic (each `IC-000` function below) is written as a plain, directly-testable function; the
CLI is a thin argument-parsing wrapper around it, the same relationship an MCP tool wrapper would have if one
gets built later. Nothing about this design commits to CLI-specific concerns (argv parsing, exit codes) leaking
into the core functions themselves. This resolves the "MCP vs CLI" half of UC-002/003/005/006's own §7 Open
Design Questions; each use case's *specific* flag/format questions are still open, and get their own subsection
here as each is decided.

### 3.3 `resolve_scope` Interface

Split into two functions rather than one. `resolve_scope_single(specifier)` resolves exactly one scope
(`@{slug}`, `@docs`, `@all`, or a filesystem path) and is what both UC-005 and UC-006 call. `resolve_chained_scope(specifiers)`
— UC-005 only — calls `resolve_scope_single` once per specifier and combines the results; UC-006 has no path to
it at all, so its own scope exclusion (no `@{slug}@{slug}` chaining) is enforced by which function exists for
it to call, not left to caller discipline.

### 3.4 Filesystem Is Not An External Dependency

Confirmed as reasoned in §6: every file-touching function (`read_source_text`, `write_index_files`,
`parse_markdown_structure`, `list_index_entries`, `remove_index_entries`) is an ordinary Internal Component
doing in-process I/O against files this project itself manages — not a formal External Dependency. No `ED-NNN`
document exists or is needed for the filesystem.

*(Still open: each use case's own specific §7 Open Design Question — UC-002's exit codes/report format,
UC-003's path/recurse/depth flag syntax, UC-005's algorithm-selection syntax and N/X defaults, UC-006's
out-of-bounds line range behavior — none decided yet.)*

## 4 Data Types

*(Not yet populated — depends on the Internal Component interfaces §3/§5 decide.)*

## 5 Internal Components

Gap Analysis (Design Feature Instructions §3) result: `docs/architecture/components/` has no existing entries
for this project (confirmed directly, not assumed), so every candidate function the four Technical
Interpretations collectively name classifies **new** — there is nothing existing to compare any of them
against. This is the inventory Gap Analysis produces; which of these actually earn a standing `IC-NNN` document
versus staying Chunk-private (Design Directory And HLD §4.3) is Solution Shape's decision (§2.3/§4), not yet
made here.

* `resolve_scope_single`, `resolve_chained_scope` — **new** — decided (§3.3) as a split interface: both UC-005
  and UC-006 call `resolve_scope_single`; only UC-005 also calls `resolve_chained_scope`, which itself calls
  `resolve_scope_single` per specifier. Supersedes the single `resolve_scope` candidate Gap Analysis originally
  surfaced.
* `parse_markdown_structure` — **new** — decided (§3.1) as one shared component satisfying both UC-002's and
  UC-003's parsing needs, superseding the separately-named `parse_document`/`parse_structure` candidates Gap
  Analysis originally surfaced.
* `compute_numbering`, `build_id_map`, `find_surviving_references`, `rewrite_headings`, `rewrite_references`,
  `format_report` — **new** (UC-002).
* `resolve_documents`, `extract_words`, `extract_todos`, `write_index_files`, `list_index_entries`,
  `find_stale_entries`, `remove_index_entries` — **new** (UC-003).
* `load_word_index`, `score_nodes`, `select_top_n`, `preview_content` — **new** (UC-005).
* `resolve_document`, `resolve_target_range`, `find_closest_section`, `read_source_text` — **new** (UC-006).

## 6 External Dependencies

None identified — confirmed as Key Decision §3.4. Every candidate in §5 that touches the filesystem
(`read_source_text`, `write_index_files`, `parse_markdown_structure`, `list_index_entries`,
`remove_index_entries`) does so against files this same project owns and manages, in-process — not a separate
real system whose behavior can only be observed by calling it (Design Directory And HLD §3's own bar: "a
network boundary, real time, real randomness, another team's own data"). A unit test can exercise these against
a temp directory without needing anything external.

## 7 Specific Behaviors

* [SB-001 — Auto-Number A Document](specific-behaviors/SB-001-auto-number-document.md) - realizes [UC-002](../../analysis/use-cases/UC-002-auto-number-document-sections.md) (stub — behaviors not yet derived)
* [SB-002 — Index A Path](specific-behaviors/SB-002-index-a-path.md) - realizes [UC-003](../../analysis/use-cases/UC-003-index-a-path.md) (stub — behaviors not yet derived)
* [SB-003 — Search Documentation](specific-behaviors/SB-003-search-documentation.md) - realizes [UC-005](../../analysis/use-cases/UC-005-search-documentation.md) (stub — behaviors not yet derived)
* [SB-004 — Extract Document Content](specific-behaviors/SB-004-extract-document-content.md) - realizes [UC-006](../../analysis/use-cases/UC-006-extract-document-content.md) (stub — behaviors not yet derived)

*(All four use cases in scope now have a Technical Interpretation and an identified operation, Gap Analysis is
done, and Phase 3 Ideation (§3) is under way — three gaps resolved (§3.1-§3.4), each use case's own specific
§7 Open Design Question still open. Ideation remains a named human-judgement point (§4.1); each remaining gap
gets presented to the architect in turn, not resolved unilaterally.)*

## 8 Technology Stack

*(Not yet populated — inherits from the workspace's own established convention for this kind of tool
(`agent-plugins/packages/<name>`: pnpm workspace package, TypeScript ESM, `tsc`, Vitest — per
`weaver-engineering docs-standards-adopted` precedent) unless Key Decisions (§3) find a reason to diverge; not
asserted as decided until §3 actually says so.)*

# Rationale

**§3.1 `parse_markdown_structure` interface.** Two other candidates were considered and discarded:

* *Two separate, single-purpose parsers* (`parse_document` for UC-002, `parse_structure` for UC-003, each
  independently walking the document). Discarded: both need the exact same underlying walk — find headings,
  detect figures, per the documentation standard's own rules — so this duplicates that walk in two places that
  would have to change in lockstep every time the standard's own heading/figure rules do, for no interface
  benefit over a single call.
* *Shared low-level AST walk, separate per-caller shaping* (`parse_markdown_ast` plus two thin callers reshaping
  its output). Discarded in favor of the simpler one-call option: with only two callers today, and both wanting
  a strict subset of the same fields rather than needing genuinely different *shapes* of the same data, the
  extra component this candidate adds doesn't earn its keep yet — reconsider if a third caller's needs ever
  diverge enough that reshaping actually matters.

The chosen option (one component, broad output, each caller reads only the fields it needs) keeps the actual
parse in exactly one place while still giving each caller a direct, un-reshaped answer.

**§3.2 CLI now, MCP later.** Two MCP-schema options were proposed (MCP tool only; MCP tool plus a thin CLI
wrapper) — both discarded by the architect's own correction: designing the MCP surface at all is premature
here. The ADD's MCP-hosting default (§1) governs how this Feature is eventually *published*, not what this
design phase has to build. Building a CLI now, with core logic kept separate from CLI-specific concerns so an
MCP wrapper is addable later without rework, delivers a real, usable tool today without committing to schema
decisions (tool naming, param typing conventions) this Feature doesn't actually need yet.

**§3.3 `resolve_scope` split.** The alternative — one `resolve_scope(specifiers)` handling both single and
chained cases internally — was discarded: UC-006 draws its own scope boundary explicitly ("not the chained
multi-project form... since extraction already knows where it's going"), and a single function accepting a list
either way relies on caller discipline to respect that boundary rather than the interface itself preventing it.
Splitting into `resolve_scope_single`/`resolve_chained_scope` makes UC-006's own exclusion structural: it has no
function to call that would even let it chain.
