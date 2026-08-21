# Unexpected Side-Effect Scanner

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-110](https://linear.app/weaver-engineering/issue/WVR-110/skill-unexpected-side-effect-scanner-design-review-71) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.1 - the reverse check this skill implements, and its Rationale entry on why resolution can't be mechanical
* @docs/workflows/feature-workflow/design-feature-instructions.md/§8 - the feedback loop this skill's findings can trigger into Analysis
* [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md) - the forward-direction sibling check

## 1 Purpose

The subset check (pseudocode-subset-checker) confirms everything required is present. This skill runs the same
comparison in reverse, and — unlike that check — can't be shortcut by a checksum: walking the `SB-NNN`'s own
recorded bound pseudocode under a specific behavior's own entry state, does it produce any External Dependency
interaction that neither the use case's Technical Interpretation nor the behavior's own Then anticipates? "The
required behaviors are all present too" does not excuse an unexpected one — it's flagged regardless.

## 2 Trigger

Runs alongside pseudocode-subset-checker as part of the same §7.1 pass, once a behavior's call tree is clean per
call-tree-reconciler.

## 3 Inputs

One `SB-NNN` behavior's entry state, its relying use case's Technical Interpretation, and the `SB-NNN`'s own
recorded bound pseudocode (§4.3).

## 4 Outputs And Effects

Read-only — detection only, never resolution. Produces a flagged discrepancy (an External Dependency interaction
with no anticipating requirement anywhere) for human judgement. Explicitly does not choose, or suggest a
default, between the two resolutions available (correct the pseudocode to exclude the effect, or correct the use
case to expect it) — Design Feature Instructions' own Rationale states this can't be mechanical, because both a
design bug and a use-case gap look identical from the design's own side.

## 5 Algorithm

Walk the `SB-NNN`'s own bound pseudocode under the behavior's own concrete entry state. For every External
Dependency interaction the walk actually reaches, check whether it's named in the use case's Technical
Interpretation or the behavior's own Then. Anything reached but not named is reported as an unexpected side
effect, flagged for human review regardless of whether the rest of the pass is otherwise clean.

## 6 Composition With Other Skills

Runs in the same pass as [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md),
[thin-shim-consistency-checker](../thin-shim-consistency-checker/thin-shim-consistency-checker-design.md), and
[unhandled-undeclared-exception-sweep](../unhandled-undeclared-exception-sweep/unhandled-undeclared-exception-sweep-design.md).
A finding here is the one path in the whole family that can hand off outside Design entirely, back into
Analysis, rather than to another skill in this list.

## 7 Cost/Benefit

Runs its own walk every time — unlike pseudocode-subset-checker, this check has no checksum shortcut, since the
question it's asking (does the bound pseudocode produce anything unanticipated) isn't reducible to "has anything
changed since last time." The benefit is catching a class of bug that's otherwise invisible: an extra, unintended
effect doesn't fail any other check in this family (the required behaviors are still all present), so without
this skill specifically, it would only surface once something downstream actually notices the extra effect
happening for real. Risk profile: detection is low-risk (deterministic once the walk is correct), but a
poorly-tuned scanner could over-flag legitimate, already-known side effects that just weren't recorded precisely
enough in the Technical Interpretation — false positives here cost real architect attention, since resolution is
always manual.

## 8 Open Questions

* What counts as "anticipated" precisely enough to not flag — does the Technical Interpretation or Then need to
  name the exact External Dependency interaction, or is a looser match (same dependency, different specific
  call) acceptable to avoid noisy false positives?
* Should repeated instances of the same unexpected side effect, across multiple behaviors sharing an operation,
  be de-duplicated into one finding, or surfaced per-behavior since each is technically a separate reconciliation
  pass?

# Built And Deployed

Built and deployed to `~/.claude/skills/unexpected-side-effect-scanner/`. Reads a behavior's own recorded call
tree from `reconciliation.behaviors.{id}.call_tree` in the `SB-NNN`'s YAML frontmatter (WVR-130/133), not an
inline body block as originally proposed — otherwise unchanged. Ran clean against real WVR-95 data throughout.
