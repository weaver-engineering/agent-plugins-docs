# Gap Classifier

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-115](https://linear.app/weaver-engineering/issue/WVR-115/skill-gap-classifier-as-is-extended-new) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§3, §4.3 - the classification this skill scaffolds, and the bound-pseudocode recording it performs once every gap closes
* @docs/templates/HLD-TEMPLATE.md - the Internal Components/External Dependencies lists this skill's §3 output populates
* @docs/templates/SPECIFIC-BEHAVIOR-TEMPLATE.md - the bound-pseudocode block this skill's §4.3 pass writes
* [pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md) - the shared judgement this skill calls, once per candidate/piece in §3 and again per relying use case in §4.3
* [next-unit-of-work-detector](../next-unit-of-work-detector/next-unit-of-work-detector-design.md) - routes here for §3 once every in-scope use case has a Technical Interpretation, and again for §4.3 once every gap is closed

## 1 Purpose

Two passes of the same underlying judgement, at two different points in Phase 3:

* **§3 classification** — reads every in-scope use case's Technical Interpretation together and, for every piece
  of it (a call, a branch, or occasionally the whole thing), proposes a classification against each plausible
  Internal Component or External Dependency candidate: as-is (an existing function already closes the loop, no
  new downstream call needed), extended (needs a call it doesn't currently make), or new (nothing existing
  serves this need).
* **§4.3 bound-pseudocode recording** — once every gap §3 surfaced is actually closed (§4.1, §4.2), walks each
  relying use case's Technical Interpretation slice one more time and substitutes each piece with the function
  now decided to satisfy it, recording the result as that operation's own bound pseudocode on its `SB-NNN`.

Design Feature Instructions calls the underlying comparison "judgement, not a literal diff" — this skill doesn't
make that judgement itself, it scaffolds it by calling
[pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md)
once per candidate/piece and assembling the results.

## 2 Trigger

**§3 pass:** routed here by next-unit-of-work-detector once every use case in scope has a non-empty Technical
Interpretation but the HLD's Internal Components/External Dependencies lists don't yet classify everything those
Interpretations touch. **§4.3 pass:** routed here again, per `SB-NNN` stub, once that stub is clean per the §3/§4
gap-resolution steps but doesn't yet carry a bound-pseudocode block for each use case relying on it.

## 3 Inputs

**§3:** every in-scope use case's Technical Interpretation pseudocode, and the project's existing catalog of
Internal Component and External Dependency functions (their `calls:` and Purpose). **§4.3:** one `SB-NNN` stub's
relying use case(s) and their Technical Interpretation slice(s), plus the now-resolved Key Decision for every
piece that was classified extended or new in §3.

## 4 Outputs And Effects

**§3:** produces a proposed classification (as-is / extended / new) per touched piece/candidate pairing, for the
architect to confirm before it's written into the HLD's Internal Components/External Dependencies lists — see
§8. **§4.3:** writes the bound-pseudocode block directly onto the relevant `SB-NNN` document's Realizes, one per
relying use case — this pass is a direct write, not a proposal, since by the time it runs every substitution it
records has already been confirmed (either through §3's own review or through §4.1/§4.2's Key Decision review).

## 5 Algorithm

**§3:** read every in-scope Technical Interpretation as one body of pseudocode, broken into pieces — a call, a
branch, or occasionally the whole thing. For each piece, against each plausible Internal Component or External
Dependency candidate, call
[pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md).
Its no/as-is/extended answer becomes this piece/candidate's classification. Only pieces and candidates that are
plausibly related are compared — the rest of the project's existing catalog is never enumerated.

**§4.3:** for each relying use case, walk its Technical Interpretation slice again, piece by piece. For every
piece §3 already classified as-is or extended against a candidate that's still the one decided (§4.1/§4.2),
re-use that result directly rather than re-calling the primitive. For every piece that was new in §3, call
pseudocode-substitution-checker once more against the function §4.1/§4.2 actually decided on, and use its bound
substitution. Assemble every piece's bound form into one continuous trace and record it as the `SB-NNN`'s bound
pseudocode for that use case.

## 6 Composition With Other Skills

Calls [pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md)
in both passes. §3's output feeds per-gap-ideation (§4.1, not currently in this skill list — architect judgement,
not a skill candidate) with the extended/new items it identifies, and is upstream of
[called-from-backward-walker](../called-from-backward-walker/called-from-backward-walker-design.md), since an
item classified extended is exactly what later triggers that walker once its actual change is decided. §4.3's
output is what [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md) and
[reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md)
check and checksum downstream, at §7.1.

## 7 Cost/Benefit

**§3** runs once per Feature (whole-Feature, not per use case) and is the highest-judgement-risk pass in the
family — a wrong classification doesn't just cost review time, it can send the whole downstream ideation phase
after solving the wrong problem. **§4.3** runs once per `SB-NNN`, but is cheaper than it looks: most of its work
is re-using §3's own already-confirmed results rather than re-invoking the substitution primitive, since only
the pieces that were genuinely new in §3 need a fresh call once their gap is closed. The benefit of both passes
is the same shape — scaffolding a comparison an architect would otherwise do by hand, function by function, or
piece by piece — with the risk concentrated in §3's initial judgement rather than spread evenly across both.

## 8 Open Questions

* Should §3's output always require explicit architect confirmation before being written to the HLD, or only for
  classifications it's genuinely uncertain about (with a confidence signal of some kind)?
* How does this skill decide which functions in a potentially large existing catalog are even "touched" by a
  given Technical Interpretation, without either an expensive full-catalog read or a search mechanism that
  doesn't fully exist yet (per this project's own [UC-005](../../analysis/use-cases/UC-005-search-documentation.md))?
* §4.3's re-use of §3's own results assumes nothing about a candidate changed between the two passes except the
  specific piece being closed — is that assumption ever actually false in practice (could resolving one gap
  invalidate another piece's still-as-is classification), and if so, should §4.3 re-verify rather than trust §3's
  cached result?
