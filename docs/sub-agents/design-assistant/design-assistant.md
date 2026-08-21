# Design Assistant

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §6 Sub-Agents
* [WVR-119](https://linear.app/weaver-engineering/issue/WVR-119/sub-agent-design-assistant-drives-design-the-feature) - the ticket this document fulfils
* [Design Assistant Persona](../../analysis/user-personas/design-assistant.md) - the WHO; this document is the WHAT/WHY/HOW
* Design Feature Instructions (@docs/workflows/feature-workflow/design-feature-instructions.md) - the human/architect-facing copy of the process this sub-agent drives (its own eventual rewrite for that audience is WVR-144, deliberately deferred)
* [Design The Feature — Process](../../design-the-feature-process.md) - the detailed, agent-facing process definition and rationale this sub-agent's own per-phase instructions are authored from; the canonical source going forward, not `design-feature-instructions.md` directly (see Rationale)
* Specific Behaviors (@docs/workflows/feature-workflow/specific-behaviors.md), Pseudocode Style (@docs/workflows/feature-workflow/pseudocode-style.md), Design Directory And HLD (@docs/workflows/feature-workflow/design-directory-and-hld.md), [Chunk Scope](@docs/workflows/feature-workflow/chunk-scope.md) - the shape and notation documents the process above depends on
* [Capability Catalog](../../architecture/capability-catalog.md) - where this sub-agent is catalogued
* [Claude Skills](../../claude-skills/) - the family of skills this sub-agent's process refers to; twelve built and deployed as of this writing, one (§4.1's cascading-invalidation lookup) still not

Canonical instructions source lives in `agent-plugins` at `sub-agents/design-assistant/design-assistant.md`, per
the Architecture Definition Document's own publishing model (§3): every capability is authored once, in
canonical form, in `agent-plugins`. This document is the design write-up that source is derived from — the
proposal an architect reviews, not the raw prompt text itself. The published, invocable copy lives at
`~/.claude/agents/design-assistant.md`, assembled from the canonical source (see `# Rationale`).

## 1 Purpose

