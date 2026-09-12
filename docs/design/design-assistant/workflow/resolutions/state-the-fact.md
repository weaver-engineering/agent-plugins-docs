# state-the-fact

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Evolving A Resolution](evolving-resolutions.md) - the evolution this document is the first product of
* [boundary-identity](../checks/boundary-identity.md) - the check that owns building this route
* [Decision Model](../../datamodel/decision-model.md) §5 - every authored fact records how it entered the model
* [Write Contract](../../serialization/write-contract.md) §2, §3, §5 - one transaction, the ten edits, and claim disposition
* [Claim Model](../../serialization/claim-model.md) §2, §4 - grounding, and prose pointers
* [Assessment And Trust](../../serialization/assessment-and-trust.md) §3 - frontmatter the service did not write is a proposal

## Purpose

Supply what is absent. This is the most common resolution in the workflow and the least interesting one to
describe, because what varies is entirely what the finding asked for — an attribute, a behavior, a fixture, a
predicate, an endpoint, the substance of an exemption.

## Applies To

`unstated-required-attributes`, `uncovered-cell`, `unexplained-exclusion`, `unassessed-manifest-setting`,
`unassessed-nfr-rule`, `unassessed-perimeter-vector`, `unresolved-type`, `unresolved-nfr-scope`,
`missing-fixture`, `no-suitable-fixtures`, `unpredicated-effect`, `unexpected-side-effect`, `missing-sli`,
`unbacked-sli`.

## Decision And Operation

| | |
|---|---|
| Decision | **inside** — the route is obvious once a position is absent; what the fact *is* is the judgement |
| Operation | **open-ended** — the prose is written, and where it goes is part of the answer |
| Shape | **elicit, then write narrowly** |
| Confirmation | none. Nothing is overwritten that was not the subject of the finding |

## What It Does

1. Establishes what the absent fact actually is — which is elicitation, not transcription, wherever the answer
   is not already written in the design's prose.
2. Writes the prose that says it, in the document where it belongs.
3. Has the service write and sign the claim indexing that prose.

## Tools

**New. This route's tool is built here**, as the first of its cluster
([Evolving A Resolution](evolving-resolutions.md) §3) — `exempt`, `record-sourcing`, `re-express` and
`prune-the-cell` are the same tool with a different question asked, so each of those is elicitation once this
exists.

One subcommand, over a service layer so a daemon or MCP server is a later swap-in. It takes the subject address,
the positions being stated, the prose, and where the prose goes — and composes whichever of
[Write Contract](../../serialization/write-contract.md) §3's edits that answer implies:

| Where the prose goes | Edit composed |
|---|---|
| a section that already says it | change the document's claims without touching prose |
| a section that should say it and does not | replace that section's prose, its claims, or both |
| no existing section is the right home | insert a section — renumbering its siblings |
| no existing document is the right home | create a document, within scope and not within a child design directory |

**The tool chooses none of this.** It executes the answer the elicitation produced. It never selects a document,
never drafts prose, and never infers a claim's disposition — where an inserted or replaced section disturbs
another claim's anchor, the disposition is stated by the author and the writer refuses to guess
([Write Contract](../../serialization/write-contract.md) §5).

Prose and claim are written as **one transaction**
([Write Contract](../../serialization/write-contract.md) §2), which is what makes same-document staleness
impossible rather than merely unlikely.

## Elicitation

Five steps, and the order matters — the first two exist to stop the resolution writing prose that the design
already contains.

**1. Read the finding out, in the model's own terms.** Not "supply `purpose`" but what `purpose` means for this
subject: what is this boundary responsible for. The finding's detail is the position list
([Evolving A Check](../checks/evolving-checks.md) §3.2), so this is presenting it rather than composing it.

**2. Ask whether the design's prose already says it.** For any design brought under the model that was not
authored through it, this is the **ordinary case**: the prose is there and only the claim is missing. Where it
is, the architect points at the prose, the claim anchors to it, and **no prose is written at all** — a
`Prose`-typed position can hold the anchor rather than a copy ([Claim Model](../../serialization/claim-model.md)
§4). Skipping this step is how the resolution ends up restating what a document already said, two sections apart.

An architect may equally have written the claim straight into the frontmatter. That is a supported route rather
than a workaround: it is read as a proposal, re-judged against the prose, then written and signed
([Assessment And Trust](../../serialization/assessment-and-trust.md) §3).

