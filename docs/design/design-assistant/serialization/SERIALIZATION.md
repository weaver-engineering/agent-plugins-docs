# Serialization

## Context
* [Data Model](../datamodel/DATA-MODEL.md) - the facts this serialization records, stated independently of any file
* [Claim Model](claim-model.md) - the unit: a fragment of an entity, grounded in prose or in a derivation
* [Anchoring](anchoring.md) - how a claim addresses the prose that authors it
* [Assessment And Trust](assessment-and-trust.md) - what makes frontmatter trustworthy, and what counts as assessed
* [Parse Contract](parse-contract.md) - reading a design directory into model state
* [Write Contract](write-contract.md) - what any writer of these documents must guarantee
* [Glossary](../../../glossary.md) - one-line definitions of every term introduced here
* @docs/standards/documentation-standards.md - the document shape and section addressing this builds on

## 1 What Serialization Is

The [Data Model](../datamodel/DATA-MODEL.md) records facts about a boundary and is deliberately independent of
where any of them land in a file. This is the other half: how those facts are written down, read back, and kept
honest against the prose an architect actually reads and reviews.

One sentence states the whole design:

> A document's frontmatter is the model's record of **what that document's prose contributes to the design**.

Everything else follows from taking that literally.

## 2 No Document Is An Entity

A document is prose. Its frontmatter is not a description *of* the document and not a schema *for* it — it is a
set of claims about what the prose in it contributes to entities of the model.

Nothing about a document's name, path, or kind constrains what it may contribute. One document may contribute
to twenty entities across three boundaries; twenty documents may each contribute a slice of one entity. There
is no document type per entity type, and no entity has a home file.

The model's state is therefore not read *from* a document. It is the **fold of every claim in scope**
([Parse Contract](parse-contract.md) §2). Two consequences run through the rest of these documents:

* the fold must be **order-independent**, because nothing determines the order documents are read in — which
  is why competing claims are findings rather than a last-writer-wins merge ([Parse Contract](parse-contract.md)
  §3);
* *which* document a fact lives in is a question for the workflow that writes it, never for this contract. A
  derived artefact with no prose to anchor to needs somewhere to live, and choosing that somewhere is not a
  serialization concern.

## 3 Scope

Serialization operates over a **design directory**: a directory, and its subdirectories, excluding any
subdirectory that is itself a design directory.

A design directory is marked by a **`DESIGN.yaml`** at its root, which declares the namespace
([Data Model](../datamodel/DATA-MODEL.md) §5.1.1) the design's addresses are rooted in. It may carry further
attributes its product requires; those are outside this contract.

Discovery is a directory walk and nothing more:

* a directory is a design directory **exactly when it contains a `DESIGN.yaml`**;
* scope is that directory and its subdirectories, and the walk **stops descending** at any directory that
  contains one of its own — which is a design directory in its own right, and out of this one's scope.

The marker has to be discoverable this way because scope must be decidable **before** parsing: parsing is
defined over a scope, so a scope inferred from parsed content would be circular. `DESIGN.yaml` makes no claims
and is not a source of design content — the parse contract treats it as a support file (§4). It is read to
establish where and what the design is, which is a question that has to be answered before there is anything to
parse.

The name follows the UPPERCASE manifest convention that @docs/standards/documentation-standards.md §2.1 already
uses for a concept accumulating satellite artifacts — `PRODUCT.md`, `SERVICE.md`, `FEATURE.md` — and a design
directory is exactly such a concept. It is `.yaml` rather than `.md` because it carries no prose: it is not a
document *about* the design, it is the declaration that a design is here.

Within a design directory, the files in scope are `*.md` and `*.yaml`. Every other file is out of scope and is
never parsed for design content.

Out of scope does not mean invisible. A fixture, an image, or a sample payload participates in the design by
being **pointed at**: a claim references it, and whatever the design needs to know about it is stated in the
frontmatter of the document making that reference ([Claim Model](claim-model.md) §5). A binary file is never
itself a source of claims, so it never raises `unparsed-document`.

## 4 File Classes

Three classes, and the parse contract tolerates all three
([Parse Contract](parse-contract.md) §1):

| Class | Shape | Grounding |
|---|---|---|
| Prose document | `*.md`: frontmatter, then prose | claims anchored in its own prose |
| Frontmatter-only document | `*.yaml` carrying claims | claims grounded in provenance, not prose |
| Support file | `*.yaml` carrying none, and every other file | none — not an error, not a contribution |

A frontmatter-only document is **not a special state category**. It is where claims that have no prose to
anchor to naturally accumulate — a derived artefact is traced, not written, so nobody authored prose for it to
point at ([Claim Model](claim-model.md) §2). The distinction is grounding, not file format.

