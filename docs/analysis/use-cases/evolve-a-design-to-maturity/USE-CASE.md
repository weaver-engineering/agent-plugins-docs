# evolve-a-design-to-maturity — Evolve A Design To Maturity

**Actor:** [The Architect](../../user-personas/architect.md) — primary. The design is theirs, and every choice
about how it evolves stays theirs. [The Agent](../../user-personas/agent.md) is a supporting actor: it assesses,
it presents, and it does the work the Architect chooses, in that order.
**Scope:** Covers evolving a design — assessing its maturity, choosing what to do next, and doing it. What any
particular check asserts, and what any particular resolution does, is the content of a configuration rather than
of this use case (§7). Implementing the design the loop produces is downstream of it.

## Context
* [Agent Plugins index](../../../agent-plugins.md) - root index for this repo
* [The Architect](../../user-personas/architect.md) - primary actor
* [The Agent](../../user-personas/agent.md) - supporting actor
* [find-and-read-documentation](../find-and-read-documentation/USE-CASE.md) - how the Agent reaches the design
  documentation it uses as context at step 3
* [Data Model §1.2.1](../../../design/design-assistant/datamodel/DATA-MODEL.md) - the document evolution loop
  this use case is the actor-level statement of
* [Design A Specifiable Boundary](../../../design/design-assistant/workflow/WORKFLOW.md) - the default check
  configuration, and the runner whose behaviour steps 2 and 4 describe from outside; its §2.3.1 is step 2's
  report stated from the design's own side
* [Glossary](../../../glossary.md) - Finding, Resolution, Check Set, Maturity Level, Next Unit Of Work

## 1 Goal

The Architect brings a design to the maturity they actually need, in iterations small enough to stay in control
of — each one telling them what is wrong with the design now, and what could be done about it, so that they
decide how it evolves and the Agent does the work of evolving it.

Two things make this worth a use case. A design that *looks* finished is not the same as one that *is*: without a
mechanical assessment, "this design is complete enough to build from" is an opinion, formed by re-reading the
same documents that formed it, and it is wrong in ways that only surface once an agent tries to implement it.
And the work of fixing what an assessment finds is mostly not architectural judgement — it is writing things
down, in the right place, in the right shape, consistently, over and over, which is precisely what the Architect
has least time for and an agent is best at.

What the Architect must not lose in the trade is authorship. The design is theirs. An assistant that decided
which of the design's shortcomings mattered, and how to address them, would be designing — and the Architect
would be reviewing a design rather than making one.

## 2 Trigger

The Architect has a design directory and wants to know what to do next with it. It may hold a single sentence, a
set of documents written long before any of this existed, or a design already near completion; these are the
same trigger, differing only in what the assessment finds.

## 3 Preconditions

* A design directory exists.

That is the whole of it. Whether it declares what it is checked against, whether its documents have ever been
assessed, whether it contains anything at all — each of those is something the assessment reports, not something
the Architect has to arrange before asking. There is no entry ceremony, and requiring one would exclude exactly
the designs that most need bringing under assessment.

* The Architect is present for the iteration. Step 3 is a decision only they can take, and step 4 elicits from
  them what the design does not already say.

## 4 Main Success Scenario

1. The Architect asks for the next unit of work in the design directory.
2. The service assesses the design and reports:
   * the design's maturity, and the addresses bounding it — what is holding it where it is;
   * which checks have passed, by level;
   * findings already **acknowledged**, grouped by the level they were raised at, with their own group for
     global checks, which belong to no level;
   * findings that are **blocked**, as a group of their own — a change request leaves its level unreachable,
     where an acknowledgement does not, so the two must not read as one kind of "already handled";
   * the findings of the first check that produced any, each with the resolutions available to it;
   * every check not yet evaluated up to the next level, and whether it could run now;
   * the levels not yet evaluated at all.
3. The Architect, assisted by the Agent and with the design's own documentation as context
   ([find-and-read-documentation](../find-and-read-documentation/USE-CASE.md)), decides which finding to pursue
   and which of its resolutions to apply.
4. The Agent applies that resolution, using the skills and tools the resolution itself names, eliciting from the
   Architect whatever the resolution needs and the design does not already say.
5. The Agent writes the result into the design documentation, where the next assessment reads it as an ordinary
   claim rather than as a record of having been told.
