# provenance-freshness

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §2 - provenance and what fresh means
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §4 - the one invalidation rule and its reach

## Purpose

Does every derivation still checksum to its sources? One rule: **when an element changes, every derived element
whose provenance names it becomes stale.** Everything else about invalidation is an application of it, which is
why provenance is uniform across every derived element rather than a bespoke block on one kind of artefact.

Staleness is not an error. It is a statement that this derivation needs re-running before anything built on it
can be trusted.

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [traces](traces.md) — the largest population of derived elements |

## What It Inspects

Every derived element — expected effects, traces, call trees, rule-pruned cells, generated dimensions, the call
graph, the function catalog — recomputing each source's checksum and comparing against what is recorded.

Checksums are computed over **content with addresses normalized**. Re-addressing is not a semantic change:
moving or renaming an element, re-ranking dimensions, or renumbering a dimension's values rewrites references
and changes no content, and must not make anything stale or clear any review.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `stale-provenance` | a derived element's sources no longer checksum to what is recorded | ● [regenerate](../resolutions/regenerate.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

Staleness propagates transitively and is computed by walking **backwards**, never by re-deriving forwards: a
changed function description reaches every behavior whose recorded call tree names it, found via `calledFrom`
and then the call trees. Reach is deliberately narrow — a behavior whose own call tree never reached the changed
function stays fresh, even when a sibling behavior of the same operation is invalidated.

Regenerating is mechanical, but what happens **next** is not always: a regenerated behavior whose result no
longer matches what was approved is a `redesign-required`, which is [regeneration](regeneration.md)'s finding
rather than this one's. This check establishes which derivations are stale; that one establishes what re-running
them produced.
