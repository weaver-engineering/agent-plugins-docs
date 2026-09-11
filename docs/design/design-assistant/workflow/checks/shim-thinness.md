# shim-thinness

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §5.2 - `dependsOn`, and why only a dependency boundary may hold it
* [Deployable Model](../../datamodel/deployable-model.md) §3.2 - the host reached through shims like any other dependency

## Purpose

Is every dependency shim still a one-for-one translation? Only a `dependency`-kind boundary may hold
`dependsOn`, which is the rule that makes external interaction locatable: every outward crossing goes through a
shim, and every shim sits on a boundary whose kind says so. A shim that has acquired logic of its own breaks
that, because an external interaction is then partly described somewhere the model treats as a pass-through.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [function-placement](function-placement.md) — a shim is a placed function on a dependency boundary |

## What It Inspects

* every function on a `dependency`-kind boundary maps to **exactly one** operation of the boundary depended on;
* no boundary of any other kind holds `dependsOn`.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `shim-inconsistency` | a shim is not a one-for-one translation of a single depended-on operation | [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

The resolution is usually to move the logic rather than to remove it: whatever the shim acquired belongs on a
business-domain or shared-logic boundary that calls the shim.

This check is load-bearing for the condition space, not merely tidy. A `dependency-state` dimension is derived
from a dependency interaction found in the call tree — so a domain function reading a dependency directly, with
no shim, leaves no call-tree node to derive the dimension from, and the non-determinism cannot be brought into
the condition space at all. The shim is what makes the dependency coverable.

Only the crossings the design actually makes are defined. A design that reads the clock defines one shim
function and nothing else; there is no obligation to enumerate the host.
