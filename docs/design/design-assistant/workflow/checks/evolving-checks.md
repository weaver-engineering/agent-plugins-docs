# Evolving A Check

## Context
* [Workflow](../WORKFLOW.md) §3 - the check interface every check satisfies
* [Workflow](../WORKFLOW.md) §4 - the default configuration, and where each check is registered
* [Data Model](../../datamodel/DATA-MODEL.md) §1 - a check defines the positions it requires
* [Claim Model](../../serialization/claim-model.md) - the claim, its grounding, and how a position is spelled
* [Parse Contract](../../serialization/parse-contract.md) - the fold every model check reads
* [Write Contract](../../serialization/write-contract.md) - what a writer guarantees, and what it is agnostic of
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §3 - findings, and the soft resolutions that key onto them

## 1 What This Document Is

Every other document in this directory states what one check is **for**: its purpose, where it is registered, what
it inspects, and the findings it raises. That is a complete design and an incomplete specification. This document
states how to take a check from there to something buildable, and §5 gives the template the result is written in.

**One thing is missing from every check document, and everything else follows from it: how the check functions.**
The algorithm is the unit of understanding. The positions a check requires, the projection it needs, the content of
its findings and the work its resolutions do are all consequences of the algorithm — which is why §3 states it
first, and why that order is not a matter of presentation (§3.1).

A check's evolution decides very little else. How a position is written, how the model is queried, who writes and
what a finding's condition is are settled for every check at once (§2). A check neither revisits them nor extends
them, which is what keeps 55 evolutions from being 55 designs.

## 2 What A Check Never Decides

### 2.1 How A Position Is Written

Positions serialise as YAML under `_claims`, spelled exactly as the data model spells them, at whatever depth the
data model puts them ([Claim Model](../../serialization/claim-model.md) §1). The parser folds every claim naming an
address: lists are additive, order where it matters is an attribute rather than a sequence, and competing or
duplicated claims are **findings rather than failures**
([Parse Contract](../../serialization/parse-contract.md) §3).

So the addressing convention is not an open question, and a check never states one. It states **which** positions it
requires (§3.2) and nothing about how they are written down.

### 2.2 The Model's Query Surface

The model sits on an **open schema**, so it offers only what an open schema can:

| Method | Returns |
|---|---|
| `model.get(kind, address)` | `positions` — a JSON object |
| `model.list(kind)` | `positions[]` — a JSON array |
| `model.list(kind, predicate)` | `positions[]` — the same, filtered |

`positions` carries more than the values. It carries the index of the **anchors and documents claiming them**, which
is what lets a resolution write back into the right anchor of the right document rather than rediscovering where a
fact lives.

A handful of things are built in because every check needs them: `Acknowledgement`, `ChangeRequest`, `Provenance`,
`Approval`, positions and findings.

**Anything that requires a schema is a projection, and a projection is the check's to define** (§3.3). The model
cannot offer typed access to a shape it does not know it has.

### 2.3 Who Writes

Three parties, and a check is none of them:

| Party | Owns |
|---|---|
| **Serialization** | what a valid claim *is* — its grounding, its anchors, the spelling of its attributes |
| **The writer** | serialising a given prose-and-claim pair with falsifiable checksums and signatures |
| **The resolution** | generating the prose and the claims, and deciding where they go |

The writer is **model-agnostic**. It is told to set the prose at an anchor to some text and bind a claim to it; it
has no opinion on what either means. So the question
[Serialization](../../serialization/SERIALIZATION.md) §2 explicitly disclaims — which document a derived claim with
no prose to anchor to lives in — does not fall to the writer either. **It belongs to whichever resolution produces
that claim**, and is answered when that resolution is evolved.

A check reads and reports. It writes nothing, holds no cache and remembers no previous run
([Workflow](../WORKFLOW.md) §2.6).

### 2.4 What A Finding's Condition Is

A finding's condition digest — what a soft resolution keys onto ([Workflow](../WORKFLOW.md) §2.5) — is:

> the subject address, the finding kind, a canonical list of the unmet positions, and a **disambiguator** where the
> check needs one.

