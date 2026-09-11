# sli-validation

## Context
* [Workflow](../WORKFLOW.md) §4.7 - where this check is registered
* [Deployable Model](../../datamodel/deployable-model.md) §5.2.1 - conformance is checked, not asserted
* https://github.com/OpenSLO/OpenSLO - the specification an SLI definition is validated against

## Purpose

Does every SLI validate against the revision it pins? An SLI expressed in a private format is a description of a
measurement; one expressed in OpenSLO is a measurement existing tooling can evaluate, and that survives leaving
this design.

## Registration

| | |
|---|---|
| Stage | maturity — `M5` |
| Model check | yes |
| Requires | [sli-coverage](sli-coverage.md) — there is nothing to validate until the SLI exists |

## What It Inspects

Every `SLI`'s `definition` — an OpenSLO object with `kind: SLI` — validated against the revision its
`specVersion` names.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `invalid-sli-definition` | a definition does not validate against the OpenSLO revision its `specVersion` names | [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M5`.

## Settings

None.

## Notes For P6

**The model says nothing about what a valid structure looks like or how validation is performed.** The standard
is authoritative for the first and the tooling owns the second; restating either would create a copy that goes
stale the moment OpenSLO revises, with nothing detecting the divergence. So this check's spec names the
validator, it does not re-specify OpenSLO.

**`specVersion` exists because without it the claim is not decidable.** "Valid OpenSLO" is not a question with
an answer unless it names a revision — the standard evolves, and a definition valid under one need not be valid
under the next. Changing an SLI's `specVersion` invalidates its validation by the ordinary rule, so it is
re-validated rather than assumed to carry over.

The version is recorded per SLI rather than once per project: a design target's SLIs normally share one, and a
mixed set is legitimate while a migration is in progress.