6. The Architect asks again, from step 1. The design has changed, so the assessment is recomputed against what
   it now says.

## 5 Postconditions

* The design documentation states what the Architect decided, in the place the next assessment will read it
  from.
* The design's maturity can be read off rather than asserted — and where it has not advanced, what is holding it
  is named.
* Every choice about how the design evolved was the Architect's; the Agent's contribution is assessment,
  presentation, and execution.

## 6 Extensions

* **2a.** The design has reached the maturity the Architect wanted → they stop. Maturity is what the Architect
  needs it to be for this design, not a ladder that must be climbed to the top. A design that will never be
  deployed has no reason to reach a level that asserts it is deployable.
* **2b.** The Architect would rather see what a different check reports than work on the one presented → they
  run any check the report lists as able to run now. The report exists to be steered from; the first check with
  findings is where the service would start, not an instruction.
* **3a.** The finding set presented is large → it is still one unit of work. Resolve one, re-run the check,
  resolve what it now reports — resolving one finding frequently removes others, so working the set as a list
  would mean repeatedly offering work already done.
* **3b.** None of the offered resolutions fits → that is itself a finding about the configuration, not a dead
  end: the resolutions a check offers are part of what a project configures, and a check whose routes do not fit
  its own findings is one to change.
* **4a.** The resolution requires a change to a different design target → a change request is raised, carrying
  its ticket. The finding is then reported as blocked on every subsequent assessment rather than as work, and
  its level stays unreachable until the request is answered.
* **4b.** The finding is a real pattern but this instance is genuinely correct → it is acknowledged: who, when,
  and why. An acknowledgement blocks nothing, and stops applying by itself if the condition that raised the
  finding changes.
* **5a.** Applying a resolution drops the design to a level below where it was → ordinary, and not a regression.
  Work done at a higher level routinely reveals what a lower-level check must now assess; the design falls back
  and climbs.

## 7 Open Design Questions (not resolved by this use case)

* **Which checks, and which levels.** This use case requires that a design is assessed against a declared
  configuration; it requires nothing about what that configuration contains. The default one is an opinion held
  by this product, not a term of this requirement.
* **Unattended evolution.** Every step here assumes the Architect is present. Whether any part of the loop can
  run without them — and which resolutions could ever be safe to apply unattended — is not settled here.
* **How the report is presented.** It is a lot of information, and the shape that makes it usable at a CLI is
  not obviously the shape that makes it usable anywhere else. This use case fixes what must be in it and not how
  it is rendered.
* **What happens to a standing acknowledgement whose check could not run.** Stated in the design as kept rather
  than spent; whether the Architect needs to see that distinction, or is better served by not being shown it,
  is an analysis question this use case does not answer.
* **Technical Interpretation.** Not yet written, here or for the other three use cases — see
  [find-and-read-documentation §7](../find-and-read-documentation/USE-CASE.md).

# Rationale

**Why the report presents findings *and* their resolutions, rather than the next action.** This is the load-
bearing requirement of the whole use case, and it is a requirement about ownership rather than about
information. A service that answered "do this next" would be making, one small decision at a time, exactly the
judgements that constitute designing — which shortcoming matters, and which of several legitimate ways to
address it is right here. The Architect would then be reviewing a design rather than authoring one, and review
is a much weaker form of control: it catches what is wrong, not what is absent, and it degrades as the volume
of things to review grows. Presenting the finding with its available resolutions keeps the mechanical half
(what is wrong, and what the routes are) with the service and the judgement half (which of these matters, and
which route) with the Architect.

**Why acknowledged and blocked findings are reported, and reported apart.** Both are findings that are not
work, and a report omitting them would look cleaner while hiding the two facts most likely to matter: what this
design has decided to live with, and what it cannot proceed past. They are separated because they differ in
consequence, not merely in reason. An acknowledgement says the level is achievable anyway; a change request says
it is not, and no amount of work inside this design will change that. Grouping them together would make a
blocked design look like a design with some accepted exceptions.

**Why the Architect stopping is an extension rather than a failure.** "Maturity" invites reading as a ladder to
be climbed to the top, and the level a design needs is a property of what it is for. Writing the stop as an
ordinary branch of the scenario is what keeps the loop a tool the Architect uses rather than a process that uses
them.