The disambiguator is the check's own, mechanically generated and idempotent. A check declares one when subject, kind
and unmet positions do not distinguish its findings from each other — which is every check whose finding is a
computed judgement over positions that are all present rather than an absence. What the value is, is the check's
business; that it is stable across runs given the same design is not.

**A check with settings must fold its effective setting values into its disambiguator.** Otherwise
[Workflow](../WORKFLOW.md) §3.4's rule that changing a budget changes the condition does not hold, and an
acknowledgement made against a budget of 15 goes on standing at 10.

A change to the digest evaporates any soft resolution keyed on it; restoring the digest reinstates it.

**The check is not part of what an acknowledgement keys on.** What an architect acknowledges is the condition,
not who noticed it — so where two checks produce findings agreeing on kind, positions *and* disambiguator, an
acknowledgement of the first acknowledges the second. That is the correct behaviour rather than a collision: two
checks that genuinely see the same condition at the same address are reporting one thing, and the disambiguator is
what keeps checks that only look similar apart.

Throughout this document **acknowledgement** covers a `ChangeRequest` too. They are not the same thing — one leaves a
level achievable and the other does not ([Workflow](../WORKFLOW.md) §2.5) — but they sit in the same place and key
on the digest identically, so the distinction is only made where it matters.

### 2.4.1 A Check Reports Its Acknowledged Findings

**A check answers with the findings it has soft-resolved as well as the ones it has open.** This costs nothing: a
check already has to compute each digest to know whether a standing acknowledgement matches it, so reporting the
matched ones is returning what was computed rather than filtering it away.

It buys two things. The architect sees what has been acknowledged and blocked at each level as well as what is
outstanding, which is what keeps them in ownership of how the design evolves rather than being handed one next
action. And an unrequired acknowledgement becomes **falsifiable**: an acknowledgement records the check that gave
rise to it, so one whose check **ran and did not report it** is answering a condition that no longer arises.

Two constraints keep that sound:

* **Only a completed check falsifies.** A skipped or blocked check reports nothing trivially
  ([Workflow](../WORKFLOW.md) §2.3), so an acknowledgement belonging to one is unknown rather than unrequired, and
  is retained.
* **Clearing is invoked, scoped and never implied.** Clearing unrequired acknowledgements — by check, by maturity
  level, or across the design — removes only those whose check completed in that run and did not report them.
  "Across the design" never means every acknowledgement, and the difference between those two readings is the
  difference between a cleanup and irreversible data loss on a partial check set.

## 3 The Evolution

Six steps. The order of the first two is load-bearing; the rest follow naturally.

### 3.1 State The Algorithm

How the check decides, in enough detail that §3.2 is transcription rather than judgement:

* what it iterates over, and what bounds that set;
* what it compares, computes or resolves for each member;
* what makes an instance a finding;
* what it deliberately does not inspect, and which check does instead.

**A check that cannot be stated this way is not yet understood**, and the remaining five steps will produce a check
that runs, reports confidently, and asks the wrong question.

### 3.2 List The Positions

The attribute paths the algorithm reads, each with its type.

**This list defines the positions; it does not report them.** The model is open, and a check is what gives a position
meaning ([Data Model](../../datamodel/DATA-MODEL.md) §1) — so the data model documents are a convenience for
understanding how positions accumulate into something later checks and reconciliations can rely on, not the authority
that licenses them. A position no model document names yet is therefore legitimate rather than a mistake: the check
declaring it is what brings it into the schema, and the model document is owed a link back to the check that defines
it.

Where the model already names a position, its spelling governs, since a claim spells an attribute exactly as the
model spells it ([Claim Model](../../serialization/claim-model.md) §1). Cite the model document in that case, for a
reader's orientation. Where it does not, the check chooses the spelling and says so.

This list is not only the check's schema contract. For every finding that reports an absence it is also the finding's
own content, since `unstated-required-attributes` names the positions **this check** requires and does not find
([Workflow](../WORKFLOW.md) §2.3).

### 3.3 Decide The Projection

Three answers, cheapest first:

| Answer | When |
|---|---|
| none — raw `model.get` / `model.list` | the algorithm reads positions and compares values |
| an existing projection, perhaps extended | another check has already built the view this one needs |
| a new projection | the algorithm needs a shape the model cannot offer over an open schema |

