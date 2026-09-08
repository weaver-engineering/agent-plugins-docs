# Parse Contract

## Context
* [Serialization](SERIALIZATION.md) - the scope and file classes a parse operates over
* [Claim Model](claim-model.md) - the claims a parse produces
* [Assessment And Trust](assessment-and-trust.md) - the trust state a parse establishes per document
* [Anchoring](anchoring.md) - the digests invalidation is computed from
* [Reconciliation Model](../datamodel/reconciliation-model.md) - the findings and gates this feeds

## 1 Per-File Purity

Parsing one file yields its trust state and its claims, and depends on **nothing but that file**: its bytes and
its own section structure. Not on other documents, not on the order files are visited in, not on what a previous
run concluded.

Every file in scope parses. A support file yields no claims, which is a result and not an error
([Serialization](SERIALIZATION.md) §4) — a parse never fails on a file for being the wrong shape, only on a file
that is malformed as YAML or markdown.

## 2 The Fold

Model state is the **fold of every claim in scope**: claims are grouped by `_target` and merged, and an entity
is whatever its claims jointly say.

The model's **elements** are every address any claim names — as a `_target`, or as the value of a ref-valued
attribute ([Claim Model](claim-model.md) §6). An address named only by references is an element with existence
and no other attributes, which is an incomplete element rather than a broken pointer.

The fold must be **order-independent**, because nothing determines the order documents are read in. Every rule
in §3 exists to keep that true, and none of them resolves competition by preferring one claim over another —
there is no last-writer-wins anywhere in this contract, because there is no defined last writer.

## 3 Merge Rules

Merging is defined over **positions**. A position is an addressable place in an entity where a value may stand:

* a scalar attribute is a position;
* an entry in a collection is a position, identified by that entry type's identity (§4).

There is no third case. Every collection in the model is unordered, and an entry whose order matters carries
that order as an attribute ([Data Model](../datamodel/DATA-MODEL.md) §5.6) — which is itself just a position
like any other, and competes like one.

Two claims **compete** only when they write the same position. Contributing different entries to one collection
is contributing to different positions, so it is not competition and needs no special additive rule — it simply
merges.

| Two claims at one position | Result |
|---|---|
| identical values | advisory `duplicate-claim`; the value stands |
| differing values | blocking `conflicting-claim`; neither value stands |

`conflicting-claim` blocks, because the model cannot say what the entity is. `duplicate-claim` is advisory: the
fold is well-defined, the design is merely stating one fact twice. It still has to be answered — an advisory
finding neither corrected nor acknowledged blocks `M4`
([Reconciliation Model](../datamodel/reconciliation-model.md) §3.1) — and the correction is normally structural:
two documents competing to state one fact is a sign the design's documents are drawn along the wrong lines.
Duplication is waste, and the pressure this creates is toward each fact having exactly one authoring document.
What a good set of lines looks like is layout guidance and belongs with the templates, not here — this contract
constrains no layout and rejects none.

Both kinds are defined in [Reconciliation Model](../datamodel/reconciliation-model.md) §3 and §3.1.

## 4 Identity Is The Data Model's To Declare

What makes two entries of a collection the same entry cannot be invented here — it is a fact about the pair
rather than about either entry, so nothing in a document can encode it. It is settled in
[Data Model](../datamodel/DATA-MODEL.md) §5.6, whose defaults cover almost every case, and without it "the same
position" is undecidable for collections and §3's rules cannot be applied at all.

Ordering places no obligation on this contract, because the model has no ordered collections to serialize:
order is carried as an attribute wherever it matters (§5.6). That is what makes §2's order-independence
unconditional rather than a property that holds while every collection is classified correctly — the case where
parse order could leak into meaning does not exist to be handled.

## 5 Invalidation

**Content hashes are the signal. `mtime` is a pre-filter and never evidence.** A modification time may be
unchanged across a checkout or a rebase that altered content, and may be identical for two writes in the same
second. It is sound for skipping work — an unchanged `mtime` with an unchanged size is a cheap hint — and is
never sufficient to conclude that anything is current.

Three independent checks, each with its own consequence:

| Check | On mismatch |
|---|---|
| `_reconciliation` against the document's current content | the document is reassessed as a whole ([Assessment And Trust](assessment-and-trust.md) §4) |
| an anchor's digest against the prose it resolves to | that claim is re-judged |
| a reference's checksum against the referenced content | that claim is re-judged |

A mismatch means **re-judge**, never *wrong*. The recorded value may well still be the right reading of the
changed prose; what is no longer true is that anybody has confirmed it. Re-judgement is a unit of work, and its
outcome may be that nothing changes.

All three checks are about a file that exists, and none of them detects a file that has stopped existing.
Deletion is a fourth signal with a different mechanism entirely (§6.1).

## 6 Idempotence And Subsets

Parsing a subset of a design directory and folding the result into existing state is **equivalent to parsing
everything**. This is what makes incremental work possible at all, and it holds because:

* a parse is a pure function of one file (§1), so re-parsing a file yields the same claims as parsing it the
  first time;
