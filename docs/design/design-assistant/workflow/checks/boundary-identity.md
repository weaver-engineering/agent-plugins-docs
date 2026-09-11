# boundary-identity

## Context
* [Workflow](../WORKFLOW.md) §4.2 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §1, §2 - the attributes a boundary carries and the three levels
* [Data Model](../../datamodel/DATA-MODEL.md) §5.2 - why `M0` is a checkpoint rather than an entry requirement

## Purpose

Is every boundary the design has named actually identified? This is the floor of the model — a design target
with an identity and nothing else is a legitimate state, and this check is what says when even that much is
missing.

## Registration

| | |
|---|---|
| Stage | maturity — `M0` |
| Model check | yes |
| Requires | [claim-competition](claim-competition.md) — a contested attribute has no value to check |

## What It Inspects

For every boundary in the design's scope:

* `slug` — unique among its parent's contained boundaries;
* `name`;
* `purpose` — what this boundary is responsible for;
* `kind` — one of `interface`, `business-domain`, `shared-logic`, `dependency`, required when the boundary is
  contained and unset when it is not.

And one fact about the design as a whole: **the root of a design is a `SpecifiableBoundary`**. You never begin a
design from a bare `FunctionalBoundary`, because being designed is what makes something a design target.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | any of the above is unclaimed for a boundary in scope | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |

One finding per boundary, naming every attribute of that boundary this check requires and does not find. Blocks
`M0`.

## Settings

None.

## Notes For P6

The interesting resolution here is rarely typing a name. A boundary with no purpose usually means the boundary
was named in passing by a decision about something else, and settling what it is responsible for is real design
work — which is why `take-a-decision` is a route and not merely `state-the-fact`.

A root that is not a design target is a modelling mistake rather than an absent attribute, and its detail should
say so rather than reporting a missing `kind`.
