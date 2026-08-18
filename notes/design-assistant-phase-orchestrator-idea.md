# Design-Assistant As A Phase Orchestrator — Extension Idea

Free-form, `notes/` — not a spec, not indexed, not reviewed for correctness. Captured from a conversation during
WVR-95 dogfooding (design-assistant driving the Doc Search & Retrieval MCP server's own design through Design
The Feature). Nothing here has been built, and no changes have been made to design-assistant's actual
instructions as a result of it — this is the idea as discussed, kept so it isn't lost.

## The problem

`design-assistant`'s instructions (`sub-agents/design-assistant/design-assistant.md`, plus the whole of
`design-feature-instructions.md`/`specific-behaviors.md` it has to hold in mind) keep growing as the process
picks up more nuance — the §5.1/§5.2 split, nested numbering, the leaf/parent rule, etc. All of that is context
the LLM carries on every turn, regardless of which phase of the process is actually active. Following the
process itself — which phase comes next — is mechanical (`next-unit-of-work-detector` already determines this
from file state alone); only *doing* a given phase needs judgment. Today those two things are conflated: one
long-lived session holds all of it, all the time.

## The idea

Split the monolithic instructions into a thin orchestrator plus narrowly-scoped, per-phase execution:

* **A thin orchestrator.** Calls `next-unit-of-work-detector`, gets back a phase (e.g.
  `5.1-agreeing-the-shape`) and a target (`SB-001`), dispatches a subagent scoped to just that phase, waits for
  its result, records it, loops. Its own instructions stay small no matter how many phases or how much nuance
  any one phase accumulates.
* **One generic phase-runner subagent, parameterized by section — not one bespoke agent per phase.** At spawn
  time it's told which section of `design-feature-instructions.md` to load (e.g. `§5.1`) and works from just
  that section's text, not the whole document. The phases already differ only in *which instructions apply*,
  not in tools or persona, so a single parameterized definition is the natural shape rather than eight
  near-duplicate agent files that all have to be kept in sync by hand.
* **Each phase's own `Exit:` line is the completion contract.** Every phase in `design-feature-instructions.md`
  already states its own exit criterion. That's exactly what a phase-runner subagent needs to know when it's
  actually done and can hand back to the orchestrator — nothing new to invent there.
* **Multi-turn elicitation stays inside one subagent invocation.** §5.1's propose/revise/approve mini-cycle
  (or any other back-and-forth with the architect) happens entirely within that one subagent's own
  conversation; it only exits once its `Exit:` condition is mechanically true.

## The enabler: this is what UC-006 already is

The missing piece — "give me just this subsection's text, not the whole document" — turns out to already be
the design target of the very feature being dogfooded. [UC-006 — Extract Document
Content](../docs/analysis/use-cases/UC-006-extract-document-content.md) resolves a reference like
`@docs/workflows/feature-workflow/design-feature-instructions.md§5.1` against a `sections.yaml` index (built by
UC-003 from UC-002's heading-depth-aware parse) and returns that section's raw source text verbatim — never
reconstructed from index data. Once WVR-95 ships, the phase-runner subagent's prompt-builder doesn't need any
bespoke extraction logic of its own (the way `next-unit-of-work-detector`'s `extractSection` helper does today)
— it can just call `extract_content` for the phase in question. The `§design-step-5-1`-style addressing
originally sketched for this idea collapses to UC-006's own reference grammar; nothing new needs inventing
there either.

## A convergence worth noting

UC-002 (Auto-Number Document Sections) computes numbering "by document position and heading depth" and parses
`§M.N(.O)?` tokens. That's the same rule as "heading depth tracks nesting depth" written into
`specific-behaviors.md` §4.1 during this same dogfooding pass (`{N}` is `##`, `{N}.{M}` is `###`, and so on) —
arrived at independently, from opposite ends of the same problem (a numbering tool needing structure to be
mechanically recoverable; a process doc needing the same thing for its own resumability). `
design-feature-instructions.md`, once indexed under UC-002/UC-003's scheme, should number-index correctly by
construction, not by coincidence.

## Known gap

`sections.yaml` as it exists today (hand-built during UC-003's own elicitation, see
`notes/uc-003-index-a-path-design-notes.md`) only covers flat `## N` headings — none of the UC docs it was built
from nest. `design-feature-instructions.md` nests three levels deep in places (`§5.1`, `§7.1`). This isn't a
special case to carve out later: any real document under `@docs` nests, so UC-003's own specific behaviors will
need to walk arbitrary heading depth to be correct for its actual scope, not just for this idea's sake. Expected
to close naturally when UC-003's `SB-NNN`s are derived.

## Open questions / risks, before this gets adopted anywhere

* **Cross-phase context loss is the load-bearing assumption.** Each phase-runner subagent starts cold, so any
  "why we chose this" reasoning that isn't written into the design docs themselves is lost between phases. This
  is arguably already true and desirable — the whole design is deliberately file-resumable by construction
  (checksums, `//TODO` placeholders, nothing relying on conversation memory surviving a session boundary) — but
  it's worth stating plainly as the thing this architecture depends on, not assuming it holds without checking.
* **Per-phase dispatch overhead vs. context savings.** More tool-call/spawn overhead per phase transition, but
  phases are already chunked coarse-grained (per `SB-NNN`, per gap), so this is likely an acceptable trade —
  not measured.
* **Sequencing dependency.** Not buildable end-to-end until WVR-95 ships `extract_content` for real; until
  then, a prototype would have to fall back to something like `next-unit-of-work-detector`'s existing
  regex-based `extractSection` as a stand-in.
* **Ownership overlap.** Touches `sub-agents/design-assistant/design-assistant.md`, the
  `next-unit-of-work-detector` skill, and WVR-95's own `extract_content` implementation — three things that
  currently live and evolve somewhat independently.
