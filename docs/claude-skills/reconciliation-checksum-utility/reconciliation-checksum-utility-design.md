# Reconciliation Checksum Utility

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-113](https://linear.app/weaver-engineering/issue/WVR-113/skill-reconciliation-checksum-utility) - the ticket this design fulfils
* @docs/templates/SPECIFIC-BEHAVIOR-TEMPLATE.md - the `reconciliation:` block this utility reads and writes
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.1 - the Rationale entry "Why reconciliation: is checksums, not a checkbox"
* [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md), [unexpected-side-effect-scanner](../unexpected-side-effect-scanner/unexpected-side-effect-scanner-design.md), [thin-shim-consistency-checker](../thin-shim-consistency-checker/thin-shim-consistency-checker-design.md), [unhandled-undeclared-exception-sweep](../unhandled-undeclared-exception-sweep/unhandled-undeclared-exception-sweep-design.md) - the four checks that call this utility to record their combined result

## 1 Purpose

The small, shared mechanism that makes every other §7.1 check's result falsifiable rather than a one-shot
checkbox: compute a checksum of each relying use case's own Technical Interpretation slice, and of every
function's pseudocode or prose the `SB-NNN`'s bound pseudocode (§4.3) names; record them once all four §7.1
checks pass; and, on a later run, recompute and compare to detect whether anything the reconciliation relied on
has since changed — without re-reading or re-reasoning about content that hasn't actually moved. This is also
the comparison pseudocode-subset-checker runs first, before ever falling back to
[pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md)'s
more expensive judgement.

## 2 Trigger

Called by pseudocode-subset-checker, unexpected-side-effect-scanner, thin-shim-consistency-checker, and
unhandled-undeclared-exception-sweep once all four pass together for a given `SB-NNN`, to record the result.
Also called by the-unit-of-work-detector's own §1 check, in read/compare mode, to decide whether an `SB-NNN`'s
existing `reconciliation:` block is still current.

## 3 Inputs

* Write mode: an `SB-NNN`'s relying use case(s), each with their own Technical Interpretation slice, and the
  full set of functions/prose its bound pseudocode names.
* Compare mode: an `SB-NNN`'s existing `reconciliation:` block, plus current access to the same content it
  originally checksummed.

## 4 Outputs And Effects

The only skill in this family that writes to a design document — it populates or updates an `SB-NNN`'s own
`reconciliation:` block (`checked_at`, `uc_technical_interpretation_checksums`, `function_checksums`). In compare
mode it's read-only, returning current-vs-stale rather than writing anything.

## 5 Algorithm

**Write:** compute one checksum per relying use case's own Technical Interpretation slice — keyed by that use
case's id, since a `SB-NNN` can name more than one (Specific Behaviors §3) and each is independently
falsifiable — and one per function/prose the bound pseudocode names; write all of them into the `SB-NNN`'s
`reconciliation:` block along with the current date, leaving `reviewed_by`/`reviewed_at` unset (§7.2 sets those
separately).

**Compare:** recompute the same checksums against current content; report stale if any recomputed value doesn't
match what's recorded, current otherwise — and, on a stale `function_checksums` entry specifically, name which
function changed, since that's exactly what pseudocode-subset-checker needs to know which piece(s) to re-run
pseudocode-substitution-checker against, rather than re-deriving the whole bound pseudocode from scratch.

## 6 Composition With Other Skills

Downstream of all four §7.1 checks (only invoked in write mode once every one of them passes) and upstream of
next-unit-of-work-detector (invoked in compare mode as part of that skill's own §1 check, step 7).

## 7 Cost/Benefit

Cheap per call (checksumming is fast, and only runs on already-identified content, not a search). High leverage
because it's shared: every other §7.1 skill and the router itself depend on this one utility's output staying
correct rather than each reimplementing its own staleness detection. Risk profile is the lowest in the family —
this is close to pure, deterministic computation with no judgement calls anywhere in it; a bug here would be a
straightforward implementation defect, not a debatable design choice.

## 8 Open Questions

* Does a stale `uc_technical_interpretation_checksums` entry ever need finer granularity than "this use case's
  slice changed" — e.g. flagging which step within it — or is routing the whole use case back through Gap
  Analysis's own re-classification always the correct response regardless?
* Compare mode already distinguishes which function's checksum went stale (§5) — should it go further and
  identify which specific piece(s) of the bound pseudocode that function was substituted for, or is leaving that
  lookup to pseudocode-subset-checker itself the right division of labor?
