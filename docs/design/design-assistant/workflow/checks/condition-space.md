# condition-space

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Condition Model](../../datamodel/condition-model.md) §1, §2, §4 - the space, its dimensions and its cells
* [Condition Model](../../datamodel/condition-model.md) §3.2 - the ranking convention

## Purpose

Does every operation have a condition space to be defined over? Coverage is asserted against this space, so
anything it does not contain is by definition not required — which makes the space the thing every completeness
claim in the design ultimately rests on.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [operation-contract](operation-contract.md) — parameter dimensions are over the signature |

## What It Inspects

For every operation, that it has a `ConditionSpace`, and that the space is structurally complete:

* **dimensions** — each with `slug`, `kind`, `rank`, `projection`, `source`, and at least one value; ranks
  unique within the space;
* **values** — each with `slug`, `ordinal` unique in its dimension, and a `predicate` stating what it means in
  terms the model can check;
* **cells** — the tree the ranked dimensions generate, each cell carrying what it `selects`, its `parent`, its
  `children` and its `status`.

It checks that the space is *there and well formed*. Whether the values actually partition anything is
[dimension-partitioning](dimension-partitioning.md); whether the cells are covered is
[cell-coverage](cell-coverage.md).

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | an operation has no condition space, or the space is missing dimensions, values, ranks, ordinals, predicates or cells | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M1`.

## Settings

None.

## Notes For P6

Only `payload` and `parameter` dimensions are expected here. `cross-cutting` dimensions accrete as each NFR
rule's selector resolves against real functions, and `dependency-state` dimensions once a call tree reveals
which dependencies the operation reaches — both later, both derived, and neither retrospectively missing now.

Accretion re-enters this level from above: a dimension added at `M3` adds cells, the cells are uncovered, and
the design falls back to `M1`. That is the mechanism working, and the resolution prose should say so, because a
design that reached `M3` and is told it is at `M1` reads as a regression unless the reason is legible.

Where nothing else dictates the order, `given` dimensions rank above `when` dimensions — state constrains which
invocations are meaningful, never the reverse — and ordering this way is also what lets pruning collapse whole
subtrees rather than rediscovering the same collapse under every variant.
