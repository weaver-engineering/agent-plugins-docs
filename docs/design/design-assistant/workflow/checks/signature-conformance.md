# signature-conformance

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §6.1.1 - conformance is compatibility, not identity
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §2.1 - `raises` as a contract

## Purpose

Do an operation and its realizing function agree? They are two facts at two addresses — the operation's
signature is its contract, settled at `M1` as part of stating what is required, and the function's is what the
code takes. What the design asserts is that they **conform**, which is a check between two facts rather than
one fact written twice.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [realization](realization.md) · [type-resolution](type-resolution.md) — a legitimate function, and types that resolve |

## What It Inspects

Three rules, for every operation and the function realizing it:

* **Parameters** — every parameter of the operation corresponds to a parameter of the function, of the same
  type. The function may declare **more**.
* **Return** — the function returns the operation's return type.
* **Exceptions** — the two declare the **same set**.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `signature-nonconformance` | any of the three rules fails | [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

**The surplus parameters are the point.** They are the translation layer's own — a correlation id, a context, a
capture mode this operation fixes and another exposes. A function obliged to match its operation exactly could
realize exactly one operation, and an `interface`-kind boundary whose whole job is translation would have
nothing left to translate.

**The exception rule is identity rather than compatibility**, because the realizing function *is* the perimeter:
whatever it declares in `raises` escapes to the consumer, so there is no room for a surplus to be absorbed. A
function that must not surface a domain failure catches it and declares its own translation instead. An
operation declaring an exception the function cannot produce promises a failure mode the design does not have,
and is the same finding from the other side.

**The return rule is identity for a narrower reason**: the dictionary has no subtype relation, so "the
operation's type, or narrower" is not a question this model can decide. If a subtype relation is ever added,
this is the rule that relaxes.
