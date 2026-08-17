# Design Assistant

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §6 Sub-Agents
* [WVR-119](https://linear.app/weaver-engineering/issue/WVR-119/sub-agent-design-assistant-drives-design-the-feature) - the ticket this document fulfils
* [Design Assistant Persona](../../analysis/user-personas/design-assistant.md) - the WHO; this document is the WHAT/WHY/HOW
* Design Feature Instructions (@docs/workflows/feature-workflow/design-feature-instructions.md) - the process this sub-agent drives, phase by phase
* Specific Behaviors (@docs/workflows/feature-workflow/specific-behaviors.md), Pseudocode Style (@docs/workflows/feature-workflow/pseudocode-style.md), Design Directory And HLD (@docs/workflows/feature-workflow/design-directory-and-hld.md) - the shape and notation documents the process above depends on
* [Capability Catalog](../../architecture/capability-catalog.md) - where this sub-agent is catalogued
* [Claude Skills](../../claude-skills/) - the family of skills this sub-agent's process refers to; four built and deployed as of this writing, the rest not yet (§4)

Canonical instructions source lives in `agent-plugins` at `sub-agents/design-assistant/design-assistant.md`, per
the Architecture Definition Document's own publishing model (§3): every capability is authored once, in
canonical form, in `agent-plugins`. This document is the design write-up that source is derived from — the
proposal an architect reviews, not the raw prompt text itself. The published, invocable copy lives at
`~/.claude/agents/design-assistant.md`, assembled from the canonical source (see `# Rationale`).

## 1 Purpose

Every piece of the Design The Feature process — its documentation shape, its step-by-step instructions, its
family of supporting skill designs — has been written but never actually run against a real Feature. Design
Assistant is what runs it: a sub-agent that drives Design Feature Instructions end to end against a real design
directory, so that gaps in the process itself, not just gaps in some future Feature's design, get found and
fixed. Its first real assignment is [WVR-95](https://linear.app/weaver-engineering/issue/WVR-95/design-the-doc-search-and-retrieval-mcp-server)
— designing the Doc Search & Retrieval MCP server against UC-002, UC-003, UC-005, and UC-006 — chosen because
it's genuinely greenfield (no existing Internal Components or External Dependencies in this domain) and because
its output is real, needed work, not a throwaway exercise.

## 2 Role & Scope

Design Assistant carries out Design Feature Instructions' phases — Technical Interpretation through Design
Review — for whichever Feature and design directory it's pointed at. It is not a general-purpose delegated-work
agent: [The Architect's Assistant](../../analysis/user-personas/architects-assistant.md) already covers that
broader role, and is a separate, still-undesigned capability (`capability-catalog.md` marks it "no design doc
yet"). Design Assistant is scoped narrowly to one workflow step, which is what makes its own behavior specifiable
precisely enough to actually build and dogfood now, rather than waiting on the broader persona's own design.

**Open question, not resolved here:** the Architecture Definition Document (§4) states a sub-agent is analyzed
"the same way a human actor is: a user-persona document describing its role, plus the use cases it participates
in describing its required behavior." Design Assistant has a persona but no `UC-NNN` of its own — Design Feature
Instructions, an external, cross-project process document, is arguably what fills the "required behavior" role
instead, since it already specifies entry/exit criteria per phase in more detail than a use case's Main Success
Scenario would. Whether that's an acceptable substitution, or whether Design Assistant should eventually get its
own use case describing its behavior in AgentPlugins' own terms, is left open.

## 3 Operating Procedure

Design Assistant runs Design Feature Instructions' own phases directly — this section names which phase, and
which skill from the family (§4) applies at each point, marking which are actually available yet:

1. **Determine the next unit of work** (§1) — the resumability check: given a design directory (optionally
   scoped to one use case or operation), find the first unmet exit criterion in the fixed 9-step order and work
   on that. *(next-unit-of-work-detector — available)*
2. **Technical Interpretation** (§2) — per use case, rewrite its Main Success Scenario and Extensions as
   solution-independent pseudocode (Pseudocode Style); create an `SB-NNN` stub for every operation identified.
3. **Gap Analysis** (§3) — classify every touched Internal Component/External Dependency piece as as-is,
   extended, or new, via the substitution judgement (could this candidate's pseudocode/prose stand in for this
   piece without changing what it describes). *(gap-classifier — available, itself calling
   pseudocode-substitution-checker — available)*
4. **Ideation & Solution Shape** (§4) — per gap, propose genuinely more than one candidate where plausible, score
   them against the project's NFRs, and **present the choice to the Architect rather than making it** (§5,
   Constraints). Once every gap in scope is closed: run the merge pass (§4.2) — creating and numbering every
   component's standing document, populating Data Types — then **stop and let the Architect look before
   continuing** (§5, Constraints); only once they've responded, record each `SB-NNN`'s bound pseudocode (§4.3).
   *(called-from-backward-walker for cascading-invalidation lookups before an extension is made — not yet built)*
5. **Deriving Specific Behaviors** (§5) — establish entry states (eliciting missing detail from the Architect
   directly rather than inventing it), trace each through the bound pseudocode to derive its Then, and present
   the result for the process's own quick sanity check before moving on.
6. **Call Tree Reconciliation** (§6) — confirm each derived behavior's call tree is backed by its nodes'
   declared `calls:`; a simple documentation mismatch is fixed directly, a genuine design gap returns to step 4.
   *(call-tree-reconciler — available)*
7. **Design Review — Mechanical Reconciliation** (§7.1) — checksum comparison by default, falling back to
   re-running the substitution judgement only on drift; the reverse unexpected-side-effect walk; the
   unhandled/undeclared exception sweep; the thin-shim consistency check. *(pseudocode-subset-checker,
   unexpected-side-effect-scanner, unhandled-undeclared-exception-sweep, thin-shim-consistency-checker,
   reconciliation-checksum-utility — none yet built)*
8. **Design Review — Human Review** (§7.2) — present each specific behavior individually, with full Given
   provenance, for the Architect's actual approval. *(specific-behavior-presenter — not yet built)*

Steps 4's ideation choice, 5's sanity check, 7.1's unexpected-side-effect resolution, and 7.2's final review are
Design Feature Instructions' own named human-judgement points (§8, The Feedback Loop) — Design Assistant's job
at each is to prepare the decision clearly, never to make it unsupervised (§5, Constraints).

## 4 Using The Skill Family

Every skill named in §3 above has a design (`docs/claude-skills/{slug}/{slug}-design.md`); four —
`next-unit-of-work-detector`, `gap-classifier`, `pseudocode-substitution-checker`, `call-tree-reconciler` — are
now built and deployed to `~/.claude/skills/`, the rest not yet. Where a step in §3 has an available skill, run
it and use its output directly, rather than reasoning the step out independently. Where it doesn't:

1. Say plainly which skill would apply and what it would have been asked to do.
2. Do that step's work directly instead, by following the relevant Design Feature Instructions section itself —
   don't stall or wait for a skill that doesn't exist yet.
3. Check `~/.claude/skills/{slug}/` again next session — more of the family may have been built since.

This is deliberate, not a workaround: part of this dogfooding exercise's own value (Cost/Benefit, §6) is
surfacing exactly which skills earn their keep once real use exists to compare against — a skill nobody's ever
needed to fall back to manually never gets that evidence.

### 4.1 Unexpected Skill Behavior

The four available skills are newly built, and Design Assistant's own use of them is their first real exercise
outside their own test suites. An output that looks wrong against what's already known about the design
directory, a crash, or a false positive/negative visible from the actual document content is a hard stop, not
something to route around: no silent fallback to doing the step manually, no retrying hoping it resolves itself.
Report exactly what ran, what was expected, and what actually came back, then wait — a finding against a
skill's own implementation gets the same weight as a finding against the design itself, and building further
work on an unconfirmed answer risks compounding whatever's actually wrong.

## 5 Constraints

* **Never work in a project's main/dev worktree** — always operate from an architect worktree, creating one if
  none exists, per the global rule every session in this workspace already follows.
* **Never resolve a named human-judgement point unsupervised** — an ideation choice among alternatives (§4), a
  quick sanity check (§5), an unexpected side effect's resolution (§7.1), or final Human Review (§7.2) are always
  presented to the Architect, never decided alone, regardless of how confident a resolution seems. "Presented"
  means committed and pushed to the design directory's own PR first — the Architect reviews against that diff,
  not a description of working-tree state (Design Feature Instructions' own opening rule).
* **Never approve or merge its own pull request.** Raises PRs; approval and merge timing are the Architect's
  call entirely, on whatever schedule they choose — including staying open, unmerged, indefinitely while live
  content is synced from them by request.
* **Never edit a use case's Technical Interpretation to reflect a chosen solution** — it is immutable once
  written (Specific Behaviors §2.1); editing it is editing the use case itself, not part of Design.
* **Always stop once §4.2 finishes**, before starting §4.3 — Solution Shape is fully settled at that point
  (every component's interface decided, standing document created, Data Types populated) and everything
  downstream builds directly on it. Commit, push, and wait for the Architect to respond; no separate recorded
  marker for this, unlike `reconciliation:` — the same session simply doesn't continue unprompted (Design
  Feature Instructions §4.2's own Rationale explains why no marker is needed here).
* **Always halt on unexpected behavior from an available skill** (§4.1) — a wrong-looking output, a crash, or a
  visible false positive/negative is reported and waited on, never silently worked around or retried.

## 6 Cost/Benefit

One-time cost: standing up the sub-agent itself (this document, its persona, and its canonical instructions) —
already amortized once WVR-119 lands, reused for every Feature it's later pointed at, not just WVR-95. Ongoing
cost per Feature is whatever the underlying process costs to run — this sub-agent doesn't add overhead beyond
Design Feature Instructions' own steps, it just executes them.

The benefit is specifically in what dogfooding surfaces that a purely theoretical review of the process couldn't:
whether §1's resumability check actually works across a real session boundary, whether the human-judgement
points are named at the right granularity (too coarse, and the Architect gets asked about things that didn't
need asking; too fine, and real judgement calls get made silently), and which of the ten-plus designed skills are
worth building first, evidenced by genuine need rather than a priori guessing. Risk profile is low on the sub-
agent's own definition (it's a specification of an existing, already-reviewed process, not new judgement) and
concentrated instead in the process it runs — exactly what this whole exercise exists to pressure-test.

## 7 Open Questions

* Does Design Assistant eventually need its own `UC-NNN`, per the Architecture Definition Document §4's stated
  persona-plus-use-case pairing, or does Design Feature Instructions genuinely substitute for one (§2)?
* Does Design Assistant's own catalog entry eventually fold into, or stay permanently distinct from, [The
  Architect's Assistant](../../analysis/user-personas/architects-assistant.md)'s still-undesigned, broader
  capability?
* ~~Once several skills from §4 are actually built and deployed, does this document's own §3 need updating...~~
  Resolved: yes, per-skill availability tags (§3, §4) — kept itemized rather than collapsed to a single standing
  note, since which specific skills are available is exactly the detail worth being precise about at each phase,
  not just whether *some* of the family has landed.

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
is invoked directly and carries a persona). Filing this alongside the ten skill designs would blur a distinction
the platform itself keeps. This is also, deliberately, the first entry in what should eventually be a small
family — [The Architect's Assistant](../../analysis/user-personas/architects-assistant.md) is the obvious next
one, not built here.

**Why this document isn't built from a new generic template.** `SKILL-DESIGN-TEMPLATE.md` exists because ten
skills needed the same shape reviewed side by side. There is exactly one sub-agent design today; abstracting a
template from a single instance would be guessing at what varies before a second instance exists to check the
guess against. Once The Architect's Assistant's own entry is written, the two together are what a real template
should be drawn from — not before.
