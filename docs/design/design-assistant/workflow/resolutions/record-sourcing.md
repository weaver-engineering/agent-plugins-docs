# record-sourcing

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Decision Model](../../datamodel/decision-model.md) §5, §5.1 - the three kinds and what they distinguish
* [Condition Model](../../datamodel/condition-model.md) §2.3 - sourcing on dimensions and values

## Purpose

Attach how an authored fact entered the model. Sourcing is the counterpart to provenance: provenance asks
whether a derivation is still valid, sourcing asks who is responsible for a fact nobody derived — and therefore
who may change it.

## Applies To

`unsourced-condition-dimension`, `unsourced-fact`.

## What It Does

Records a `kind` and a `basis`:

| Kind | Documented in | Changeable by | `basis` holds |
|---|---|---|---|
| `document` | a document outside this design's scope | change control against the owning document | the `ExternalRef`, with a checksum |
| `elicited` | a document inside this design's scope | the architect, directly | what was asked, and when |
| `inferred` | a document inside this design's scope | the architect, once they have approved it | what it was inferred from, and the reasoning |

Where no document inside the design states the fact yet, this resolution **writes one** — the architect may
supply it or have the process write it for them.

## Mechanical

No.

## What Must Be True Afterwards

* the fact is documented, whatever its kind — `elicited` does not mean undocumented;
* a `document` source carries its `ExternalRef` and checksum, so a change to it is detectable;
* an `inferred` fact has been approved, or is visibly awaiting approval.

## Notes For P6

**Every authored fact is documented.** A requirement that lives only in a conversation is not durable: it cannot
be reviewed, checksummed or invalidated. What varies is where the document sits and who may change it.

**`inferred` is the only kind an agent may assign to itself, and it is the weakest.** An agent filling a gap by
inference is often exactly right and is a large part of what makes the design assistant useful. The risk is not
that inference happens; it is that an inference presented alongside elicited and documented facts becomes
indistinguishable from them and is approved as though a human supplied it.

So this resolution must never let an agent record `elicited` for its own inference. That is the failure mode the
whole mechanism exists to prevent, and it is invisible once made.
