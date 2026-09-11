# operation-contract

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §6 - the operation's attributes and their checkpoints
* [Boundary Model](../../datamodel/boundary-model.md) §6.1.1 - why the operation's signature is a fact of its own

## Purpose

Does every operation state its contract? The signature is what a consumer is offered — parameters, return type,
declared exceptions — and it is settled as part of stating what is *required*, a whole checkpoint before any
function exists to derive it from.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [operation-identity](operation-identity.md) — an unnamed operation has no contract to state |

## What It Inspects

For every operation on every design target in scope, its `signature`: the parameters with their names,
positions and types, the return type, and the exceptions it declares with the condition under which each is
raised.

Type **names** are checked here; whether they resolve to definitions is `M2` and belongs to
[type-resolution](type-resolution.md). A design target with type names in its signatures and no dictionary to
resolve them against is legal below `M2`.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | an operation has no signature, or one missing its parts | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M1`.

## Settings

None.

## Notes For P6

Deciding a signature means deciding what data the operation takes and returns, which is a decision with
candidates rather than a transcription — hence `take-a-decision`. Where the design already has an idea of the
data shapes, this is also the point at which those shapes get names, even though nothing has to define them
until `M2`.

The operation's signature and its realizing function's are deliberately two facts at two addresses, so nothing
here competes with anything at `M2`; what the design asserts is that they *conform*, which
[signature-conformance](signature-conformance.md) checks.
