# Design The Feature — Process

## Context
* [Agent Plugins index](agent-plugins.md) - root index for this repo
* `sub-agents/design-assistant/design-assistant.md` (once merged — currently only in the stale, undecided PR #15) - the sub-agent that executes this process; its own standing instructions are cross-cutting rules only, not this document
* @docs/workflows/feature-workflow/design-feature-instructions.md - this repo's own copy of this process, kept for the architect's own human-facing understanding of how it works and their role in it (WVR-144, not yet rewritten as of this document's creation) — this document is now the detailed, agent-facing source of truth the two are kept consistent with, not the other way around
* @docs/workflows/feature-workflow/design-directory-and-hld.md - the HLD, Internal Component, and External Dependency shapes this process populates
* @docs/workflows/feature-workflow/specific-behaviors.md - the `SB-NNN` shape and Given/When/Then/Call Tree format this process populates
* @docs/templates/HLD-TEMPLATE.md, @docs/templates/INTERNAL-COMPONENT-TEMPLATE.md, @docs/templates/EXTERNAL-DEPENDENCY-TEMPLATE.md, @docs/templates/SPECIFIC-BEHAVIOR-TEMPLATE.md - the fill-in-the-blank shapes this process fills in
* @docs/templates/USE-CASE-TEMPLATE.md/§Technical Interpretation - what §2 below produces
* @docs/workflows/feature-workflow/pseudocode-style.md - the notation §2, §4, and §7.1 write and compare
* @docs/workflows/feature-workflow/chunk-scope.md - the per-design-task record §5.2 and §7.2 write incrementally
* @docs/workflows/feature-workflow/feature-workflow.md - the workflow step (`2 Design The Feature`) this process carries out, and what consumes its output (`3 Chunk The Design`)

## Why This Document Lives Here

`weaver-engineering/docs` is for human (architect) consumption: how the process works, and the architect's own
role in it. This document is the detailed process definition and rationale — the source per-phase agent
instruction files (shipped with `next-unit-of-work-detector`, `claude-skills/next-unit-of-work-detector/instructions/`)
and `design-assistant.md` itself are authored from. The two documents describe the same process; this one is
maintained as the authoritative detail, `weaver-engineering/docs`'s own copy is maintained separately for its own
audience.

These are the steps an agent follows to carry out the `Design The Feature` step of the Feature Workflow and
produce a complete design directory. The architect's judgement is required at specific, named points (§4.1
ideation, §5 elicitation and sanity-checks, §7.1's side-effect resolution, §7.2 final review) — everywhere else
the process is mechanical. It is also iterative, not a strict waterfall — see §8 — and deliberately broken into
small, independently-resumable units of work: §1 defines how to tell, from the current state of a design
directory alone, exactly which unit comes next, so that a session with no memory of any previous one can pick up
immediately.

Every point where this process "presents" something to the architect — a Key Decision's candidates, a freshly
derived behavior, a flagged side effect, a batch ready for final review — assumes the content is already
committed and pushed to the design directory's own pull request. The architect reviews against that PR, not a
description of working-tree state; presenting something not yet pushed isn't presenting it at all, it's just
narrating uncommitted work.

## 1 Determining The Next Unit Of Work

Before doing anything, check the design directory's current state in this order. The first gap found is the
next unit of work; everything before it is already done.

1. Does the HLD exist with its Scope naming the use case(s) this design task covers, under their own Design Task
   entry (Design Directory And HLD §2)? Scope accumulates across however many separate design tasks a Feature
   takes — this only requires *this task's own* use cases to be named, not every use case the Feature will ever
   have. If not, confirm scope before anything else — nothing downstream can start.
2. For each use case in scope: does it have a non-empty `## Technical Interpretation`? Any that don't need §2,
   one use case at a time.
3. Does the HLD's Internal Components and External Dependencies list classify every function the Technical
   Interpretations collectively touch as as-is, extended, or new? If not, §3 is next.
4. For every item classified extended or new, and every Open Design Question carried by a use case in scope: is
   there a resolved Key Decision with a Rationale entry naming every alternative considered? Any unresolved need
   §4.1, one gap at a time. Once every individual gap is resolved, has the merge pass (§4.2) run since the last
   one was added? If not, that's next.
5. For every `SB-NNN` stub clean per step 4: does it carry a bound-pseudocode block (§4.3) for each use case
   that relies on it? Any that don't need §4.3, one `SB-NNN` at a time.
6. For every `SB-NNN` stub created in §2: has its outline of entry conditions been proposed and approved, with a
   numbered section for each — parents holding their real Given, leaves holding a placeholder `//TODO` (§5.1)?
   Any that don't need §5.1, one `SB-NNN` at a time. Once every section exists: does each leaf hold real derived
   content, confirmed and with no `//TODO` or `//REVIEW` line remaining (§5.2)? First one that's still a `//TODO`
   or still flagged `//REVIEW` needs §5.2, for that specific behavior.
7. For every derived behavior: does its call tree's every node appear in its parent's declared `calls:`? Any
   mismatch needs §6, one reconciliation issue at a time.
8. For every `SB-NNN` clean per §6 (step 7): does its `reconciliation:` block (§7.1) have checksums that still
   match the design's current content? If the block is empty, or a checksum no longer matches, §7.1 is next.
9. Project-wide, not scoped to this Feature — every `SB-NNN` in every Feature's own design directory: does every
   leaf behavior have a `reviewed` entry (§7.2), with no `//REDESIGN_REQUIRED` flag standing against it? A leaf
   with no entry (never reviewed, or a function change cleared it — §7.1), or one flagged `//REDESIGN_REQUIRED`,
   needs §7.2 — regardless of which Feature or use case it belongs to.

Steps 1–8 can be scoped to one use case, one operation, or the whole Feature: told to "work on `UC-105`," an
agent runs the same sequence restricted to that use case's own artifacts. Step 9 can't be scoped that way — its
whole purpose is catching invalidation that reaches outside the Feature currently being worked on (§7.2) — so it
always runs project-wide. This Feature's own design is only complete, ready for `Chunk The Design` (Feature
Workflow §3), once its own `SB-NNN`s are clean through step 8 *and* a full project-wide step 9 scan finds
nothing left needing §7.2 anywhere.

## 2 Phase 1: Technical Interpretation

For each use case in scope, independent of every other (chunkable per use case): rewrite its Main Success
Scenario and Extensions as pseudocode, in technical language, entirely independent of any solution — naming no
Internal Component, no External Dependency, no call tree. Record it as the use case's own `## Technical
Interpretation` appendix (Use Case Template), not in the design directory.

While writing this pseudocode, every point where the actor crosses the system's own boundary is an operation
(Design Directory And HLD §4.4). Identify each one as it's written and immediately create its `SB-NNN` stub:
filed, linked from this Technical Interpretation, with a single `//TODO` standing in for its behaviors — Given,
When, Then, and Call Tree aren't known yet, that's §5. Do this for every operation the use case implies,
regardless of whether anything about how it's satisfied is understood yet; an operation that later turns out to
need no new design work at all still gets its stub here, because §5 still has to derive its specific behaviors.

Exit: every use case in scope has a Technical Interpretation, and every operation it implies has a linked
`SB-NNN` stub.

## 3 Phase 2: Gap Analysis

Whole-Feature, not per use case: read every in-scope use case's Technical Interpretation together, as one body
of pseudocode, and walk it piece by piece — a single call (`<--[...]`), an entire branch, or, on occasion, a
whole Technical Interpretation in one go — asking, of each candidate Internal Component or External Dependency
function: could this function's own pseudocode or prose stand in for this piece without changing what it
describes? The answer is always one of:

* **As-is** — yes, and the candidate needs no call it doesn't already make. Its `calls:`/pseudocode doesn't
  change; its usage lists (Design Directory And HLD §3.4, §4.5) still grow to record the new use case relying on
  it.
* **Extended** — yes, but only once the candidate gains a call it doesn't currently make.
* **New** — no existing function stands in for this piece at all.

This is judgement, not a literal diff: compare what the piece needs against each candidate's existing `calls:`
and Purpose, not against its exact wording. Only relevant functions get classified — the rest of the project's
existing catalog is never enumerated just to mark it irrelevant. The same question, asked again later against
the design's current state rather than a candidate's, is what §7.1's reconciliation re-checks.

This classification is scoped to this Feature's own HLD — a snapshot of this Feature's own relationship to each
candidate, not a permanent status recorded against the function itself. The candidate's own `IC-NNN`/`ED-NNN`
document carries no as-is/extended/new field of its own (its usage lists, Design Directory And HLD §3.4/§4.5,
record *who* relies on it, not what any one Feature classified it as). The next Feature's own Gap Analysis
re-classifies every candidate fresh, against its own needs, never inheriting what an earlier, unrelated
Feature's HLD once said about it — a function this Feature classifies new is, by the time the next Feature
starts, simply part of the existing catalog like any other.

Exit: the HLD's Internal Components and External Dependencies sections list every relevant function, each
classified as-is, extended, or new (HLD Template).

## 4 Phase 3: Ideation And Solution Shape

Every item classified extended or new in §3, and every Open Design Question carried by a use case in scope, is
a gap needing a decision. This phase runs in three passes.

### 4.1 Per-Gap Ideation

Chunkable one gap at a time, independent of every other gap. For each: ask "how might we close this gap" and
generate candidate solutions — genuinely more than one where more than one is plausible, since the question's
own conditionality ("might") means no candidate starts out favored. Score each against the project's NFRs and
the gap's own requirements, then choose one. Record the choice as a Key Decision (Design Directory And HLD
§2.1). Record every candidate that wasn't chosen in the HLD's `# Rationale`, with why it was discounted —
analysis of its qualities, a logical argument that rules it out, or a proof-of-concept's finding. A candidate
ruled out by a proof-of-concept records the PoC's finding in that same Rationale entry; the PoC itself doesn't
need its own permanent artifact.

