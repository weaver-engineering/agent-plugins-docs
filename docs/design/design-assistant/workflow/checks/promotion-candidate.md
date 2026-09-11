# promotion-candidate

## Context
* [Workflow](../WORKFLOW.md) §4.8 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §3.1 - promotion, its two warrants and its cost
* @docs/standards/design-layout-standards.md §7 - why the layout decides what promotion costs

## Purpose

Has a contained boundary earned its own design? A `FunctionalBoundary` is promoted when repeating its behaviors
per consumer would duplicate its requirements and swamp review, or when it is intricate enough to need designing
on its own terms rather than as incidental detail of its callers.

Promotion is not free, and the cost is planning toil: a new design target needs its own design work, its own
ticket, its own review and its own NFR assessment. It is worth paying where it removes duplicated requirements,
and not otherwise — which is a judgement, so this check reports and never acts.

## Registration

| | |
|---|---|
| Stage | global |
| Model check | yes |
| Requires | [boundary-identity](boundary-identity.md) · [traces](traces.md) — consumers are counted from call trees |

## What It Inspects

Each contained non-design-target boundary's promotion **spend**, in the same cumulative shape the document
budget uses. Each indicator above its threshold adds one.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `promotion-candidate` | a contained boundary's promotion spend is above zero | [promote](../resolutions/promote.md) · [acknowledge](../resolutions/acknowledge.md) |

**Global: it blocks nothing.** A boundary that should have been promoted and was not is a design that is
harder to review, not one that is incomplete or inaccurate.

## Settings

| Path | Type | Default | Meaning |
|---|---|---|---|
| `promotion.consumer-budget` | `Int` | 1 | distinct consumers outside the boundary reaching it; above this, its requirements are being restated per consumer |
| `promotion.function-count-budget` | `Int` | 9 | function count standing in for complexity |
| `promotion.depth-budget` | `Int` | 1 | levels of contained boundary beneath it |
| `promotion.dependency-operation-budget` | `Int` | 1 | for a `dependency` boundary, depended-on operations whose interaction is a design problem in itself |

Deliberately **not** sharing `boundaries.function-count-budget` with
[document-granularity](document-granularity.md), despite the same default: that one asks what a boundary's own
documents can carry, this one uses the count as a stand-in for complexity, and a project moving one should not
silently move the other.

## Notes For P6

**Acknowledgement is keyed to the spend**, exactly as the document budget is: acknowledging a spend of 1 says
nothing about a spend of 2, and a boundary acquiring a third consumer raises the question again.

**Promotion changes a boundary's type in place, so no address changes** — an address nests through the
boundaries that structure an element, not through the design target governing it. The artefacts move on disk,
because a design's artefacts are scoped to a directory, and that is the whole of the cost when the boundary
already occupies a directory of its own.

**Promotion should cost no human review**, and that is a property worth checking rather than assuming: the
containing design's traces now stop at the promoted target instead of walking into it, and should regenerate to
the same expected effects. A promotion producing a wave of `redesign-required` has changed something it should
not have, and the finding to investigate is the promotion.

**Extraction and relocation are different operations** and this check does not propose them. Both change the
boundary's *position* and therefore re-address it and everything beneath it, where promotion changes only its
type.
