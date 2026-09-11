# anticipation

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §2.3 - anticipation, and why it cannot be shortcut
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §3 - one of the three kinds that never resolve mechanically

## Purpose

Does the design do anything nobody asked for? Every expected `dependency-interaction` and `state-change` must be
anticipated by some required effect. One that is not is an **unexpected external side effect**, and "everything
required is present too" does not excuse it.

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [traces](traces.md) — the expected effects to walk |

## What It Inspects

Every `ExpectedEffect` of kind `dependency-interaction` or `state-change`, against the behavior's required
effects.

**This half cannot be shortcut by a checksum.** What it looks for is an effect nobody has recorded anywhere, so
there is no prior record for a checksum to compare against — it has to be re-derived from the walk each time the
walk is re-run.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unexpected-side-effect` | an expected dependency interaction is anticipated by no required effect | [state-the-fact](../resolutions/state-the-fact.md) · [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

**Never mechanical, and a genuine hard stop.** An anticipation failure is not necessarily a defect at all: the
design may be right and the requirement incomplete. A dependency interaction the requirement never mentioned
looks identical from the design's side whether it is a bug in the design or a gap in the use case's
understanding, and only someone looking at what the effect actually *is* can tell.

So the two routes are opposite corrections, and the resolution must present them as such rather than offering
one:

* the requirement was incomplete — record the effect as required, which is `state-the-fact`;
* the design is wrong — it should not be producing this effect under this entry condition, which is
  `correct-the-design`.

This is the one finding whose resolution can legitimately send work back out of design and into analysis.
Automating it would mean the model silently picking one of two opposite corrections.
