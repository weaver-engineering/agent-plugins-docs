# realization

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §6.1 - realization and its three placement rules

## Purpose

Does every operation name a function that could realize it? The realizing function is where a trace starts, so
an operation without one has no entry point for anything at `M3` to walk from — and one naming the wrong
function has an entry point that does not exist on its perimeter.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [function-placement](function-placement.md) · [operation-contract](operation-contract.md) — both ends must exist |

## What It Inspects

For every operation, that `realizedBy` is present and that the function it names:

* is **contained by this design target**, transitively;
* is **not inside a contained design target**;
* is **on the `interface`-kind boundary**, where the target contains one.

`realizedBy` is **not exclusive**. One function may realize several operations, each exposing a different part
of that function's parameter space — one exposing a capture mode the others fix, one exposing a caller identity
the others take from context. Several operations naming one function is correct, not a duplicate.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | an operation has no `realizedBy` | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |
| `invalid-realization` | the named function is outside this target, inside a contained one, or off the interface boundary | [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

Naming a function inside a contained design target is the interesting failure, and it usually means the
containment is wrong rather than the reference. An operation realized inside a black box would let the
containing design's trace walk somewhere it is not entitled to look — so the resolution should examine whether
that boundary should have been promoted, or whether this operation belongs to it rather than here.

Whether the two signatures agree is [signature-conformance](signature-conformance.md), which requires this
check: there is nothing to compare until the realizing function is a legitimate one.
