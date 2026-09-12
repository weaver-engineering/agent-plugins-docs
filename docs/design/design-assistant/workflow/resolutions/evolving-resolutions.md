# Evolving A Resolution

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions, whose prose and tools this document is about writing
* [Workflow](../WORKFLOW.md) §2.3, §2.5 - the resolution loop, and soft resolution
* [Evolving A Check](../checks/evolving-checks.md) - the other half, and what a check owes a resolution
* [Write Contract](../../serialization/write-contract.md) §3, §5 - the edits every writing resolution composes
* [Claim Model](../../serialization/claim-model.md) §2 - grounding, and why prose location follows from it
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §3.1, §6 - acknowledgement and review
* [Decision Model](../../datamodel/decision-model.md) §3 - the `KeyDecision` a few resolutions produce

## 1 What This Document Is

Every other document in this directory states what one resolution is **for**. [Workflow](../WORKFLOW.md) §7 fixes
the set of routes, what each one means, and whether it is mechanical — and says outright that the prose and the
tools are P6's to write. This document states how to write them, and §5 gives the template the result is written
in.

A resolution is a **skill**: prose instructions plus tools. So the two things missing from every resolution
document are the tools it calls and the elicitation it conducts. Everything else is already there, including the
postcondition, which the existing `What Must Be True Afterwards` sections state well.

Unlike a check, a resolution needs no algorithm. What varies is not how it decides — mostly it does not decide,
the architect does — but **what it asks, what it calls, and what it leaves behind**.

## 2 What A Resolution Never Decides

### 2.1 It Does Not Write

The service writes. Every obligation involving an anchor, a digest or a signature belongs to the writer, and the
author never sees a checksum ([Write Contract](../../serialization/write-contract.md) §1). A resolution decides
what a document should **say** and what that prose **claims**; it never produces frontmatter.

[Write Contract](../../serialization/write-contract.md) §3's ten edits are therefore the vocabulary every writing
resolution composes, and §5's rule binds all of them: where an edit disturbs a claim's anchor, the **disposition
is stated and never inferred**. A resolution that deletes, splits or merges a section owes that statement, and a
resolution that guesses it produces a well-formed attested document making a claim nobody checked.

### 2.2 Where What It Writes Lives

Nowhere in particular. No document is an entity and the model is the fold over every claim in scope
([Serialization](../../serialization/SERIALIZATION.md) §2), so a claim's location carries no meaning.
**Acknowledgements and reviews live wherever they are written.** There is no location policy to design, and a
resolution that invents one is imposing a constraint the fold does not have.

The one thing that is not free is a consequence of grounding rather than of location: an authored claim must
anchor within its own document ([Claim Model](../../serialization/claim-model.md) §2), so deciding where the prose
goes *is* deciding which document carries the claim. They are one act, not two.

### 2.3 Which Condition It Is Addressing

The finding arrives **disambiguated**. A finding kind can describe two or three different situations, and the
disambiguator ([Evolving A Check](../checks/evolving-checks.md) §2.4) collapses them to the one this instance is.
So a resolution never re-derives which case it is looking at, and a resolution document does not enumerate the
cases of every kind it applies to — which is what stops the broadest of them,
[correct-the-design](correct-the-design.md), from having to account for twenty-two.

## 3 Mechanical, Properly Stated

[Workflow](../WORKFLOW.md) §7 marks a resolution mechanical or not. Read carelessly that looks like a question
about who performs the edit, and it is not: the service always performs it (§2.1). It is a question about whether
a **decision** is required — and it has two independent parts that one field hides.

| | Asks |
|---|---|
| **Decision** | is there one, and does it sit in *choosing the route* or *inside the resolution* once chosen |
| **Operation** | once decided, is the result determined, or is the edit open-ended |

[promote](promote.md) is the clearest case of the split. Deciding *to* promote is a real judgement, because a new
design target costs its own design work, ticket, review and NFR assessment — but once taken the operation has five
defined effects and no further choices. [acknowledge](acknowledge.md) is the opposite arrangement: choosing the
route is a decision *and* the body is a judgement, since the reason is its entire content.
[regenerate](regenerate.md) has neither.

**The two parts together decide what gets built**, which is why this replaces a yes/no rather than rewording it:

