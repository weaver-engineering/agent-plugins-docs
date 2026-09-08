# Write Contract

## Context
* [Claim Model](claim-model.md) - the claims a write maintains alongside the prose
* [Anchoring](anchoring.md) - the anchors and digests a writer owns and an author never touches
* [Assessment And Trust](assessment-and-trust.md) - the attestation every write produces
* [Parse Contract](parse-contract.md) - what a reader is entitled to assume because writes behave this way
* [Reconciliation Model](../datamodel/reconciliation-model.md) - §4.3, re-addressing is not a semantic change

## 1 Why There Is A Write Contract

Nothing in this serialization can be maintained by the agent authoring the design. An author who computes their
own digests and produces their own attestation is certifying their own work, which is exactly what the
attestation exists to detect ([Assessment And Trust](assessment-and-trust.md) §3).

So every obligation in these documents that involves an anchor, a digest, or a signature is an obligation on
the **writer**, and the writer is the service. An agent states what it wants a document to say and what that
prose contributes; it never sees a checksum.

This document states what any writer must guarantee. How those guarantees are offered — the shape of the
interface, its transport, its errors — belongs to the service that provides it, not here.

## 2 Prose And Claims Change Together

A write is a single transaction over the prose, the claims, their anchors, their digests, and the document's
attestation. There is no state in which a document's prose has been updated and its frontmatter has not, or
the reverse.

The consequence is worth stating explicitly, because a great deal rests on it: **same-document staleness cannot
occur**. A claim can never be stale with respect to the prose in its own document, because the two are only
ever written together. The only staleness this contract admits is a reference to content elsewhere
([Anchoring](anchoring.md) §5), and the only inconsistency is an edit made outside the writer — which the
attestation catches and which resolves by re-judgement rather than by repair.

## 3 Edits That Must Not Require A Rewrite

A writer must be able to make each of the following as a single act, without the author restating any content
it does not concern, and without the author handling frontmatter at all:

| Edit | Notes |
|---|---|
| Replace a section's prose, its claims, or both | |
| Insert a section | renumbers its siblings and everything below |
| Delete a section | claim disposition required (§5) |
| Split a section | claim disposition required (§5) |
| Merge two sections | claim disposition required (§5) |
| Move a section | pure re-addressing (§4) |
| Change a document's claims without touching prose | |
| Create a document | within scope, and not within a child design directory |
| Delete a document | claim disposition required (§5) |
| Move documents between design directories | §4, promotion and extraction |

The requirement is that each is *one* operation. A writer that can only replace whole documents technically
satisfies every other rule here and fails this one, because it forces the author to reproduce content it did
not intend to change — which is both the largest source of accidental edits and the reason an agent would
otherwise be handling frontmatter it should never see.

Deleting a document is not an error, and needs no special handling beyond §5. The entities its claims fed lose
those attributes, anything derived from them goes stale by the ordinary invalidation rule, and a reference to
the deleted document can no longer be checksummed — which is stale provenance, and a unit of work.

## 4 Re-Addressing

Two kinds of address move, and neither may invalidate anything or clear any review
([Reconciliation Model](../datamodel/reconciliation-model.md) §4.3).

**Section renumbering** is local. Inserting, deleting or moving a section renumbers the sections around it, and
that reaches only the document being written: anchors are document-local ([Anchoring](anchoring.md) §1), and
section numbers are normalized out of digests ([Anchoring](anchoring.md) §3). The document is re-signed and
nothing else changes.

**A model address change** is not local. Renaming or moving an element re-addresses it and every reference to
it ([Data Model](../datamodel/DATA-MODEL.md) §5.1), which reaches every claim in the design directory whose
`_target` — or whose ref-valued attributes — names it. A writer must therefore maintain an index from model
address to the claims mentioning it, and rewrite them all as one act.

That rewrite touches frontmatter only. No prose changes, so no anchor digest moves, so nothing is invalidated
and no review is cleared; the affected documents are re-signed and are otherwise untouched. This is the
property that makes path-derived addressing affordable, and the way to get it wrong is to rewrite prose while
doing it, which silently clears review state across the design. (A writer that *misses* a claim does not leave
a dangling address — the leftover claim goes on asserting the old address exists, and it surfaces as an element
with almost no attributes, [Claim Model](claim-model.md) §6.)

