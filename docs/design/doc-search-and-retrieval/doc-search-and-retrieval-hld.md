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

*(Not yet populated — Phase 2 Gap Analysis, Design Feature Instructions §3, hasn't run yet. This section fills
in once each use case's Technical Interpretation is written and the Feature's combined pseudocode is read
against the project's existing Internal Components and External Dependencies — currently none, since this is
the first Feature in this domain.)*

## 3 Key Decisions

*(Not yet populated — Phase 3 Ideation, Design Feature Instructions §4, hasn't run yet. Every Open Design
Question carried by the four use cases in scope must be addressed here, resolved or explicitly deferred:
UC-002 §7 (CLI flags/exit codes/report format), UC-003 §7 (CLI flags for path/recurse/depth), UC-005 §7
(algorithm-selection syntax, N/X defaults for details mode, and the deliberate single-component allocation for
document- and section-level scoring), UC-006 §7 (out-of-bounds line range behavior).)*

## 4 Data Types

*(Not yet populated — depends on the Internal Component interfaces §3/§5 decide.)*

## 5 Internal Components

*(Not yet populated — Phase 2 Gap Analysis (§3 above) hasn't classified any candidate functions yet. Expect
everything to classify as new: this is a greenfield domain with no existing Internal Components or External
Dependencies to reuse.)*

## 6 External Dependencies

*(Not yet populated — see §5. The filesystem itself (reading/writing `.md` and `.index/` files) is the only
candidate dependency visible from the use cases so far; whether that's modeled as an External Dependency proper
or as ordinary in-process I/O is a Gap Analysis / Ideation question, not decided here.)*

## 7 Specific Behaviors

* [SB-001 — Auto-Number A Document](specific-behaviors/SB-001-auto-number-document.md) - realizes [UC-002](../../analysis/use-cases/UC-002-auto-number-document-sections.md) (stub — behaviors not yet derived)

*(UC-003, UC-005, UC-006 still need their own Technical Interpretation and Operations identified before their
SB-NNN stubs exist — see the HLD's own state for what's next.)*

## 8 Technology Stack

*(Not yet populated — inherits from the workspace's own established convention for this kind of tool
(`agent-plugins/packages/<name>`: pnpm workspace package, TypeScript ESM, `tsc`, Vitest — per
`weaver-engineering docs-standards-adopted` precedent) unless Key Decisions (§3) find a reason to diverge; not
asserted as decided until §3 actually says so.)*

# Rationale

*(Populated as Key Decisions (§3) are made — each entry there gets its justification and discarded
alternatives recorded here, per Design Feature Instructions §4.1.)*
