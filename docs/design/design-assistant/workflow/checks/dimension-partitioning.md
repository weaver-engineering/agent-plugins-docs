# dimension-partitioning

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Condition Model](../../datamodel/condition-model.md) §2.1 - values must be exhaustive and mutually exclusive
* [Data Dictionary](../../datamodel/data-dictionary.md) §4 - the predicate vocabulary values are written in

## Purpose

Do a dimension's values actually partition what they are over? A dimension whose values leave a gap has entry
conditions that fall into no cell, and one whose values overlap has entry conditions in two — and in both cases
the coverage claim over that space is worth less than it appears, while every cell in it looks perfectly
covered.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [condition-space](condition-space.md) — there are no values to partition until the space exists |

## What It Inspects

For every dimension, whether its values' predicates are jointly **exhaustive** and pairwise **mutually
exclusive** over the thing they partition: a field of the input type, a depended-on boundary's state, a
parameter, or a condition an NFR rule contributes.

`order-value` split into `< 1000` and `>= 1000` partitions; split into `< 1000` and `> 1000` does not, and the
gap is one value wide.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `non-partitioning-dimension` | a dimension's values leave a gap, or two of them overlap | [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M1`.

## Settings

None.

## Notes For P6

Decidability varies by predicate. Ranges over an ordered scalar and enumerated values are mechanically
solvable against the type's own definition; a predicate over a shape the dictionary does not yet define is not,
and the check should report what it could not decide rather than passing it silently — an undecided partition
and a correct one are not the same answer.

This is the check most likely to want a settings knob later: a project may reasonably want the undecidable case
reported, or not.
