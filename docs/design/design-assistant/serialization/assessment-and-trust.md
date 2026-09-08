# Assessment And Trust

## Context
* [Serialization](SERIALIZATION.md) - the file classes this applies to, and why the documents are the database
* [Claim Model](claim-model.md) - the claims `_reconciliation` covers
* [Parse Contract](parse-contract.md) - what a reader does with each trust state
* [Data Model](../datamodel/DATA-MODEL.md) - §1.1, the `unparsed-document` finding this makes decidable

## 1 `_reconciliation`

Every document the service has written carries a root-level `_reconciliation`:

```yaml
_reconciliation:
  written_by: "design-assistant/0.1"
  written_at: "2026-09-08T09:14:22Z"
  frontmatter_digest: "sha256:…"   # canonical frontmatter, excluding _reconciliation
  prose_digest: "sha256:…"         # the document's prose, absent for a frontmatter-only document
  signature: "…"                   # over both digests, by the service
```

It covers two things, and needs both:

* the **frontmatter digest** makes the claims tamper-evident — a hand edit to a claim, its anchors, or its
  digests is detectable;
* the **prose digest** makes the document's *whole* content part of what was signed, which is what licenses
  reading unanchored prose as deliberately unanchored rather than merely unread (§4).

Reconciliation is distributed through the documents rather than gathered into one place. There is no index of
signatures, no manifest of assessed documents, and nothing to keep in step: a document carries its own
attestation, and a document that is moved or copied carries it along.

## 2 Trust States

Three states, decidable from the document alone:

| State | Condition | What a reader does |
|---|---|---|
| Attested | `_reconciliation` present and verifies | trust the claims as model input |
| Unverified | frontmatter present, `_reconciliation` absent or failing | treat every claim as a **proposal** (§3) |
| Unassessed | no frontmatter at all | the document has not been looked at |

Only the first is model input. The other two are units of work, and neither is an error.

These are the states of a **claim-bearing** document — a prose document, or a frontmatter-only one. A support
file has no trust state at all, because it makes no claims for anything to trust
([Serialization](SERIALIZATION.md) §4).

## 3 Hand-Written Frontmatter Is A Proposal

Frontmatter the service did not write is never rejected and never trusted. It is read as a proposal: the
service re-judges each claim against the prose, and on agreeing, writes and signs it. What was proposed becomes
attested, and the service has taken responsibility for it.

This is what lets an architect write a claim directly into a document — the fastest way to state something the
prose already says — without either being blocked by a signing mechanism or smuggling an unchecked fact into
the model. It is also what makes hand editing safe: an edited claim is not silently believed, it is re-examined.

The same applies to an entire document that arrived with frontmatter from somewhere else. There is no import
concept and no separate adoption path ([Data Model](../datamodel/DATA-MODEL.md) §1.1); an unverified document
is one whose claims have not been judged yet, exactly like one that never had any.

## 4 Assessment

A document is **assessed** when its `_reconciliation` verifies against its current content. That single test
resolves what would otherwise be ambiguous.

Absent frontmatter has two incompatible meanings — nobody has looked, or somebody looked and found nothing to
record — and only the first is work ([Data Model](../datamodel/DATA-MODEL.md) §1.1). The prose digest
distinguishes them, because it puts the whole document inside what was signed:

* `_reconciliation` **verifies** — the service saw this document in exactly this state. Prose that no claim
  anchors is prose that was looked at and contributes nothing.
* `_reconciliation` **does not verify, or is absent** — the document may now say something nobody has judged.
  The whole document is reassessed, not merely the claims whose anchors moved: the change may have *added*
  content, and added content has no anchor to go stale.

**Assessment applies to prose documents and to nothing else.** `unparsed-document` is raised for exactly the
`*.md` documents in scope that are not assessed. It is never raised for a `*.yaml` file, a binary, or anything
else out of scope ([Serialization](SERIALIZATION.md) §3): a data file is not a source of claims, so there is no
content in it for anybody to have failed to look at.

### 4.1 A Prose Document That Establishes Nothing

A prose document may be assessed and correctly contribute nothing. It records that with an **empty claim
list**:

```yaml
_reconciliation:
  …
_claims: []
```

`_claims: []` is a positive statement — *this document was assessed and establishes nothing*. It is not what
distinguishes an assessed document from an unassessed one; the attestation already does that, since only the
service can produce one that verifies. It earns its place by being legible to a reader and by keeping the shape
uniform: every prose document carries a claim list, and one that establishes nothing carries an empty one
rather than being recognised by an absence.

**This is available to prose documents only, and the asymmetry is not an oversight.** A markdown document has
frontmatter, which exists to be written in. A YAML file *is* data with a schema of its own — `_claims` is not
in that schema, and writing one in would corrupt the file in order to answer a question nobody is asking of it.
So a `*.yaml` carrying no claims is a support file on its shape alone ([Serialization](SERIALIZATION.md) §4),
with nothing recorded about it and nothing to record.

`DESIGN.yaml` is exactly that case: it is read first to establish the scope ([Serialization](SERIALIZATION.md)
§3), carries the namespace declaration and whatever else its product requires, and is never assessed — which
also removes the bootstrapping question of how the file that defines a design's scope comes to be attested.

## 5 What The Signature Is Worth

The signature detects that frontmatter was written by something other than the service. With a locally-run
service the key is on the same disk as the documents, so this is **tamper-evidence, not tamper-proofing**: it
catches hand edits, merge artefacts, partial reverts, and generated-then-modified frontmatter, which are the
things that actually happen. It does not defend against someone determined to forge an attestation, and
nothing here should be built on the assumption that it does.

That is a worthwhile bargain because of what a false trust costs. An unverified claim is re-judged, which is
cheap and frequent; the mechanism's job is to make sure re-judgement *happens*, not to prove who wrote a file.

# Rationale

**Why one document-level attestation rather than a per-section assessment record.** An earlier form recorded a
digest per section, so that a section contributing nothing could be marked as looked-at. It works, and it
duplicates at section granularity exactly what a prose digest already establishes at document granularity —
while adding an entry per section to every document's frontmatter, which is the verbosity this schema is
otherwise careful to avoid. Signing the prose makes the whole document the unit of assessment, and unanchored
prose needs no record of its own.

**Why a mismatch reassesses the whole document rather than only the stale claims.** Anchor digests detect that
an existing claim's basis moved. They cannot detect content that *arrived*, because new prose is anchored by
nothing and so has no digest to move. A document whose overall content has changed may contain a contribution
nobody has judged, and the only way to find out is to look at the document rather than at its existing claims.

**Why unverified frontmatter is a proposal rather than an error.** Rejecting it would make hand editing
impossible, which would make the architect dependent on tooling for the smallest correction and would guarantee
the tooling is worked around. Trusting it would make the signature meaningless. Re-judging it is the only
option that keeps both hand editing and the trust boundary, and it costs one pass over a document somebody was
already editing.
