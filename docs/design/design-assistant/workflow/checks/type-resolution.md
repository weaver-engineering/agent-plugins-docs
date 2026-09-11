# type-resolution

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Data Dictionary](../../datamodel/data-dictionary.md) §2.1 - ownership and outward resolution
* [Data Dictionary](../../datamodel/data-dictionary.md) §2.2 - referencing across namespaces
* [Data Model](../../datamodel/DATA-MODEL.md) §5.1.1 - how an unprefixed address resolves

## Purpose

Does every name in a signature resolve to a definition? A design target with type names in its signatures and
no definitions to resolve them against is legal below `M2` and a finding at or above it.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [type-definitions](type-definitions.md) — nothing resolves until the definitions exist |

## What It Inspects

Every type reference in every signature, field and dimension source. An **unprefixed** address resolves by
walking outward from the referencing boundary, through each boundary containing it and onward through
containing design targets, taking the nearest definition, up to the root of the current namespace. A
**prefixed** address resolves in the named namespace's own address space.

The walk cascades **through** containing design targets: a promoted domain resolves a type its parent service
defines with no prefix and no restatement, because a design target bounds authority and tracing, not naming.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unresolved-type` | a signature names a type the dictionary does not define | [state-the-fact](../resolutions/state-the-fact.md) · [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

Two resolutions, and which is right is a real question. Either the type genuinely needs defining — on the
boundary entitled to define it, which is the nearest one containing everything that uses it — or the reference
is wrong, and the name should be the one already defined somewhere the walk reaches.

A shape shared across several contained boundaries is defined **once**, on the boundary containing them all. A
resolution that defines it separately per consumer produces a type the dictionary now holds twice under two
addresses, which nothing detects as a duplicate because they are two different types.

Naming a type across a namespace does not make its design a dependency of anything — no `dependsOn`, no shim, no
interaction. It names a shape defined elsewhere and nothing more.
