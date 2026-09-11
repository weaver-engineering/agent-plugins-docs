# design-authority

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §3.2 - authority and change requests
* [Decision Model](../../datamodel/decision-model.md) §4 - the `ChangeRequest` and the blocked state

## Purpose

Has this design changed something it does not own? A design target's operations and behaviors may only be
changed by its own design. If a boundary was complex enough to earn its own design, then changing what it
promises is design work on *that* boundary, not a side effect of work on a neighbour.

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [boundary-identity](boundary-identity.md) — authority follows from which boundaries are design targets |

## What It Inspects

Every claim this design makes whose `_target` is an operation or behavior belonging to **another** design
target.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unauthorized-change` | a design has altered an operation or behavior belonging to another design target | [correct-the-design](../resolutions/correct-the-design.md) · [raise-a-change-request](../resolutions/raise-a-change-request.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

The resolution is nearly always the same shape: withdraw the claim, and raise a change request for the change
that was wanted. The finding is then blocked on the ticket, which is the honest state — the design needs
something it cannot have yet.

Raising a change request and blocking is what makes the dependency visible and schedulable. It also gives the
model an honest terminal state — blocked, incomplete, not failing — instead of forcing a design either to
overreach or to pretend it is finished.

A design target bounds **authority and tracing, not naming**. Reading a containing design's type definition is
not changing it, and must not be reported here.
