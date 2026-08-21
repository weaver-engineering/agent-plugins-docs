# Next Unit Of Work Detector

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-107](https://linear.app/weaver-engineering/issue/WVR-107/skill-next-unit-of-work-detector-for-the-design-feature-process) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§1 - the process this skill implements
* [gap-classifier](../gap-classifier/gap-classifier-design.md), [call-tree-reconciler](../call-tree-reconciler/call-tree-reconciler-design.md), [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md) - the skills this one routes work to, including gap-classifier's two separate passes (§3 and §4.3)

## 1 Purpose

Design is deliberately broken into small, independently-resumable units of work, and a fresh session — or a
"design-assistant" sub-agent invoked cold, with no memory of any previous session — has to be able to pick up
immediately. That only works if "what's next" is derivable mechanically from a design directory's own current
state, not recalled from conversation context that doesn't exist. This skill *is* that derivation: given a
design directory, tell the caller exactly which phase, and which specific artifact within it, needs work next.

## 2 Trigger

Manual, at the start of essentially every design session — this is the first thing an agent (or a
"design-assistant" sub-agent) runs before doing anything else, per Design Feature Instructions' own framing.
Also re-run after any other skill in this family finishes a unit of work, to confirm what's next rather than
assuming the caller already knows.

## 3 Inputs

* A design directory path (`docs/design/{feature-slug}/` in some project's own docs repo).
* An optional scope restriction — one use case (`UC-{NNN}`) or one operation (`SB-{NNN}`) — to check only that
  artifact's own state rather than the whole Feature.

## 4 Outputs And Effects

Read-only. Produces a single answer: which phase is next (§2–§7 of Design Feature Instructions), and the
specific artifact it applies to (a use case id, an operation id, an `SB-NNN` id, or a named reconciliation
issue) — or, if every `SB-NNN` in scope has reached step 8, a "design complete, ready for Chunk The Design"
result. Never edits a document itself.

## 5 Algorithm

Final shape adds a Step 0 ahead of everything else, and reworks steps 6 and 9 substantially from what was
originally proposed — see Rationale for why. Check, in this fixed order, against the design directory's current
state — the first gap found is the answer:

0. **Entry requirements, unconditional on every call** (WVR-138, WVR-143): does the HLD's `Feature {slug}`
   bullet link to a real, non-stub initial feature document? Do every UC nested under the current Design Task
   link back to that same feature document? Is the checked-out branch (if it matches `task/{REF}`) tracked by a
   currently open PR? Any failure here is `error` — Design The Feature doesn't own fixing its own entry
   requirements, and no skill auto-creates the missing PR (check-only, by design).
1. Does the HLD exist with its Scope naming this design task's own use cases, nested under a `Design Task: {ref}`
   entry (Scope accumulates across separate design tasks, so this only requires *this task's* use cases, not
   every use case the Feature will ever have)? If not: confirm scope first.
2. For each use case in scope: does it have a non-empty `## Technical Interpretation`? First one that doesn't →
   Technical Interpretation (§2) for that use case.
3. Does the HLD's Internal Components and External Dependencies list classify every function the Technical
   Interpretations collectively touch as as-is, extended, or new? If not → Gap Analysis (§3), gap-classifier's
   §3 pass.
4. For every item classified extended or new, and every Open Design Question: is there a resolved Key Decision
   with a Rationale entry naming every alternative considered? First unresolved gap → Per-Gap Ideation (§4.1).
   Once every gap is resolved, has the merge pass (§4.2) run since the last one was added? If not → that.
5. For every `SB-NNN` stub clean per step 4: does it carry a bound-pseudocode block (§4.3) for each use case that
   relies on it? First one that doesn't → Recording The Bound Pseudocode (§4.3), gap-classifier's second pass.
6. **Split into two passes** (§5.1/§5.2, reworked from the original single-step proposal — see Rationale): has
   an outline of numbered entry conditions been proposed and approved for this `SB-NNN`, written as numbered
   placeholder headings (parents holding their real Given, leaves holding `//TODO`)? If not → Agreeing The Shape
   (§5.1). Once the outline exists: does every leaf hold real derived content, with no `//TODO` or `//REVIEW`
   line remaining? First leaf still `//TODO` or `//REVIEW` → Deriving Each Behavior (§5.2), for that specific
   behavior. Correctly checks every id carrying its own `reconciliation.behaviors.{id}` entry, not just ids
   without children — a "dual-role" id (a complete behavior *and* a parent to further permutations, Specific
   Behaviors §4.1) needs exactly this check too (WVR-142, a real bug in an earlier build: id with children was
   wrongly skipped entirely, regardless of it carrying its own entry).
7. For every derived behavior: does its call tree's every node appear in its parent's declared `calls:`? First
   mismatch → Call Tree Reconciliation (§6) for that issue.
8. For every `SB-NNN` clean per §6: does its `reconciliation:` frontmatter have `checked_at` set? If empty or
   stale → Mechanical Reconciliation (§7.1) — pseudocode-subset-checker's cheap checksum comparison first,
   falling back to pseudocode-substitution-checker only on drift.
9. **Project-wide, not scoped to this Feature** (WVR-130/134, a substantial rework from the original per-Feature
   proposal — see Rationale): for every `SB-NNN` in *every* Feature's own design directory, does every leaf (or
   dual-role) behavior have a `reviewed` entry in its own `reconciliation.behaviors.{id}`, with no
   `//REDESIGN_REQUIRED` flag standing against it? A behavior with no entry (never reviewed, or a function
   change cleared it per §7.1's own invalidation walk), or one flagged `//REDESIGN_REQUIRED`, needs §7.2 —
   regardless of which Feature or use case it belongs to. Steps 1–8 can be scoped to one Feature's own design
   directory; step 9 can't, since its whole purpose is catching invalidation reaching outside the Feature
   currently being worked on — pointing `<design-dir>` at the project's `docs/design/` root itself (one level up
   from any Feature subdirectory) runs only this step, across every Feature discovered beneath it.

Once every `SB-NNN` in scope reaches step 8 *and* a full project-wide step 9 scan finds nothing left needing
§7.2 anywhere: design complete.

## 6 Composition With Other Skills

This is the router every other skill in the family sits behind — it doesn't perform any phase's work itself, it
identifies which one to hand off to. Final routing table: gap-classifier for both its §3 and §4.3 passes,
call-tree-reconciler for §6, the §7.1 family (pseudocode-subset-checker, unexpected-side-effect-scanner,
thin-shim-consistency-checker, unhandled-undeclared-exception-sweep, reconciliation-checksum-utility) for
mechanical reconciliation, and — added after the §7.2 rework (WVR-130) — behavior-regeneration-checker first at
§7.2, with specific-behavior-presenter only once that confirms a genuine match to present. Also gained a small,
standalone reverse-lookup mode not reachable through the ordinary routing at all: `--find-design-task {ref}
<project-design-root>` scans every Feature's own HLD for the matching `Design Task:` entry and returns its
Feature slug and use case list — what makes resuming a design task by ticket ref alone possible with no other
context supplied. `called-from-backward-walker` (still not built) and `pseudocode-substitution-checker` are
invoked *by* other skills as they run, never directly reachable from this router's own output.

**A structural limit worth naming, found live rather than anticipated**: this skill's own `<design-dir>` never
crosses repository boundaries. When a design task's branch has diverged from its own project's `main` (e.g. an
early tracking PR was squash-merged, severing ancestry — WVR-143's own motivating case), reconciling that
divergence is a git-history problem this router has no visibility into and doesn't attempt to solve — it can
only detect that a tracking PR is currently missing (Step 0), never resolve a merge conflict once one exists.

## 7 Cost/Benefit

Highest-frequency skill in the family by a wide margin — invoked at the start of nearly every design session,
and again after most other skills finish. The check itself is cheap (a handful of document reads against a
fixed checklist), but the benefit isn't in the check's own cost — it's in what it replaces: an agent otherwise
re-deriving "what's already done" from scratch each session, which is exactly the failure mode WVR-106 was
raised to close. Risk profile is low — the check is a direct reading of already-explicit exit criteria (each
phase's own "Exit:" line in Design Feature Instructions), not a judgement call; a wrong answer here is a bug in
the skill, not a debatable interpretation.

## 8 Open Questions

Resolved by build and dogfooding: an incomplete whole-Feature phase always takes precedence over a scope
restriction, since steps 1–8 already implicitly filter to the given scope where the step itself is per-artifact,
and step 9's own project-wide nature makes "relative to this scope" not meaningful for it at all. "Design
complete" reports completion only — transitioning to `Chunk The Design` stays the architect's own call, never
suggested automatically.

# Built And Deployed

Built and deployed to `~/.claude/skills/next-unit-of-work-detector/`, and the most heavily iterated skill in the
family — five follow-up tickets after its initial build (WVR-122, 134, 138, 142, 143, plus WVR-145/147/148/149/153
for the per-phase `instructions` field described below), each found live while dogfooding it against a real
design directory rather than anticipated in advance.

**A significant late addition, not originally proposed here**: the tool's own `complete: false` result now
carries an `instructions` field — the full, self-contained guidance for whichever phase it names, read verbatim
from a static file shipped with the skill itself (`instructions/{phase}.md`, one per distinct phase string,
authored from [Design The Feature — Process](../../design-the-feature-process.md)). This is what let
`design-assistant`'s own standing instructions shrink to cross-cutting rules only (WVR-144/145/146/147) — the
per-phase procedure and which-skill-applies detail moved out of the sub-agent's own context entirely and into
this tool's live output, fetched fresh every call rather than held statically regardless of relevance.

# Rationale

**Why step 6 splits into two passes (§5.1/§5.2), not the single step originally proposed.** The original
proposal only checked "does at least one fully-derived behavior exist" — weaker than Design Feature Instructions
§5's own exit criterion, which requires every happy path and every identified unhappy path. Dogfooding surfaced
this directly: the process would derive one behavior, treat the `SB-NNN` as touched, and never come back for the
rest, since nothing forced it to. Splitting the check into "has an outline been agreed" and, separately, "is
every agreed placeholder actually filled in" closes that gap by making the full set of required behaviors an
explicit, resumable artifact rather than something the router had no way to verify against.

**Why step 9 became project-wide, not scoped to the Feature.** The original proposal treated Human Review as
another per-Feature step, same shape as steps 1–8. Design Feature Instructions §7.1's own invalidation walk
doesn't respect Feature boundaries — a changed function can reach a behavior in any Feature's own design
directory, including one already shipped. Scoping step 9 to just the current Feature would let those
invalidations sit uncaught indefinitely. No new CLI argument was needed to fix this: pointing `<design-dir>` at
the project's own `docs/design/` root (one level up from any single Feature's subdirectory) is enough for the
tool to discover every Feature beneath it and run step 9 across all of them.
