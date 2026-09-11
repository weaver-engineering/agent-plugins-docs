# accept-the-regeneration

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.3 - resolving `redesign-required`

## Purpose

The design's evolution is right and the recorded behavior is stale. The design moved deliberately, the trace now
produces something different, and what it produces is what the design should be doing.

## Applies To

`redesign-required`.

## What It Does

1. Presents what regenerated against what was recorded, concretely enough that the difference is the thing being
   judged rather than the summary of it.
2. Replaces the recorded expected effects with the regenerated result.
3. Returns the behavior to `pending`.

## Mechanical

No. The regeneration itself is mechanical; deciding that its result is the right one is not.

## What Must Be True Afterwards

* the recorded expected effects are the regenerated ones, with fresh provenance;
* the review state is `pending`, **never `approved`**;
* the behavior is presented for approval again through [approve](approve.md), which the next run will ask for.

## Notes For P6

**Accept never returns straight to `approved`.** What ends up recorded is not the thing that was originally
approved — it is a new result — and returning straight to approved would mean trusting an outcome nobody has
looked at, which defeats the purpose of having detected the disconnect at all.

The same holds for the reject route, which is [correct-the-design](correct-the-design.md): a design that reaches
the old result by a new route is still not the thing that was approved.

**Where the address belongs to work that has already shipped**, accepting a changed behavior has a consequence
past the design: code was produced from the now-superseded behavior. That is downstream of this workflow and
needs its own handling, but the resolution should say so rather than presenting the acceptance as free.

**A wave of these after a promotion is a finding about the promotion.** Promotion should regenerate to the same
expected effects, so accepting a wave of differences would quietly ratify a restructuring that changed the
design. The right response there is to investigate the promotion, not to work through the behaviors.