A projection is **model-derived computation, not an accessor**. `new Behaviours(operation).getGivenTree()` computes
something that is nowhere claimed. It is a design unit in its own right, it is the expensive answer, and it is
shareable — which is why §4 makes it the thing that orders work within a stage.

**A projection may raise a finding**, and must, where positions do not support the shape it builds: an inconsistency
that stops a projection resolving is a design fault needing resolution, not an error to swallow.

Where that inconsistency **should already have been reported by an earlier check**, the projection fails with an
**exceptional finding**: kindless, carrying a log of what was inconsistent. Four properties follow from having no
kind:

* it is **ambiguous by construction** — either the design is inconsistent and no check caught it, or a check is
  missing from the configuration. The log exists because the tool cannot tell which, and the two resolve
  differently, which is precisely why it has no kind. Triage is human.
* it is **not soft-resolvable**. No kind means no declared resolution routes, so there is nothing to acknowledge and
  no change request to raise against it. Acknowledging that a projection broke on positions nobody has diagnosed
  would ratify the inconsistency.
* it therefore **needs no condition digest** (§2.4). It is a different category, not a finding with a hole in it.
* it **needs no new runner state**. A check that raises one did not complete, so
  [Workflow](../WORKFLOW.md) §2.3 skips everything requiring it and §2.4 withholds the level. Nothing in the runner
  changes to accommodate it, though the check interface is owed a mention of it.

While the check set is deliberately partial — which it is throughout delivery — an exceptional finding is the signal
**naming the check still owed**, which is how each stage discovers the next one to build rather than relying on
someone noticing.

### 3.4 Define The Findings

For each kind the check produces:

| States | Meaning |
|---|---|
| kind | referenced, or defined inline ([Workflow](../WORKFLOW.md) §3.2) |
| raise condition | the state of the positions that produces it |
| subject | the address the finding is against |
| detail | what the finding says, concretely — for an absence, the positions from §3.2 |
| disambiguator | the check's own, or that it needs none (§2.4) |
| blocking | `at-registration`, `computed` or `advisory`; where `computed`, how `blocks` is decided per instance |

Aggregation is part of this: one finding per subject naming every unmet position is the usual shape, and a check that
departs from it says so.

### 3.5 Establish The Resolution Deltas

For each route the check's findings offer, whether the existing resolution already does this or needs new behaviour.
**The first check to need a route is the one that builds it** — including the prose, the tools, and for any resolution
producing a derived claim, where that claim lives (§2.3).

Tools are CLI subcommands written over a service layer, so that a daemon or an MCP server is a later swap-in on the
same interface rather than a rewrite.

### 3.6 Work An Example

Against real design content: the findings raised, the resolution applied, and the check clean on re-run.

This is the check's acceptance criterion, not an illustration. It is also the cheapest part of the evolution while
the tool is being dog-fooded against a live design, because the content is already there and the check has to be run
against something regardless.

## 4 Order Within A Stage

Identify which checks in the stage need a **new projection** (§3.3) before starting any of them, and evolve those
first. A projection built for one check is free to every later one, and the shape of a projection is far easier to get
right against a second real consumer than against an imagined set of them.

Otherwise, registration order ([Workflow](../WORKFLOW.md) §4). It is already a valid dependency order, because
`requires` must point earlier in the sequence ([Workflow](../WORKFLOW.md) §3.3).

## 5 The Template

```markdown
# {check-slug}

## Context
{links to the workflow section registering it, and to every model document defining a position it reads}

## Purpose
{the question this check asks, and why it is worth asking separately}

## Registration
| | |
|---|---|
| Stage | {pre-parse | maturity — `MN` | global} |
| Model check | {yes | no — and why} |
| Requires | {each required check, and what it establishes that this one needs} |

## What It Inspects
{the reader-facing statement: what this check looks at, in prose}

## Algorithm
{§3.1 — how it decides: what it iterates, what it compares, what makes a finding, what it leaves to others}

## Positions
| Position | Type | Model reference |
|---|---|---|
{§3.2 — every attribute path the algorithm reads; `new` where this check is what brings the position into the schema}

## Projection
{§3.3 — none, an existing one, or a new one specified here}

## Findings
| Kind | Raised when | Subject | Detail | Disambiguator | Blocking | Resolution routes |
|---|---|---|---|---|---|---|
{§3.4}

## Settings
{each setting's path, meaning, type and default — or `None.`}

## Resolutions
{§3.5 — per route: existing and sufficient, or the delta this check owes}

## Worked Example
{§3.6 — content, findings, resolution, clean re-run}

## Notes For P6
{the sharp edges: what is easy to get wrong, and what a reader should not conclude}
```

