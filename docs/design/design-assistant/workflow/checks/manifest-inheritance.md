# manifest-inheritance

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §3.3.1 - inheritance, tightening, and why a contradiction is a finding

## Purpose

Does a contained design target tighten what it inherits rather than contradict it? You cannot change language
midway through a service, and a contained Library compiled into a different runtime is not contained at all —
it is a `dependsOn`.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [build-manifest](build-manifest.md) — there is nothing to compare until both manifests are assessed |

## What It Inspects

For every contained design target, each setting it declares against the same setting on its container:

* **tightening** is permitted — narrowing the approved dependency matrix, banning something more;
* **loosening** and **contradicting** are not.

This is the same accumulate-never-exempt shape NFR rules follow, and for the same reason: a part cannot relieve
itself of a constraint the whole is under.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `build-manifest-conflict` | a contained target's setting contradicts or loosens what it inherits | [correct-the-design](../resolutions/correct-the-design.md) · [raise-a-change-request](../resolutions/raise-a-change-request.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

A contradiction is a finding, **not a local override** — the resolution must never be to silently let the
contained target win.

Both directions are legitimate outcomes. Often the contained target is wrong and conforms. Sometimes the
container is wrong, and then the change belongs to the container's own design — which is
`raise-a-change-request`, and the finding becomes blocked.

**Extraction must materialise the inherited manifest before the target leaves.** A design target losing the
parent it was inheriting from would otherwise become an uncontained design target with no manifest at all, which
this check would then report as `unassessed-manifest-setting` across the board.
