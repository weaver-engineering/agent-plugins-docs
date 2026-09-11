# acknowledge

## Context
* [Workflow](../WORKFLOW.md) §2.5 - soft resolution
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §3.1 - advisory findings and acknowledgement
* [Parse Contract](../../serialization/parse-contract.md) §7 - how an acknowledgement keys onto a recomputed finding

## Purpose

Record that this instance is correct despite the pattern. Some patterns are usually wrong and legitimately right
often enough that a gate would be worse than a note — and where the model genuinely cannot tell which case this
is, the honest resolution is a person saying so, on the record.

## Applies To

`duplicate-claim`, `duplicate-metric-emitter`, `unresolved-nfr-scope`, `boundary-over-budget`,
`promotion-candidate`.

## What It Does

Records an `Acknowledgement` against the finding's subject:

| Attribute | Holds |
|---|---|
| `acknowledgedBy` | the architect accepting this instance |
| `acknowledgedAt` | when |
| `reason` | why this instance is correct despite the pattern |

## Mechanical

No — and it is the one resolution whose whole content is a judgement.

## What Must Be True Afterwards

* the finding is **soft-resolved**: still reported, no longer a unit of work;
* the level the finding would otherwise block is achievable;
* the acknowledgement keys onto the finding's kind, subject, and a digest of the **condition** that produced it.

## Notes For P6

**Acknowledgement is scoped to the instance, not the kind.** Accepting one metric with two emitters says nothing
about the next one. A blanket suppression would turn the detector off; an instance-level record leaves every
future occurrence still to be judged.

**The condition digest is what makes cumulative findings work.** An acknowledged boundary spend of 1
acknowledges a spend of **1**. At 2 the condition differs, the acknowledgement no longer matches, and the
finding is raised unanswered — to be resolved by reducing the spend or acknowledging the new one.

**A spent acknowledgement is deleted.** If the condition disappears entirely — the duplication removed by a
decision that had nothing to do with the finding — the acknowledgement says nothing about the present and is
removed mechanically, surfacing nothing. If the same condition later recurs, it is judged afresh: answering a
new occurrence from a record made about an old one is exactly the blanket suppression instance-scoping exists to
rule out, arrived at by accident and silently.

So the matching pass runs **both ways**: computing findings and looking up each one's acknowledgement can never
see an orphan, and the same pass must walk the recorded acknowledgements and confirm each still has a finding to
answer. No acknowledgement is retired while an `unparsed-document` stands, because the model is then
known-incomplete and the finding that would have matched may simply not have been computable.
