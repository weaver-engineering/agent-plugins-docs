# call-declarations

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §5 - call tree reconciliation and its two causes
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §4 - the forward invariant

## Purpose

Was every traced call declared? Every call tree node's function must appear in the `calls` declared by its
parent node's function. A call actually traced but never declared means either a stale declaration or a call
nobody decided on.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [traces](traces.md) — there is no call tree to reconcile until a trace has produced one |

## What It Inspects

Every node of every recorded call tree, against the `calls` declared by its parent's function.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `call-declaration-mismatch` | a call tree node is absent from its parent function's declared `calls` | ● [regenerate](../resolutions/regenerate.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

**The model records which of the two causes it was, because they have different consequences for provenance.**

* A **documentation error** — the `calls` list is stale or mistyped — is corrected directly. It changes no
  description and invalidates nothing.
* A **genuine gap** — the call was never actually decided — returns to the decision that owns it. It changes a
  function and invalidates everything downstream of it.

Treating the second as the first is the failure worth designing against: correcting the list would make the
design assert a call nobody chose, with the trace that revealed it now looking like confirmation.

So the mechanical route is only available once the resolution has established that the call was decided and the
declaration merely missed it.
