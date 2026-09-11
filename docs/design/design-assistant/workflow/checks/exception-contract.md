# exception-contract

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §5 - the exception contract over the graph
* [Function And Call Graph](../../datamodel/function-and-call-graph.md) §2.1 - `raises` as a contract rather than a summary

## Purpose

Is every exception caught or declared onward? For every function and every call it makes, an exception the
callee declares in `raises` is either caught by the caller in its own description, or declared onward in the
caller's own `raises`. Anything that is neither is a failure mode nobody has designed a response for.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [function-descriptions](function-descriptions.md) — catching happens in a description |

## What It Inspects

Every edge of the call graph: the callee's declared exceptions against the caller's description and its own
`raises`.

This is detected by walking the graph, not by reading any one function in isolation — a function's own `raises`
is a claim about what it produces, and whether that claim is complete depends on what its callees produce, which
is not visible from the function itself.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `undeclared-exception` | an exception is neither caught by its caller nor declared in its `raises` | [correct-the-design](../resolutions/correct-the-design.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

The two resolutions are "catch it" and "declare it", and choosing between them is a design decision about where
a failure is handled rather than a documentation fix — which is why `take-a-decision` is a route.

The choice reaches the perimeter. Whatever a realizing function declares escapes to the operation's consumer,
and the operation must declare the same set — so declaring an exception onward at the perimeter changes the
operation's contract, and that is a change to what the design promises rather than an internal detail. A
function that must not surface a domain failure catches it and declares its own translation instead.
