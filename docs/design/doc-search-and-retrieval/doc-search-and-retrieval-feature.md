# Doc Search & Retrieval — Feature

## Context
* [Architecture Definition Document](../../architecture/architecture-definition-document.md) §4 - names this server as the worked exemplar bundling the use cases below
* [Capability Catalog](../../architecture/capability-catalog.md) - lists this server under MCP Servers
* [UC-002 — Auto-Number Document Sections](../../analysis/use-cases/UC-002-auto-number-document-sections.md)
* [UC-003 — Index A Path](../../analysis/use-cases/UC-003-index-a-path.md)
* [UC-005 — Search Documentation](../../analysis/use-cases/UC-005-search-documentation.md)
* [UC-006 — Extract Document Content](../../analysis/use-cases/UC-006-extract-document-content.md)
* [Doc Search & Retrieval — High-Level Design](doc-search-and-retrieval-hld.md) - this Feature's design directory entry point

## 1 What

An MCP server bundling four documentation-tooling capabilities as one hosted server, rather than shipping each
as a separate bare tool: numbering a document's own sections (UC-002), building the `.index/` data a project's
docs are searched and extracted through (UC-003), searching across that index (UC-005), and reading raw content
located by search or by direct reference (UC-006).

## 2 Who

No human actor persona. Every one of the four bundled use cases is invoked by an agent — Claude Code, or any
other tool-calling agent needing document content — never a human directly. UC-002 is the one partial exception:
the Architect may invoke it directly (e.g. after manually reordering sections), but it's still agent-shaped
tooling, not a human-facing feature.

## 3 Why Bundled As One Server, Not Four Tools

All four operations read or write the same underlying `.index/` data model
([Documentation Standards](../../standards/documentation-standards.md) §4) for the same corpus — a project's own
`docs/` tree. Search (UC-005) and extraction (UC-006) are two different reads of index data UC-003 produced;
numbering (UC-002) is what keeps the section ids that data model depends on stable. Hosting them together means
one process holds the shared understanding of that data shape, instead of four independent tools each
re-deriving or duplicating it. This Feature is also this workspace's own worked exemplar for the Design The
Feature process itself (Architecture Definition Document §4) — the first Feature it's been run against in full.

## 4 Where / When

Runs wherever an agent is working inside a project's own docs repo (or a `weaver-engineering` workspace spanning
several), triggered on demand: a document is authored or restructured (UC-002), a path needs indexing before it's
searchable (UC-003), an agent needs to find which document covers a subject (UC-005), or needs the actual content
at an already-known or approximately-known location (UC-006).

## 5 Scope Boundary

Indexing (UC-003) and numbering (UC-002) never decide document structure or content — they operate on what's
already written. Search (UC-005) computes relevance; it doesn't fetch content itself (UC-006's job). Extraction
(UC-006) reads raw source text using `.index/` data only to locate it; it doesn't compute relevance and doesn't
index anything itself. None of the four capabilities author or edit documentation content on an agent's behalf —
that stays a separate, human-in-the-loop concern (UC-001).

## 6 Design Task History

* `WVR-95` — [Doc Search & Retrieval — High-Level Design](doc-search-and-retrieval-hld.md), covering UC-002,
  UC-003, UC-005, UC-006 in full. In progress.
