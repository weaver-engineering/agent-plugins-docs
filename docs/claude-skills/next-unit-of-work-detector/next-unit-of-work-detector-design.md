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

Check, in this fixed order, against the design directory's current state — the first gap found is the answer:

1. Does the HLD exist with its Scope naming every use case in this Feature? If not: confirm scope first.
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
6. For every `SB-NNN` stub: does it have at least one fully-derived behavior, not only its placeholder marker?
   First one that doesn't → Deriving Specific Behaviors (§5) for that `SB-NNN`.
7. For every derived behavior: does its call tree's every node appear in its parent's declared `calls:`? First
   mismatch → Call Tree Reconciliation (§6) for that issue.
8. For every `SB-NNN` clean per §6: does its `reconciliation:` block have checksums that still match current
   content? If empty or stale → Mechanical Reconciliation (§7.1) — pseudocode-subset-checker's cheap checksum
   comparison first, falling back to pseudocode-substitution-checker only on drift.
9. For every `SB-NNN` clean per §7.1: does its `reconciliation:` block have `reviewed_by` set? If not → Human
   Review (§7.2).

Once every `SB-NNN` in scope reaches step 9: design complete.

## 6 Composition With Other Skills

This is the router every other skill in the family sits behind — it doesn't perform any phase's work itself, it
identifies which one to hand off to (gap-classifier for both its §3 and §4.3 passes, call-tree-reconciler for
§6, the §7.1 family for mechanical reconciliation, specific-behavior-presenter for §7.2). Called-from-backward-walker,
reconciliation-checksum-utility, and pseudocode-substitution-checker are invoked *by* other skills as they run,
not directly reachable from this router's own output.

## 7 Cost/Benefit

Highest-frequency skill in the family by a wide margin — invoked at the start of nearly every design session,
and again after most other skills finish. The check itself is cheap (a handful of document reads against a
fixed checklist), but the benefit isn't in the check's own cost — it's in what it replaces: an agent otherwise
re-deriving "what's already done" from scratch each session, which is exactly the failure mode WVR-106 was
raised to close. Risk profile is low — the check is a direct reading of already-explicit exit criteria (each
phase's own "Exit:" line in Design Feature Instructions), not a judgement call; a wrong answer here is a bug in
the skill, not a debatable interpretation.

## 8 Open Questions

* Should scope restriction (checking one `UC-{NNN}` or `SB-{NNN}` only) return a result relative to *that*
  artifact even when earlier, unscoped phases (e.g. Gap Analysis, which is whole-Feature) are themselves
  incomplete — or should an incomplete whole-Feature phase always take precedence regardless of what scope was
  asked for?
* Should the "design complete" result at step 8 automatically suggest transitioning to `Chunk The Design`, or
  stop at reporting completion and leave that call to the architect?