| Shape | Decision | Operation | Built as |
|---|---|---|---|
| **Run it** | none | determined | one subcommand, invoked and finished |
| **Confirm and run it** | the route, or a confirmation | determined | one subcommand behind a confirmation gate |
| **Elicit, then write narrowly** | inside | open-ended | an elicitation loop over the writer's narrow edits |

In the default set, *run it* is [regenerate](regenerate.md) alone; *confirm and run it* covers
[promote](promote.md), [remove-the-element](remove-the-element.md), [acknowledge](acknowledge.md),
[approve](approve.md) and [declare-the-design](declare-the-design.md); everything else elicits. A confirmation
gate is not uniform, either — [remove-the-element](remove-the-element.md) requires an unambiguous confirmation
naming exactly what goes, never a general nod at a batch
([Reconciliation Model](../../datamodel/reconciliation-model.md) §6.3).

**This grouping is what orders the work.** Resolutions cluster by the tool they compose, and the clusters cut
across the eighteen — `state-the-fact`, `exempt`, `record-sourcing`, `re-express` and `prune-the-cell` are all
"prose plus claim, a different question asked." So the real inventory is the writer's edits, a few record-writers
and the two genuinely determined operations, which is far fewer than eighteen tools. Build a cluster's tool once,
against its first real consumer, and the rest of the cluster is elicitation.

## 4 The Evolution

### 4.1 State The Decision And The Operation

§3's two questions, answered for this resolution, which settles which of the three shapes it is and therefore
what there is to build. Where a confirmation gate is required, state what it must name.

### 4.2 Establish The Tool

Which of [Write Contract](../../serialization/write-contract.md) §3's edits it composes, which record it writes,
or which determined operation it invokes — and whether that tool already exists, needs extending, or is new.

A new tool is the expensive answer and the shareable one, so it is worth knowing before a cluster is started
rather than discovered inside it. Tools are CLI subcommands over a service layer, so that a daemon or an MCP
server is a later swap-in on the same interface.

### 4.3 Write The Elicitation

For an eliciting resolution, what the architect is actually asked, and in what order. This is the resolution's
substance and the reason it is a skill rather than a function.

Two obligations recur and are worth stating in any elicitation that can reach them. A resolution must never
**invent a fact to clear a finding** — a `purpose` written to satisfy a check is worse than an absent one, because
the absence was reportable and the invention is not. And where the correct fix belongs to another design target,
the resolution is the wrong one and [raise-a-change-request](raise-a-change-request.md) is right; the tell is
authority, not difficulty.

For a determined resolution, say **none** and say why.

### 4.4 State The Postcondition

What must be true afterwards. One clause is universal and comes from the resolution loop
([Workflow](../WORKFLOW.md) §2.3): **the check that raised the finding no longer reports it for that subject.**
Re-running the check is what closes the loop, so it is also the resolution's own acceptance test.

The rest is particular, and the existing `What Must Be True Afterwards` sections are already the right shape.

### 4.5 Decide What Is Logged

The design assistant keeps a **log**, keyed on the product or service slug and held outside the products
directory. It exists for debugging, troubleshooting and metrics, and it is **never load-bearing**: the model is
fully derivable from the design directory alone, so **no check may read the log**. A check that read it would make
it load-bearing and break that property.

That makes it the right home for the **options a resolution considered and set aside**. The first change that
would evaporate a finding is often not the best one, so real effort belongs in finding the better one — and the
options examined on the way are worth keeping without being worth recording *in the design*:

* **A discard is state-relative.** Once the design changes, the question is being asked of a different design, so
  an option rejected before may be right now. Recording it in the design would make an expiring judgement look
  permanent, and the design's registers hold its current state rather than its history.
* **A `KeyDecision` is the stronger thing, and most corrections do not raise one.** A key decision settles
  something about what the design *is* — adding a boundary — and its discarded candidates are durable, which is
  what stops a rejected option being re-proposed
  ([take-a-decision](take-a-decision.md)). Most corrections are iterative evolution of prose and of the functions
  on a boundary, and raise nothing of the sort. The test is whether the discard survives the design changing.
* **Logging them makes the search reviewable.** A later review of the log can surface what a single architect may
  not notice, and what several architects working one design almost certainly will not: that the same solution
  keeps being proposed and rejected for weak reasons, or on cost. The more often a solution is rejected because
  it is expensive, the likelier that cost is worth bearing — each rejection means a workaround was paid for
  instead, and those accumulate where the one-off cost would not.

