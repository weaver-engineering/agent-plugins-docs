# satisfaction

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §2.3 - the two matching directions
* [Data Model](../../datamodel/DATA-MODEL.md) §3 - the verification claim this check is the centre of

## Purpose

Does the design do what was required? For every behavior, every required effect has a corresponding expected
effect. This is the comparison the whole model exists to make decidable — layers 3 and 4 kept separate so that
the match is between two independently-sourced facts rather than one field edited until it agrees with itself.

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [effect-predicates](effect-predicates.md) — an unpredicated effect cannot be matched |

## What It Inspects

For every behavior, whether each `RequiredEffect` has a corresponding `ExpectedEffect`.

**This is a subset relation, not equality.** The design is allowed to do more than the use case demanded, and a
use case is only ever part of the story for a shared operation. The reverse direction — is anything here that
nobody asked for — is [anticipation](anticipation.md), and it is a genuinely different question.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `satisfaction-failure` | a required effect has no corresponding expected effect | [correct-the-design](../resolutions/correct-the-design.md) · [take-a-decision](../resolutions/take-a-decision.md) · [raise-a-change-request](../resolutions/raise-a-change-request.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

**A satisfaction failure is a design defect**: the design does not do what was demanded. That is the honest
default reading, and it distinguishes this check from its mirror, where a finding may mean the requirement was
incomplete rather than the design wrong.

Nothing derived from the design may edit a required effect. The design does not get to resolve a satisfaction
failure by deciding it was not required after all — changing the requirement means changing its source, and
where that source is a document owned elsewhere it means change control against the owning document, which for a
use case means going back to Analysis.

An uninstrumented failure path lands here: a metric the design says is emitted but which no behavior's effects
account for is a satisfaction failure on a cell, found by the same check that finds any other missing effect.