`What It Inspects` is kept alongside `Positions` deliberately. The first is prose for someone deciding whether this
check is the one they are looking for; the second is the contract an implementation is written against. They have
different readers, and collapsing them would cost the first.

## 6 When A Check Is Done

* the algorithm is stated to the point where the position list is transcription;
* every position is listed and typed, cited to a model document where one names it and marked new where none does;
* the projection is named — none, reused, or new and specified;
* every finding kind states its raise condition, subject, detail, disambiguator or none, and blocking mode;
* every resolution route is either existing and sufficient, or has its delta specified;
* settings are declared, or declared to be none;
* the worked example runs: findings raised, resolution applied, check clean.

# Rationale

**Why the algorithm comes before the position list.** The position list is the tempting place to start, because it
looks like the deliverable and it can be assembled by reading the model documents. Assembled that way it is a guess
that then gets justified, and the justification is indistinguishable from understanding — the check compiles, runs,
reports plausibly, and asks a question nobody checked. Deriving the list from a stated algorithm makes the list
falsifiable: a position the algorithm never reads has no business in it, and one the algorithm needs and the list
omits is a gap anyone can see.

**Why the projection decision gets its own section rather than living inside the algorithm.** It is the expensive
answer and the reusable one, so it is the thing that decides the order work is done in (§4). Making it findable by
scanning a check document, rather than by reading the algorithm closely, is what lets a stage be planned before it is
started.

**Why an exceptional finding has no kind.** A kind declares resolution routes, and the two things an exceptional
finding might mean — a design inconsistency nothing caught, or a check that does not exist yet — are resolved in
completely different places. Giving it a kind would mean choosing one of those readings at the moment the tool has
least information, and the log exists precisely because that choice cannot be made mechanically. Leaving it kindless
keeps the ambiguity visible and makes triage an explicit human act rather than a misrouted resolution.

**Why an unrequired acknowledgement is falsified by its check rather than swept while the model is built.** The
obvious sweep has to distinguish "this condition is gone for good" from "this is a different
finding of the same kind at the same address", and at parse time nothing can: the model holds conditions, not the
judgements that would raise them. The check is the only thing that knows which conditions it currently reports, so
asking it is the only way the question has an answer — which makes the sweep a check's output rather than a step in
folding the model. Keeping it deliberate and scoped rather than automatic follows from the cost of being wrong:
re-acknowledging is a minor annoyance, and deleting an acknowledgement belonging to a check that never ran is
irreversible.

**Why the check is recorded on an acknowledgement but is not part of its key.** The two do different jobs. What is
acknowledged is a condition, so the condition is what it keys on and an acknowledgement of one check's finding
stands against an identical finding from another — anything else would ask an architect to agree twice to one
thing. What the
recorded check buys is attribution for the *absence*: knowing which check should have reported a digest is what
turns "nothing reported this" into a fact about the design rather than a fact about which checks happened to run.

**Why a check writes nothing, stated as a rule about parties rather than a constraint on checks.** The temptation in
a check that has just diagnosed something precisely is to fix it, and the reason not to is not that checks are
forbidden from writing — it is that three separate concerns would collapse into one. Serialization decides what a
valid claim is, a resolution decides what to say and where, and the writer makes it durable without understanding
any of it. A check that wrote would have to hold all three opinions, and the model-agnosticism that makes the writer
reusable would be the first thing lost.

**Why the worked example is an acceptance criterion rather than documentation.** Every other part of a check
specification can be internally consistent and still ambiguous, because prose describing an algorithm is checked
only by whoever reads it. An example run against real content is checked by the tool. It is also nearly free during
dog-fooding, where the check has to be run against a live design anyway — so the marginal cost is recording the
result rather than producing it.
