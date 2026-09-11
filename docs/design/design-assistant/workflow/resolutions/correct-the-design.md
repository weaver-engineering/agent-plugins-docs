# correct-the-design

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Write Contract](../../serialization/write-contract.md) §3, §5 - the edits a writer must support, and claim disposition

## Purpose

Change the design so the condition no longer holds. The broadest of the standard resolutions, and the default
wherever a finding says something is genuinely wrong rather than merely absent.

## Applies To

`conflicting-claim`, `duplicate-claim`, `malformed-document`, `unresolved-type`, `signature-nonconformance`,
`invalid-realization`, `orphan-function`, `shim-inconsistency`, `build-manifest-conflict`,
`non-partitioning-dimension`, `unexplained-exclusion`, `unresolved-selector`, `unauthorized-change`,
`mock-inconsistency`, `undeclared-exception`, `duplicate-metric-emitter`, `satisfaction-failure`,
`unexpected-side-effect`, `redesign-required` (the reject route), `invalid-sli-definition`, `unbacked-sli`,
`missing-sli`.

## What It Does

1. Establishes **what** is wrong — which of the finding's two or three possible causes this instance is.
2. Makes the edit, as prose and claims written together in one transaction.
3. States the disposition of any claim whose anchor the edit disturbs (§5 of the write contract): on a deleted,
   split or merged section, which claims survive and where they anchor.

## Mechanical

No. Which of a finding's causes applies is the judgement, and it is what decides whether the edit invalidates
anything downstream.

## What Must Be True Afterwards

* the condition that raised the finding no longer holds;
* every claim the edit touched is re-anchored and re-signed, and the disposition of any orphaned claim was
  **stated rather than guessed**;
* anything derived from what changed is stale, and reported as such by
  [provenance-freshness](../checks/provenance-freshness.md) on the next run.

## Notes For P6

**Claim disposition is never inferred.** Every plausible default is wrong often enough to be dangerous: keeping
claims on the first half of a split, dropping claims on a deleted section, preferring the earlier document on a
merge. Each produces a well-formed, attested document making a claim nobody checked — indistinguishable from a
correct one, and exactly the failure the attestation cannot catch, because the writer really did write it.

**The edit must be narrow.** A writer that can only replace whole documents forces the author to reproduce
content it did not intend to change, which is both the largest source of accidental edits and the reason an
agent would end up handling frontmatter it should never see.

Where the correction turns out to belong to another design target, this is the wrong resolution and
[raise-a-change-request](raise-a-change-request.md) is the right one. The tell is authority, not difficulty.
