# approve

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.1 - the review states
* [Decision Model](../../datamodel/decision-model.md) §5.1 - presenting a behavior means presenting its sourcing

## Purpose

A human takes responsibility for what the code will be made to do. `approved` is the **only** state a human can
put a behavior into, and the design assistant can never grant it to itself. Everything else about review is
mechanical.

## Applies To

`unapproved-behavior`.

## What It Does

1. Presents the behavior: what it `realizes`, each **Given** condition annotated with its provenance, the
   **When**, the required effects, the expected effects, and the call tree that produced them.
2. The architect corrects, the agent revises, the architect approves — or does not.
3. Records `reviewedBy` and `reviewedAt` on approval.

## Mechanical

No, and this is the one resolution where that is the entire point rather than a consequence.

## What Must Be True Afterwards

* the behavior's review state is `approved`, with who and when;
* nothing was approved that is stale, unsatisfied, or producing effects nobody anticipated — which is why
  [behavior-approval](../checks/behavior-approval.md) requires those checks to be clean first.

## Notes For P6

**Presenting a behavior for approval means presenting the provenance of each of its Given conditions**: which
document defined it, whether the architect said so, or whether it was inferred and on what basis. An inferred
condition presented as though it came from a use case is the failure mode this exists to prevent, and it is
invisible at the moment it matters.

**Approval does not survive invalidity.** An approved behavior whose cell stops supporting it returns to
`pending` — the responsibility was taken for something no longer being claimed. A design must not be able to
reach `M4` on a confirmation nobody actually gave.

**A restored approval is not an approval granted.** Where a regeneration reproduces exactly what was approved,
the approval is restored mechanically and this resolution is not invoked: nothing changed, and asking again
would be re-litigating a decision nobody disputed.

This resolution is the closest thing in the workflow to a sub-workflow of its own, and it is where the
architect's time actually goes. Everything else in a design exists so that it can be done with confidence.
