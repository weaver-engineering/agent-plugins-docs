# agent-plugins-docs

Documentation for the
[agent-plugins](https://github.com/weaver-engineering/agent-plugins)
project.

## What agent-plugins is

Skills and subagents that help weaver-engineering **architects** work
productively with AI, outside the automated spec → test → build (or
quick) cycle that
[the-loom](https://github.com/weaver-engineering/the-loom) runs.
the-loom's own plugins tool up AI to operate *within* that cycle
(`gate-checks`, `task-phases`, and the `test-writer`/`build-implementer`/
`quick-scaffolder` subagents that execute it); agent-plugins instead
supports the architect driving the cycle from outside it — analysis,
design, chunking and sequencing a backlog into specs, checking a spec's
output actually satisfies what the next phase needs, and smoothing
handovers between phases to catch a design miss before it reaches an
agent mid-cycle.

## What belongs here

Design docs for agent-plugins' own architecture, in the same shape
[magpieweaver-docs](https://github.com/weaver-engineering/magpieweaver-docs)
and
[the-loom-docs](https://github.com/weaver-engineering/the-loom-docs)
carry for their own projects: architecture/LLD documents under `docs/`,
and working notes under `notes/` as they accumulate. Nothing has been
designed yet, so this repo currently just carries the CI scaffolding
that validates commits landing on `main`.

The open design question worth documenting first, once it's settled:
how to define a plugin's actual logic exactly once and expose it
correctly to both Claude Code (skills + subagents) and OpenCode (tools +
agents) — the two platforms' plugin formats aren't identical, and that
mechanism isn't decided yet.

See [WVR-55](https://linear.app/simonemmott/issue/WVR-55) for the
originating ticket.
