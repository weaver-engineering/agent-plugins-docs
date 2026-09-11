# traces

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §4 - what a trace is and what it produces
* [Behavior Model](../../datamodel/behavior-model.md) §4.1 - where a trace stops
* [Condition Model](../../datamodel/condition-model.md) §2.2 - the dimensions a call tree reveals

## Purpose

Does every behavior have a trace, a call tree and expected effects? This is where the design's own account of
what it does comes into existence — derived by walking the design, never authored. An expected effect somebody
wrote down is a claim about the design rather than a reading of it, and the whole comparison at `M4` is
worthless if the two can be confused.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [fixture-suitability](fixture-suitability.md) · [function-descriptions](function-descriptions.md) — concrete state to trace against, and descriptions to trace through |

## What It Inspects

For every behavior: a `trace`, the `callTree` it produced, and the `expectedEffects` it yielded — each carrying
provenance naming every function description walked and every fixture used, with a checksum of each.

Tracing starts at the operation's realizing function with the cell's entry condition and its chosen fixture set,
and follows each call into the called function's own description, recursively, **within this design target**. It
terminates at three kinds of node and walks through everything else:

| Stops at | Takes |
|---|---|
| a contained design target's operation | that operation's own behavior, via the fixture standing in for it |
| a dependency boundary's shim | the fixture for the depended-on boundary's state |
| a function with no further calls | its own effects |

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | a behavior has no trace, call tree or expected effects | [regenerate](../resolutions/regenerate.md) · [state-the-fact](../resolutions/state-the-fact.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

**Resolving this check derives more than the trace.** The call tree is what reveals which dependencies the
operation actually reaches, so `dependency-state` dimensions accrete into the condition space as a consequence —
which adds cells, which are uncovered, which returns the design to `M1`. That is the single most surprising
movement in the whole workflow, and it is correct: coverage previously asserted against a smaller space is not
coverage of the larger one.

The call tree is the **concrete walk for this entry condition**, not the abstract call graph. Two behaviors of
one operation have different call trees wherever their entry conditions take different branches, and that
difference is what scopes invalidation to the behaviors that actually reached a changed function rather than
those that could have.

There is deliberately no bound-pseudocode artefact between the requirement and the design. With the requirement
stated as effects there is nothing left to bind, and the trace's provenance records exactly what the bound
pseudocode's checksums used to.