Choosing an interface means choosing what data it takes and returns, not just its name and signature. Where that
data isn't already captured, record its shape in the HLD's own Data Types (Design Directory And HLD §2, item 4)
as part of the same Key Decision — concrete enough for Deriving Specific Behaviors (§5) to instantiate with
literal example values, not left described only in prose inside the Key Decision itself.

Where the gap is closed by extending an existing function (§3), find every other use case now relying on
pseudocode that's about to change before making the change. An `IC-000` function or an External Dependency
operation names them directly (Design Directory And HLD §4.5, §3.4). A non-entry-point Internal Component
function doesn't carry that list itself — walk its `called_from:` (Design Directory And HLD §4.1) back, one hop
at a time, until reaching the `IC-000` function(s) it terminates at, then read their usage lists from there.
Either way, every use case found this way has an existing `reconciliation:` block (§7.1) that becomes stale the
moment the change is made, not at some later point someone happens to notice; each becomes due for
re-verification, which §1's own check picks up mechanically the next time it runs for that `SB-NNN`, via the
checksum that no longer matches.

Exit, per gap: a resolved Key Decision with a Rationale entry naming every considered alternative and why it
was discounted, and, where the interface introduces a data shape not already captured, an entry for it in the
HLD's Data Types section.

### 4.2 The Merge Pass