**A change of containment** is the third kind, and the only one that moves documents between design
directories. Which operations change addresses is the model's to say, and it names all three
([Boundary Model](../datamodel/boundary-model.md) §3.1): promotion changes a boundary's type in place and
leaves addresses alone, while extraction and relocation change its position and therefore its address. What
serialization adds is that **design directory membership moves independently of addresses**:

| Operation | Addresses | Design directory |
|---|---|---|
| Promotion in place | unchanged | changes — the artefacts leave for their own (Boundary Model §3.1) |
| Extraction to a Library | re-rooted into a new namespace | changes, and a new one comes into being |
| Relocation under a different parent | change with containment | may change |

Two obligations follow. **The subtree must be separable as a directory**, because scope is directory-based
([Serialization](SERIALIZATION.md) §3): a design target's artefacts can leave a design's scope only by
occupying a directory of their own. Where they already do, the move is made by adding a `DESIGN.yaml` to that
directory — the scope walk stops there, and no document moves at all. Where they are interleaved with the rest
of the design's documents, documents are moved until they are not. This is the one case in which re-addressing
entails moving files, and it is forced by how scope is defined rather than by anything about addresses.

**Both designs are rewritten, not one.** Extraction leaves the containing design naming addresses that have
re-rooted, so its claims need the namespaced form, while the extracted design's own claims are re-rooted into
its new namespace. The obligation covers every design directory the writer can reach, and does not extend past
it: a design in another repository holding a prefixed address into what was extracted is out of reach. That is
a general consequence of changing a published design's addresses rather than anything particular to extraction,
and this contract does not settle it.

The rest composes from rules already stated:

* moving a document does not disturb its claims — anchors are document-local and digests are over span content,
  so a move is the deletion and creation the fold does not notice
  ([Parse Contract](parse-contract.md) §6.1);
* re-rooting the addresses inside claims is the frontmatter-only rewrite above, applied in both designs;
* nothing is invalidated and no review is cleared — which holds *only* because digests normalize model
  addresses out ([Anchoring](anchoring.md) §3). Without that, extracting one boundary would re-judge every
  claim in both designs, which is the clearest demonstration of what the normalization rule is for.

## 5 Claim Disposition Is Never Inferred

Four of the edits in §3 leave claims whose anchors no longer exist, or no longer unambiguously identify what
the claim was about. In each case **the author must state the disposition, and the writer must not guess**:

| Edit | What must be stated |
|---|---|
| Delete a section | for each claim anchored there: dropped, or re-anchored where |
| Split a section | which side each claim's anchors go to |
| Merge two sections | which claims survive, where both sections' claims cover the same position |
| Delete a document | acknowledgement that its whole contribution is withdrawn |

A writer cannot infer these, because the question is what the prose now establishes — a judgement about
meaning, not about text. Guessing would produce a claim that looks attested and rests on prose that no longer
says what it said, which is precisely the state this serialization is built to make impossible.

# Rationale

**Why the write contract is stated here rather than left to the service.** It looks like an implementation
concern and is not: the schema is only safe *because* something maintains it. Requiring digests, anchors and an
attestation is a reasonable design if a writer guarantees them and an unreasonable one if the author is left to
produce them by hand. Stating the guarantees alongside the schema keeps the two from being read separately, and
keeps the schema from being adopted with the obligations dropped.

**Why single-operation editing is a requirement and not an optimisation.** Whole-document rewriting appears
adequate — the result is the same document either way — and it quietly moves the frontmatter into the author's
hands, since an author reproducing a document must reproduce its frontmatter too. Every guarantee in
[Assessment And Trust](assessment-and-trust.md) then rests on an agent faithfully copying content it has no
reason to understand. Making narrow edits expressible is what keeps the author's concern to prose and
contribution.

**Why disposition is demanded rather than defaulted.** Every plausible default is wrong often enough to be
dangerous: keeping claims on the first half of a split, dropping claims on a deleted section, or preferring
the earlier document on a merge. Each produces a well-formed, attested document making a claim nobody checked
— which is indistinguishable from a correct one, and is exactly the failure the attestation cannot catch,
because the writer really did write it.
