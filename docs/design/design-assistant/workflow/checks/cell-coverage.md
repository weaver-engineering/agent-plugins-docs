# cell-coverage

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §1 - behaviors exist only at leaves
* [Condition Model](../../datamodel/condition-model.md) §2.2 - accretion, and why added cells are uncovered

## Purpose

Does every valid leaf cell have a behavior, and does that behavior require something? This is the coverage claim
itself: every entry condition that can actually occur has a statement of what must happen.

A cell is covered by a behavior or collapsed by a rule. A cell in neither is outstanding work.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [condition-space](condition-space.md) · [cell-exclusions](cell-exclusions.md) — an unexplained exclusion is not yet a decision about coverage |

## What It Inspects

Every `valid` leaf cell in every operation's condition space:

* it has a `Behavior`;
* that behavior carries **at least one** `RequiredEffect`.

A non-leaf cell has no behavior of its own and is not inspected — its outcome is not determined until a child
resolves it.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `uncovered-cell` | a valid leaf cell has no behavior | [state-the-fact](../resolutions/state-the-fact.md) · [prune-the-cell](../resolutions/prune-the-cell.md) |
| `unstated-required-attributes` | a behavior exists but requires nothing | [state-the-fact](../resolutions/state-the-fact.md) |

Blocks `M1`.

## Settings

None.

## Notes For P6

This is the check whose findings are most often many at once, and the clearest case for the unit of work being
the check rather than the finding: a dimension added to an operation of any size adds cells by the dozen, and
they are one sitting. Re-running between resolutions matters here more than anywhere — settling one behavior
frequently settles several neighbours.

An `invalid-behavior` at a cell does **not** also raise `uncovered-cell`. The cell is effectively uncovered, so
the two overlap, and `invalid-behavior` is the more informative: it says there is something here to re-express,
where this finding says only that there is nothing.

A required effect may be prose at `M1`. Predicates are not required until `M4`, because an effect is often first
captured as prose during elicitation and the point of `M1` is to settle what is required, not how it will be
checked.
