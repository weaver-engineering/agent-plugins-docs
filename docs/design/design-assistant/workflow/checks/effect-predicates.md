# effect-predicates

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §2 - the effect shape and its kinds

## Purpose

Is every effect stated in checkable terms? A required and an expected effect share one shape precisely so that
matching them is mechanical. An effect with no predicate cannot be matched — only read — so it silently converts
the design's central comparison into a person forming an opinion.

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [traces](traces.md) — expected effects must exist before both sides can be required to be checkable |

## What It Inspects

Every `RequiredEffect` and `ExpectedEffect`, for a `predicate` stating the effect in checkable terms, alongside
its `kind`, `target` and `description`.

| `kind` | `target` |
|---|---|
| `returns`, `raises` | the operation |
| `dependency-interaction` | a dependency boundary's operation |
| `state-change` | a dependency boundary |
| `stream-output` | `stdout` / `stderr` |
| `exit-code` | the process |
| `emits-metric` | a metric |

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unpredicated-effect` | an effect has no checkable predicate | [state-the-fact](../resolutions/state-the-fact.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

A predicate may legitimately be absent at `M1`, when a required effect is often first captured as prose during
elicitation. This check is registered at `M4` for exactly that reason — the point of `M1` is to settle what is
required, and the point of `M4` is to establish that the design delivers it, which is the first moment the
predicate is load-bearing.

Making the absence a reportable gap rather than a silent downgrade to human judgement is the whole value:
without it, a design reaches `M4` with a comparison that was never actually performed.
