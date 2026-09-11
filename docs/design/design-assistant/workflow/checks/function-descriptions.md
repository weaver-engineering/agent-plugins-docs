# function-descriptions

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §2.2 - the three description forms
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §6 - metrics, defined by the function that emits them

## Purpose

Can every function be traced through? A function's description is what the design actually says it does, and it
is what a behavior is traced through. A description that cannot be traced is not a description for this model's
purposes, whatever its literary merits.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [function-placement](function-placement.md) — a function must be placed before its content is required |

## What It Inspects

For every function in the catalog:

* `descriptions` — at least one of `prose`, `pseudocode` or `sequence`, sufficient to track behavior from a
  perimeter operation through to every external dependency it reaches;
* `calls` — the functions this one invokes;
* `emits` — the metrics it emits, each with `slug`, `kind`, `measures`, `unit` and `labels`.

A function may carry **several** description forms at once: they answer different questions, and one that
coordinates several boundaries genuinely needs a sequence diagram *and* pseudocode.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | a function is missing a description, its `calls`, or a metric's own attributes | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

`measures` and `unit` answer different questions and the model needs both. `measures` is prose — a reader has to
know a number counts failed records rather than failed batches, and no enumeration carries that. `unit` is an
enumeration, because a value is uninterpretable without one and a machine has to compare and aggregate them.

A function's `emits` says what it *can* produce; whether it actually does under a given entry condition is an
effect on a behavior. Both are needed, and this check only asks for the first.

`calls` is the authored direction; `calledFrom` is derived and materialized, and is never authored here.
