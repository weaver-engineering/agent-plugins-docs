# documents-assessed

## Context
* [Workflow](../WORKFLOW.md) §4.1 - where this check is registered
* [Assessment And Trust](../../serialization/assessment-and-trust.md) - the three trust states and what makes a document assessed
* [Data Model](../../datamodel/DATA-MODEL.md) §1.1 - applying the model to a design it did not author

## Purpose

Has every prose document in scope been judged, and does that judgement still hold? This is the check that makes
the parse trustworthy: it establishes that the model the parse is about to build is the model the design's
documents actually describe, rather than the model of whichever documents somebody got round to.

It is also the whole of the "bring an existing design under the model" story. There is no import, no adoption
and no conversion — a design that arrived from anywhere is a directory full of documents nobody has judged
yet, and this check reports exactly that.

## Registration

| | |
|---|---|
| Stage | pre-parse |
| Model check | no — it verifies attestations, which is a property of files |
| Requires | [documents-parseable](documents-parseable.md) — a malformed document cannot be assessed |

## What It Inspects

For every `*.md` in scope, whether its `_reconciliation` is present and verifies against the document's current
content — both the frontmatter digest and the prose digest.

* **Attested** — the service saw this document in exactly this state. Prose that no claim anchors was looked at
  and contributes nothing.
* **Unverified** — frontmatter present, attestation absent or failing. Every claim is a proposal, and the
  document needs re-judging.
* **Unassessed** — no frontmatter. Nobody has looked.

The last two are the same finding, because they are the same work. A `*.yaml` file is never assessed: it either
carries claims, and is a frontmatter-only document whose claims are grounded in provenance, or it is data with
a schema of its own and nothing to record.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unparsed-document` | a prose document in scope carries no verifying attestation | [re-judge](../resolutions/re-judge.md) |

Blocks `M0` — the model cannot assert anything about a boundary while part of what defines it has not been
looked at.

## Settings

None.

## Notes For P6

A failing attestation reassesses the **whole document**, not merely the claims whose anchors moved: an edit may
have added content, and added content has no anchor to go stale.

The ordinary outcome of re-judging is that the recorded claims were right. That is worth saying in the
resolution prose, because a finding that usually resolves to "nothing changed" reads as noise unless its
purpose is clear — what it establishes is not that something is wrong but that somebody has looked.
