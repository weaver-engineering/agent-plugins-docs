# archetype

## Context
* [Workflow](../WORKFLOW.md) §4.7 - where this check is registered
* [Deployable Model](../../datamodel/deployable-model.md) §5.1 - the archetype and the dimensions it demands

## Purpose

What kind of delivery is this? The archetype is not descriptive: it determines which dimensions of service
delivery must have an SLI, which is what turns "observability is important" into a coverage claim the model can
check.

## Registration

| | |
|---|---|
| Stage | maturity — `M5` |
| Model check | yes |
| Requires | [boundary-identity](boundary-identity.md) — an archetype belongs to an identified deployable boundary |

## What It Inspects

Every `DeployableBoundary` has one `ServiceArchetype`:

| Archetype | SLI dimensions it demands |
|---|---|
| `request-response` | availability, latency, quality |
| `batch` | coverage, correctness, freshness, throughput |
| `storage` | durability, throughput, latency |

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | a deployable boundary has no archetype | [state-the-fact](../resolutions/state-the-fact.md) |

Blocks `M5`.

## Settings

None.

## Notes For P6

A composite may contain boundaries of **different** archetypes — a database service is `request-response` at its
server and `storage` at its files — so this is asked per deployable boundary rather than once per design.

The archetype answers "which delivery dimensions", and criticality answers "which operations". Neither
substitutes for the other, and [sli-coverage](sli-coverage.md) is the product of the two.