Whole-Feature, once every individual gap has its own resolution: read every Key Decision from §4.1 together and
look for gaps that turned out, once visible side by side, to want the same thing — two independently-chosen
functions that are really one (a Key Decision for "post a large purchase order" and another for "post a
purchase order" to the same queue, say, that should just be one function). Where they are, consolidate them into
a single Key Decision and a single Internal Component or External Dependency function, and update every affected
`SB-NNN` stub's expected call tree to match. Consolidating means removing the superseded candidates' own entries
from the HLD's §5/§6 (§3's own Gap Analysis pass, which ran before the merge, has no way to have known they'd
turn out to be the same thing) — the HLD lists only the single, consolidated function afterward, never both the
surviving name and the one it replaced (§8's own rule on revising in place applies here too).

Once every gap's Key Decision is settled and consolidated, every Internal Component or External Dependency named
in the HLD's §5/§6 needs its own standing document — that document is the actual design artifact defining its
functions, not just the HLD's own summary of it, and it will always be needed once something is listed there at
all. For each one not yet created: create it — Internal Component Template or External Dependency Template —
assigned the next free `IC-NNN`/`ED-NNN` in the project's own sequence, with one numbered `§M`/`§M.N` section per
function or operation this Feature currently needs (a later Feature may add more to the same document rather
than creating a competing one, per Design Directory And HLD §3.2's ownership rule). Each section's own purpose
statement and concrete signature — the template's required floor — is transcribed from the interface already
decided in that function's own Key Decision (§4.1), not left as a placeholder to fill in later. Link the document
from the HLD's §5/§6 entry, replacing the bare name Gap Analysis (§3) recorded there.

`IC-000` is the one component every project needs from its first Feature onward (Design Directory And HLD §4.4).
If this is that first Feature, `IC-000`'s own document doesn't exist yet either — creating it, with this
Feature's own operations as its first numbered functions, is part of this same step, not a special case to defer
or skip.

This closes Solution Shape — every component this Feature needs is now decided, documented, and addressable,
including the shape of the data each interface takes and returns (§4.1). Commit and push, then stop: this is a
natural point to pause and let the architect look over the diff before §4.3 builds bound pseudocode on top of
these interfaces, the same way every other unit of work in this process ends by handing back rather than
continuing unprompted into the next one. No separate record of the review is needed — the session simply doesn't
resume §4.3 until the architect responds, and any response that continues the session at all (not just an
explicit "go ahead") counts as having looked.

Exit: no two Key Decisions from this Feature describe functions that should have been the same one, and every
component or dependency named in the HLD's §5/§6 has its own standing document — numbered, linked from the HLD,
with a placeholder section per function or operation this Feature needs.

### 4.3 Recording The Bound Pseudocode

Once every gap in scope is closed (§4.1, §4.2), each `SB-NNN` stub's operation has, for every piece of Technical
Interpretation it covers, either an as-is/extended function already classified in §3 or a newly-decided one from
§4.1/§4.2. For each use case relying on that operation (Specific Behaviors §3), walk that use case's own
Technical Interpretation slice one more time and substitute each call, branch, or whole body with the function
now decided to satisfy it — binding each abstract target (`[name - args]`) to its real address
(`[address: name - args]`, Pseudocode Style §2). Record the result as this `SB-NNN`'s own bound pseudocode,
alongside its existing step-range Realizes (Specific Behaviors §3, §4) — one bound-pseudocode block per relying
use case, since each use case's own Technical Interpretation is a separate, immutable source, even where two
happen to bind to the exact same functions.

The Technical Interpretation itself is never edited by this step. Substituting into it produces a new, derived
artifact recorded on the `SB-NNN` document — a change to the use case's own Technical Interpretation is a change
to the use case (Specific Behaviors §2.1), not something this step, or any step of Design, is permitted to make.
This bound pseudocode is what §5 traces to derive each behavior's Then, and what §7.1 checksums against —
rather than either re-deriving the substitution from scratch each time, or comparing the Technical Interpretation
directly against a function's own pseudocode with nothing on record showing how the two were ever actually bound
together.

Exit: every `SB-NNN` stub in scope carries a bound-pseudocode block for each use case that relies on it.

## 5 Phase 4: Deriving Specific Behaviors

Per `SB-NNN` stub created in §2 (chunkable one at a time), regardless of whether §3/§4 did anything with the
operation it covers. Two passes: agree the shape, then fill it in.

### 5.1 Agreeing The Shape

Establish every valid entry state (Given) this operation needs a behavior for. The use case's own Preconditions
and Extensions are the first source; where they don't fully specify one, elicit the missing detail directly from
the architect rather than inventing it. Organize them the way Specific Behaviors §4.1 describes: a base
condition as a top-level number, each permutation of it nested beneath.

Propose this as an outline, not individual behaviors yet — the use case's own goal in a sentence or two,
followed by the nested, numbered list of entry conditions being considered — and present it (committed and
pushed, per this document's own opening rule). Number each entry condition with the literal dotted-decimal id
it will carry as a heading (`1`, `1.1`, `1.2`, `1.2.1`, ...), written out in full as the list item's own text —
not markdown's native nested-list numbering, which restarts at `1.` under every parent and only implies nesting
through indentation. The proposal has to be presented in exactly the id scheme the `SB-NNN` document's headings
will carry, or there's a translation step between what's approved and what gets written where the hierarchy can
silently drift. This may take more than one round: revise and re-propose against the architect's feedback until
they approve the shape, the same as any other design revision (§8) — a mini-cycle of its own, not a single
take-it-or-leave-it presentation.

Once approved, write the `SB-NNN` document's own numbered sections to match — one heading per entry condition,
replacing the single stub-level `//TODO` §2 created. Not every section gets the same placeholder treatment: a
node is a leaf if the outline gives it no further nested condition beneath it (Specific Behaviors §4.1) — its
own Given resolves to an outcome, so a leaf is a complete behavior, just not yet a *derived* one, and gets only
a `//TODO` in place of its actual Given/When/Then; its call tree doesn't exist yet either, so there's no
frontmatter entry for it at all until §5.2. A node with children below it is a parent, not a leaf, and its own
Given is already known — it's exactly what the approved outline stated for that entry condition — so write it
directly rather than placeholding it; it has no When/Then to placehold, and no call tree or frontmatter entry to
placehold either, since its own outcome genuinely isn't determined at all until a child resolves it. This is
what makes the approved shape itself resumable: a fresh session can read the `SB-NNN` document directly and see
exactly which entry conditions were agreed on, without the approval conversation itself needing to be
remembered.

Exit: every entry condition the architect approved has its own numbered section in the `SB-NNN` document — each
leaf holding its placeholder `//TODO`, each parent holding its real Given.

### 5.2 Deriving Each Behavior

For each leaf's placeholder section, in order: systematically trace its entry state — its own Given plus every
parent's Given it inherits from (Specific Behaviors §4.1) — through this `SB-NNN`'s own bound pseudocode (§4.3)
— following each bound call into the Internal Component or External Dependency's own pseudocode or prose it
names — to derive the concrete Then and the call tree that produced it (Specific Behaviors §2.6), rather than
authoring either freehand. Parent nodes were already settled in §5.1 and need no further derivation here.

Tracing occasionally surfaces a Data Type whose Key Decision (§4.1) never actually specified a value or
behavior for the case at hand — not something validly inferable from what the Key Decision does state, but a
real absence in it. That's the same genuine-design-gap situation §6 handles for an undecided call, just found
here instead of during reconciliation: don't invent a convention to paper over it. Name the gap and return to
§4.1 to make the missing decision, the same as any other Key Decision found incomplete downstream of where it
was made.

Write the derived Given/When/Then in place of the leaf's `//TODO`, but flag it as unconfirmed until the architect
actually agrees: prefix the section's body with its own `//REVIEW` line, the same convention a placeholder's
`//TODO` already uses, so a resumed session can tell "derived, not yet confirmed" from "confirmed" from document
state alone, without needing the conversation that confirmed it. Write its call tree into the document's own
frontmatter at the same time, under `reconciliation.behaviors."{this leaf's id}".call_tree` (Specific Behavior
Template) — `reviewed` stays absent until §7.2 confirms it, the frontmatter-side equivalent of the body's own
`//REVIEW` flag. A behavior derived here for the first time is new work this design task is introducing — record
it as `new` in the design task's own chunk scope (Chunk Scope) at the same time, not deferred to some later
summarizing pass. Commit and push this (per this document's own opening rule), then present it for a quick
sanity check — not a formal approval, just "is this really what the use case demands" — as: the section's own
number, the condition itself restated as bullet points, and the expected result the design produces.

Revise and re-present, still flagged, if the architect disagrees. Once confirmed, remove the `//REVIEW` line in
a follow-up commit before moving to the next placeholder section.

Exit: every `SB-NNN` has its happy path and every identified unhappy path (Specific Behaviors §2.5) recorded as
a fully-derived behavior in place of its placeholder `//TODO`, each confirmed and with no `//REVIEW` line
remaining.

## 6 Phase 5: Call Tree Reconciliation

Chunkable per individual reconciliation issue, and idempotent — re-running it when nothing has changed just
re-confirms there's nothing to do. For every derived behavior, check that every node in its call tree appears in
the `calls:` declared by its parent (Specific Behaviors §2.7). Where it doesn't:

* If it's a genuine design gap — the call was never actually decided — return to §4.1 to make that decision
  (the same move §5.2 makes when tracing surfaces an incomplete Data Type instead).
* If it's a simple documentation error — the `calls:` list is stale or mistyped — correct it directly; no new
  decision is needed.

Exit: every behavior's call tree is fully backed by its nodes' declared `calls:`.

## 7 Phase 6: Design Review

### 7.1 Mechanical Reconciliation

The subset relationship this check protects — under some valid entry state, does the operation's bound
pseudocode (§4.3) produce every behavior the relying use case's Technical Interpretation requires? — was already
established once, piece by piece, when that bound pseudocode was substituted into existence. Re-establishing it
here isn't a fresh semantic walk by default: it's confirming nothing it depended on has since changed. Recompute
the checksum of each relying use case's Technical Interpretation slice and of every function's pseudocode or
prose the bound pseudocode names, and compare against what's recorded in the `SB-NNN`'s own `reconciliation:`
block. A match means the substitution is still valid, cheaply. A mismatch — the Technical Interpretation changed
(a use-case-level edit, invalidating the requirement itself), or some function's pseudocode changed (an
extension elsewhere, found via §4.1's own `called_from:` walk) — means §4.3's substitution has to run again for
this operation: the same judgement as the first time, not a shortcut around it.

A changed function's reach isn't confined to this one `SB-NNN`, or this Feature. Walk backward from the changed
function, project-wide, to every behavior — in any `SB-NNN`, in any Feature's own design directory — whose own
recorded `call_tree:` (the concrete walk that behavior actually traced, not just the abstract call graph a
change was found in) contains that function's address. Clear the `reviewed` entry (Specific Behavior Template)
for exactly those behaviors, and no others in the same document — a sibling behavior whose own call tree never
reached the changed function stays approved untouched. This is what feeds §7.2's own project-wide scan (§1 step
9): a behavior with no `reviewed` entry needs §7.2 whether it's never been reviewed at all, or was reviewed once
and just lost that approval here.

The check also runs the other way, and this half can't be shortcut by a checksum: walking the bound pseudocode
under this behavior's own entry state, does it produce any External Dependency interaction that neither the
Technical Interpretation nor the behavior's own Then anticipates? That's an unexpected external side effect, and
"the required behaviors are all present too" doesn't excuse it — it gets flagged regardless. Resolving it is
never mechanical: either the pseudocode or prose is wrong and needs to conditionally exclude the effect for this
entry state, or the use case's own understanding was incomplete and the use case itself needs correcting to
expect it. Which way to go is always a human judgement call (§8) — this is the one point in the whole process
where a finding can send the design back past its own scope, into Analysis.

Run this for every `SB-NNN` clean per §6, against its bound pseudocode — plus, for every External Dependency
operation involved, the same subset check against its `used_by:` list (Design Directory And HLD §3.4): is every
relying use case's actual usage still something the shim's declared interface is capable of, or has one quietly
started needing more than a thin shim can honestly give it? Unlike the operation-level check above, this one
isn't the same substitution judgement run again — it's comparing several already-settled usages against each
other and against the shim's own declared interface for uniformity, not asking whether one thing can stand in
for another.

Also walk the bound pseudocode for exceptions that are both unhandled and undeclared: every `RAISE` and every
uncaught propagation from a call, checked against whether it's either caught locally or added to that function's
own declared contract for whatever calls it (Pseudocode Style §4). Anything neither caught nor declared is a
reconciliation failure — a failure mode nobody has designed a response for — not something to wave through
because the rest of reconciliation is otherwise clean.

Record a passing result in the `SB-NNN` document's own `reconciliation:` block (Specific Behavior Template): a
checksum of each relying use case's own Technical Interpretation slice, and a checksum of every function's
pseudocode or prose the bound pseudocode names, as of the moment reconciliation passed. This makes the record
falsifiable — recomputing the same checksums later and finding a mismatch means something the reconciliation
depended on has since changed and it needs to be re-run, without re-reading or re-reasoning about content that
hasn't actually moved.

Exit: the `SB-NNN`'s `reconciliation:` block has checksums matching the design's current content.

### 7.2 Human Review

Not "present what's recorded" — this is the pass that confirms the design still actually produces it. Earlier
derivation (§5.2) happened while the design was still fluid, by definition: the first pass through is exactly
about making the design support the use case, correcting it where it doesn't. By the time §7.2 runs the design
is meant to be static, so this pass is verification, not (re-)authorship: for each behavior needing §7.2 (§1
step 9 — never reviewed, or a function change cleared its approval per §7.1), regenerate its expected result by
tracing its own entry state through the *current* design, the same walk §5.2 first did, using whatever functions
are now checksummed as current. Regenerating is agent work; asserting the result is correct is not, and never
becomes the agent's to grant itself.

* **Regenerated result matches what's recorded** — the design is still sound for this behavior. Refresh the
  checksums either way. What happens next depends on whether this behavior already carried a genuine prior
  `reviewed_by`/`reviewed_at` that §7.1's own invalidation walk just cleared (a real, once-confirmed approval
  this pass is re-verifying) or has never been reviewed at all (first time reaching §7.2, whether or not it's
  ever matched before): only the first case skips human touch — restore `reviewed` to what it was, done, since
  nothing about what was previously approved has actually changed and manufacturing a fresh review for a
  provably-unchanged result would just be re-litigating a decision nobody's disagreed with. The second case
  still needs a real first review: present it via the normal path below — a match here only means there's no
  disconnect to resolve first, not that presentation and genuine confirmation can be skipped. On a Feature's
  first pass through §7.2 project-wide, every behavior is necessarily this second case — nothing has shipped yet
  for anything to have been previously approved.
* **Regenerated result doesn't match** — the design no longer produces the agreed behavior. Flag
  `//REDESIGN_REQUIRED` on the behavior (Specific Behavior Template), recording the actual disconnect found — what
  regenerated versus what's recorded, and why — not just the fact that one exists, so a cold session doesn't have
  to re-derive it. Surface it to the architect; this is always their call, never resolved automatically, and it's
  three-way, not two:
  * **Accept the new behavior.** The design's evolution is correct, and the prior agreement is what's stale.
    Update the recorded content in place (§8) to the regenerated result, then present it fresh — `//REVIEW`, not
    straight back to approved, since what's now recorded was never itself confirmed. Whether this needs its own
    chunk scope entry depends on whose work is being revised: if the current design task's own chunk scope
    already has a `new` entry for this address (this task derived it and hasn't shipped it yet — nothing has,
    until `Chunk The Design` runs), nothing further is recorded; it stays `new`, since `Chunk The Design` only
    ever sees this task's final delivered state, not how many times it was revised internally before then. Only
    if this address has no entry in the current task's own chunk scope — meaning it belongs to a *different*,
    already-completed design task, and this task's own function change is what invalidated it — record it as
    `mutated` in *this* task's own chunk scope: an existing, already-shipped behavior's expected result just
    changed, which is exactly what that status means.
  * **Reject it.** Push the design back (§8) to evolve the function further, until it satisfies whatever prompted
    the change *and* this behavior regenerates to match its original, already-agreed content again. Nothing
    about the recorded behavior itself has changed, so nothing gets recorded in chunk scope for this resolution.
  * **Remove it.** Sometimes neither of the above is true: the evolved design doesn't produce a *different*
    result, it doesn't produce this behavior under any entry state at all anymore. Delete the leaf section and
    its `reconciliation.behaviors.{id}` entry entirely — mechanically trivial once decided, no re-derivation
    needed — but the decision itself carries at least as much weight as accept or reject, arguably more, since
    it's irreversible. It needs its own explicit bar, not a routine "does this look right" nod folded in with
    everything else being presented: ask the architect an unambiguous yes/no question naming exactly what's being
    removed, and require an unqualified affirmative in response before deleting anything. The same same-task/
    cross-task test as Accept (above) applies: if this address only has a `new` entry in the *current* design
    task's own chunk scope, it was never shipped — remove that entry entirely rather than adding a `deleted` one,
    since there's nothing for `Chunk The Design` to ever have seen. Only an address belonging to a different,
    already-completed design task gets a genuine `deleted` entry recorded in *this* task's own chunk scope,
    before or alongside the deletion itself.
  Accept and reject both resolve through a fresh `//REVIEW` — never straight back to approved, because what gets
  confirmed next is, in both branches, not the thing that was invalidated. Remove has no further `//REVIEW`: once
  confirmed, the behavior is simply gone.

For a behavior actually reaching a human (first-time review, or `//REDESIGN_REQUIRED` accepted and re-presented):
present it individually, not batched, with the use case detail it realizes, the provenance of each Given
condition (which document defined it, whether the architect supplied it directly, or it was inferred and on what
basis), and its effects. This is the real review — what's approved here becomes the specific behaviors a Chunk's
failing tests are built from (Specific Behaviors §2.9).

§7.2 runs project-wide (§1 step 9), not scoped to this Feature, and it's a fixed-point pass, not a single sweep:
accepting a changed behavior, or evolving a function to reject one, can itself invalidate other, already-approved
behaviors — in any `SB-NNN`, from any Feature, including ones already shipped through `Chunk The Design` — via
§7.1's own invalidation walk. Those re-enter scope the same as anything else needing §7.2, regardless of which
Feature or use case originally drove them. §7.2 for this Feature isn't complete when this Feature's own behaviors
are all approved; it's complete once a full project-wide scan (§1 step 9) finds nothing left needing it anywhere.

Exit: project-wide, every `SB-NNN`'s `reconciliation:` block has a `reviewed` entry for every one of its leaf
behaviors, with no `//REDESIGN_REQUIRED` flag standing against any of them.

## 8 The Feedback Loop

Design is iterative, not a strict pass through §2–§7. A problem found during §7.2 review, or later during
`Chunk The Design` (Feature Workflow §3), sends the design back to whichever phase actually owns the broken
decision — usually §4.1 (a Key Decision needs revisiting) or §5 (a behavior was wrong) — which gets revised
there. "Revised" means updated in place: the HLD, and every other design document, always reflects the design's
current, actual state — removing or correcting whatever's now wrong, not leaving a superseded classification,
Key Decision, or candidate name standing alongside its replacement as if both were still true. A reader (or a
mechanical script) has no way to tell a deliberately-retained historical note from an accidentally-orphaned one;
the design directory is never its own changelog. Everything downstream is then re-validated by re-running §1's
own check from that point forward, rather than assumed still correct: a stale `reconciliation:` block (§7.1) is
exactly the mechanism that catches this without anyone needing to remember to check by hand. The same mechanism
is what catches the cascading case in §4.1: extending a function that other use cases already rely on invalidates
their `SB-NNN`s' own reconciliation — surfaced as `//REDESIGN_REQUIRED` (§7.2) for exactly the behaviors whose
own call tree actually reaches the changed function, not just the gap that prompted the change.

That cascade isn't bounded by this Feature. §7.2 runs project-wide (§1 step 9) precisely because a function
change can invalidate an already-approved behavior from an unrelated, earlier Feature — one that may already be
built and shipped through `Chunk The Design`. This process resolves the *design* side of that fully: the prior
behavior either gets accepted as genuinely changed or the design evolves to preserve it, either way ending in a
fresh, correct approval. What it does not resolve is the deployed code a shipped Chunk already produced from the
now-superseded behavior — that's downstream of Design The Feature entirely, and needs its own handling (most
likely as chunk-scope's own "mutated behavior" case, Feature Workflow §3) rather than being silently left
implied.

Most findings loop back within Design. One doesn't: an unexpected external side effect (§7.1) can be resolved
by correcting the use case itself rather than the pseudocode, which sends the design back past its own scope
into Analysis — the one point in this process where that's the right destination, not a sign the process has
gone somewhere it shouldn't.

# Rationale

**Why this document lives in `agent-plugins-docs`, not only in `weaver-engineering/docs`.** `weaver-engineering/docs`
is for human (architect) consumption of the process and their own role in it; this document is the detailed,
agent-facing source the per-phase instruction files shipped with `next-unit-of-work-detector` and
`design-assistant.md` itself are authored from. An earlier attempt tried to have a tool mechanically extract
sections from `weaver-engineering/docs`'s own copy at runtime — rejected because it conflated two different
audiences into one document sliced two ways. Authoring separately, once, here, and keeping
`weaver-engineering/docs`'s own copy for its own (eventually rewritten, WVR-144) audience, is simpler and correct
for both readers.

**Why this is a separate document from Design Directory And HLD and Specific Behaviors, rather than folded into
them.** Those two documents define what a complete design looks like — the shape of the HLD, the format of a
specific behavior. This document defines how to get there. Burying the process inside the shape definitions
means a reader trying to find "what do I do next" has to reconstruct a sequence from scattered mechanics
described for other reasons; keeping it separate means the process can be read start to end on its own, and the
shape documents stay focused on what they're actually for.

**Why §1 exists at all, ahead of the phases themselves.** The entire point of breaking design into small,
resumable units (per WVR-106) is that a new session, with no memory of any previous one, can pick up immediately
— which only works if "what's next" is derivable mechanically from the documents' own current state, not
recalled from context that a fresh session doesn't have. Every phase's own exit criteria (stated at the end of
each section) is written so §1's check can be automated, which `next-unit-of-work-detector` now does.

**Why Gap Analysis (§3) needs three states, not two.** "New or extended" was the original framing, but it
collapses a real distinction: an existing function this design relies on but doesn't change at all ("as-is") is
a different fact from one gaining a call it doesn't currently make ("extended") — the first needs no further
decision, the second needs one in §4. Two states would either force as-is items to be called "extended" (and
then need a Key Decision they don't actually require), or leave them unclassified (and then be indistinguishable
from something nobody checked at all).

**Why classification doesn't need an explicit reset between Features.** Once a project has more than one
Feature, a natural worry is what stops a "new" classification from one Feature's HLD reading as still current
once the next Feature's own Gap Analysis starts. It never needed resetting because it was never global state to
begin with — each Feature's classification lives only in that Feature's own HLD, a document that isn't touched
again once the Feature ships. The candidate's own `IC-NNN`/`ED-NNN` document, the one artifact every Feature
actually reads, never carried a classification field at all. The fix here isn't a new mechanism, only saying
outright what was already true: scoping was correct by construction, it just wasn't written down, which is
exactly the kind of assumption a mechanical implementation (rather than a careful human reader) can get wrong.

**Why ideation (§4.1) requires recording discarded alternatives, not just the winner.** A Key Decision that only
states what was chosen looks identical whether one option was ever seriously considered or five were. Recording
every discarded candidate and why is what makes "how might we" a real question asked with initially equal
weight, rather than a formality wrapped around a decision already made — and it gives a later reviewer, or a
later Feature revisiting the same gap, the actual reasoning to check against instead of just a conclusion.

**Why the merge pass (§4.2) is a separate step from per-gap ideation, not folded into it.** A gap considered on
its own has no visibility into any other gap's resolution — two independently-correct answers to two different
questions can still turn out to want the same underlying function, and there's no way to notice that until both
answers already exist to compare. Running it as its own whole-Feature pass, after every individual gap is
resolved, is what makes that comparison possible at all.

**Why the HLD has to lose the superseded candidates, not just gain the consolidated one.** Classification is
scoped to this Feature's own HLD (§3's own Rationale) precisely because that document is meant to be read as
the design's current, actual state — not a log of every candidate anyone ever considered. A merge that only
adds the winning, consolidated function without removing the two (or more) it replaced would leave the HLD
claiming three functions exist where the design actually decided on one — indistinguishable, to a later reader
or a mechanical script, from a real gap nobody noticed. This is the same principle §8 states generally for any
revision; it's called out again here specifically because the merge pass is where it's most likely to be
missed — consolidation reads as *adding* the merged decision, and it's easy to stop there without also
retracting what it replaced.

**Why standing document creation is folded into §4.2 rather than left implicit.** The first real design pass
(dogfooding this process against WVR-95) closed out every gap in §4.1, decided every component's interface, and
only then noticed nothing in the process actually said when those components' own `IC-NNN`/`ED-NNN` documents
get created and numbered — including `IC-000` itself, which had never been created at all, since this was the
project's first Feature. §4.1 alone can't be where this happens: a gap considered in isolation can't yet know
whether the merge pass is about to fold it into another one, and numbering a document only to immediately
discover it duplicates another wastes the one thing a project-level number is supposed to be — stable once
assigned. §4.2, once the deduplicated set of components is finally known, is the first point where creating and
numbering them doesn't risk exactly that.

**Why Data Types is populated in §4.1, not its own separate step.** The same dogfooding pass that found the
missing document-creation step also found this document (Design Directory And HLD §2) requires an HLD's Data
Types section without this process ever saying when it gets filled in. Unlike document creation (§4.2, which
has to wait for the merge pass to avoid numbering something that turns out duplicate), a data shape doesn't have
that problem — choosing an interface and choosing the shape of what it takes and returns are the same decision,
not two that could later turn out to be redundant with each other. Deferring it to its own pass would just mean
re-opening a Key Decision that was already, correctly, closed in §4.1 to add the one thing it was actually
missing.

**Why §4.2's checkpoint has no recorded review marker, unlike §7.1/§7.2's `reconciliation:`.** The reconciliation
block exists because §7.1/§7.2 have to survive a genuinely cold session, possibly long after the work it covers
was done, with nothing but document state to derive from. §4.2's checkpoint doesn't have that problem — it's the
same session, at the same sitting, handing back at the natural end of one unit of work the same way every other
unit of work in this process already does, not a fact that needs to outlive the session it was made in. Adding a
YAML marker here would be recording a fact for a scenario — a cold session needing to know whether this
particular checkpoint was looked at — that this checkpoint doesn't actually create.

**Why §5's per-behavior check and §7.2's review are different events, not one.** §5 happens the moment a
behavior is first derived, informally, to catch an obviously wrong result before moving on to the next one —
speed matters more than rigor there. §7.2 happens only once §7.1's mechanical reconciliation is already clean,
with full provenance for every condition, because what's approved there is what a later Chunk's failing tests
are built from — rigor matters more than speed there. Merging them would either slow down §5's fast iteration
loop or under-scrutinize the review that actually matters.

**Why §5 splits into agreeing the shape (§5.1) before deriving anything (§5.2).** Dogfooding WVR-95 surfaced two
compounding problems at once. First, §1's own resumability check only ever required "at least one" fully-derived
behavior per `SB-NNN` before treating it as done — weaker than §5's own Exit criterion, which requires every
happy path and every identified unhappy path. Left uncorrected, the process would walk every operation's own
happy path and move on, never coming back for the unhappy paths, since nothing forced it to. Second, entry
conditions were being discovered one at a time, as a side effect of deriving and presenting each behavior, so
the architect only ever saw the shape of an operation's coverage piecemeal, after the fact, never as a set they
could actually review before content got written against it. §5.1 fixes both by treating the outline itself as
a distinct, resumable artifact — proposed, revised, and approved before any Given/Then exists — written into the
`SB-NNN` document as numbered placeholder sections the moment it's agreed, so §1's own check can tell, from
document state alone, whether the shape is settled and, separately, whether every placeholder in it has actually
been filled in.

**Why §5.1's outline must use the literal dotted-decimal id, not markdown's own nested-list numbering.**
Dogfooding WVR-95 caught this directly: an outline for `SB-004` was proposed with ordinary nested markdown list
items — `1.`, `2.` restarting under each parent, nesting shown only by indentation — and by the time it reached
several levels deep, the hierarchy the architect actually intended had drifted from what the indentation
implied. "A nested, numbered list" doesn't, by itself, require the numbers themselves to be the id a heading
will later carry; markdown's own auto-numbering satisfies that description just as well while throwing away the
one thing that actually matters — which parent a condition permutes. Writing `1.4.3.1` out as literal text
instead of relying on indentation removes the translation step entirely: what's approved in the proposal is
character-for-character what becomes the heading, nothing has to be inferred from nesting depth after the fact.

**Why only leaves get a `//TODO` placeholder, not every node in the outline.** A parent node's Given is already
fully known the moment the outline is approved — it's exactly what the architect just agreed to — so placeholding
it and then "deriving" it again in §5.2 would be re-deciding something already settled, with nothing left to
derive. Only a leaf's Then genuinely depends on tracing the bound pseudocode (§5.2's actual work); a parent has
no Then to trace, because its own condition doesn't yet determine one (Specific Behaviors §4.1). Placeholding
every node uniformly would also break §1's own resumability check: a parent's `//TODO` could never be resolved
by §5.2's derivation loop, so a document with parents left as placeholders would look permanently incomplete no
matter how much real derivation happened.

