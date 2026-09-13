# Agent Plugins

Canonically defined plugins — sub-agents, skills and tools — authored once
and delivered as a product offering per platform (Claude Code, Codex,
OpenCode, and others as they matter), helping weaver-engineering architects
work productively with AI outside the automated spec/test/build cycle that
The Loom runs.

## Context
* [README](../README.md) - full project description

## What Is Emerging From It

* [Configurable Documentation Evolution](analysis/configurable-documentation-evolution.md) — the design assistant's tool is a configured check set and the next unit of work detector that runs it. The process those constitute is a product in its own right, and AgentPlugins is its genesis rather than its identity — this is what that process is, and why it is configurable

## 1 Use Cases

* [document-a-concept](analysis/use-cases/document-a-concept/USE-CASE.md) — the Architect gets a concept out of their head and into linked, reviewable documentation
* [evolve-a-design-to-maturity](analysis/use-cases/evolve-a-design-to-maturity/USE-CASE.md) — the Architect iteratively evolves a design, deciding each step from findings and their available resolutions
* [find-and-read-documentation](analysis/use-cases/find-and-read-documentation/USE-CASE.md) — a memoryless Agent reaches the sections that bear on its task without reading whole documents
* [number-document-sections](analysis/use-cases/number-document-sections/USE-CASE.md) — section, figure and reference numbering stays standards-compliant without being maintained by hand

## 2 User Personas

* [The Architect](analysis/user-personas/architect.md) — the human in charge of the agentic development, and the primary actor of every use case they appear in
* [The Agent](analysis/user-personas/agent.md) — the general persona: memoryless, working within a finite context budget, doing what the Architect delegates
  * [The Architect's Assistant](analysis/user-personas/architects-assistant.md) — specializes it for delegated documentation work
    * [The Design Assistant](analysis/user-personas/design-assistant.md) — specializes that further, fixed to the `Design The Feature` step

Each specialization states only what its narrower role adds; goals, frustrations and technical proficiency are inherited from the persona it indents under.

## 3 Design

* [Cross-Platform Capability Parity](design/cross-platform-capability-parity.md) — how capability parity between Claude Code and OpenCode is achieved (placeholder, WVR-94)
* [CI/CD Pipeline & Branch Protection](design/ci-cd-pipeline.md) — the existing GitHub Actions workflows and rulesets for both repos
* [Design The Feature — Process](design-the-feature-process.md) — the detailed process definition and rationale design-assistant executes, and the source the per-phase agent instruction files shipped with next-unit-of-work-detector are authored from

## 4 Architecture

* [Architecture Definition Document](architecture/architecture-definition-document.md) — what AgentPlugins delivers, for whom, and how it's built and deployed
* [Capability Catalog](architecture/capability-catalog.md) — living registry of AgentPlugins' sub-agents, tools, and MCP servers

## 5 Claude Skills

Claude Code Skills supporting weaver-engineering's Design The Feature process (WVR-107–115, 117, 130, 139).
Twelve built and deployed to `~/.claude/skills/`; one design below (`called-from-backward-walker`) not yet
built — every other phase but its own (§4.1's cascading-invalidation lookup) has full skill coverage.

* [Next Unit Of Work Detector](claude-skills/next-unit-of-work-detector/next-unit-of-work-detector-design.md) — the resumability router every design session starts with
* [Call Tree Reconciler](claude-skills/call-tree-reconciler/call-tree-reconciler-design.md) — forward and reverse `calls:`/`called_from:` consistency
* [Pseudocode Subset Checker](claude-skills/pseudocode-subset-checker/pseudocode-subset-checker-design.md) — does the design cover every requirement
* [Pseudocode Substitution Checker](claude-skills/pseudocode-substitution-checker/pseudocode-substitution-checker-design.md) — the shared "can this stand in for this" primitive gap-classifier and pseudocode-subset-checker both call
* [Unexpected Side-Effect Scanner](claude-skills/unexpected-side-effect-scanner/unexpected-side-effect-scanner-design.md) — does the design do anything it shouldn't
* [Thin-Shim Consistency Checker](claude-skills/thin-shim-consistency-checker/thin-shim-consistency-checker-design.md) — catches a shim that's stopped being thin
* [Unhandled/Undeclared Exception Sweep](claude-skills/unhandled-undeclared-exception-sweep/unhandled-undeclared-exception-sweep-design.md) — every exception either caught or declared
* [Reconciliation Checksum Utility](claude-skills/reconciliation-checksum-utility/reconciliation-checksum-utility-design.md) — the shared falsifiability mechanism the four checks above record through
* [Called-From Backward Walker](claude-skills/called-from-backward-walker/called-from-backward-walker-design.md) — finds every use case affected when a shared function changes (design only, not yet built)
* [Gap Classifier](claude-skills/gap-classifier/gap-classifier-design.md) — as-is / extended / new, scaffolded, and the bound pseudocode recorded once every gap closes
* [Specific-Behavior Presenter](claude-skills/specific-behavior-presenter/specific-behavior-presenter-design.md) — standardised, provenance-rich presentation for final human review
* [Behavior Regeneration Checker](claude-skills/behavior-regeneration-checker/behavior-regeneration-checker-design.md) — §7.2's regenerate-and-compare step, ahead of Specific-Behavior Presenter
* [Chunk Scope Utility](claude-skills/chunk-scope-utility/chunk-scope-utility-design.md) — shared read/write primitive for a design task's own chunk-scope.yaml

## 6 Sub-Agents

* [Design Assistant](sub-agents/design-assistant/design-assistant.md) — drives the Design The Feature workflow
  step (WVR-119), built and dogfooded to completion against
  [WVR-95](https://linear.app/weaver-engineering/issue/WVR-95/design-the-doc-search-and-retrieval-mcp-server) —
  see its own [Architect's Guide](sub-agents/design-assistant/architect-guide.md) for how to actually work with it
