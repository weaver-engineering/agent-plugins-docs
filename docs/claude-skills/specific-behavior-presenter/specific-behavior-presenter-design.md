# Specific-Behavior Presenter

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-117](https://linear.app/weaver-engineering/issue/WVR-117/skill-specific-behavior-presenter-design-review-72) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.2 - the human review this skill's output feeds
* @docs/workflows/feature-workflow/specific-behaviors.md/§2.9 - why this review is the critical checkpoint, not a formality
* [reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md) - gates this skill; only runs once its result is current

## 1 Purpose

Once §7.1's mechanical reconciliation is clean for an `SB-NNN`, a human still has to actually read and
understand each of its specific behaviors and assert it's genuinely what the use case requires — not trust that
a systematic process got there on its own. This skill compiles and presents each behavior individually, with
full provenance, so that review; it does not perform the review itself.

## 2 Trigger

Routed here by next-unit-of-work-detector once an `SB-NNN`'s `reconciliation:` block is current (per §7.1) but
`reviewed_by` is not yet set.

## 3 Inputs

One `SB-NNN` document, its relying use case(s), and — for each Given condition in each of its behaviors — enough
of the derivation history from §5 (Deriving Specific Behaviors) to state where each condition actually came
from.

## 4 Outputs And Effects

Read-only with respect to design content — produces a formatted, one-behavior-at-a-time presentation: the
use-case detail it realizes, each Given condition's provenance (which document defined it, whether the architect
supplied it directly during elicitation, or it was inferred and on what basis), and its effects. Does not set
`reviewed_by`/`reviewed_at` itself — that's the architect's own action once they've actually reviewed, recorded
via reconciliation-checksum-utility.

## 5 Algorithm

For each specific behavior in the `SB-NNN`, in order: assemble its Realizes (the use-case steps it's a variation
of, from the document-level Realizes plus its own), Given (each condition annotated with where it came from),
When, Then, and Call Tree into one consistent, compact presentation. Present them one at a time — not batched —
so review attention isn't diluted across several at once. Move to the next only once the current one has been
explicitly addressed.

## 6 Composition With Other Skills

Strictly downstream of [reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md)
— will not run against an `SB-NNN` whose reconciliation isn't current, since presenting behaviors for a review
that's about to be invalidated by a stale check would waste the architect's attention on content that might
still change.

## 7 Cost/Benefit

The ticket's own review flagged this as high-value: standardised, reviewable output plus a large reduction in
output tokens compared to an agent re-deriving the presentation format from scratch each time it needs to show a
behavior for review. Runs once per `SB-NNN` that reaches this stage — moderate frequency, but every design
eventually produces every one of its behaviors this way, so the token savings compound across a whole Feature.
Risk profile is low on the presentation itself (a formatting/compilation task, not a judgement call) — the real
risk this skill has to guard against is *omitting* provenance detail that would have changed the architect's
read of a behavior, which is a completeness concern for the skill's own design, not a judgement risk in what it
outputs.

## 8 Open Questions

* How far back does "provenance" actually need to trace for an inferred Given condition — the immediate
  reasoning step, or the full chain back to whatever documented source ultimately grounds it?
* Should this skill also surface, alongside each behavior, whether it's a happy path or which specific unhappy
  path it is (§2.5's taxonomy), to help the architect calibrate how much scrutiny a given behavior needs?