**Why a Data Type gap found while tracing (§5.2) gets the same "return to §4.1" treatment as an undecided call
(§6).** Dogfooding WVR-95 surfaced a Key Decision that named an interface's Data Type but never specified what
one of its non-nullable fields should hold for a case that only became concrete once real pseudocode was traced
against it. §6 already has the right instinct for this — a gap found downstream of where it should have been
decided goes back to where Key Decisions are made, not papered over on the spot — but its wording only covers
`calls:` mismatches, discovered mechanically during reconciliation. A Data Type gap is discovered differently
(by judgment, while tracing, not by a mechanical list comparison) but it's the same situation underneath: the
Key Decision that owns this interface is incomplete. Generalizing the existing rule keeps "found downstream of
§4.1 → goes back to §4.1" as one rule with two triggers, rather than inventing a second one that just happens to
say the same thing. The test for a real gap, versus a value that's a valid inference from what the Key Decision
already states: does the Key Decision say nothing about this case, or does it follow from an invariant it
already states? A non-nullable field with no stated value for a case that can legitimately arise is squarely the
former.

**Why a derived leaf needs its own `//REVIEW` marker, unlike §4.2's checkpoint.** The same test this document
already applies to §4.2 ("Why §4.2's checkpoint has no recorded review marker," above) gives the opposite answer
here: does this fact need to survive a genuinely cold session, with nothing but document state to derive from?
§4.2's checkpoint doesn't, because the session simply stops and waits there — nothing proceeds until a human
resumes it, so there's no way for "was this looked at" to matter to anything downstream. §5.2's loop is
different: it moves on to the next placeholder itself, in the same sitting, once a behavior is confirmed. A
session that dies between writing a leaf and presenting it leaves document state that's indistinguishable from
one that died after confirmation — and §1's own mechanical check, run cold by a fresh session or
`next-unit-of-work-detector`, would read "not `//TODO`" as "done" either way, silently skipping the one check
§5.2 exists to perform. The marker costs one line, removed once confirmed, in exchange for closing that gap —
cheap enough not to fight §5.2's own "speed over rigor" character (see "Why §5's per-behavior check and §7.2's
review are different events," above), unlike a full `reconciliation:`-style block. `//REVIEW` is also what
§7.2's own `//REDESIGN_REQUIRED` resolves back to (below) — one marker, two roads in: a behavior's first
derivation, or a later re-derivation after an invalidation gets fixed.

