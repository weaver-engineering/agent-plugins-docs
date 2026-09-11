# re-judge

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Assessment And Trust](../../serialization/assessment-and-trust.md) §3, §4 - proposals, and what makes a document assessed
* [Parse Contract](../../serialization/parse-contract.md) §5 - a mismatch means re-judge, never wrong

## Purpose

Re-read the prose and re-establish what it contributes. **The ordinary outcome is that nothing changes** — the
recorded value may well still be the right reading. What is no longer true is that anybody has confirmed it.

## Applies To

`unparsed-document`, `stale-reference`.

## What It Does

1. Reads the document — the **whole** document where its own attestation failed, not only the claims whose
   anchors moved.
2. Judges what its prose contributes to the design: which entities, which attributes, anchored where.
3. Has the service write the claims and sign the document, which is what makes them model input rather than
   proposals.

For a `stale-reference` the document being re-read is the **referenced** one, which is never parsed into the
model — what is re-judged is the claim that depended on it.

## Mechanical

No. What a document contributes is a judgement about meaning.

## What Must Be True Afterwards

* the document's `_reconciliation` verifies against its current content;
* every claim it makes is grounded — anchored in its own prose with a digest, or carrying provenance;
* a document that genuinely contributes nothing carries `_claims: []`, which is a positive statement rather than
  an absence.

## Notes For P6

**A mismatch reassesses the whole document rather than only the stale claims.** Anchor digests detect that an
existing claim's basis moved; they cannot detect content that *arrived*, because new prose is anchored by
nothing and so has no digest to move.

**Frontmatter the service did not write is never rejected and never trusted.** It is a proposal: re-judged
against the prose and, on agreement, written and signed. That is what lets an architect state something the
prose already says by typing it straight into the frontmatter, without either being blocked by a signing
mechanism or smuggling an unchecked fact into the model.

Where re-judging a `stale-reference` finds the referenced document genuinely changed what it requires, the
consequence may reach past this design — which is [raise-a-change-request](raise-a-change-request.md), or a
return to Analysis, reached through this resolution rather than offered instead of it.
