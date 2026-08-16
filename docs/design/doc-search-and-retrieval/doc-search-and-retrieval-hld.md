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

*(Remaining §3.1-style subsections — one per Internal Component interface, plus one per use case's Open Design
Question — get added here as each is decided. Still open: `resolve_scope`'s exact `@{scope}`/`@{slug}` grammar
as one shared interface for both UC-005 and UC-006 despite their slightly different needs; the
filesystem-as-in-process-I/O modeling choice from §6; and UC-002/003/005/006's own §7 Open Design Questions
(CLI flags/report format, CLI flags for path/recurse/depth, algorithm-selection syntax + N/X defaults,
out-of-bounds line range behavior) — none decided yet.)*

## 4 Data Types

*(Not yet populated — depends on the Internal Component interfaces §3/§5 decide.)*

## 5 Internal Components

Gap Analysis (Design Feature Instructions §3) result: `docs/architecture/components/` has no existing entries
for this project (confirmed directly, not assumed), so every candidate function the four Technical
Interpretations collectively name classifies **new** — there is nothing existing to compare any of them
against. This is the inventory Gap Analysis produces; which of these actually earn a standing `IC-NNN` document
versus staying Chunk-private (Design Directory And HLD §4.3) is Solution Shape's decision (§2.3/§4), not yet
made here.

* `resolve_scope` — **new** — named identically in both UC-005 and UC-006's Technical Interpretation (the
  `@{scope}` resolution rules differ slightly between them — UC-005 allows chained `@{slug}@{slug}`, UC-006
  doesn't — but both need it). One candidate, two relying use cases, not two candidates.
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

None identified. Every candidate in §5 that touches the filesystem (`read_source_text`, `write_index_files`,
`parse_document`/`parse_structure`, `list_index_entries`, `remove_index_entries`) does so against files this
same project owns and manages, in-process — not a separate real system whose behavior can only be observed by
calling it (Design Directory And HLD §3's own bar: "a network boundary, real time, real randomness, another
team's own data"). A unit test can exercise these against a temp directory without needing anything external.
This reasoning, not just its conclusion, belongs in Key Decisions (§3) once Ideation confirms it — recorded
here for now since Gap Analysis is what surfaced the question.

## 7 Specific Behaviors

* [SB-001 — Auto-Number A Document](specific-behaviors/SB-001-auto-number-document.md) - realizes [UC-002](../../analysis/use-cases/UC-002-auto-number-document-sections.md) (stub — behaviors not yet derived)
* [SB-002 — Index A Path](specific-behaviors/SB-002-index-a-path.md) - realizes [UC-003](../../analysis/use-cases/UC-003-index-a-path.md) (stub — behaviors not yet derived)
* [SB-003 — Search Documentation](specific-behaviors/SB-003-search-documentation.md) - realizes [UC-005](../../analysis/use-cases/UC-005-search-documentation.md) (stub — behaviors not yet derived)
* [SB-004 — Extract Document Content](specific-behaviors/SB-004-extract-document-content.md) - realizes [UC-006](../../analysis/use-cases/UC-006-extract-document-content.md) (stub — behaviors not yet derived)

*(All four use cases in scope now have a Technical Interpretation and an identified operation, and Gap
Analysis (§5/§6 above) is done. Per Design Feature Instructions §1, the next unit of work is step 4: Phase 3
Ideation, one gap at a time — a named human-judgement point (§4.1), not something this document resolves on
its own.)*

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