**Why `//REDESIGN_REQUIRED` always resolves through a fresh `//REVIEW`, never straight back to approved.**
Dogfooding WVR-95's own §7.2 pass surfaced that an invalidated behavior isn't automatically safe again just
because its disconnect got resolved — what's recorded after a fix is, in both the accept and reject resolutions
(accept the new behavior, or evolve the design to preserve the old one), *not the thing that was originally
invalidated*. Skipping straight back to approved would mean trusting an outcome nobody has actually looked at
yet, defeating the entire purpose of the invalidation catching it in the first place. Routing back through
`//REVIEW` costs nothing extra beyond what §5.2's own first derivation already costs, and guarantees the thing
eventually marked approved is always the thing someone actually confirmed.

**Why removal is a third resolution, not a special case of reject.** The same dogfooding pass surfaced a case
neither accept nor reject actually covers: the evolved design doesn't produce a *different* result for this
behavior, it doesn't produce this behavior under any entry state at all anymore — there's nothing left to accept
or preserve. Treating that as "reject" would leave a behavior standing that the design can no longer actually
exercise; treating it as "accept" would mean recording a Then that doesn't exist. Removing it outright is the
only honest option, but it's the one resolution here that's irreversible in a way the other two aren't — accept
and reject both leave a real, re-derivable behavior on record either way, removal leaves nothing. That's why it
gets its own explicit bar (an unambiguous question, an unqualified affirmative) rather than inheriting whatever
scrutiny the accept/reject choice already carries — the two aren't the same weight of decision even though both
resolve `//REDESIGN_REQUIRED`.

