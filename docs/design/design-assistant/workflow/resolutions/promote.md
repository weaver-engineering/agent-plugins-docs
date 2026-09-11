# promote

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Boundary Model](../../datamodel/boundary-model.md) §3.1 - promotion and its defined effects
* [Boundary Model](../../datamodel/boundary-model.md) §7.5 - promotion splits selection
* [Write Contract](../../serialization/write-contract.md) §4 - a change of containment, and what moves

## Purpose

Make a contained boundary a design target of its own. Promotion is a **mechanical operation with defined
effects** — but deciding to pay for it is not, because a new design target needs its own design work, its own
ticket, its own review and its own NFR assessment.

## Applies To

`promotion-candidate`.

## What It Does

Once the decision is taken, the operation itself is mechanical and has five effects:

1. the boundary's functions enter the new target's catalog scope and leave the containing target's — **the
   functions do not move**, only which catalog spans them changes;
2. the functions its consumers call become its **operations**, and the behaviors those consumers required of
   them become its own required behaviors;
3. every cross-cutting boundary of the containing target whose selector reached into it is **split**, so nothing
   loses an NFR obligation at the moment of promotion;
4. fixtures standing in for the new target come into existence, where before the containing design's traces
   walked straight through;
5. artefacts move on disk — a `DESIGN.yaml` and an entry document are added, and where the boundary already
   occupies a directory, **no document moves at all**.

## Mechanical

The operation is; the decision is not. The move is **delegated to the tooling and never performed by hand** —
which is the condition under which path-derived addressing is affordable at all.

## What Must Be True Afterwards

* **no address changes.** Promotion changes a boundary's type in place, not its position, and an address nests
  through the boundaries that structure an element rather than the design target governing it;
* the new `DESIGN.yaml` declares its namespace, and either names a check configuration or says nothing and lets
  the walk resolve the containing design's — which is the ordinary case, and what keeps the promoted boundary
  assessed by exactly the configuration it was the moment before;
* the containing design's traces now stop at the promoted target, and **regenerate to the same expected
  effects**.

## Notes For P6

**Promotion should cost no human review**, and that is a property worth checking rather than assuming. Every
affected behavior should land in the "regeneration matches a prior approval, restore it" path. A promotion
producing a wave of `redesign-required` has changed something it should not have, and the finding to investigate
is the promotion rather than the behaviors it disturbed.

**A promoted directory with no configuration is unassessable from the moment it is promoted**, which is the one
way to get this wrong mechanically.

**Extraction and relocation are different operations and are not this resolution.** Extraction takes the target
out of containment entirely and re-roots its addresses into its own namespace; relocation moves it under a
different parent. Both change the boundary's *position*, and position is what an address is derived from.
Extraction additionally has to materialise the inherited build manifest before the target leaves, or it becomes
an uncontained design target with no manifest at all.
