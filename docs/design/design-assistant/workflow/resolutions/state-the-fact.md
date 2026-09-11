# state-the-fact

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Decision Model](../../datamodel/decision-model.md) §5 - every authored fact records how it entered the model
* [Write Contract](../../serialization/write-contract.md) - what a writer guarantees when a claim is written

## Purpose

Supply what is absent. This is the most common resolution in the workflow and the least interesting one to
describe, because what varies is entirely what the finding asked for — an attribute, a behavior, a fixture, a
predicate, an endpoint, the substance of an exemption.

## Applies To

`unstated-required-attributes`, `uncovered-cell`, `unexplained-exclusion`, `unassessed-manifest-setting`,
`unassessed-nfr-rule`, `unassessed-perimeter-vector`, `unresolved-type`, `unresolved-nfr-scope`,
`missing-fixture`, `no-suitable-fixtures`, `unpredicated-effect`, `unexpected-side-effect`, `missing-sli`,
`unbacked-sli`.

## What It Does

1. Establishes what the absent fact actually is — which is elicitation, not transcription, wherever the answer
   is not already written in the design's prose.
2. Writes the prose that says it, in the document where it belongs.
3. Has the service write and sign the claim indexing that prose.

## Mechanical

No. The service writes the claim; deciding what the claim should say is the architect's.

## What Must Be True Afterwards

* the fact is stated in prose a person can read, not only in frontmatter;
* the claim carries `_sourcing` — how the fact entered the model and who may change it;
* re-running the check that raised the finding produces nothing for that subject.

## Notes For P6

**An architect may write a claim straight into the frontmatter**, and that is a supported route rather than a
workaround: it is read as a proposal, re-judged against the prose, then written and signed. The resolution
should offer it for the case where the prose already says the thing and only the claim is missing.

What this resolution must never do is invent a fact to clear a finding. A `purpose` written to satisfy a check
is worse than an absent one, because the absence was reportable and the invention is not. Where the answer is
not known, the honest outcome is [take-a-decision](take-a-decision.md) or an open design question — both of
which leave the gap visible.