Being YAML does not make a file frontmatter; carrying claims does. A `*.yaml` file that carries none is
**data** — a fixture, a dataset, a configuration — and is a support file on the strength of its shape alone.
Nothing is added to it and nothing is recorded about it: it has its own schema, `_claims` is not in it, and
writing one in would corrupt the file to answer a question that is not being asked of it.

Support files therefore need no assessment, which puts a `*.yaml` data file in exactly the position a binary
fixture is already in (§3): the design **points at** it, and whatever the design needs to know about it is
stated by the claim doing the pointing. Only a prose document can hold design content that nobody has looked
at, so only a prose document is ever assessed
([Assessment And Trust](assessment-and-trust.md) §4).

## 5 The Documents Are The Database

There is **no service store**. Every fact in the model is either written in some document's frontmatter or
computed from what is ([Parse Contract](parse-contract.md) §7). Nothing is held anywhere else, and nothing has
to be kept in step with anything else.

Losing frontmatter is therefore not free, but it does not damage the design:

| Lost | Cost |
|---|---|
| an authored claim | the prose still says it; the contribution needs re-judging |
| a derived claim | it is re-derived from the design, which recreates its provenance |
| a review | whatever was reviewed needs reviewing again |
| an acknowledgement | whatever was acknowledged needs acknowledging again |

In every case the recovery is a unit of work, not a reconstruction of something unrecoverable. That is what
licenses the whole scheme: frontmatter is a durable cache over prose and derivation, and the prose is the
thing that must not be lost.

## 6 Reading Order

[Claim Model](claim-model.md) → [Anchoring](anchoring.md) →
[Assessment And Trust](assessment-and-trust.md) → [Parse Contract](parse-contract.md) →
[Write Contract](write-contract.md).

# Rationale

**Why frontmatter records contribution rather than describing its document.** The obvious design gives each
entity type a document type and a matching frontmatter schema: an operation document carries operation
frontmatter. It fails on contact with real documents, which explain several things at once and are organised
for a reader rather than for a model. Recording contribution instead means a document may be structured however
serves the architect, and the model still gets exact facts out of it — and it removes file layout from the
model's vocabulary entirely, which is what [Data Model](../datamodel/DATA-MODEL.md) §1 already asserts.

**Why the design directory is marked by a file rather than inferred.** Every alternative is circular or fragile.
Inferring it from a claim inside a document requires parsing to discover what is parseable. Inferring it from
path convention breaks the moment a design is extracted or republished. A marker is decidable by directory walk,
and it has a real job besides delimiting scope: it declares the namespace, which is the one fact that cannot be
a claim, because claims are addressed within the namespace it defines.

**Why `DESIGN.yaml` is a support file rather than a document making claims.** It would be natural to let the
marker claim the root boundary it introduces, and it cannot: the namespace it declares is what every claim's
address is resolved against, so a claim inside it would have to be addressed within a namespace the same file
is still in the process of establishing. Keeping it outside the claim mechanism entirely is what stops that
from being a special case in the parser — it is read as configuration, before parsing begins, and the parse
contract then meets an ordinary `*.yaml` file that happens to make no claims.

**Why only prose documents are assessed.** An earlier form gave every file in scope an assessment record, so
that one contributing nothing could be marked as looked-at rather than merely unread. That cannot work for
YAML: a data file has a schema of its own, `_claims` is not in it, and writing a marker in would corrupt the
file in order to answer a question nobody is asking of it. The asymmetry that resolves it is real rather than a
concession — prose is the only thing that can *contain* design content nobody has judged. A YAML file either
carries claims, in which case it is a frontmatter-only document, or it is data, in which case its meaning to the
design is whatever the design says about it in the claim that points at it. Neither leaves anything for an
assessment record to record.

**Why scope is `*.md` and `*.yaml` only.** The alternative — parsing anything that might contribute — makes
every binary in the tree a potential unassessed document, and there is nothing to assess: a fixture's meaning to
the design is whatever the design says about it, which is stated in the frontmatter of the document that
references it. Restricting the extensions puts that judgement where it belongs and keeps `unparsed-document`
answerable.

**Why there is no service store.** A store alongside the documents would immediately need reconciling with them
— on checkout, on rebase, on a hand edit, on a second working copy — and the failure mode is silent divergence
between what the service believes and what the repository says. Making the documents the whole system of record
removes that class of problem entirely. The price is that a lost review must be redone, which is a bounded cost
paid rarely, against an unbounded cost paid continuously.