**3. Where the prose does not say it, establish the fact — and take the honest exit where there is one.**

| What the architect's answer turns out to be | Route |
|---|---|
| known, and merely unwritten | continue here |
| something that has to be **chosen** rather than transcribed | [take-a-decision](take-a-decision.md) |
| owned by **another design target** | [raise-a-change-request](raise-a-change-request.md) |
| **not knowable yet** | an `OpenDesignQuestion` — recorded with what it blocks; the finding stands |

The third row's tell is **authority, not difficulty**. The fourth resolves the unit of work without resolving the
finding, which is the honest outcome and not a failure of this resolution.

**4. Ask where the prose belongs.** This is also the choice of which document carries the claim — an authored
claim anchors within its own document, so they are one act rather than two
([Evolving A Resolution](evolving-resolutions.md) §2.2). The layout standard shapes where such prose belongs; the
architect decides, and the tool is told.

**5. Write, and re-run the raising check.** Re-running is the resolution loop, not a verification step
([Workflow](../WORKFLOW.md) §2.3) — and resolving one position frequently clears findings elsewhere in the same
check's set.

**Never invent a fact to clear a finding.** A `purpose` written to satisfy a check is worse than an absent one,
because the absence was reportable and the invention is not. Where the answer is not known, step 3's fourth row
is the outcome, and it leaves the gap visible.

## What Must Be True Afterwards

* the raising check no longer reports that finding for that subject
  ([Evolving A Resolution](evolving-resolutions.md) §4.4);
* the fact is stated in prose a person can read, not only in frontmatter;
* the claim carries `_sourcing` — how the fact entered the model and who may change it
  ([Decision Model](../../datamodel/decision-model.md) §5);
* the claim is anchored in prose within its own document, with a digest
  ([Claim Model](../../serialization/claim-model.md) §2);
* where the edit disturbed another claim's anchor, its disposition was **stated rather than guessed**.

## What Is Logged

**Nothing beyond the operation.**

The log exists for options a resolution **considered and set aside**
([Evolving A Resolution](evolving-resolutions.md) §4.5), and this resolution does not choose among options: an
absent fact has one answer, and finding it is elicitation rather than search. Wording a `purpose` two ways and
preferring one is drafting, not a design option, and logging it would fill the log with the noise a later review
has to read past.

Where step 3 exits to another route, whatever was weighed belongs to **that** resolution's log if it keeps one —
`take-a-decision` records its candidates in the design itself, durably, because a key decision's discards survive
the design changing.

## Worked Example

**Not yet a recorded run**, for the same reason as [boundary-identity](../checks/boundary-identity.md): the
pre-parse stage is unbuilt, so no design directory is parseable and there is nothing to run against. This is the
acceptance test to be run when the tool is built.

Against `boundary-identity`'s second expected finding — `bnd/design-assistant/bnd/parser` missing `name`,
`purpose` and `kind`, a boundary that exists only because a function address names it:

1. The positions are read out: what is `parser` called, what is it responsible for, and what is its role inside
   `design-assistant`.
2. Asked whether the prose already says it — and here it does not, because `parser` was conjured by an address.
3. The fact is established. `kind` is `business-domain`; `name` and `purpose` follow from what the architect
   intends `parser` to be responsible for. Had the answer been "nothing — that address is wrong", the route is
   `correct-the-design` and this resolution is not the one.
4. The prose belongs in the document describing the design's structure; the claim will anchor there.
5. Written in one transaction. `boundary-identity` re-runs and reports nothing for `bnd/.../parser`.

## Notes For P6

**Step 2 is the step that will get dropped, and it is the one that earns the most.** Every instinct in an
eliciting agent is to ask the architect for the fact, and for an adopted design the fact is usually already
written down — so the resolution's first move should be to look, not to ask
([Data Model](../../datamodel/DATA-MODEL.md) §1.1).

**This resolution builds the cluster's tool, so its shape will be visibly wrong by the third consumer.** That is
expected and is better planned for than avoided: `exempt` and `record-sourcing` will want the same write with a
different question, and the commonalities only become apparent against real cases. One deliberate refactor of the
tool around the third or fourth consumer beats over-specifying it now.

**The postcondition that matters least in prose matters most in practice.** "The fact is stated in prose a person
can read, not only in frontmatter" is what keeps the design recoverable when frontmatter is lost
([Serialization](../../serialization/SERIALIZATION.md) §5), and it is the one a tool optimised for clearing
findings quickly would quietly violate.
