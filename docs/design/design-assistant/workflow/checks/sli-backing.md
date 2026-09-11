# sli-backing

## Context
* [Workflow](../WORKFLOW.md) §4.7 - where this check is registered
* [Deployable Model](../../datamodel/deployable-model.md) §5.3 - what the model adds to the standard
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §6 - metrics, defined by their emitting functions

## Purpose

Does every SLI measure something the design emits and the operation reaches? An SLI whose queries reference a
metric no function emits measures something the design does not produce. One referencing a metric the operation
cannot reach is the same defect from the other direction.

## Registration

| | |
|---|---|
| Stage | maturity — `M5` |
| Model check | yes |
| Requires | [sli-validation](sli-validation.md) · [traces](traces.md) — a valid definition to read queries from, and call trees to decide reach |

## What It Inspects

`combines` is **derived** by reading the metric queries in the definition and resolving them against the metrics
the design's own functions emit. Two conditions:

* every metric named resolves to one a function in this design emits;
* every metric named is emitted by a function **that operation reaches**, which the behaviors' call trees
  record.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unbacked-sli` | an SLI's queries reference a metric no function emits, or one its operation cannot reach | [state-the-fact](../resolutions/state-the-fact.md) · [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M5`.

## Settings

None.

## Notes For P6

**This is the check that closes the observability loop.** Metrics are emitted as effects on behaviors, so an SLI
resolving to real metrics is transitively an SLI resolving to something a behavior actually causes under a known
entry condition.

The architect **authors the queries**, which name metrics explicitly; what is mechanical is only resolving those
names against what the design's functions emit. That is why an SLI querying a metric nothing emits is a finding
rather than an empty derivation.

`state-the-fact` is the route where the metric should exist and does not — the function that would emit it gains
it, and the behaviors that reach it gain the effect. `correct-the-design` is the route where the query is wrong.

A deployable boundary's SLIs may combine metrics emitted by functions **anywhere inside it**, including in
contained boundaries and contained design targets it did not author. That is the intended direction: the service
is what is measured, whoever emitted the numbers.
