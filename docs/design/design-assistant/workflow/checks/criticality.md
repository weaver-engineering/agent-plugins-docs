# criticality

## Context
* [Workflow](../WORKFLOW.md) §4.7 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §6.2 - criticality, and why it sits on the operation
* [Decision Model](../../datamodel/decision-model.md) §5 - the sourcing kinds

## Purpose

Which operations owe a service contract, and who says so? `critical` says whether a consumer depends on this
operation achieving a service contract, and it is what decides which operations need SLIs at all — an operation
nobody's journey depends on needs a correct behavior, not a service level.

## Registration

| | |
|---|---|
| Stage | maturity — `M5` |
| Model check | yes |
| Requires | [operation-identity](operation-identity.md) — criticality is a property of an operation |

## What It Inspects

For every operation on a deployable boundary, that `critical` is **stated** and carries `Sourcing`, either way
round:

* a **critical user journey** naming the operation, held as an `ExternalRef` with a checksum like any other
  document source;
* the **architect's own assertion**, recorded as an elicited fact.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | an operation's `critical` is not stated | [state-the-fact](../resolutions/state-the-fact.md) |
| `unsourced-fact` | `critical` is stated with no `Sourcing` | [record-sourcing](../resolutions/record-sourcing.md) |

Blocks `M5`.

## Settings

None.

## Notes For P6

Which operations are on a critical user journey is **Analysis's determination, and Analysis does not block
design**. A design that had to consult analysis to decide whether its `M5` gate was met would be blocked on
analysis having happened. Recording the flag locally, with sourcing that says whether a journey named it or the
architect asserted it, keeps the gate mechanical and keeps the judgement falsifiable — an unrecorded assumption
about criticality is one nobody can later find and disagree with.

`M5` self-scopes this: it applies only to a `DeployableBoundary`, and a Library has no service level to state,
so a Library's operations never need the flag.

`false` is an answer. The finding is the absence of a statement, not the absence of criticality.
