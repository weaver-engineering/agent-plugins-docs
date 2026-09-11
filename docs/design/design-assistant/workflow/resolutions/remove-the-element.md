# remove-the-element

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.3, §6.4 - removal and its higher bar
* [Claim Model](../../serialization/claim-model.md) §6 - an address leaves the model when the last claim naming it goes

## Purpose

Delete something the design no longer holds. **Removal is irreversible in a way no other resolution is**: accept
and reject both leave a re-derivable artefact on record, and removal leaves nothing.

## Applies To

`invalid-behavior`, `redesign-required`, `orphan-function`, `unstated-required-attributes` where the element is
the residue of a missed rename.

## What It Does

1. Obtains an **unambiguous confirmation naming exactly what is being removed** — never a general nod at a
   batch, and never folded into a routine "does this look right".
2. Removes every claim naming the address, which is what actually takes it out of the model: an address leaves
   only when the last claim naming it goes.
3. Deals with what the removal frees — a behavior's cell becomes uncovered, which either prunes with a reason or
   raises `uncovered-cell` on the next run.

## Mechanical

No, and deliberately gated more heavily than any other route.

## What Must Be True Afterwards

* no claim names the removed address;
* nothing derived from it survives pointing at it;
* where a behavior was removed, its cell is either pruned with a recorded reason or reported as uncovered.

## Notes For P6

**The confirmation bar is different in kind, not merely in degree.** Accept and reject leave a behavior that can
be re-derived and re-examined if the decision was wrong. Removal leaves nothing to re-examine, and the cell it
frees is indistinguishable from a cell nobody ever reached. That asymmetry justifies a different standard of
confirmation, not more care within the same one.

**It bites hardest on `invalid-behavior`**, where the cell itself may already be gone — pruned by a validity rule
added later. That is the one variant where re-expression is not available and removal is the only resolution,
and it is also the one where there is least left to check the decision against.

Two removals in the model need no confirmation at all and are not this resolution: a **spent acknowledgement**
and a **satisfied change request** are both deleted mechanically, because nothing re-examinable is lost — the
instance each was about is gone.
