# mock-consistency

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §3.1 - mock consistency and why trace termination depends on it
* [Boundary Model](../../datamodel/boundary-model.md) §3 - mockability and trace-bounding as one property

## Purpose

Does every mock agree with the design it stands for? A `stub` or `mock` declares the result of an execution that
crosses a boundary — which is a claim about what the other side does, and a claim nobody checks is an assumption
written down.

This is what makes trace termination sound rather than merely convenient. A trace stops at a contained design
target because that target's declared behavior is authoritative; a mock contradicting it would let the
containing design derive expected effects from something the mocked design never agreed to.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [fixture-presence](fixture-presence.md) — the fixtures whose claims are checked |

## What It Inspects

For every `stub` or `mock` whose `standsFor` names an operation of a **contained design target**: that there
exists a behavior of that operation whose expected effects match what the fixture declares.

Where the fixture stands for an **unmodelled** `dependsOn` boundary there is nothing to reconcile against, and
the fixture is simply authored. The check applies where the other side exists in the model, and not otherwise.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `mock-inconsistency` | a stub or mock declares a result no behavior of the operation it stands for produces | [correct-the-design](../resolutions/correct-the-design.md) · [raise-a-change-request](../resolutions/raise-a-change-request.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

Two resolutions with opposite owners, and choosing between them is the judgement. Either **this** design's mock
is wrong and should match what the other side actually produces — or the other side is wrong, and the operation
should produce what this design needs. The second is not this design's to change: it raises a change request and
blocks.

The fixture's provenance names the mocked operation and its behavior, so a change on the other side invalidates
the fixture — and therefore every behavior traced against it — by the ordinary invalidation rule. A mock stands
in for a design target; it does not insulate anything from it.