**Why a regeneration that matches the recorded result doesn't need fresh human review — only when it's re-verifying
an actual prior approval.** §7.2's whole invalidation mechanism exists to catch cases where the design genuinely
no longer produces what was agreed — not to manufacture review work every time a dependency's checksum merely
changes. If tracing a behavior's entry state through the current, checksummed design reproduces exactly what's
already recorded, and this behavior already carried a real, human-granted `reviewed_by`/`reviewed_at` that §7.1's
invalidation walk just cleared, nothing about the actual, previously-approved outcome has changed — only
bookkeeping needed refreshing. Regenerating and confirming the match is squarely mechanical work the agent can do
itself there; asking a human to re-bless a result that's provably identical to what they already blessed would be
re-litigating a decision nobody has disagreed with, for the sake of a checksum that happened to move.
`reconciliation-checksum-utility`'s own `write` mode already reflects this — it refreshes checksums without
touching `reviewed` on a clean pass — this section just makes explicit what that implementation choice depends
on: that a real regenerate-and-compare step ran first and found a match *against an already-approved baseline*,
not that checksums matching alone is sufficient. A behavior that has never carried `reviewed_by`/`reviewed_at` at
all — reaching §7.2 for the first time, as every behavior does on a Feature's first pass through it — has no
prior human judgement to re-litigate in the first place; a match there says the recorded content is technically
consistent with current design state, nothing about whether anyone has actually looked at it and agreed it's
right. That first look is never something a match result can stand in for.

