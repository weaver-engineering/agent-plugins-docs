# Pseudocode Substitution Checker

## Context
* [WVR-118](https://linear.app/weaver-engineering/issue/WVR-118/skill-pseudocode-substitution-checker-shared-primitive) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§3, §4.3, §7.1 - the three points that all resolve to this same judgement
* [gap-classifier](../gap-classifier/gap-classifier-design.md) - calls this once per candidate/piece during Gap Analysis, and again once every gap is closed, to record bound pseudocode (§4.3)
* [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md) - calls this to re-establish a subset relationship only when reconciliation's checksums have gone stale
* [reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md) - records what this primitive's own calls produced, once stable

## 1 Purpose

Both Gap Analysis's as-is/extended/new classification and design review's subset check ask, underneath the
surface, the exact same question: could this candidate function's own pseudocode or prose stand in for this piece
of pseudocode — a single call, an entire branch, or occasionally a whole Technical Interpretation — without
changing what it describes? Neither "judgement, not a literal diff" (§3's own phrasing) nor "matched
mechanically" (§7.1's) is a deterministic algorithm; both are one and the same LLM-backed comparison, asked at
two different points in the pipeline against two different targets — a candidate under consideration (§3), or
the design's current, already-bound state (§7.1). This skill is that comparison, factored out once so neither
caller has to re-describe it.

## 2 Trigger

Called by [gap-classifier](../gap-classifier/gap-classifier-design.md), once per candidate function against each
piece of an in-scope Technical Interpretation (§3), and again, per relying use case, once every gap is closed
(§4.3). Called by [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md)
only when a reconciliation checksum has gone stale — never on a clean pass, where the checksum comparison alone
is enough (Design Feature Instructions §7.1). Never invoked directly by the architect or by
next-unit-of-work-detector.

## 3 Inputs

* One piece of pseudocode to be replaced: a single call (`<--[...]`), an entire branch, or a whole Technical
  Interpretation, from whichever source the caller is working against.
* One candidate's own pseudocode or prose — an Internal Component or External Dependency function under
  consideration (§3), or, on a §7.1 re-check, that same function's current pseudocode.

## 4 Outputs And Effects

Read-only — returns one of three answers: no (the candidate cannot stand in for this piece), as-is (it can,
without gaining any call it doesn't already make), or extended (it can, but only once it gains a call it doesn't
currently make). On as-is or extended, also returns the bound form of the piece (`[address: name - args]`,
Pseudocode Style §2) for the caller to substitute in. Never writes to a design document itself —
gap-classifier and pseudocode-subset-checker are what record a result, each into the document it already owns.

## 5 Algorithm

Given one piece of pseudocode and one candidate: read the piece's own intent (what it computes, what it calls,
under what condition) against the candidate's declared Purpose, `calls:`, and its own pseudocode or prose. Ask
whether invoking the candidate as currently specified already produces the same outcome the piece describes.
This is the same three-way judgement Design Feature Instructions §3 describes directly — as-is, extended, or no
match at all — applied here as a single, reusable comparison rather than restated at each call site. Where the
answer is as-is or extended, also produce the bound substitution: the piece's abstract call target rebound to
the candidate's real address, ready for the caller to splice into whatever pseudocode it's assembling (§4.3's
bound pseudocode, or a re-validated one at §7.1).

## 6 Composition With Other Skills

Called by [gap-classifier](../gap-classifier/gap-classifier-design.md) (§3's initial classification pass, and
again at §4.3 once every gap is closed) and by
[pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md) (only on a stale
checksum, per [reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md)'s
compare mode). Not called by
[thin-shim-consistency-checker](../thin-shim-consistency-checker/thin-shim-consistency-checker-design.md) — that
check compares several already-settled usages against each other and against a declared interface for
uniformity, a different question from whether one thing can substitute for another, and is deliberately not
built on this primitive.

## 7 Cost/Benefit

Invocation frequency tracks its two callers': once per candidate/piece pairing during Gap Analysis (potentially
many calls for a large Feature), then again, cheaply, only on the reconciliation checksums that actually go
stale — most §7.1 passes never call this at all, since a clean checksum comparison is enough on its own (Design
Feature Instructions §7.1). Factoring it out once, rather than letting gap-classifier and pseudocode-subset-checker
each describe their own version of "compare pseudocode to pseudocode" independently, is what keeps the two from
silently drifting into two different standards for the same judgement. Risk profile is judgement-assisting, not
mechanical — a wrong classification here is exactly the risk gap-classifier's own §7 already names (sending a
whole gap-closing decision after the wrong problem), so this skill's output is a proposal for the caller to act
on, never an unreviewed write.

## 8 Open Questions

* How much of a candidate's own pseudocode/prose should this primitive actually read for one comparison — the
  whole function, or can it be scoped to the specific branch/section a piece's own call target suggests, to keep
  large comparisons cheap?
* Should a "no" answer carry any structured reason (what specifically doesn't match), or is a bare
  no/as-is/extended sufficient, leaving the caller to explain the gap in its own terms?

# Rationale

**Why this exists as a separate skill rather than duplicated logic inside gap-classifier and
pseudocode-subset-checker.** Both calls already agreed, this session, to be the same underlying judgement asked
at two different points against two different targets — gap-classifier's own §8 open question ("how does this
skill decide which functions... are even 'touched'") and pseudocode-subset-checker's own §8 open question ("how
is 'produces the same outcome' matched mechanically") turned out to be the same unanswered question twice.
Factoring the comparison out once means a future refinement to how the judgement itself works — a better prompt,
a narrower scope for what gets read — only has to change in one place, and the two callers stay guaranteed
consistent with each other by construction rather than by discipline.

**Why thin-shim-consistency-checker isn't built on this primitive.** This skill answers "can A stand in for B" —
a one-to-one substitution question. Thin-shim-consistency-checker answers "are these N already-accepted usages,
and the interface they all rely on, still mutually consistent" — a uniformity question across a set, with no
single candidate being judged as a replacement for anything. The two only look similar because both eventually
compare pseudocode-shaped content; the actual comparison being made is structurally different, so collapsing them
into one primitive would blur a distinction worth keeping.

# Built And Deployed

Built and deployed to `~/.claude/skills/pseudocode-substitution-checker/`, algorithm unchanged from this
proposal. Called by both `gap-classifier` and `pseudocode-subset-checker` exactly as designed throughout
WVR-95's own dogfooding.
