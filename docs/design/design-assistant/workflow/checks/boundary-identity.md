# boundary-identity

## Context
* [Workflow](../WORKFLOW.md) §4.2 - where this check is registered
* [Evolving A Check](evolving-checks.md) - the evolution this document is the first product of
* [Boundary Model](../../datamodel/boundary-model.md) §1, §2 - the attributes a boundary carries and the three levels
* [Boundary Model](../../datamodel/boundary-model.md) §3, §3.1 - design targets, and what promotion changes
* [Boundary Model](../../datamodel/boundary-model.md) §4 - the four boundary kinds
* [Claim Model](../../serialization/claim-model.md) §6 - naming an address asserts it exists
* [Data Model](../../datamodel/DATA-MODEL.md) §5.2 - why `M0` is a checkpoint rather than an entry requirement

## Purpose

Is every boundary the design has named actually identified? This is the floor of the model — a design target
with an identity and nothing else is a legitimate state, and this check is what says when even that much is
missing.

## Registration

| | |
|---|---|
| Stage | maturity — `M0` |
| Model check | yes |
| Requires | [claim-competition](claim-competition.md) — a contested attribute has no value to check |

## What It Inspects

For every boundary in the design's scope:

* `name`;
* `purpose` — what this boundary is responsible for;
* `kind` — one of `interface`, `business-domain`, `shared-logic`, `dependency`, required when the boundary is
  contained and unset when it is not.

And one fact about the design as a whole: **the root of a design is a `SpecifiableBoundary`**. You never begin a
design from a bare `FunctionalBoundary`, because being designed is what makes something a design target.

## Algorithm

**What it iterates.** Every **`bnd/` address any claim in scope names** — not only those some claim targets.
Naming an address asserts it exists ([Claim Model](../../serialization/claim-model.md) §6), so a boundary reached
only through a function's address, a type's address, or another boundary's `contains` list is in the model and is
iterated. One consequence to expect rather than treat as a fault: a single function address can raise a finding
for a boundary nobody deliberately created, which is the model reporting an element that exists with nothing else
said about it.

The set is bounded by the parse scope ([Serialization](../../serialization/SERIALIZATION.md) §3) — the design
directory and its subdirectories, excluding any that is itself a design directory.

**What it requires of each.** Partitioned by what the design has authority to say:

1. **The root boundary** — the one `bnd/` address no other boundary's `contains` names, and which every other
   address nests beneath. It requires `name`, `purpose`, and `level` claimed as `specifiable` or `deployable`.
2. **A contained design target** — a contained boundary whose `level` is claimed `specifiable` or `deployable`.
   It requires `kind` only. `name` and `purpose` belong to that target's own design and are required by its own
   run of this check; requiring them here would have one design speak for another
   ([Boundary Model](../../datamodel/boundary-model.md) §2.2, §3.2).
3. **Every other contained boundary** — requires `name`, `purpose` and `kind`.

**What makes an instance a finding.** Any position in that boundary's own requirement set being unclaimed. One
finding per boundary, naming every position this check requires of it and does not find.

**The root is the one case where a claimed value is wrong rather than absent.** A root whose `level` is claimed
`functional` is a modelling mistake, not a missing attribute, and its detail says so rather than reporting an
absence.

**What it deliberately does not inspect.**

| Not inspected | Whose |
|---|---|
| whether a position is contested | [claim-competition](claim-competition.md), which it requires |
| operations | [operation-identity](operation-identity.md) |
| every other element named so far | [element-identity](element-identity.md) |
| `kind` claimed on an **uncontained** boundary, where the model says it is unset | nothing yet — see Notes |
| whether `level` is `specifiable` or `deployable` specifically | the `M5` checks, which are registered only for a `DeployableBoundary` |

## Positions

| Position | Type | Model reference |
|---|---|---|
| `name` | `Name` | [Boundary Model](../../datamodel/boundary-model.md) §1 |
| `purpose` | `Prose` | [Boundary Model](../../datamodel/boundary-model.md) §1 |
| `kind` | `BoundaryKind` — `interface` \| `business-domain` \| `shared-logic` \| `dependency` | [Boundary Model](../../datamodel/boundary-model.md) §1, §4 |
| `level` | `BoundaryLevel` — `functional` \| `specifiable` \| `deployable` | **new** — this check defines it (below) |
| `contains` | `FunctionalBoundary[]` — read to find the root and to classify a boundary as contained | [Boundary Model](../../datamodel/boundary-model.md) §1 |

**`slug` is not a position.** An address is derived from composite containment
([Data Model](../../datamodel/DATA-MODEL.md) §5.1), so a boundary's slug *is* its last address segment: it can
never be found unclaimed, and "unique among its parent's contained boundaries" cannot be violated — two
boundaries with one slug under one parent have one address and are one boundary. The uniqueness clause is a
leftover from the flat `NNN` registry P2 replaced.