**Why §7.2 runs project-wide (§1 step 9), not scoped to the Feature being worked on.** §7.1's own invalidation
walk (above) doesn't stop at this Feature's boundary — a changed function can reach any behavior whose call tree
touches it, in any `SB-NNN`, from any Feature, including one already shipped. Scoping §7.2 to just the current
Feature's own `SB-NNN`s would let those invalidations sit uncaught, silently leaving a previously-approved
behavior stale while this Feature's own review proceeds around it. The same reasoning is why it's a fixed-point
scan, not a single sweep: resolving one disconnect (accepting a change, or evolving a function to reject one) can
itself invalidate a different, previously-clean behavior discovered mid-pass, which has to re-enter scope rather
than being missed because the scan already passed it once.

**Why §7.1 is a subset check, not an equality check.** A use case's Technical Interpretation and an entry point's
own designed pseudocode are written for different purposes and can never read the same — one is deliberately
solution-independent, the other names real addresses (Pseudocode Style §2). Requiring them to match textually
would be requiring something that's structurally impossible by design, not a meaningful check. Requiring instead
that everything the Technical Interpretation asks for has a corresponding path through the designed pseudocode
is the actual property that matters — the design satisfies the use case — and it's the same relationship a
shared operation already needs between several use cases at once (§3): each one only needs to be covered, not to
be the whole story.

