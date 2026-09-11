# metric-emitters

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §6.2 - several emitters of one metric
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §3.1 - advisory findings and acknowledgement

## Purpose

Does any metric have more than one emitter? It usually means the emission belongs in a shared function, or that
one metric is doing the work of two — and it is legitimately what you want where a single error counter is
incremented on several distinct failure paths.

The model cannot tell which, so it says so rather than guessing.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [function-descriptions](function-descriptions.md) — `emits` must be stated before emitters can be counted |

## What It Inspects

Every metric slug, and the set of functions declaring it in `emits`.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `duplicate-metric-emitter` | more than one function emits one metric | [correct-the-design](../resolutions/correct-the-design.md) · [acknowledge](../resolutions/acknowledge.md) |

**Advisory**: it does not block on its content, and blocks `M4` while neither corrected nor acknowledged. Being
detected mechanically, leaving it unanswered is not a decision anyone made — the finding is a unit of work like
any other, and the work is a judgement rather than an edit.

## Settings

None.

## Notes For P6

**Acknowledgement is scoped to the instance, not the kind.** Accepting one metric with two emitters says nothing
about the next one, which is the point: a blanket suppression would turn the detector off, while an
instance-level record leaves every future occurrence still to be judged.

An acknowledgement carries provenance: if the set of emitters changes, the acknowledgement no longer applies to
what is now there and the finding is raised again unanswered. If the duplication disappears entirely, the
acknowledgement is spent and is deleted mechanically — nothing re-examinable is lost, because the instance it
was about is gone.
