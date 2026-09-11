# regeneration

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.2 - regeneration and its three outcomes
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.3 - resolving `redesign-required`

## Purpose

Does re-deriving a stale behavior reproduce what was approved? When a behavior's provenance goes stale its trace
is re-run against the current design and the result compared with what is recorded. The comparison has three
outcomes and only one of them is work.

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [provenance-freshness](provenance-freshness.md) — which behaviors are stale is that check's answer |

## What It Inspects

Every behavior whose provenance is stale:

| Outcome | What happens |
|---|---|
| matches, and the behavior was previously `approved` | restore the approval and refresh provenance — **no human involved** |
| matches, and the behavior was never approved | refresh provenance; it stays `pending` |
| does not match | raise `redesign-required`, recording what regenerated against what was recorded |

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `redesign-required` | regeneration produced a result that does not match what was reviewed | [accept-the-regeneration](../resolutions/accept-the-regeneration.md) · [correct-the-design](../resolutions/correct-the-design.md) · [remove-the-element](../resolutions/remove-the-element.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

**Never mechanical: all three resolutions are human.**

* **Accept** — the design's evolution is right and the recorded behavior is stale. Record the regenerated
  result.
* **Reject** — the design is wrong. Evolve it further until the behavior regenerates to its original result.
  That is `correct-the-design`.
* **Remove** — the design no longer produces this behavior under any entry condition. The behavior is deleted
  and its cell becomes uncovered, which either prunes with a reason or raises `uncovered-cell`.

**Accept and reject both return the behavior to `pending`, never straight to `approved`.** What ends up recorded
is not the thing that was originally approved — accept records a new result, reject records a design that
reached the old result by a new route — and returning straight to approved would mean trusting an outcome nobody
has looked at, which defeats the purpose of having detected the disconnect.

**A match against a prior approval restores it without a human, and a match with no prior approval does not.**
The two look identical mechanically and mean completely different things: in the first a human already agreed to
this exact result and nothing about it changed; in the second a match only says the record is internally
consistent, which is not what approval is for.

**A wave of these findings after a promotion is a finding about the promotion.** Promotion should cost no human
review — the containing design's traces now stop at the promoted target rather than walking into it, and should
regenerate to the same expected effects. If they do not, something changed that should not have, and the thing
to investigate is the promotion rather than the behaviors it disturbed.