Every piece of the Design The Feature process — its documentation shape, its step-by-step instructions, its
family of supporting skill designs — had been written but never actually run against a real Feature. Design
Assistant is what ran it: a sub-agent that drives Design Feature Instructions end to end against a real design
directory, so that gaps in the process itself, not just gaps in some future Feature's design, get found and
fixed. Its first real assignment, [WVR-95](https://linear.app/weaver-engineering/issue/WVR-95/design-the-doc-search-and-retrieval-mcp-server)
— designing the Doc Search & Retrieval MCP server against UC-002, UC-003, UC-005, and UC-006 — is now complete:
every use case's Technical Interpretation through §7.2's project-wide Human Review, merged (PR #21). It was
chosen because it's genuinely greenfield (no existing Internal Components or External Dependencies in this
domain) and because its output is real, needed work, not a throwaway exercise — both held up in practice: being
greenfield is exactly what surfaced [[WVR-151]]/[[WVR-152]] (process rules that silently assumed something had
already shipped, which nothing had, project-wide, until this run).

## 2 Role & Scope

Design Assistant carries out Design Feature Instructions' phases — Technical Interpretation through Design
Review — for whichever Feature and design directory it's pointed at. It is not a general-purpose delegated-work
agent: [The Architect's Assistant](../../analysis/user-personas/architects-assistant.md) already covers that
broader role, and is a separate, still-undesigned capability (`capability-catalog.md` marks it "no design doc
yet"). Design Assistant is scoped narrowly to one workflow step, which is what makes its own behavior specifiable
precisely enough to actually build and dogfood, rather than waiting on the broader persona's own design.

**Open question, not resolved here:** the Architecture Definition Document (§4) states a sub-agent is analyzed
"the same way a human actor is: a user-persona document describing its role, plus the use cases it participates
in describing its required behavior." Design Assistant has a persona but no `UC-NNN` of its own — Design Feature
Instructions, an external, cross-project process document, is arguably what fills the "required behavior" role
instead, since it already specifies entry/exit criteria per phase in more detail than a use case's Main Success
Scenario would. Whether that's an acceptable substitution, or whether Design Assistant should eventually get its
own use case describing its behavior in AgentPlugins' own terms, is still left open.

## 3 Operating Procedure

Design Assistant's own standing instructions (`agent-plugins/sub-agents/design-assistant/design-assistant.md`,
deployed as `~/.claude/agents/design-assistant.md`) are deliberately small — cross-cutting rules only. They do
**not** enumerate phases or skills the way an earlier draft of this document once did: that per-phase detail
proved to be exactly the wrong place to keep it (see Rationale, "Why the per-phase procedure moved out of this
sub-agent's own standing instructions").

The actual procedure is:

1. **Call `next-unit-of-work-detector`** against the design directory. This is the resumability check (Design
   Feature Instructions §1): given a design directory — optionally scoped to one use case or operation — it
   finds the first unmet exit criterion, project-wide for §7.2, and returns which phase is next.
2. **Follow the returned `instructions` field verbatim.** The tool attaches the full, self-contained guidance
   for that specific phase — sourced from static files shipped with the skill itself
   (`claude-skills/next-unit-of-work-detector/instructions/{phase}.md`, authored from [Design The Feature —
   Process](../../design-the-feature-process.md)) — including which skill applies and how to use it. Design
   Assistant doesn't separately hold or re-derive this; it reads it fresh, every call.
3. **Run whichever skill the returned instructions name**, and use its output directly rather than reasoning
   the step out independently. Where the instructions say no skill exists yet for this phase (true only for
   §4.1's cascading-invalidation lookup as of this writing): say plainly what would have been asked of it, do
   that step's work directly instead by following the returned instructions text, and check again next session.
4. **Never resolve a named human-judgement point unsupervised** (§5, Constraints) — Per-Gap Ideation's "how
   might we," §5.1/§5.2's outline-and-derivation sanity checks, §7.1's unexpected-side-effect resolution, and
   §7.2's Human Review (including every `//REDESIGN_REQUIRED` accept/reject/remove decision) are always
   presented, never decided alone.

## 4 Unexpected Skill Behavior

Treat any output that looks wrong against what's already known about the design directory, a crash, or a false
positive/negative visible from the actual document content as a hard stop, not something to route around: no
silent fallback to doing the step manually, no retrying hoping it resolves itself. Report exactly what ran, what
was expected, and what actually came back, then wait.

This is no longer a hedge against untested skills — it's proven practice with a real track record. Running the
full family for the first time against real, live WVR-95 data caught five genuine implementation bugs this way
([[WVR-142]], [[WVR-149]], [[WVR-150]], [[WVR-153]], [[WVR-154]] — three of them silent data corruption or
truncation a test suite alone hadn't caught) and two genuine errors in the *process documentation itself*, not
any skill's code ([[WVR-151]], [[WVR-152]] — both assumed something had already shipped project-wide, which
never happens on a Feature's first design task). Every one of these was caught specifically because Design
Assistant held the line here rather than working around an output that merely looked plausible.

## 5 Constraints

* **Never work in a project's main/dev worktree** — always operate from an architect worktree, creating one if
  none exists, per the global rule every session in this workspace already follows.
* **Never resolve a named human-judgement point unsupervised** — an ideation choice among alternatives (§4.1), a
  §5.1/§5.2 sanity check, an unexpected side effect's resolution (§7.1), or Human Review including every
  `//REDESIGN_REQUIRED` resolution (§7.2) are always presented to the Architect, never decided alone, regardless
  of how confident a resolution seems. "Presented" means committed and pushed to the design directory's own PR
  first — the Architect reviews against that diff, not a description of working-tree state (Design Feature
  Instructions' own opening rule).
* **Never approve or merge its own pull request.** Raises PRs; approval and merge timing are the Architect's
  call entirely, on whatever schedule they choose.
* **Never edit a use case's Technical Interpretation to reflect a chosen solution** — it is immutable once
  written (Specific Behaviors §2.1); editing it is editing the use case itself, not part of Design.
* **Always stop once §4.2 finishes**, before starting §4.3 — Solution Shape is fully settled at that point
  (every component's interface decided, standing document created, Data Types populated) and everything
  downstream builds directly on it. Commit, push, and wait for the Architect to respond.
* **Always halt on unexpected behavior from an available skill** (§4) — a wrong-looking output, a crash, or a
  visible false positive/negative is reported and waited on, never silently worked around or retried.

## 6 Cost/Benefit

One-time cost: standing up the sub-agent itself (this document, its persona, and its canonical instructions) —
already amortized once WVR-119 lands, reused for every Feature it's later pointed at, not just WVR-95. Ongoing
cost per Feature is whatever the underlying process costs to run — this sub-agent doesn't add overhead beyond
Design Feature Instructions' own steps, it just executes them.

The benefit, evidenced now rather than speculative: dogfooding a single real Feature end to end found seven real
defects that no amount of reviewing the process or the skills in the abstract had caught — five in shipped skill
code, silent on data the skills' own test suites happened not to exercise ([[WVR-142]], [[WVR-149]], [[WVR-150]],
[[WVR-153]], [[WVR-154]]), and two in the process documentation itself, both stemming from the same root cause:
a rule written assuming something had already shipped, on a project where nothing ever had yet ([[WVR-151]],
[[WVR-152]]). It also validated the resumability model directly — §1's check genuinely let sessions restart cold
and pick up exactly where a prior one left off, across a cold-start, a runtime restart, and several handoffs
between this sub-agent and its supervising session, with no shared memory beyond document state. Risk profile
stayed low on the sub-agent's own definition throughout (it's a specification of an existing, already-reviewed
process, not new judgement); every defect found was in the process or the skills it runs, exactly what this
exercise existed to pressure-test.

## 7 Open Questions

* Does Design Assistant eventually need its own `UC-NNN`, per the Architecture Definition Document §4's stated
  persona-plus-use-case pairing, or does Design Feature Instructions genuinely substitute for one (§2)?
* Does Design Assistant's own catalog entry eventually fold into, or stay permanently distinct from, [The
  Architect's Assistant](../../analysis/user-personas/architects-assistant.md)'s still-undesigned, broader
  capability?
* The squash-merge/tracking-PR history divergence this dogfooding run hit (a design task's own long-lived branch
  diverging from `main`'s squash-merged history of that same branch's earlier work) needed a manual "take ours"
  merge resolution once, for WVR-95's own final PR. Whether a better structural answer exists — since it will
  recur for every design task's own eventual tracking PR — is tracked as part of [[WVR-155]] (the dogfooding
  retrospective), not resolved here.

# Rationale

**Why the definition lives in `agent-plugins-docs`, with only the raw instructions text canonically sourced in
`agent-plugins`.** A skill combines mechanical function with reasoning prose, and its mechanical half genuinely
needs a code repository home (`agent-plugins/claude-skills/{slug}/`). A sub-agent is pure reasoning — there's no
mechanical component to build or package. Splitting the design write-up (this document, in `agent-plugins-docs`,
alongside its persona and every other piece of this sub-agent's analysis) from the raw canonical prose
(`agent-plugins`, per the ADD's existing publishing-model rule) keeps the Architecture Definition Document's own
publishing rule intact without duplicating the actual reasoning content across two repositories — the
`agent-plugins` copy is a distillation of this document's §3, not an independent second draft of it.

**Why `docs/sub-agents/`, not `docs/claude-skills/`.** Claude Code treats Skill and sub-agent as different
artifact shapes (a Skill is auto-discovered from its own description and carries its own reasoning; a sub-agent
is invoked directly and carries a persona). Filing this alongside the skill designs would blur a distinction the
platform itself keeps. This is also, deliberately, the first entry in what should eventually be a small family —
[The Architect's Assistant](../../analysis/user-personas/architects-assistant.md) is the obvious next one, not
built here.

**Why this document isn't built from a new generic template.** `SKILL-DESIGN-TEMPLATE.md` exists because the
skill family needed the same shape reviewed side by side. There is exactly one sub-agent design today;
abstracting a template from a single instance would be guessing at what varies before a second instance exists
to check the guess against. Once The Architect's Assistant's own entry is written, the two together are what a
real template should be drawn from — not before.

**Why the per-phase procedure moved out of this sub-agent's own standing instructions.** An earlier draft of §3
(and the canonical `design-assistant.md` it was distilled from) enumerated every phase and named which skill
applied at each, directly in the sub-agent's own standing instructions — the same content the agent had to hold
as context on every single session, whether or not that phase was actually relevant to the very next call.
Dogfooding surfaced this as real, unnecessary weight: the standing instructions grew every time a new phase's
skill mapping was added, none of it varying by the actual next unit of work. The fix (WVR-144/145/146/147) moved
that content out entirely: `next-unit-of-work-detector` now returns each phase's own instructions live, sourced
from static files shipped with the skill itself and authored from [Design The Feature —
Process](../../design-the-feature-process.md) (the new agent-facing detail source — see that document's own
Rationale for why it, not `design-feature-instructions.md` directly, is now canonical for this purpose). Design
Assistant's own standing instructions shrank from 137 lines to under 100, and — the actual point — stopped
requiring the whole process family to be held as context regardless of relevance. §3 above describes the
resulting procedure, not the phase-by-phase detail itself, which now genuinely lives elsewhere.

**Why `docs/analysis/use-cases/design-feature-instructions.md` isn't the canonical agent-facing source anymore.**
`weaver-engineering/docs` is human (architect) documentation — how the process works, and the architect's own
role in it. It shouldn't also be the mechanically-consumed source per-phase agent instructions get authored from;
conflating the two is exactly what the per-phase procedure move (above) corrected at the delivery-mechanism
level. [Design The Feature — Process](../../design-the-feature-process.md), in this repo, is now that detailed
agent-facing reference; `design-feature-instructions.md` keeps its own copy for the architect's own audience,
its own eventual rewrite tracked separately (WVR-144).