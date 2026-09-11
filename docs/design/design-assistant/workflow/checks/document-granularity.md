# document-granularity

## Context
* [Workflow](../WORKFLOW.md) §4.8 - where this check is registered
* @docs/standards/design-layout-standards.md §2.3 - the trivial boundary
* @docs/standards/design-layout-standards.md §2.4 - the advisory count
* [Anchoring](../../serialization/anchoring.md) §4 - granularity as the lever controlling re-judgement precision

## Purpose

Is a boundary outgrowing the documents holding it? The default an agent falls back to is writing everything in
one document. That parses, folds and reconciles perfectly well, and it gets steadily harder to read, review and
re-judge as the design grows.

Two mechanisms make the cost concrete: two documents competing to state one fact raises a `duplicate-claim`, and
a claim's anchor covers every section nested beneath it — so a coarse document re-judges a great deal on every
edit.

## Registration

| | |
|---|---|
| Stage | global |
| Model check | yes |
| Requires | [boundary-identity](boundary-identity.md) — spend is counted per boundary |

## What It Inspects

Each boundary's **spend** against the trivial-boundary budget. A trivial boundary comfortably stays a single
document; each thing that pushes it past the budget adds one to the spend.

Only types that **cross** the boundary count. Shapes used only by a boundary's private functions still have
types; the dictionary makes no completeness claim about them, so they place no obligation on its documents.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `boundary-over-budget` | a boundary's spend is above zero | [partition](../resolutions/partition.md) · [acknowledge](../resolutions/acknowledge.md) |

**Global: it blocks nothing.** How a design is cut into documents says nothing about whether the design is
complete or accurate, so a boundary over budget is real work to do and leaves the design exactly as mature as it
was.

## Settings

| Path | Type | Default | Meaning |
|---|---|---|---|
| `boundaries.interface-count-budget` | `Int` | 1 | interfaces before the boundary is no longer trivial |
| `boundaries.function-count-budget` | `Int` | 9 | functions before the boundary is no longer trivial |
| `boundaries.crossing-type-allowance` | `Int` | 1 | pooled allowance of new **crossing** types per function, drawn on across functions rather than capped per function |
| `boundaries.exception-allowance` | `Int` | 1 | pooled allowance of new exceptions per function, same pooling |
| `boundaries.trivial-types-may-nest` | `Bool` | false | whether a type counted as trivial may have nested structure |

## Notes For P6

**The spend is the condition, and that is what makes acknowledgement work.** An acknowledged spend of 1
acknowledges a spend of **1**, not 2. At a spend of 2 the condition is different, the acknowledgement no longer
matches, and the finding is raised unanswered — resolved either by reducing the spend or by acknowledging the
new one. A boundary may sit at a high spend indefinitely because the architect has looked each time and decided
it reads better as it is.

**The spend changes the volume of the prompt, never the outcome.** Whether a boundary actually splits is the
architect's choice; at a spend of 1 mention it, at several press the point. Nothing acts on the count.

Every threshold above is configurable, which is the point: a cumulative advisory puts the observation in front
of the architect and keeps the decision where the judgement is, without hard-coding one project's sense of "too
big" into every project's layout.
