# Pseudocode Subset Checker

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-109](https://linear.app/weaver-engineering/issue/WVR-109/skill-pseudocode-subset-checker-design-review-71) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.1 - the assertion this skill implements
* @docs/workflows/feature-workflow/pseudocode-style.md/§2 - the two vocabularies this check compares between
* [pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md) - the judgement this skill falls back to only when a checksum comparison finds drift
* [reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md) - records this skill's passing result, and is what this skill compares against first

## 1 Purpose

The subset relationship — under some valid entry state, does an `SB-NNN`'s bound pseudocode produce every
behavior the relying use case's Technical Interpretation requires — was already established once, piece by
piece, when gap-classifier's §4.3 pass substituted that bound pseudocode into existence. This skill doesn't
re-establish it from scratch by default: it confirms nothing it depended on has changed since, via checksum
comparison, and only falls back to re-running the substitution judgement on an actual mismatch. A Technical
Interpretation step whose bound pseudocode no longer checksums clean, and whose re-substitution still can't find
a covering piece, is the gap this check exists to catch.

## 2 Trigger

Routed here by the next-unit-of-work-detector once a specific behavior's call tree is clean per
call-tree-reconciler (§6) but its `reconciliation:` block is empty or stale.

## 3 Inputs

* One `SB-NNN`'s recorded bound pseudocode and its existing `reconciliation:` block (checksums of each relying
  use case's Technical Interpretation slice, and of every function's pseudocode/prose the bound pseudocode
  names).
* Current content for everything those checksums cover, to recompute against.

## 4 Outputs And Effects

Read-only with respect to design content — produces a pass/fail per relying use case and, on a full pass, hands
its result to
[reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md)
to record. Does not itself write the `reconciliation:` block, and does not write the bound pseudocode it may
cause to be regenerated — that stays gap-classifier's own §4.3 output.

## 5 Algorithm

Recompute the checksum of each relying use case's Technical Interpretation slice and of every function's
pseudocode or prose the bound pseudocode names; compare against what's recorded. If every checksum matches: pass,
without walking anything — the subset relationship established at §4.3 still holds. If the Technical
Interpretation slice's own checksum changed, that's a use-case-level edit, out of this skill's scope entirely
(Technical Interpretation is immutable within Design — see Specific Behaviors §2.1). If a function's pseudocode
checksum changed: for the specific piece(s) that function was substituted for, call
[pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md)
again against that function's current pseudocode. A still-valid substitution updates the bound pseudocode in
place and the check passes; a piece that no longer has a covering candidate is reported as a gap.

## 6 Composition With Other Skills

Sibling to [unexpected-side-effect-scanner](../unexpected-side-effect-scanner/unexpected-side-effect-scanner-design.md)
(the reverse-direction check over the same bound pseudocode),
[thin-shim-consistency-checker](../thin-shim-consistency-checker/thin-shim-consistency-checker-design.md), and
[unhandled-undeclared-exception-sweep](../unhandled-undeclared-exception-sweep/unhandled-undeclared-exception-sweep-design.md)
— all four run as part of the same §7.1 pass, and only once all four are clean does
[reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md)
record a passing result. Calls
[pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md)
only on the drift path, never on a clean checksum comparison.

## 7 Cost/Benefit

Runs once per `SB-NNN`, and again any time its `reconciliation:` checksums go stale. Unlike the original framing,
most runs are now cheap — a checksum comparison, not a graph walk — with the expensive substitution judgement
reserved for the (expected to be rarer) case where something actually changed. This is still the single most
safety-critical check in the family — it's what stands between "the design looks plausible" and "the design
actually satisfies the use case" — but its typical cost is now proportional to how much of the design is actually
churning, not to the size of the graph it happens to sit on. Risk profile: the checksum path is fully
deterministic (a wrong pass/fail here is a bug); the drift-triggered re-substitution path inherits
pseudocode-substitution-checker's own judgement-assisting risk profile.

## 8 Open Questions

* When only some pieces of a bound pseudocode are affected by a changed function, does re-checking need to
  re-verify the whole subset relationship for that `SB-NNN`, or only the specific piece(s) downstream of the
  change?
* Should a first-ever reconciliation pass (no prior `reconciliation:` block to compare against) skip the checksum
  step entirely and always confirm §4.3's bound pseudocode was assembled correctly, or is trusting gap-classifier's
  own output on a first pass acceptable?

# Built And Deployed

Built and deployed to `~/.claude/skills/pseudocode-subset-checker/`. `reconciliation:` is now true YAML
frontmatter (WVR-130/131), not an inline body block as originally proposed — this skill's own read/compare logic
is otherwise unchanged. Ran clean against real WVR-95 data throughout the project.