So a logged option wants enough structure to be **filtered** — the option, the finding it was considered against,
and the shape of the reason — because that is what narrows a review to the entries worth reading. Whether two
entries are *the same solution rejected again* is a **judgement** rather than a count: the same option described
in different words is still the same option, and the review that notices is an agent reading the log, not a query
over rows. Structure serves the narrowing; the judgement stays judgement.

### 4.6 Work An Example

A real finding, the elicitation as it actually runs, the edit, and the check clean on re-run. As with a check, this
is the acceptance criterion rather than an illustration, and it is nearly free while the tool is being dog-fooded
against a live design.

## 5 The Template

```markdown
# {resolution-slug}

## Context
{links to WORKFLOW §7, and to every document defining what this resolution writes or invokes}

## Purpose
{what this resolution does, and why it is a distinct route rather than a case of another}

## Applies To
{every finding kind naming this route}

## Decision And Operation
| | |
|---|---|
| Decision | {none | the route | inside} |
| Operation | {determined | open-ended} |
| Shape | {run it | confirm and run it | elicit then write narrowly} |
| Confirmation | {what a gate must name, or none} |

## What It Does
{the steps, as the existing documents already state them}

## Tools
{§4.2 — the writer edits composed, the record written, or the operation invoked; existing, extended or new}

## Elicitation
{§4.3 — what the architect is asked and in what order; or `None.` with the reason}

## What Must Be True Afterwards
{§4.4 — including that the raising check no longer reports the finding for that subject}

## What Is Logged
{§4.5 — the options considered and set aside, structured enough to filter; or `Nothing beyond the operation.`}

## Worked Example
{§4.6 — finding, elicitation, edit, clean re-run}

## Notes For P6
{the sharp edges, and what a reader should not conclude}
```

`Decision And Operation` **replaces** `Mechanical` rather than sitting beside it: unlike a check's
`What It Inspects` and `Positions`, which serve different readers, these two would answer one question twice. The
existing eighteen documents keep `Mechanical` until each is evolved.

## 6 When A Resolution Is Done

* the decision and the operation are both stated, and the shape follows from them;
* any confirmation gate says what it must name;
* every tool is identified as existing, extended or new, and a new one is specified;
* the elicitation is written, or declared unnecessary with a reason;
* the postcondition includes the raising check reporting nothing further for that subject;
* what is logged is stated, structured enough to filter a later review;
* the worked example runs.

# Rationale

**Why a resolution needs no algorithm where a check does.** A check's whole content is how it decides, so stating
the algorithm is most of specifying it. A resolution mostly does not decide — the architect does — so its content
is the question put to them, the call made afterwards, and what is true when it returns. Asking for an algorithm
would invite writing down a decision procedure for something deliberately left to a person.

**Why `Mechanical` decomposes rather than being reworded.** As a single flag it conflates three things: who edits,
whether a judgement is required, and whether the operation has one outcome. The first is never in question. The
other two vary independently — promotion is a hard decision with a determined operation, acknowledgement an easy
one whose whole content is judgement — and the pair is exactly what decides whether the thing built is a
subcommand, a gated subcommand, or an elicitation loop. A flag that cannot distinguish those is a label rather
than a specification.

**Why discarded options go to the log and not into the design.** They look like the discarded candidates of a
`KeyDecision`, and they are not, because a correction's premise moves the moment the correction lands. A durable
record of "this was considered and rejected" is right for a decision about what the design *is*, and wrong for a
judgement about how to adjust the design as it stood an hour ago — it would deter exactly the reconsideration that
a changed design makes legitimate. The log keeps the trail without making the claim.

**Why the log must stay unreadable to checks.** Its value is that it records things the design deliberately does
not, which only stays true while nothing depends on it. A check that read the log would make the log load-bearing,
and the property that the model is fully derivable from the design directory — which is what makes the whole
scheme safe to lose and rebuild — would quietly stop holding.

**Why logged discards carry structure without being made countable.** The reviewable question is not "what was
considered here" but "has this been rejected before, and why" — and that is a judgement, because the same option
described in different words is still the same option. So the review is an agent reading the log rather than a
query counting rows, and structure earns its place by narrowing what has to be read rather than by computing the
answer. Demanding a countable form would buy a precision the question does not have, and would force a category
vocabulary into existence before there are any logs to derive one from.