**`level` is new, and this check is what brings it into the schema.** The model states the three levels as
*classes* ([Boundary Model](../../datamodel/boundary-model.md) §2) and gives them no attribute, so nothing in a
claim could previously say which one a boundary is — while this check has to assert that a design's root is a
design target. The check therefore chooses the spelling: `level`, valued `functional`, `specifiable` or
`deployable`. `boundary-model.md` §1 is owed a link back to this check
([Evolving A Check](evolving-checks.md) §3.2).

**An unclaimed `level` on a contained boundary means `functional`.** That is inference from absence, which this
model normally refuses — but the alternative is claiming `level: functional` on every shared-logic grouping in
every design to state the overwhelmingly common case, and promotion is the event that makes the level worth
stating. The root is the exception: there, `level` is required, because that is the assertion this check exists
to make.

## Projection

**None.** The algorithm enumerates addresses and tests whether positions are claimed, which `model.list` and
`model.get` answer directly ([Evolving A Check](evolving-checks.md) §2.2). Finding the root is a walk over
`contains` values, not a shape the model has to be taught.

## Findings

| Kind | Raised when | Subject | Detail | Disambiguator | Blocking | Resolution routes |
|---|---|---|---|---|---|---|
| `unstated-required-attributes` | any position this check requires of a boundary is unclaimed | the boundary's address | every required position not found, named | none | `at-registration` — `M0` | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |
| `unstated-required-attributes` | the root's `level` is claimed `functional` | the root's address | that the root of a design must be a design target, and that `level` says otherwise — **not** an absence | none | `at-registration` — `M0` | [correct-the-design](../resolutions/correct-the-design.md) |

**One finding per boundary**, naming every required position it is missing, rather than one per position. The
positions of one boundary are one sitting ([Workflow](../WORKFLOW.md) §2.3).

**No disambiguator.** Subject, kind and the unmet position list already distinguish every finding this check
raises from every other: two findings of this kind at one address would have to name the same missing positions,
which makes them one finding. Nothing this check reports is a computed judgement over positions that are all
present, which is the case a disambiguator exists for ([Evolving A Check](evolving-checks.md) §2.4).

## Settings

None.

## Resolutions

| Route | State |
|---|---|
| [state-the-fact](../resolutions/state-the-fact.md) | **This check builds it.** First check in registration order to offer the route, so it owns the prose, the tool and the elicitation ([Evolving A Check](evolving-checks.md) §3.5). Evolved alongside this document. |
| [take-a-decision](../resolutions/take-a-decision.md) | Not built here. Reachable from this check's findings and left to the first check that cannot proceed without it — see Notes. |
| [correct-the-design](../resolutions/correct-the-design.md) | Not built here. Only the root-`level` finding routes to it, and that finding is rare enough that building the broadest resolution in the set for it would be the wrong first consumer. |

## Worked Example

**Not yet a recorded run.** §3.6 asks for an example against real design content, and there is none: the
pre-parse stage is unbuilt, so no design directory is parseable yet and this check has nothing to run against.
What follows is therefore the **acceptance test to be run when the check is built**, not a result.

Given a design directory whose claims name `bnd/design-assistant` as root with `name` and `purpose` claimed but
no `level`, and name `bnd/design-assistant/bnd/parser/fn/fold-claims` and nothing else about `parser`:

Expected findings, two, both `unstated-required-attributes` blocking `M0`:

| Subject | Detail |
|---|---|
| `bnd/design-assistant` | `level` |
| `bnd/design-assistant/bnd/parser` | `name`, `purpose`, `kind` |

The second is the conjured-boundary case: `parser` exists only because a function address names it.

Then: `state-the-fact` on the root's `level`, and the check re-run reports only the `parser` finding.
`state-the-fact` three times on `parser`, or once naming all three, and the check re-runs clean.

## Notes For P6

**The interesting resolution is rarely typing a name.** A boundary with no `purpose` usually means the boundary
was named in passing by a decision about something else, and settling what it is responsible for is real design
work — which is why [take-a-decision](../resolutions/take-a-decision.md) is a route and not merely
[state-the-fact](../resolutions/state-the-fact.md). The elicitation has to offer that exit rather than pressing
for a sentence.

**The conjured boundary is a feature, and will look like a bug.** A design that mentions
`bnd/x/bnd/y/fn/z` once has committed to `y` existing, and this check says so. The right response is often to
correct the address rather than to describe `y` — which is `correct-the-design`, reached through the finding
rather than offered by it.

**A `kind` claimed on an uncontained boundary is not reported, and nothing else reports it either.** The model
says `kind` is unset on an uncontained boundary ([Boundary Model](../../datamodel/boundary-model.md) §1), so a
claimed one is an attribute stated where it has no referent. That is a different shape from an absence, no
existing finding kind covers it, and inventing one here would be specifying a check before there is a second
instance to shape it. Recorded as a check the default configuration may owe.

**`level` being new is the first real instance of a check extending the schema**, and it is worth noticing how
cheap it was: no model document changed, and the position exists because a check requires it
([Data Model](../../datamodel/DATA-MODEL.md) §1). What `boundary-model.md` §1 owes is a link back, not an
amendment.
