# exempt

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Boundary Model](../../datamodel/boundary-model.md) §7.3 - why an exemption must be declared rather than inferred
* [Deployable Model](../../datamodel/deployable-model.md) §3.1 - the same rule on the perimeter

## Purpose

Record that this has no referent here, with a reason. An exemption is an **answer**, not a blank — and the whole
value of a closed enumeration is being able to assert that every item was examined, which requires the examining
to leave a record.

A design with no auth boundary and a design that has decided none of its functions need one are
indistinguishable if silence is permitted, and the difference is the point of the assessment.

## Applies To

`unassessed-manifest-setting`, `unassessed-nfr-rule`, `unassessed-perimeter-vector`, `unresolved-selector`.

## What It Does

1. Establishes that nothing in this design has a referent for the item — no function on that NFR boundary,
   nothing crossing that perimeter vector, no build stage of that kind.
2. Records the exemption against the item, with the reason.

## Mechanical

No. Whether something has a referent here is exactly the local judgement the assessment is asking for.

## What Must Be True Afterwards

* the exemption names the item exempted and carries a reason a later reader can disagree with;
* it is a claim in the design, reviewable and falsifiable like any other.

## Notes For P6

**An exemption is a claim, not a silence**, which is what makes it useful later: a Product can read every
design's exemptions together and identify ones that have stopped being true. A reason of "not applicable" gives
a reader nothing to check and should be pushed back on.

Exemption is often the *right* answer and should not be framed as a lesser one. A Library genuinely has no
container build stages; a single-package repository has no module structure worth stating; a service that reads
no files genuinely has nothing on `mounted-file`.

It is not available for an NFR rule the design **does** apply somewhere — a rule is applied or exempted, and
applying it to some functions while exempting others is a selection decision, not an exemption.
