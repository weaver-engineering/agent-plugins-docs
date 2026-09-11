# sli-coverage

## Context
* [Workflow](../WORKFLOW.md) §4.7 - where this check is registered
* [Deployable Model](../../datamodel/deployable-model.md) §5.1 - the product over operations and dimensions
* [Deployable Model](../../datamodel/deployable-model.md) §5.2 - the `SLI` and what it holds

## Purpose

Does every critical operation have an SLI for every delivery dimension its archetype requires? This is a
**product over operations and dimensions**, not a single per-boundary check — a request/response service does
not have one latency SLI, it has a latency SLI per operation a consumer depends on.

## Registration

| | |
|---|---|
| Stage | maturity — `M5` |
| Model check | yes |
| Requires | [archetype](archetype.md) · [criticality](criticality.md) — the two answers whose product this is |

## What It Inspects

For every operation flagged `critical`, and every delivery dimension the boundary's archetype demands: that an
`SLI` exists naming that operation and that dimension, carrying its `slug`, `definition` and `specVersion`.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `missing-sli` | a critical operation has no SLI for a dimension its archetype requires | [state-the-fact](../resolutions/state-the-fact.md) · [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M5`.

## Settings

None.

## Notes For P6

**This kind is a gap in the default set that P5 identified**: `invalid-sli-definition` and `unbacked-sli` both
presuppose an SLI exists, so nothing reported the absent case. It folds into the metamodel's own table rather
than being defined only here.

`correct-the-design` is a real route: the honest resolution is sometimes that the operation is not actually
critical, which is a correction to the flag rather than a missing SLI. That must go through
[criticality](criticality.md)'s own fact and its sourcing, not be assumed here.

For `batch` and `storage` the product usually collapses to close to a per-boundary check, since those typically
have a single entry point — but that is a property of those archetypes rather than a different rule.

The **SLO** that monitors an SLI stays outside the design. The design owns the measurement; the Product owns the
promise about acceptable values of it.
