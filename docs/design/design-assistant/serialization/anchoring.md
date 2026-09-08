# Anchoring

## Context
* [Claim Model](claim-model.md) - the claims whose `_anchors` this document defines
* [Serialization](SERIALIZATION.md) - the scope anchors operate within
* [Write Contract](write-contract.md) - who maintains anchors and digests, and why never the agent
* [Reconciliation Model](../datamodel/reconciliation-model.md) - §4.3, why re-addressing must not invalidate
* @docs/standards/documentation-standards.md - §4 section ids and §6 section reference syntax

## 1 Anchors Are Document-Local

An anchor always names a section of **the document whose frontmatter carries it**. A claim is a statement about
what this document's prose contributes; it can no more anchor into another document than it can speak for it.

This is not a restriction so much as a consequence, and it buys the property that makes the write contract
simple: restructuring a document can never invalidate, or require rewriting, anything in another document
([Write Contract](write-contract.md) §4). Dependencies on other documents exist, and they are references, not
anchors (§5).

## 2 Section Addressing

An anchor is a **section id** as defined by @docs/standards/documentation-standards.md §4, written with the §
sigil of that standard's §6: `§2`, `§2.1`, `§2.1.3`. The notation goes to whatever depth the document's own
sections go.

Two properties of that standard are what this contract relies on, and neither is restated here:

* every section has an id, and the id is unique within the document;
* the id is structural, derived from the section's position, so it exists whether or not the visible heading
  displays a number.

The second is what lets an externally-authored document — one that never heard of these standards, with
unnumbered headings — be anchored with no additional machinery and no second addressing scheme.

**An anchor covers the sections nested beneath it.** An anchor at `§2` covers `§2.1` and `§2.2` and everything
below them. A claim anchored at a parent therefore depends on all of its children, and a prose pointer
([Claim Model](claim-model.md) §4) may resolve to any section within an anchor as well as to the anchor
itself.

Anchoring a whole document requires an addressable root. The standard already defines the document itself as a
node with the implicit id `0`; this contract needs that node to be anchorable and, by the containment rule
above, to cover every section in the document. That is a requirement on the indexer, not a second convention
defined here.

## 3 Digests

`_anchors` maps each anchor to a digest of the prose that anchor resolves to.

The digest is computed over **resolved span content, normalized**, never over the literal file text. Two things
are normalized out, for the same reason in both cases — they change without anything meaning to change:

* **model addresses appearing in the prose**, so that re-addressing an element does not invalidate every
  document that mentions it ([Reconciliation Model](../datamodel/reconciliation-model.md) §4.3);
* **section numbers**, so that inserting or moving a section does not invalidate claims anchored below it.

Line numbers are never part of an anchor or a digest. They are a resolution artefact, recomputed on every read,
and trusting them across an edit would make every claim in a document stale whenever anything above it grew by
a line.

## 4 Granularity Is A Document-Structure Choice

Because an anchor covers its nested sections, how finely a document is subdivided determines how precisely
invalidation lands:

* a claim anchored at `§2` is re-judged when anything under `§2` changes;
* split the prose into `§2.1` and `§2.2` and anchor two claims separately, and an edit to one stops
  invalidating the other.

The architect therefore controls re-judgement granularity directly, through document structure, with nothing to
configure. Splitting a section is not only an editing convenience — it is the mechanism for tightening
invalidation ([Write Contract](write-contract.md) §3). Well-structured prose is rewarded with less spurious
re-judgement, which is the incentive this contract wants to create.

## 5 The Three Kinds Of Pointer

A claim points at things in three different ways, and conflating any two of them goes wrong quickly:

| | Anchor | Document reference | Model address |
|---|---|---|---|
| Names | a section of this document | a document, or part of one, elsewhere | an element of the model |
| Resolved to a span | yes | never | n/a |
| Digested | yes, over normalized span content | yes, over the referenced content | never — the model is not a document |
| Rewritten when the target moves | yes, mechanically | never | yes, mechanically ([Write Contract](write-contract.md) §4) |
| Parsed | yes | never ([Data Model](../datamodel/DATA-MODEL.md) §5.4) | n/a |
| Can point at nothing | no | yes — the target may be deleted | no — naming it is what makes it exist ([Claim Model](claim-model.md) §6) |

The distinction that does the most work is *maintained* versus *left alone*. An anchor and a model address both
point inside what this design owns and restructures, so both are rewritten mechanically when their target moves.
A document reference points at something owned elsewhere, so it is recorded, checksummed, and never touched.

A referenced section that is renumbered under the design's feet is a case this handles correctly rather than
one it avoids: recomputing the checksum at the recorded address yields different content, the checksum
mismatches, and the claim is re-judged. Slightly conservative — nothing semantically changed — and correct,
because a design cannot mechanically re-address into a document it never parses. Re-judgement is the honest
price of depending on something you do not own.

## 6 Documents That Do Not Comply

A document in scope may not comply with @docs/standards/documentation-standards.md at all — it may have
arrived from outside this ecosystem, or predate the standard. Anchoring degrades rather than failing:

* headings, however written, yield section ids by position (§2), so anchors work;
* a document with no headings has a single root node, and claims anchor to it;
* the coarser the structure, the coarser the invalidation — every claim on a single-node document is re-judged
  whenever anything in it changes.

Nothing about this is an error state, and no claim is unavailable because a document is untidy. The cost of
non-compliance is paid in re-judgement volume, which is the same currency §4 rewards structure in.

# Rationale

**Why anchors are document-local rather than free.** Allowing a claim to anchor into another document would
require an index from every section to the claims referencing it, maintained across every restructuring, and
would make each write a repository-wide transaction rather than a file-scoped one. It buys nothing: a claim is
a statement about what a document contributes, so a claim anchored elsewhere would be a document speaking for
prose it does not contain. Cross-document dependency is a genuine need and it is served by references, which
require no index because they are never rewritten.

**Why digests normalize addresses and section numbers.** Path-derived addressing makes renames frequent and
mechanical, and section renumbering is a routine consequence of editing. If either were inside the digest, the
tidiest possible action — renaming an element accurately, inserting a missing section — would invalidate claims
and clear review state across the design. Normalizing both is what makes the addressing scheme and the write
contract affordable at the same time.

**Why no separate anchoring scheme exists for non-compliant documents.** The tempting alternative is a fallback
ladder: section ids where available, heading paths otherwise, whole-document as a last resort. It adds a second
addressing vocabulary, and everything that reads an anchor then has to handle both. Since section ids are
positional, they already exist for any document with headings and degrade to a single root node for one
without — the ladder turns out to have one rung.
