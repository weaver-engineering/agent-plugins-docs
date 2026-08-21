# Capability Catalog

A living registry of every capability AgentPlugins delivers — sub-agents,
tools, and MCP servers — authored once in canonical form and published to
each target platform (see the [Architecture Definition Document](architecture-definition-document.md),
§1 Capability Model). Populated incrementally: an entry is added here once a
capability has analysis (a persona and/or use cases) to point to, even
before its design is written — design status is shown per entry.

## Context
* [Architecture Definition Document](architecture-definition-document.md) - defines the three capability categories catalogued here

## 1 Sub-Agents

* [The Architect's Assistant](../analysis/user-personas/architects-assistant.md) — delegated work on the
  Architect's behalf; supporting actor for judgment/dialogue use cases
  ([UC-001](../analysis/use-cases/UC-001-discuss-concept-and-document.md)), primary actor for mechanical
  delegation ([UC-002](../analysis/use-cases/UC-002-auto-number-document-sections.md),
  [UC-003](../analysis/use-cases/UC-003-index-a-path.md),
  [UC-005](../analysis/use-cases/UC-005-search-documentation.md),
  [UC-006](../analysis/use-cases/UC-006-extract-document-content.md)) (no design doc yet)

* [Design Assistant](../analysis/user-personas/design-assistant.md) — carries out the Design The Feature
  workflow step (weaver-engineering/docs `design-feature-instructions.md`) on the Architect's behalf; a
  narrower specialization of The Architect's Assistant, scoped to one workflow step rather than general
  mechanical delegation. Built and dogfooded to completion against
  [WVR-95](https://linear.app/weaver-engineering/issue/WVR-95/design-the-doc-search-and-retrieval-mcp-server)
  ([WVR-119](https://linear.app/weaver-engineering/issue/WVR-119/sub-agent-design-assistant-drives-design-the-feature),
  [design doc](../sub-agents/design-assistant/design-assistant.md))

## 2 Tools

*(none yet — every tool analysed so far is MCP-hosted; see MCP Servers)*

## 3 MCP Servers

* [Doc Search & Retrieval](../design/doc-search-and-retrieval/doc-search-and-retrieval.md) — placeholder,
  WVR-95. Bundles:
  * [UC-002 — Auto-Number Document Sections](../analysis/use-cases/UC-002-auto-number-document-sections.md)
  * [UC-003 — Index A Path](../analysis/use-cases/UC-003-index-a-path.md)
  * [UC-005 — Search Documentation](../analysis/use-cases/UC-005-search-documentation.md)
  * [UC-006 — Extract Document Content](../analysis/use-cases/UC-006-extract-document-content.md)
