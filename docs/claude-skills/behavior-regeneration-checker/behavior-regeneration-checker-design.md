# Behavior Regeneration Checker

## Context
* [WVR-130](https://linear.app/weaver-engineering/issue/WVR-130/7172-rework-per-behavior-approval-regenerate-and-compare-project-wide) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.2 - the regenerate-and-compare step this skill implements
* [Pseudocode Substitution Checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md) - the sibling judgement-assisting skill this one's risk profile matches; both stay pure prose for the same reason
* [Reconciliation Checksum Utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md) - reports which behaviors need this check; this skill calls its `write` CLI directly on a match
* [Chunk Scope Utility](../chunk-scope-utility/chunk-scope-utility-design.md) - called by the architect's own accept/remove resolution once this skill flags a mismatch, not by this skill itself
* [Specific-Behavior Presenter](../specific-behavior-presenter/specific-behavior-presenter-design.md) - only ever presents a behavior once this skill confirms it's actually sound

## 1 Purpose

Every other §7.1 check confirms the bound pseudocode itself still structurally satisfies the use case. None of
them re-derive one specific behavior's own concrete Given/Then/Call Tree from scratch and check it still matches
what's recorded — they verify substitution validity, not "does the design, traced under this exact scenario,
still land where it used to." §7.2 needs exactly that question answered for every previously-approved behavior
whose reconciliation has gone stale: has anything it depends on changed in a way that actually changes this
behavior's own outcome, or did the design stay sound under the change?

## 2 Trigger

Routed here by `next-unit-of-work-detector` whenever it reports `7.2-human-review` — for a behavior never
reviewed at all, or one whose `reviewed` entry a function change cleared (Design Feature Instructions §7.1's
invalidation walk). Runs ahead of `specific-behavior-presenter` in both cases; only a confirmed match (or an
architect's own accept-and-rematch) reaches presentation.

## 3 Inputs

* An `SB-NNN` document path and a specific behavior id.
* A regenerated `{then, callTree}` pair — produced by the calling agent tracing the behavior's own current Given
  through the relying use case's current Bound Pseudocode and every named function's current pseudocode/prose
  (the interpretive act this skill deliberately does not perform itself — see §5).
* On a mismatch, a plain-text summary of the actual disconnect, for `redesign-required`.

## 4 Outputs And Effects

`compare` is read-only: reports `{"status": "match"}` or `{"status": "mismatch", "thenMismatch"?, "callTreeMismatch"?}`,
naming both recorded and regenerated content on each mismatch. On a match, the calling agent (not this skill)
runs `reconciliation-checksum-utility write` directly to refresh checksums, leaving `reviewed:` untouched. On a
mismatch, `redesign-required` mutates the `SB-NNN` document: writes `//REDESIGN_REQUIRED — {summary}` as the
behavior's own leading body content and clears its `reconciliation.behaviors.{id}.reviewed` entry — never
touches `call_tree` or checksums, both of which stay exactly as recorded until the disconnect is resolved.

## 5 Algorithm

The regeneration itself — reading a behavior's own current Given, walking Bound Pseudocode under those concrete
values, following every named function's own current pseudocode or prose to see what actually happens — is the
same interpretive act as originally deriving the behavior in §5.2. No script walks prose pseudocode with
concrete values deterministically; that's exactly why `pseudocode-substitution-checker` stays pure prose rather
than mechanical, and why this skill only owns the mechanical half *around* that judgement:

1. Only run for a behavior `reconciliation-checksum-utility` (or `next-unit-of-work-detector`'s own Step 8) has
   already reported as affected by something that changed — never regenerate every behavior on every pass.
2. Regenerate by reading every relevant document fresh from disk — never trace against a cached mental model of
   the design from earlier in the session, since the whole point is confirming *current* state, not remembered
   state.
3. Compare the regenerated `{then, callTree}` against what's recorded — string/structural comparison, no
   judgement.
4. On a match: no human touch. Refresh checksums via `reconciliation-checksum-utility write` directly; leave
   `reviewed:` exactly as it was.
5. On a mismatch: record `//REDESIGN_REQUIRED` with the actual disconnect, clear `reviewed:`, stop. Resolving it
   (accept/reject/remove) is explicitly not this skill's job — see §6.

## 6 Composition With Other Skills

Runs after `reconciliation-checksum-utility` (or `next-unit-of-work-detector`'s Step 8) has reported a
behavior's checksums as stale — never on a clean comparison, mirroring `pseudocode-subset-checker`'s own
checksum-shortcut pattern. Calls `reconciliation-checksum-utility write` directly on the match path (agent-
orchestration composition, not a code import, the same pattern the rest of this family follows). Does *not*
call `chunk-scope-utility` itself — that's the architect's own accept/remove resolution, a separate act (Design
Feature Instructions §7.2) this skill deliberately doesn't perform. `next-unit-of-work-detector` routes §7.2
here first; `specific-behavior-presenter` only ever presents a behavior once this skill (or a first-time,
never-reviewed state) confirms it's actually sound.

## 7 Cost/Benefit

Runs only on the rarer path — a behavior whose checksums have actually gone stale, not every pass — same
invocation-frequency shape as `pseudocode-substitution-checker`. High value: without this step, a changed
function silently invalidates every behavior that reaches it, with no mechanism to tell "still sound" apart from
"now wrong" other than a human re-deriving the whole trace by hand. The compare/write half is fully
deterministic — a wrong match/mismatch call is a straightforward implementation defect. The real risk lives in
the regeneration step itself: a sloppy or stale-context trace could report a false match (a real disconnect goes
unnoticed) or a false mismatch (wastes architect attention on a non-issue) — mitigated only by insisting the
trace always reads current disk content, never a cached mental model.

## 8 Open Questions

None outstanding at design time. Dogfooded through WVR-95's entire §7.2 pass, including catching two distinct,
real bugs in its own shared heading-extraction dependency that a prior test suite hadn't exercised (WVR-149,
WVR-153 — see `SKILL.md`'s "Validated against real data").

# Rationale

**Why the trace itself stays the calling agent's own job, never this skill's.** Regenerating a fresh Then/Call
Tree means interpreting prose pseudocode with concrete values — the same act §5.2's original derivation
performs, and the same reason `pseudocode-substitution-checker` stays pure prose rather than mechanical. A
skill that tried to walk pseudocode deterministically would either be wrong on anything genuinely novel or would
have to reimplement a general-purpose interpreter — neither is what this family is for.

**Why a match needs "no human touch" but a mismatch always does.** §7.2's whole invalidation mechanism exists to
catch cases where the design genuinely no longer produces what was agreed — not to manufacture review work every
time a dependency's checksum merely changes. A confirmed match means nothing about the previously-approved
outcome actually changed, only bookkeeping needed refreshing — asking a human to re-bless a provably-identical
result would be re-litigating a decision nobody's disagreed with. This shortcut only ever applies to a behavior
that already carried a real, human-granted approval being re-verified — never to a first-time review (see the
Design Feature Instructions §7.2 Rationale entry this exact distinction corrected, WVR-152 — found live on this
skill's own first real use, since WVR-95 was this Feature's first design task and nothing had ever shipped
project-wide to have a prior approval at all).

**Why resolving `//REDESIGN_REQUIRED` is explicitly out of this skill's own scope.** Design Feature Instructions
§7.2 gives the architect three resolutions (accept, reject, remove), each carrying real design-content weight —
rewriting a recorded Then, evolving a function further, or deleting a behavior outright. That's §5.2-derivation
territory, requiring the same human judgement §5.2 itself requires the first time, not a mechanical consequence
of a detected mismatch. Folding it into this skill would blur exactly the line WVR-130 draws between
"regenerate and detect" (mechanical, this skill's job) and "decide what to do about it" (never this skill's, or
any skill's, to grant itself).