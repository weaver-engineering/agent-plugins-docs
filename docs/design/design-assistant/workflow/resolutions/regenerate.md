# regenerate

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.2 - regeneration and its outcomes
* [Behavior Model](../../datamodel/behavior-model.md) §4 - what a trace produces

## Purpose

Re-run a derivation and write the result. This is the one resolution that is fully mechanical: nothing about it
needs a human, and nothing about it is a decision.

## Applies To

`stale-provenance`, `calls-index-mismatch`, `out-of-date-diagram`, `call-declaration-mismatch` (once the call
has been established as decided), `unstated-required-attributes` where the absent attribute is a derived one.

## What It Does

Depending on what is being regenerated:

* **a trace** — re-walk from the operation's realizing function with the cell's entry condition and chosen
  fixtures, producing the call tree, the expected effects, and fresh provenance;
* **the `calledFrom` index** — rebuild it from the `calls` declarations, which are right by definition;
* **a derived diagram** — resolve its key against the model, redraw, and record the new checksum;
* **a derived dimension or a rule-pruned cell** — re-emit it from the rule or call tree that generates it.

## Mechanical

● **Yes.** No human is involved and no judgement is made.

## What Must Be True Afterwards

* the regenerated element carries provenance naming every source with a checksum of its content **now**;
* nothing authored has been touched — a regeneration that edits a required effect has crossed the line the whole
  comparison rests on.

## Notes For P6

**Regenerating is mechanical; what happens next sometimes is not.** A regenerated behavior whose result no
longer matches what was approved raises `redesign-required`, which is human. So this resolution's tool produces
the new result and the comparison, and hands off rather than deciding.

**A match against a prior approval restores it without a human.** Nothing about what was approved has actually
changed, and asking for a fresh confirmation of a provably identical result would be re-litigating a decision
nobody disputed. A match with **no** prior approval refreshes provenance and stays `pending`: a match says the
record is consistent with the design, not that anyone has agreed it is right.

**Re-addressing must not trigger this**, because checksums normalize model addresses out of content. The one
deliberate exception is a derived diagram, where renaming an element really does change the labels in the
picture — and redrawing costs nothing.
