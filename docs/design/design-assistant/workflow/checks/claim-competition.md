# claim-competition

## Context
* [Workflow](../WORKFLOW.md) §4.2 - where this check is registered
* [Parse Contract](../../serialization/parse-contract.md) §3 - the merge rules and what competition means
* [Data Model](../../datamodel/DATA-MODEL.md) §5.6 - collection identity, without which "the same position" is undecidable

## Purpose

Does the design contradict or repeat itself? The model is the fold of every claim in scope, and the fold has to
be order-independent — so two claims writing one position are never resolved by preferring one, they are
reported.

This is the first model check because its findings say the model is not what it appears to be. Everything after
it reads positions, and a contested position has no value to read.

## Registration

| | |
|---|---|
| Stage | maturity — `M0` |
| Model check | yes |
| Requires | — |

## What It Inspects

Every **position** two or more claims write: a scalar attribute, or an entry in a collection identified by that
entry type's own identity. Contributing different entries to one collection is contributing to different
positions and is not competition.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `conflicting-claim` | two contributions state differing values for one position | [correct-the-design](../resolutions/correct-the-design.md) |
| `duplicate-claim` | two contributions state the same value for one position | [correct-the-design](../resolutions/correct-the-design.md) · [acknowledge](../resolutions/acknowledge.md) |

`conflicting-claim` blocks the checkpoint at which the **contested attribute** becomes required — contradictory
statements of a boundary's purpose block `M0`, of an SLI block `M5`. Its `blocking` is `computed`: the finding
carries the level, the check does not.

`duplicate-claim` is advisory. The fold is well defined and the value stands; the design is merely saying one
thing twice. Left neither corrected nor acknowledged, it blocks `M4`.

## Settings

None.

## Notes For P6

The normal correction for a duplicate is structural — two documents competing to state one fact is usually a
sign the documents are drawn along the wrong lines — but not always. A behavior legitimately in scope of two
NFR rule views is stated twice by design, and that instance is acknowledged rather than corrected.

The two kinds share a detection pass and differ only in whether the competing values agree, which is why one
check produces both.
