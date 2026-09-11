# fixture-suitability

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §3.2 - the possible set and the chosen set

## Purpose

Can every cell be traced against something concrete? A cell's **possible** fixture set is derived — the fixtures
exposing **every** value the cell selects — and its **chosen** set is a selection from it. A cell whose possible
set is empty has no concrete state it could be traced against.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [fixture-presence](fixture-presence.md) — the possible set is derived from what the values claim |

## What It Inspects

For every valid leaf cell:

* its **possible** set is non-empty, taken per fixture role — one payload fixture has to exhibit all of that
  cell's payload values **at once**, not one of them each;
* its **chosen** set is drawn from the possible set: one fixture for the payload, one for the output, and one
  per dependency the cell's condition puts in a state.

The possible set de-duplicates by fixture identity, not by value: two values one cell selects may name the same
fixture, and it appears once.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `no-suitable-fixtures` | a cell's possible fixture set is empty | [state-the-fact](../resolutions/state-the-fact.md) · [prune-the-cell](../resolutions/prune-the-cell.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

The interesting failure is a combination nothing realizes **while every value in it is individually covered** —
`order-value >= 1000` and `payment-method: crypto` may each have fixtures of their own while no single payload
exhibits both. That is the case `missing-fixture` cannot see, and it is why the possible and chosen sets are
distinguished rather than collapsed into a union.

`prune-the-cell` is a real route and needs care. Sometimes nothing realizes the combination because the
combination cannot occur — which is a validity rule waiting to be written, and writing it is the better
resolution because it prunes mechanically and re-derives. Sometimes nothing realizes it because nobody has built
the fixture yet, and pruning would quietly remove a requirement.
