# behavior-approval

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.1 - the review states
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.5 - review is project-wide and a fixed point
* [Decision Model](../../datamodel/decision-model.md) §5.1 - presenting a behavior means presenting its sourcing

## Purpose

Has a human taken responsibility for every behavior this design decided anything about? `approved` is the only
state a human can put a behavior into, and the design assistant can never grant it to itself. This is
deliberately *the* human in the loop: it is the point at which a person takes responsibility for what the code
will be made to do.

The qualifier is load-bearing rather than a softening: a behavior whose every fixture is external decided
nothing here, and asking for a signature on it would dilute the ones that matter. It also means this check
will never put such a behavior in front of anyone — the review of it happened when its fixtures were
authored, upstream and out of this design's sight
([Reconciliation Model](../../datamodel/reconciliation-model.md) §6.1).

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [regeneration](regeneration.md) · [satisfaction](satisfaction.md) · [anticipation](anticipation.md) — nothing should be presented for approval that is stale, unsatisfied, or doing something nobody asked for |

## What It Inspects

Every behavior's `review` state. A behavior is outstanding while it is `pending` — derived, presented or not,
but not yet confirmed — or `redesign-required`.

**Except where every one of its chosen fixtures is external.** A behavior resting entirely on fixtures this
design references rather than authored ([Behavior Model](../../datamodel/behavior-model.md) §3.0) is owed no
approval and is not outstanding for want of one: no Given condition of it was arrived at here, so there is
nothing for a signature to stand behind (see Notes below, and
[Reconciliation Model](../../datamodel/reconciliation-model.md) §6.1). One locally authored fixture among them
and the behavior is outstanding like any other.

An approved behavior that becomes **invalid** returns to `pending`: what the human agreed to was a behavior at a
cell that supported it, and the cell no longer does.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unapproved-behavior` | a behavior has no standing human approval | [approve](../resolutions/approve.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

**Review is project-wide and a fixed point, not a pass over the boundary in hand.** A function change reaches
behaviors in any boundary whose call tree names it, including boundaries whose design was finished long ago, and
resolving one disconnect can invalidate another. The pass is complete only when a full scan finds nothing
outstanding anywhere.

**Presenting a behavior for approval means presenting the provenance of each of its Given conditions**: which
document defined it, whether the architect said so, or whether it was inferred and on what basis. An inferred
condition presented as though it came from a use case is the failure mode that makes the whole approval
worthless, and [authored-sourcing](authored-sourcing.md) is what guarantees there is something to present.

This is the check whose resolution is most nearly a whole workflow of its own: the architect and the agent
assess the operation's prose and anything bearing on it, the agent proposes a behavior, the architect corrects
it, the agent revises, the architect approves. Everything else in the design exists so that this can be done
with confidence.
