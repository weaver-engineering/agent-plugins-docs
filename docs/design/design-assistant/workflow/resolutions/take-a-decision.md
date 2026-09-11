# take-a-decision

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Decision Model](../../datamodel/decision-model.md) §3, §3.1 - the `KeyDecision` and its candidates
* [Decision Model](../../datamodel/decision-model.md) §2 - open design questions

## Purpose

Close a genuine gap with a decision that records what was considered. Every element that exists above `M1`
traces to a decision — a function nobody decided on is either an orphan or evidence that a decision was made and
not recorded.

## Applies To

`unstated-required-attributes` where the absent fact has to be chosen rather than transcribed,
`call-declaration-mismatch` where the call was never decided, `undeclared-exception`, `nfr-conflict`,
`satisfaction-failure`.

## What It Does

1. States the question — the gap being closed.
2. Generates candidates, **genuinely more than one where more than one is plausible**, and assesses each:
   `analysis` (scored worse against the NFRs and the gap's own requirements), `logical-argument` (it cannot
   work), or `poc-finding` (a proof of concept demonstrated otherwise).
3. Chooses one, records the decision with every candidate and what ruled it out, and names the elements the
   decision `produces`.

Where the question cannot be answered yet, the honest outcome is an `OpenDesignQuestion` instead — recorded,
with what it blocks. That is a resolution of the *unit of work*, not of the finding: the finding stands.

## Mechanical

No.

## What Must Be True Afterwards

* the decision holds at least two candidates wherever more than one was plausible, each with its assessment;
* every element the decision produced exists at its address;
* a decision consolidating others records them in `supersedes`, and **the elements they produced are deleted**
  rather than left standing beside their replacement.

## Notes For P6

**Recording only the winner makes a decision where one option was ever considered look identical to one where
five were**, which removes the only thing a later reader can check the reasoning against. A proof of concept
records its finding in the candidate's assessment and needs no permanent artefact of its own.

The register holds the design's **current state, not its history**. A superseded decision is retained and marked
superseded, because "this was considered and replaced" is still true of the present — and it is what stops the
same rejected option being re-proposed.

Choosing an interface means choosing what data it takes and returns, not just its name and signature. Those
types are part of the same decision.
