# authored-sourcing

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Condition Model](../../datamodel/condition-model.md) §2.3 - sourcing on dimensions and values, and why its absence is a finding
* [Decision Model](../../datamodel/decision-model.md) §5 - the three sourcing kinds and what they distinguish
* [Behavior Model](../../datamodel/behavior-model.md) §2.1 - required effects are authored and carry sourcing

## Purpose

Does every authored fact record how it entered the model? Sourcing is the counterpart to provenance: provenance
asks whether a derivation is still valid, sourcing asks who is responsible for a fact nobody derived, and
therefore who may change it.

A list of dimensions cannot distinguish "these are the behaviour-affecting variations, and they were
considered" from "these are the ones somebody happened to write down", and only the first supports a coverage
claim. Recording the basis is what makes the difference legible at review.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [condition-space](condition-space.md) — the dimensions and values to be sourced |

## What It Inspects

Every **authored** fact this check requires sourcing for:

* an authored `ConditionDimension` — how the fact that these are the behavior-affecting variations entered the
  model;
* an authored `ConditionValue` — how the bucketing did, which is the part that is pure judgement;
* an authored `RequiredEffect` — how the demand entered the model.

A **derived** dimension or value carries provenance instead and is not this check's business; a derived
dimension may still have authored values, and those are.

Each must name a `kind` — `document`, `elicited` or `inferred` — and a `basis`.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unsourced-condition-dimension` | an authored dimension or value carries no `Sourcing` | [record-sourcing](../resolutions/record-sourcing.md) |
| `unsourced-fact` | an authored required effect carries no `Sourcing` | [record-sourcing](../resolutions/record-sourcing.md) |

`unsourced-condition-dimension` blocks **the checkpoint at which that dimension or value becomes required**, so
its `blocking` is `computed`: a `payload` or `parameter` dimension and its values at `M1`, a `dependency-state`
dimension's values at `M3`, a `cross-cutting` dimension's values wherever its rule's selector resolves. That is
what keeps accretion intact — a dimension arriving at `M3` is not retrospectively unsourced at `M1`.

## Settings

None.

## Notes For P6

Analysis *should* define the dimensions and values a service must behave over, and analysis cannot block design.
Where the feed-in does not define them it falls to the architect's assertion, and doing that analysis is then
the architect's job. Both are complete answers; what is not an answer is silence.

`inferred` is the only kind an agent may assign to itself and it is the weakest: a design may hold inferred
facts, and may not hold inferred facts nobody has looked at. The resolution has to carry that distinction, since
an inferred condition presented as though it came from a use case is the exact failure mode this exists to
prevent.
