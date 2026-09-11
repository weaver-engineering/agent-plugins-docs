# element-identity

## Context
* [Workflow](../WORKFLOW.md) §4.2 - where this check is registered
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §1.2 - a function's lifecycle, and what it carries at `M0`
* [Boundary Model](../../datamodel/boundary-model.md) §7.1 - the cross-cutting boundary's own `M0` attributes
* [Claim Model](../../serialization/claim-model.md) §6 - naming an address is what brings it into existence

## Purpose

Is every other element the design has named so far identified? Naming an address is what brings an element into
the model, so a design accumulates elements that have been referred to and not yet described — a function named
by a key decision, a cross-cutting boundary named by an assessment. Those are legitimate and incomplete, and
this check is what stops them staying that way silently.

## Registration

| | |
|---|---|
| Stage | maturity — `M0` |
| Model check | yes |
| Requires | [boundary-identity](boundary-identity.md) — an element's identity is checked against the boundary structuring it |

## What It Inspects

For every **function** in scope: `slug`, unique on its boundary, and `purpose`, one line of what it does. A
function may legitimately be nothing more than these at `M0` — it becomes addressable, which is what lets the
rest of the design reference it before it is finished.

For every **cross-cutting boundary** in scope: `slug`, unique on the design target, and `kind`, one of
`security`, `resilience`, `concurrency`, `state-transaction`.

It does not check placement, signature or selection — those are `M2`, and belong to
[function-placement](function-placement.md) and [selector-resolution](selector-resolution.md).

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | a function or cross-cutting boundary in scope lacks its `M0` attributes | [state-the-fact](../resolutions/state-the-fact.md) · [remove-the-element](../resolutions/remove-the-element.md) |

Blocks `M0`.

## Settings

None.

## Notes For P6

`remove-the-element` is a real route here and not a formality. An element with almost no attributes is exactly
what a **missed rename** looks like: re-addressing must rewrite every claim naming the moved element, and a
claim that was missed goes on asserting the old address exists. The old element then surfaces here as
conspicuously unfinished work, which is the model reporting the mistake without being asked.

So the resolution prose should ask which of the two this is — an element genuinely awaiting description, or the
residue of a rename — before offering to fill anything in.
