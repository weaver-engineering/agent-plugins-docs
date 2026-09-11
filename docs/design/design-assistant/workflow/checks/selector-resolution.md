# selector-resolution

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §7.1 - what a cross-cutting boundary selects
* [Boundary Model](../../datamodel/boundary-model.md) §7.4 - no reach-through across a design target
* [Condition Model](../../datamodel/condition-model.md) §5.1 - reach, and why cross-cutting dimensions accrete

## Purpose

Does every cross-cutting selector reach real functions? A rule applied by a boundary that selects nothing is an
assessment that looks complete and constrains nothing — and since the cells a rule generates are what its
coverage is judged over, a selector resolving to nothing silently removes a whole NFR from the design's
obligations.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [nfr-assessment](nfr-assessment.md) · [function-placement](function-placement.md) — an applied rule, and functions for it to reach |

## What It Inspects

For every cross-cutting boundary, that its `selects` resolves to at least one real function within **this design
target's own scope**. A selector reaches down through contained non-design-target boundaries and **stops at any
contained `SpecifiableBoundary`**: a design target's functions are selected only by its own cross-cutting
boundaries.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unresolved-selector` | a cross-cutting boundary's selector reaches no function in this design's scope | [correct-the-design](../resolutions/correct-the-design.md) · [exempt](../resolutions/exempt.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

`exempt` is the honest resolution where the answer turns out to be that no function here is on that boundary.
That is a complete assessment — but it must be recorded as an exemption against the rule rather than left as a
boundary selecting nothing, because the two are indistinguishable to anyone reading the design and only one is
a claim.

**Resolving a selector is what makes cross-cutting dimensions accrete.** Once the selector resolves, the rule
emits its dimensions into the condition space of every operation whose call tree reaches a selected function —
which adds cells, which are uncovered, which returns the design to `M1`. Reach is only fully computable from
`M3`, so this happens in two waves.

A promoted domain gets cross-cutting dimensions from its **own** boundaries only. Nothing goes uncovered,
because promotion splits the containing target's selections and the promoted target assesses the same in-scope
rules itself.
