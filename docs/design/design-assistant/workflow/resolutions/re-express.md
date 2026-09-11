# re-express

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.4 - resolving `invalid-behavior`
* [Behavior Model](../../datamodel/behavior-model.md) §1.1 - validity as a property of fit

## Purpose

Restate a requirement against the condition its cell now expresses. The requirement still holds; what moved was
the structure it sits in — a value's predicate narrowed, or a dimension inserted above it — so what was judged
against one condition is now standing against another.

## Applies To

`invalid-behavior`.

## What It Does

1. Establishes what the cell's condition **now** is, from its selected dimension values.
2. Restates the required effects against that condition, keeping what still holds and adjusting what does not.
3. Returns the behavior to `pending`.

## Mechanical

No. Whether a requirement survives its condition moving is a judgement, and the alternative —
[remove-the-element](remove-the-element.md) — is a different judgement about the same facts.

## What Must Be True Afterwards

* the behavior reconciles with its cell's dimensions and its fixtures;
* its review state is `pending`, **never `approved`**;
* its required effects still carry sourcing, and sourcing that is still true of what they now say.

## Notes For P6

**Re-expression never returns straight to `approved`**, for the same reason the `redesign-required` resolutions
do not: what is now recorded has not itself been confirmed. An approved behavior that became invalid already
lost its approval when the finding was raised — what the human agreed to was a behavior at a cell that supported
it, and the cell no longer does.

The neighbouring case is worth keeping separate in the prose. `invalid-behavior` says the **requirement's
context** moved; `redesign-required` says the **design** moved. Both can hold at once, they resolve differently,
and offering one resolution's routes for the other's finding would lose the distinction the model went to some
trouble to keep.

Where re-expression finds the requirement no longer makes sense at this cell at all, the honest outcome is
removal rather than a strained restatement.