* the fold is order-independent (§2), so it does not matter which files were parsed when;
* every claim is attributable to the document that carries it, so re-parsing a document **replaces that
  document's contribution entirely** — including removing claims it no longer makes.

That last point is what makes a subset parse sound rather than merely additive. A claim deleted from a document
must disappear from the fold on re-parse, and it does, because the unit replaced is the document's whole
contribution rather than each claim individually.

### 6.1 A Deleted Document Is Not Re-Parsed

The argument above covers new and modified documents and misses the case that breaks it. **A deleted document
is never re-parsed, because there is nothing to parse** — so a subset chosen as "the files that changed" never
visits it, and its claims stand in the fold indefinitely. Subset-equivalence is then false: a full parse would
not include them and an incremental one would.

So the unit a subset parse works over is not the set of changed files but the **difference between the file set
now and the file set the model was built from**, disappearances included.

That needs nothing stored. §6's own attribution requirement already makes the model name every document that
contributed to it, so the previous file set is derivable from the fold: **a document named by a claim in the
model but absent from the directory has been deleted, and its contribution is dropped.** A document that
contributed no claims needs no such check, because it contributed nothing to remove.

Note that `mtime` and content hashes are no help here (§5): both are properties of a file that exists.
Deletion is found only by comparing the directory walk against what the model says should be in it.

A **moved** document is a deletion and a creation, and the fold does not notice. Anchors are document-local and
digests are over span content, so the same claims reappear attributed to a new path; a claim's place in the
fold is its target and position, never the document it arrived in.

This is the same shape as the acknowledgement sweep
([Reconciliation Model](../datamodel/reconciliation-model.md) §3.1) and the `calls`/`calledFrom` reverse check:
a forward pass over what exists cannot see what has stopped existing, and needs a walk from the records back to
their referents.

## 7 Findings Are Computed, Not Stored

Findings are a mechanical extrapolation of model state. They are never serialized, never stale, and never need
reconciling with anything — they are recomputed from the fold on demand and feed the detection of the next unit
of work.

Two things attached to findings *are* durable, because they are human acts rather than derivations: a `Review`
and an `Acknowledgement`. Each is serialized as a claim like anything else, and each must key onto a
recomputed finding by what raised it — its kind, its subject address, and a digest of the condition that
produced it. That key is what makes the specified behaviour fall out rather than needing a rule of its own: if
the condition changes, the recomputed finding no longer matches the recorded acknowledgement, and it is raised
again unanswered ([Reconciliation Model](../datamodel/reconciliation-model.md) §3.1).

Because findings are not stored, an acknowledgement cannot be composed into one the way a review is composed
into its behavior. It is held against the finding's **subject** instead, and therefore survives its own
condition: an acknowledgement matched by no recomputed finding is an orphan, and the model requires it to be
deleted rather than left inert (§3.1). Serialization's part is only that this is an ordinary claim removal —
the writer drops it from the document holding it, under §6's rule that re-parsing replaces a document's whole
contribution. There is no separate mechanism for retiring a spent record, and nothing that needs to remember
that one was retired.

# Rationale

**Why merging is defined over positions rather than as a set of per-shape rules.** Stating it as "scalars
conflict, collections are additive unless uniqueness is violated" is two rules that have to be kept consistent
with each other, and it leaves the identical-entry case to be decided separately for scalars and for collection
entries. Naming the position makes it one rule — same position twice is competition, different positions never
are — and the additive behaviour of collections stops being a rule at all and becomes a consequence. It also
absorbs order without a case of its own: an order-carrying attribute is a position, so two contributions
disagreeing about where something sits is the same competition as any other.

**Why competition is a finding rather than a resolution.** Any resolution rule needs a winner, and every
available tiebreak is a fact about the parse rather than about the design: file order, path order, timestamp.
Choosing one would make the fold order-dependent in substance while appearing deterministic, and would silently
adopt one of two contradictory statements about the design. A finding says the true thing — the design
currently states two incompatible facts — and leaves it to whoever can actually decide.

**Why `mtime` is admitted at all if it cannot be trusted.** Hashing every file in a large design directory on
every read is affordable but not free, and `mtime` is a sound *negative* filter in the common case where
nothing has been touched. The distinction that matters is between skipping work and concluding a fact:
`mtime` may do the first and never the second, which is why it appears here as a pre-filter with the content
hash still the only thing that decides.

**Why re-parsing replaces a document's whole contribution.** The alternative, merging a re-parsed document's
claims into what was already known, cannot express deletion: a claim removed from a document would persist in
the fold with nothing to remove it, and the model would keep asserting something no document says any more.
Replacing wholesale makes the document the unit of truth about its own contribution, which is the same
principle the trust attestation applies at document granularity.

**Why deletion needs no record of the previous file set.** The obvious implementation keeps a manifest of what
was parsed last time and diffs against it — which is state alongside the documents, and would need reconciling
with them on every checkout and every second working copy, the very thing having no service store avoids
([Serialization](SERIALIZATION.md) §5). It is also unnecessary: the model already names every document that
contributed to it, because attribution is what makes replacing a contribution possible at all. Asking which of
those documents still exists costs a directory walk that a parse is doing anyway, and cannot go stale, because
it is derived from the same fold it is checking.
