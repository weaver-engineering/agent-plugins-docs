# calls-index

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §4 - the reverse invariant
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §4.2 - what the index is for

## Purpose

Does the reverse index still agree with the declarations it is built from? `calledFrom` is materialized rather
than computed on demand, because invalidation walks it constantly from arbitrary starting points across a whole
project — and anything materialized can go stale.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [function-descriptions](function-descriptions.md) — `calls` is the authored fact the index is built from |

## What It Inspects

Every entry of the materialized `calledFrom` index against the `calls` declarations across the design, in both
directions: an entry with no declaration behind it, and a declaration with no entry in front of it.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `calls-index-mismatch` | the index disagrees with the declarations | ● [regenerate](../resolutions/regenerate.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

**Fully mechanical, and the only check here where one side is right by definition.** This is a staleness check on
a cache, not a reconciliation between two independent claims: a function declares what it calls, so where the
index and the declarations disagree the declarations are right and the index is rebuilt. There is no judgement
and no alternative resolution.

Both directions are needed for the same reason the acknowledgement sweep and the deleted-document check are: a
forward pass over what exists cannot see what has stopped existing, so the pass has to walk from the records
back to their referents as well as forward.
