# operation-identity

## Context
* [Workflow](../WORKFLOW.md) §4.2 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §6 - what an operation is, and why it is not an endpoint
* [Data Model](../../datamodel/DATA-MODEL.md) §5.2 - named operations as `M0`'s own requirement

## Purpose

Can this boundary be asked to do anything, and is each of those things named? An operation is a point on the
design target's perimeter at which it can be invoked from outside itself, and a design target with none has not
yet said what it is for.

## Registration

| | |
|---|---|
| Stage | maturity — `M0` |
| Model check | yes |
| Requires | [boundary-identity](boundary-identity.md) — there is nothing to hang an operation on until the boundary is identified |

## What It Inspects

* the design target has **at least one** operation;
* every operation has a `slug`, unique on its boundary;
* every operation has a `purpose` — what invoking it is for.

It checks this for every design target in scope, including contained ones. It does not check the signature,
which is `M1` and belongs to [operation-contract](operation-contract.md).

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | a design target has no operations, or an operation lacks slug or purpose | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M0`.

## Settings

None.

## Notes For P6

"This boundary has no operations" is the single most common first finding a new design will see, and it is the
start of the design conversation rather than a defect — the resolution prose should read as elicitation, not as
a correction. It is the point at which "I have an idea" becomes a boundary that can be designed.

A contained boundary that is **not** a design target correctly has no operations, and must not be reported. What
it must *do* follows from the required behaviors of its consumers.
