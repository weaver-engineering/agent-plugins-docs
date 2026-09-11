# orphan-functions

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §4 - the call graph derived from `calls`
* [Decision Model](../../datamodel/decision-model.md) §3.2 - superseded elements are deleted, not left standing

## Purpose

Is every function reachable from an operation or called by something? A function nobody calls and no operation
reaches is either evidence that a decision was made and not recorded, or the residue of a decision that was
superseded and left its elements standing.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [function-placement](function-placement.md) — reachability is over placed functions |

## What It Inspects

Every function in the design target's catalog, for whether it is reachable from an operation's realizing
function through `calls`, or named in some other function's `calls`.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `orphan-function` | a function is neither reachable from an operation nor called by anything | [correct-the-design](../resolutions/correct-the-design.md) · [remove-the-element](../resolutions/remove-the-element.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

Both routes are common and they mean opposite things. Either the function is wanted and something should call it
— a call nobody declared — or it is left over and should go.

The second case is what consolidation produces: when two decisions turn out to want the same function, one
supersedes the others and **the elements they produced are deleted**. A reader or a script has no way to
distinguish a deliberately-retained obsolete function from one nobody noticed was orphaned, which is exactly why
the model deletes rather than marking.

At `M2` the `calls` declarations may be incomplete — they are not required until `M3` — so this check will
report functions that a later declaration would have reached. That is correct rather than premature: it surfaces
the missing declaration early, when it is cheap.
