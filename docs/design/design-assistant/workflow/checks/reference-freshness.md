# reference-freshness

## Context
* [Workflow](../WORKFLOW.md) §4.6 - where this check is registered
* [Claim Model](../../serialization/claim-model.md) §5 - document references, checksummed and never resolved
* [Parse Contract](../../serialization/parse-contract.md) §5 - a mismatch means re-judge, never wrong
* [Data Model](../../datamodel/DATA-MODEL.md) §5.4 - references out, and why they are never parsed

## Purpose

Does every referenced document still checksum to what is recorded? A design depends on documents it does not own
— a use case, a standard, a contract, a `.proto`, a fixture file — and it must detect that one changed without
ever parsing it. That is exactly what a reference is for: enough to invalidate, not enough to interpret.

## Registration

| | |
|---|---|
| Stage | maturity — `M4` |
| Model check | yes |
| Requires | [claim-competition](claim-competition.md) — a contested claim's reference is not yet the design's statement |

## What It Inspects

Every `ExternalRef` the design holds: a `document`-kind `Sourcing`'s basis, a behavior's `realizes`, an
inherited NFR rule's provenance link, a checksummed contract a shim refers to, a fixture's content file. Each
address is re-read and re-checksummed against what is recorded.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `stale-reference` | a referenced document no longer checksums to what is recorded | [re-judge](../resolutions/re-judge.md) |

Blocks `M4`.

## Settings

None.

## Notes For P6

**This is a gap `stale-provenance` does not cover**, and the distinction is worth holding onto. That kind is
defined over *derived* elements, whose sources are inside the design. A `document`-sourced fact is **authored**
— it carries sourcing rather than provenance — and its source is owned elsewhere, so nothing about the design
changing invalidates it and nothing about the design's own attestations detects it.

**A mismatch means re-judge, never wrong.** The recorded value may still be the right reading of the changed
document; what is no longer true is that anybody has confirmed it. Re-judgement is a unit of work whose ordinary
outcome is that nothing changes.

A referenced section renumbered under the design's feet lands here, and is handled correctly rather than
avoided: recomputing at the recorded address yields different content, and the claim is re-judged. Slightly
conservative and correct, because a design cannot mechanically re-address into a document it never parses.

Where the re-judgement finds the referenced document genuinely changed what it required, the change may reach
past this design — which is `raise-a-change-request` against whoever owns it, reached through the re-judgement
rather than offered here.
