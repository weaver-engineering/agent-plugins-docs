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

*(Not yet populated — Phase 3 Ideation, Design Feature Instructions §4, hasn't run yet. Every Open Design
Question carried by the four use cases in scope must be addressed here, resolved or explicitly deferred:
UC-002 §7 (CLI flags/exit codes/report format), UC-003 §7 (CLI flags for path/recurse/depth), UC-005 §7
(algorithm-selection syntax, N/X defaults for details mode, and the deliberate single-component allocation for
document- and section-level scoring), UC-006 §7 (out-of-bounds line range behavior).)*

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
* `parse_document` (UC-002) and `parse_structure` (UC-003) — **new**, listed separately since the Technical
  Interpretations name them separately, but they read as the same underlying capability (parse a markdown
  document's headings/figures) requested for two different purposes (renumbering vs. indexing metadata).
  Flagged for Ideation to decide: one shared component with a broader contract, or two genuinely distinct ones.
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

*(Populated as Key Decisions (§3) are made — each entry there gets its justification and discarded
alternatives recorded here, per Design Feature Instructions §4.1.)*
