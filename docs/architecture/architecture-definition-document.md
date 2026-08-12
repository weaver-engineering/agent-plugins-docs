# Architecture Definition Document

## Context
* [README](../../README.md) - full project description
* [Agent Plugins](../agent-plugins.md) - the root index: use cases and personas driving this architecture

## 1 Capability Model

AgentPlugins delivers three categories of capability: sub-agents, tools, and MCP servers.

* Sub-agents are actor-like: they carry a role, judgment, and a scope of responsibility, invoked to accomplish
  a task that requires reasoning rather than a fixed procedure. They are analyzed via a user-persona document
  (their role) plus the use cases they participate in (their required behavior) (§4).
* Tools are narrow, deterministic functions invoked as a step by an actor — a human persona or a sub-agent.
  They are analyzed directly by a use case describing their required behavior; they carry no persona of their
  own (§4).
* MCP servers are the default delivery mechanism for tools, not the exception. MCP is an open, cross-platform
  standard: a tool built as an MCP server is authored once and installs identically wherever MCP is supported,
  so building one avoids the toil of maintaining a separate bare-tool integration per platform. Bare delivery
  is the exception — justified only when a tool is stateless *and* the benefit it provides doesn't justify the
  cost of standing up and operating an MCP server for it: the one-time cost of building and configuring the
  server, plus the ongoing operational cost of keeping its process running, which a bare tool has no
  equivalent of.

Every capability, regardless of category, is authored once in canonical form and published to each target
platform (§3). The mechanics of that publication, and what a canonical capability must avoid relying on to stay
portable across platforms, are covered separately in
[Cross-Platform Capability Parity](../design/cross-platform-capability-parity.md).

The inventory of capabilities that actually exist is not embedded in this document — it lives in the
[Capability Catalog](capability-catalog.md), a living registry populated as each capability is built.

## 2 Platform Targets

Claude Code and OpenCode are the initial platform targets, with the architecture designed to accommodate
additional platforms in future without redesign — a new platform requires a new per-platform transform (§3),
not a change to how capabilities are authored.

The two platforms diverge in one way that matters: Claude Code's Skill (a markdown-and-frontmatter capability
with its own reasoning, auto-discovered from its description) has no OpenCode equivalent. This drives a real
authoring constraint — a capability meant to behave identically on both platforms must not depend on Skill's
reasoning capability unless it is delivered via MCP instead, since that is the one capability shape Claude Code
offers that OpenCode structurally cannot match.

Several other differences were investigated and found not to be capability gaps, only differences in mechanism:

* **Permission scoping** differs in locus, not expressiveness: Claude Code splits allow/ask decisions to
  user/session-level settings and deny to a skill or subagent's own tool-allowlist; OpenCode collapses
  allow/deny/ask into the tool/agent definition itself via a glob-keyed ACL. A capability's permission scope
  resolves to one authoritative place either way.
* **Sub-agent frontmatter** (`tools`, `permission`, `model`, and the markdown body instructing the LLM) has a
  direct equivalent on both platforms. OpenCode's broader third-party model catalog affects which platform a
  given use case is best built on, not the schema itself.
