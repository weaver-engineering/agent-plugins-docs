# Agent Plugins

Skills and subagents that help weaver-engineering architects work
productively with AI, outside the automated spec/test/build cycle that
The Loom runs.

## Context
* [README](../README.md) - full project description

## 1 Use Cases

* [UC-001 — Discuss A Project Concept And Document It](analysis/use-cases/UC-001-discuss-concept-and-document.md)
* [UC-002 — Auto-Number Document Sections](analysis/use-cases/UC-002-auto-number-document-sections.md)
* [UC-003 — Index A Path](analysis/use-cases/UC-003-index-a-path.md)
* [UC-004 — Index Document Words (Retired)](analysis/use-cases/UC-004-index-document-words.md) — merged into UC-003
* [UC-005 — Search Documentation](analysis/use-cases/UC-005-search-documentation.md)
* [UC-006 — Extract Document Content](analysis/use-cases/UC-006-extract-document-content.md)

## 2 User Personas

* [The Architect](analysis/user-personas/architect.md)
* [The Architect's Assistant](analysis/user-personas/architects-assistant.md)

## 3 Design

* [Cross-Platform Capability Parity](design/cross-platform-capability-parity.md) — how capability parity between Claude Code and OpenCode is achieved (placeholder, WVR-94)
* [CI/CD Pipeline & Branch Protection](design/ci-cd-pipeline.md) — the existing GitHub Actions workflows and rulesets for both repos

## 4 Architecture

* [Architecture Definition Document](architecture/architecture-definition-document.md) — what AgentPlugins delivers, for whom, and how it's built and deployed
* [Capability Catalog](architecture/capability-catalog.md) — living registry of AgentPlugins' sub-agents, tools, and MCP servers

## 5 Claude Skills

Design proposals for candidate Claude Code Skills supporting weaver-engineering's Design The Feature process
(WVR-107–115, 117–118), for architect review before implementation.

* [Next Unit Of Work Detector](claude-skills/next-unit-of-work-detector/next-unit-of-work-detector-design.md) — the resumability router every design session starts with
* [Call Tree Reconciler](claude-skills/call-tree-reconciler/call-tree-reconciler-design.md) — forward and reverse `calls:`/`called_from:` consistency
* [Pseudocode Subset Checker](claude-skills/pseudocode-subset-checker/pseudocode-subset-checker-design.md) — does the design cover every requirement
* [Pseudocode Substitution Checker](claude-skills/pseudocode-substitution-checker/pseudocode-substitution-checker-design.md) — the shared "can this stand in for this" primitive gap-classifier and pseudocode-subset-checker both call
* [Unexpected Side-Effect Scanner](claude-skills/unexpected-side-effect-scanner/unexpected-side-effect-scanner-design.md) — does the design do anything it shouldn't
* [Thin-Shim Consistency Checker](claude-skills/thin-shim-consistency-checker/thin-shim-consistency-checker-design.md) — catches a shim that's stopped being thin
* [Unhandled/Undeclared Exception Sweep](claude-skills/unhandled-undeclared-exception-sweep/unhandled-undeclared-exception-sweep-design.md) — every exception either caught or declared
* [Reconciliation Checksum Utility](claude-skills/reconciliation-checksum-utility/reconciliation-checksum-utility-design.md) — the shared falsifiability mechanism the four checks above record through
* [Called-From Backward Walker](claude-skills/called-from-backward-walker/called-from-backward-walker-design.md) — finds every use case affected when a shared function changes
* [Gap Classifier](claude-skills/gap-classifier/gap-classifier-design.md) — as-is / extended / new, scaffolded, and the bound pseudocode recorded once every gap closes
* [Specific-Behavior Presenter](claude-skills/specific-behavior-presenter/specific-behavior-presenter-design.md) — standardised, provenance-rich presentation for final human review
