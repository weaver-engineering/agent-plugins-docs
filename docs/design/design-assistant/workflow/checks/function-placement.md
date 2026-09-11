# function-placement

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §1, §1.1 - a function's attributes and its visibility
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §3 - interfaces and how membership is declared

## Purpose

Does every function have a boundary, a visibility, an interface where it needs one, and a signature? Every
function belongs to exactly one boundary — that is what makes the boundary graph a partition of the design's
logic rather than a loose grouping — and a function missing its placement is a hole in that partition.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [element-identity](element-identity.md) — a function must be identified before it can be placed |

## What It Inspects

For every function in the design target's catalog — its own subtree down to, but not into, any contained design
target:

* `boundary` — the single boundary it belongs to;
* `visibility` — `perimeter` or `private`;
* `interface` — required only when `visibility` is `perimeter`; every perimeter function is a member of exactly
  one interface;
* `signature` — parameters with names, positions and types; return type; declared exceptions.

And for every interface: its `slug` and `purpose`.

`Interface.members` is derived from `Function.interface` and is never inspected — deriving the weaker direction
from the stronger one removes the possibility of disagreement rather than adding a check for it.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | a function or interface is missing what `M2` requires of it | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

A `private` function is not "on no boundary" — it is not on its boundary's *perimeter*. Keeping membership total
is what makes the partition exception-free while leaving the data dictionary's obligation scoped to what
actually crosses.

The boundary a function belongs to is frequently a plain `FunctionalBoundary` — shared logic, an unpromoted
business domain — and the function's definition belongs **there**, not to the design target above it. What the
design target owns is the catalog. Getting this backwards is what makes promotion look like it should re-address
things, and it does not.