**Why an unexpected side effect can't be resolved mechanically.** The subset check (above) can tell, mechanically,
whether an effect is present or absent — it can't tell whether an unanticipated one is a bug in the design or a
gap in the use case's own understanding, because both look identical from the design's side: an External
Dependency interaction the Technical Interpretation never mentioned. Only a human looking at what the effect
actually is, in context, can tell which. That's also why it's the one finding in this whole process allowed to
send work back into Analysis rather than staying inside Design (§8) — the design didn't necessarily do anything
wrong, so the fix isn't necessarily the design's to make.

**Why the bound pseudocode is recorded on the `SB-NNN`, not left implicit in §3's classification.** Classifying
a function as-is, extended, or new records *that* something satisfies a piece of the Technical Interpretation;
it doesn't record *which* piece, or how the substitution actually reads once made. Without recording the bound
pseudocode itself, every later step — deriving a Then (§5), reconciling it (§7.1) — would have to re-derive the
same substitution from the classification and the Technical Interpretation each time, silently repeating
judgement work that only ever needed doing once. Recording it once, on the `SB-NNN` it belongs to, is also what
makes reconciliation a cheap checksum comparison (§7.1) instead of a semantic walk run from scratch on every
check.

**Why substitution isn't fixed at single-call granularity.** An earlier framing of gap analysis considered only
one call (`<--[...]`) at a time. That's too narrow: a single existing function is often broad enough to satisfy
an entire branch of a Technical Interpretation's pseudocode, or, occasionally, the whole thing — and forcing the
judgement down to one call at a time in those cases would produce a bound pseudocode that's technically
substituted but reads as a needlessly fragmented restatement of what one function already does in full. Letting
the unit of substitution be whatever piece — a call, a branch, or the whole body — a candidate's own pseudocode
or prose genuinely stands in for keeps the bound pseudocode as simple as the actual design allows.

**Why `reconciliation:` is checksums, not a checkbox.** A checkbox only ever records that a check passed once;
it can't say whether it's still true. Checksums make the record falsifiable: recompute them later, and a
mismatch against what's recorded means something the check depended on has changed, without needing to re-read
or re-reason about content that hasn't actually moved — the same shape of argument this repo's own `.index/`
files (documentation-standards.md §4) make for staying accurate without a human re-deriving them by hand.