* **Reasoning effort** (OpenCode's `/variant`; an analogous Claude Code control) is configured above the
  sub-agent/tool definition on both platforms, out of scope for a manifest-level comparison.
* **Temperature** is exposed per sub-agent in OpenCode with no Claude Code equivalent at the
  subagent-definition level — sidestepped by policy (canonical capabilities do not use temperature) rather than
  needing reconciliation.

Full mechanics of achieving parity across these platforms — the canonical authoring format and the
per-platform transform — are documented separately in
[Cross-Platform Capability Parity](../design/cross-platform-capability-parity.md).

## 3 Publishing Model

Capabilities are authored once, in canonical form, in `agent-plugins` (§6). A per-platform build step
transforms that canonical source into each target's actual artifact shape — Claude Code's skill/subagent
markdown+frontmatter tree, OpenCode's agent markdown+frontmatter and tool TypeScript modules.

"Published" means built and attached as GitHub Release artifacts on the `agent-plugins` repository — not
submitted to either platform's marketplace or a package registry. Both platforms support installing plugins
directly from the filesystem, and since the goal is sharing these capabilities across Weaver Engineering
rather than distributing them publicly, a downloadable release artifact is sufficient.

## 4 Scope & Document Boundaries

This document defines what AgentPlugins delivers, for whom, and how it's built and deployed. It explicitly
excludes:

* **Why AgentPlugins exists and what it does** — the analysis:
  [UC-001](../analysis/use-cases/UC-001-discuss-concept-and-document.md) through
  [UC-006](../analysis/use-cases/UC-006-extract-document-content.md), and the personas
  ([The Architect](../analysis/user-personas/architect.md),
  [The Architect's Assistant](../analysis/user-personas/architects-assistant.md)).
* **How it works internally** — the design documents, one per capability being built.
* **The capability inventory itself** — the [Capability Catalog](capability-catalog.md), a living registry
  populated incrementally as capabilities are built, not embedded here.

Which analysis and design documents apply to a given capability depends on its category (§1):

* **Sub-agents** are analyzed the same way a human actor is: a user-persona document describing its role, plus
  the use cases it participates in describing its required behavior. That analysis pair drives the sub-agent's
  design and implementation.
* **Tools** are analyzed directly by a use case describing their required behavior; they get no persona.
* **MCP servers** get no persona or use case of their own — the tool(s) they expose are analyzed exactly like
  bare tools, one use case each. What's specific to the server lives in a design document: which tool(s) it
  bundles, and its own operational concerns (credentials, keeping the server running).

Design documents for an MCP server live in their own folder under `docs/design/`, named for the server — the
server's own design doc at the folder root, plus one design doc per tool it bundles, with further
subdirectories as needed.
[Doc Search & Retrieval](../design/doc-search-and-retrieval/doc-search-and-retrieval.md) is the worked
exemplar: it bundles UC-002, UC-003, UC-005, and UC-006 (each already analyzed as its own standalone use case —
no persona, since none of these tools are actor-like) and will capture why they're hosted together as one MCP
server rather than shipped as bare tools (currently a placeholder, tracked as WVR-95).

## 5 Security Overview

Canonical source for every capability lives in `agent-plugins`, a private Weaver Engineering repository.
Published artifacts (§3) are GitHub Release artifacts attached to that same repository — nothing crosses into a
public marketplace, registry, or third-party distribution channel. The trust boundary is therefore Weaver
Engineering's own GitHub organization membership: anyone able to tamper with or substitute a package between
authoring and install would already need access inside that boundary.

Permission scoping is not something AgentPlugins defines itself — it is inherited entirely from whichever
platform a capability is installed into. Canonical source declares what a capability needs (e.g. which tools a
sub-agent may call), but the actual grant is enforced by the installing platform's own mechanism at
install/runtime: Claude Code's user-level settings plus a skill or subagent's own tool-allowlist, or OpenCode's
glob-keyed tool/agent permission block (§2). AgentPlugins does not, and cannot, override or bypass either
platform's native permission model — an installer's own configuration is always the final word on what an
installed capability can actually do.

MCP servers are the one capability category with credentials of their own — real secrets to manage, and the
operational cost of keeping the server running, are exactly the costs weighed against a tool's benefit when
deciding whether it qualifies for the bare-delivery exception instead of the MCP default (§1). Those
credentials are never stored in canonical source or in a
published artifact; they're supplied at deploy/run time through whatever secret-handling mechanism the hosting
environment provides, scoped to that server's own runtime process. Each MCP server's own design document (e.g.
[Doc Search & Retrieval](../design/doc-search-and-retrieval/doc-search-and-retrieval.md), WVR-95) states its
specific credential requirements — this section states the rule all of them follow.

## 6 Codebase & Delivery Reference

AgentPlugins spans two repositories in the `weaver-engineering` GitHub organization:
[`agent-plugins`](https://github.com/weaver-engineering/agent-plugins) (canonical source, pnpm/TypeScript
monorepo) and [`agent-plugins-docs`](https://github.com/weaver-engineering/agent-plugins-docs) (this document
and all analysis/design/architecture documentation).

Branching strategy: a task branch per Linear issue (`task/WVR-NNN`), cut from current `origin/main`, merged
only via an approved pull request enforced by GitHub branch rulesets in both repos — `main` cannot be pushed to
directly.

CI/CD is GitHub Actions, gate-checks-based, inherited from the-loom's established pattern rather than designed
specifically for AgentPlugins. Full detail — workflows, ruleset configuration, the squash-vs-rebase
merge-method split, and a known current gap in `agent-plugins`' own gate-checks availability — is documented in
[CI/CD Pipeline & Branch Protection](../design/ci-cd-pipeline.md). This is explicitly provisional: Weaver
Engineering intends to define an org-wide standard CI/CD pipeline
([WVR-38](https://linear.app/weaver-engineering/issue/WVR-38), currently blocked on ADR-021), which will
supersede this project-specific one once it exists.
