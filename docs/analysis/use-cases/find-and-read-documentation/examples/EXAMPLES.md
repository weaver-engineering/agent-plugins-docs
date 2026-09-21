# find-and-read-documentation — Examples

Concrete instances of the artefacts [find-and-read-documentation](../USE-CASE.md) deals in, at its minimum,
written down before anything has been analysed.

**They are here to expose variation**, and that is the only job they have. An analysis asserts what must be
true of how a thing changes, and nothing can assert that until it can see how the thing might change: a
corpus can be empty or enormous, a document can have no sections, a file can not be a document at all, an
answer can be cut. Seeing the ways things vary is what makes it possible to say what holds however they do.

**Every one of these could be true.** Each is an instance of some fixture the analysis might end up
asserting — not that fixture, because it asserts nothing, but drawn from the same world. Nothing here is
impossible, and nothing impossible has been written down in order to show that it would be rejected: a
combination that cannot arise has no instance to show, and the analysis rules it out by stating a rule that
is true rather than by exhibiting something that is not.

**The unhappy path is here only where the use case named it.** These cover the happy path and the six of the
use case's eight extensions that survive the minimum (§2.1) — each of those is a route to the goal, so each
is part of what must be true for the Agent to reach it. Everything else that could go wrong is absent on
purpose.

**They are not fixtures and must not become them.** A fixture asserts; an example says *this is roughly how
this varies*. Nothing here may be cited as a requirement, nothing here is locked, and none of it has been
polished past the point where it shows something — an example worked hard enough to be a fixture is an
analysis that was skipped.

## Context
* [find-and-read-documentation](../USE-CASE.md) - the use case whose operations these are examples for
* [1 — Register A Path](../operations/1-register-a-path.md) - the operation §3 covers
* [4 — Search The Registry](../operations/4-search-the-registry.md) - the operation §4 covers; its §5 result
  shapes are what those answers are examples of
* [WeaverDocs Architecture](../../../../architecture/weaverdocs/ARCHITECTURE.md) - §2.2, §2.3 and §2.4, the
  three operations in the minimum
* [Analysing A Use Case](../../../../../notes/analysing-a-use-case.md) - its §1 is what examples are for,
  and the ladder §2 below reports against
* [fixtures/](../fixtures/) - the per-cell fixtures, which assert; these do not

## 1 The Minimum Viable Use Case

The narrowest thing that still reaches the goal: the Agent finds documentation it could not have named, and
reads only the part that bears on its task.

| In | Out |
|---|---|
| registering a directory of markdown documents, recursively | registering a single document, bounded depth |
| searching the registry the Agent is standing in | named registries — no `@{slug}` scopes |
| a ranked answer of documents and sections together | previews of a result's own prose |
| a results list capped at a default | a caller-set cap, or any caller-set bound |
| reporting a reference in full, with its context path | reporting part of a reference by line range |
| the human rendering, and the machine rendering of one answer | — |

What is out is out of the *minimum*, not out of the use case. Each is an extension, and each attaches to a
dimension whose default ordinal is the behaviour shown here. Cutting them is what makes the first pass
finishable; nothing here forecloses adding them.

## 2 What Is Here, And What Is Not

Examples are indexed by **fixture type per operation**, not by narrative. The minimum is one of each — for a
state, one of what it could be before and one of what it could be after — covering the happy path and every
exception the use case names.

| Operation | Fixture type | Examples | |
|---|---|---|---|
| register a path | the call | [`register.txt`](register.txt) header | 1 |
| | the state before | [`registered-before.md`](registered-before.md) | 1 |
| | the state after | [`registered.md`](registered.md) | 1 |
| | the report | [`register.txt`](register.txt) | 1 |
| | a report that registered nothing | [`register-path-absent.txt`](register-path-absent.txt), [`register-path-unreadable.txt`](register-path-unreadable.txt) | 2 |
| | a report that dropped something | [`register-after-deletion.txt`](register-after-deletion.txt) | 1 |
| search the registry | the call | each `search-*.txt` header | 4 |
| | the state it runs against | [`registered.md`](registered.md) — search does not mutate, so before and after are one state | 1 |
| | **answer** | [`search-answer.txt`](search-answer.txt) | 1 |
| | **answer, truncated** | [`search-truncated.txt`](search-truncated.txt), [`search-truncated.json`](search-truncated.json) | 2 |
| | **empty answer** | [`search-empty.txt`](search-empty.txt), [`search-excluded-zone.txt`](search-excluded-zone.txt) | 2 |
| report a reference | the call | each `report-*.txt` header | 4 |
| | the state it runs against | [`registered.md`](registered.md) — likewise unmutated | 1 |
| | the reported content | [`report-section.txt`](report-section.txt), [`report-document.txt`](report-document.txt), [`report-rationale.txt`](report-rationale.txt) | 3 |
| | a reference that does not resolve | [`report-stale-reference.txt`](report-stale-reference.txt) | 1 |

### 2.1 The Named Exceptions

A use case is the happy path, and the exceptions it names are the ones with a way round to the goal. Each of
those needs an example. [USE-CASE.md §6](../USE-CASE.md) names eight; the minimum cuts two of them, and the
other six are covered:

| | | |
|---|---|---|
| **1a** path resolves to a single non-markdown document | **out of the minimum** — the minimum registers a directory, never a single path | — |
| **1b** nothing at the path | in — and only because the goal was widened, see below | [`register-path-absent.txt`](register-path-absent.txt) |
| **1c** path exists, cannot be read | in — likewise | [`register-path-unreadable.txt`](register-path-unreadable.txt) |
| **2a** a source document was deleted | in | [`register-after-deletion.txt`](register-after-deletion.txt) |
| **4a** the query matches nothing | in | [`search-empty.txt`](search-empty.txt) |
| **4b** the scope cannot be resolved | **out of the minimum** — there are no scopes to be unresolvable | — |
| **7a** the Agent needs justification, not fact | in | [`report-rationale.txt`](report-rationale.txt) |
| **8a** a reference no longer resolves | in | [`report-stale-reference.txt`](report-stale-reference.txt) |

**1b and 1c are here because the goal was widened to admit them.** As the use case first stood they were dead
ends — nothing registered, no way round, no route to the goal — and by
[the method's §5](../../../../../notes/analysing-a-use-case.md) a use case may not name a failure it cannot
get past. But they are where the applicable stops being applicable, which is precisely what a condition space
has to be drawn around, and losing them here means rediscovering them at design once the analysis they should
have informed is written. So [§1 of the use case](../USE-CASE.md) now closes *or learns what it must fix in
order to*, and both are genuine routes to it. The manoeuvre is deliberate, slightly naughty, and recorded in
both places rather than done quietly.

**Nothing else on the unhappy path is here, and nothing else should be.** A disk that fills, a corpus that
changes mid-run, a registry that is corrupt — none of them is part of what must be true for the Agent to
reach its goal, and none of them earns an example until the use case names it as a route to that goal.

**Nothing impossible is here either.** Where a combination cannot arise, the analysis says so as a rule — a
true statement about the boundary — and there is no artefact to show, which is what makes it invalid.

### 2.2 Where This Sits

**The minimum is met.** Search and report sit a rung above it, with several per result shape, each picked to
vary something.

Most of these are related: one corpus underlies everything derived from `corpus/`, so where two are related
the pair is a combination that could be true. Three stand outside it —
[`register-path-absent.txt`](register-path-absent.txt),
[`register-path-unreadable.txt`](register-path-unreadable.txt) and
[`report-stale-reference.txt`](report-stale-reference.txt) — because each needs a world where something is
missing or has changed since registration, which a fixed corpus cannot show. They say at the top what world
they are in. Unrelated is the default and costs nothing.

**What is deliberately not here:** a `before` state that is not empty. Registering over a registry that
already holds documents is the more interesting case, because registering is absolute rather than
differential. That is an edge worth an example when elicitation reaches it, and not before.

## 3 Register A Path

`corpus/` holds four markdown documents in two directories, and one file that is not a document.

| | |
|---|---|
| [`corpus/`](corpus/) | what is registered |
| [`registered-before.md`](registered-before.md) | the registry beforehand — empty |
| [`register.txt`](register.txt) | what the run reports |
| [`registered.md`](registered.md) | the registry afterwards |

Four things in the corpus are deliberate, and each one is there to make something visible that a corpus of
plain documents would hide:

* **`procedures/cache-tuning.md` carries a Rationale and an Appendix.** Both register as structure — they have
  a type, a line span and a place in the tree — and neither contributes words. They stay addressable and are
  never matched. Both contain the phrase *eviction policy*, and neither is ever among §4's answers; and the
  word *thrashing*, which occurs in the corpus twice and both times inside one of them, answers nothing at
  all.
* **Every document carries a `Context` section**, which is likewise structure without words.
* **`cache-tuning.md` carries an outstanding TODO**, so registration has one to record.
* **`corpus/notes.txt` is not a markdown document.** It is not registered, no answer mentions it, and nothing
  reports it as a problem. A file that is not a document is not a failure.

## 4 Search The Registry

Four searches against the state §3 leaves. They are not a sequence and nothing connects them; each was picked
because it varies something, against the shapes
[4 — Search The Registry §5](../operations/4-search-the-registry.md) already names.

| | Shape | What it shows |
|---|---|---|
| [`search-truncated.txt`](search-truncated.txt) | **answer, truncated** | 16 nodes answered, the default cap admitted 10, and the answer says so |
| [`search-truncated.json`](search-truncated.json) | the same, machine rendering | the same answer in the same order, every field present |
| [`search-answer.txt`](search-answer.txt) | **answer** | 7 answered, nothing cut, documents and sections ranked against each other |
| [`search-empty.txt`](search-empty.txt) | **empty answer** | nothing answered, and that is an answer rather than a failure |
| [`search-excluded-zone.txt`](search-excluded-zone.txt) | **empty answer** | a word that *is* in the corpus, twice, and is unreachable because both occurrences sit in a Rationale or an Appendix |

The last of those is the only place an invariant is witnessed here rather than described. It is worth the
extra file: prose saying excluded zones are never matched is a claim, and an empty answer to a word that
demonstrably occurs in the corpus is evidence.

Each result row carries its reference, its relevance, and the word count that relevance was measured against —
and beneath it the ancestry chain down from the document, each ancestor with its own word count. That is what
lets the Agent choose what to fetch without fetching anything.

**A section and the document containing it are separate results.** `policies/retention-policy` and
`policies/retention-policy$2` both answer `retention class` and are ranked against each other on their own
merits. Neither suppresses the other.

## 5 Report A Reference

| | |
|---|---|
| [`report-section.txt`](report-section.txt) | a section reference — verbatim text, and the context path down to it |
| [`report-document.txt`](report-document.txt) | a document reference — the same, where the chain is the document alone |
| [`report-rationale.txt`](report-rationale.txt) | extension 7a — a rationale, which no search will ever hand back and which is addressable all the same |
| [`report-stale-reference.txt`](report-stale-reference.txt) | extension 8a — a reference the document no longer has, answered with the closest surviving one |

Each carries the line span and the document's total length, so what was reported is never mistaken for all
there is. In the minimum a report is never bounded, so that count is always the whole of it — which is
exactly the kind of thing that looks like an invariant here and turns out to be an artefact of the cut.

The rationale one is worth its place twice over. It is the only artefact showing a node that is registered as
structure, never indexed, and still reachable — the same node whose words §4 proves are unreachable. The
Agent gets there by deriving the reference from the section it justifies, because nothing ever offered it.

## 6 What These Already Show Is Unsettled

This is what the examples were for. Writing them down surfaced these; none is answered here, and each is a
question the analysis inherits.

* **Ranking by density alone ranks badly.** The figures come from the crudest function that honours the one
  constraint the use case already states ([USE-CASE.md](../USE-CASE.md) §7: matching more of the query's distinct terms beats matching one
  of them often). Even so, `policies/retention-policy$3 Expiry` outranks `policies/eviction-policy` on the
  query *eviction policy* — a passing mention in a short section beating the document actually about it. The
  weighing of coverage against frequency is the open question, and this is what it looks like when it is left
  crude.
* **Whether the query is stemmed is undecided, and it changes the answer set.** `eviction` does not match
  *evicted* here, so `policies/eviction-policy$3 What Is Never Evicted` — which is about nothing else — never
  answers. The use case leaves the query language open; this shows it is not a free choice.
* **Whether a document's word count includes its sections'.** These figures say yes: a document's count is
  everything under it, minus what is excluded. So `Cache Eviction Policy` is 161 words while its own prose
  outside any section is almost none. If relevance is a ratio against that count, a long document is penalised
  for being long — which may be right, and is not obviously right.
* **Whether an ancestry shows the answering node itself.** It does here, as the last link with no count of its
  own, because its count is already in the row. That is a rendering decision wearing the clothes of a model
  decision.
* **What a reference actually is.** Written here as a path relative to the registry root with `$` and a
  section number. Nothing has settled whether a reference is a path, an identifier, or a pair.

## 7 The Figures

The line numbers, counts and rankings are computed from `corpus/` by [`derive.py`](derive.py) rather than
typed, which cost nothing and made them accurate. Accuracy is worth having where it is free: the better these
match something real, the better the analysis they support.

```
python3 derive.py            rewrite every derived file
python3 derive.py --check    report any file that has drifted from the corpus
```

**`derive.py` specifies nothing.** It is not a design, a prototype, or a claim about how any of this should
work. Its scoring is the crudest thing that produces consistent figures, and §6 is where that shows.

**None of this is maintained.** These change once, if elicitation on the model shows one of them is wrong.
After that the analysis moves on to aspects, and the examples' work is finished. Adding a new example later to
make a point is cheap and worth doing; going back to tidy these is not.

# Rationale

**Why examples live beside fixtures rather than among them.** They answer different questions and carry
different authority. A fixture in `fixtures/` witnesses a cell of a condition space: it exists because
analysis found that cell, and it asserts. An example exists before there is a condition space at all, and
asserts nothing. Filing them together would put a seed and a conclusion under one name, and the first agent to
read the directory would cite the seed as a requirement.

**Why there is no single narrative running through this.** One corpus is used throughout because that was the
cheapest way to write it, not because these compose into a story. They deliberately do not: the searches are
not what an Agent would run in sequence, and the reports are not the references a search handed back. A tidy
run-through would cost effort to keep coherent and expose no variation that these do not, and coherence is not
what an example is for.

**Why the minimum is cut this hard.** Every dimension carried into a first analysis multiplies the condition
space, and a space too large to draw is a space nobody checks. The cuts in §1 are all extensions with a
default ordinal, so the minimum is a complete, coherent behaviour rather than a broken one — the Agent really
does find its documentation and really does read only what bears on the task. Adding `@{slug}` scopes,
previews and caller-set bounds later adds ordinals to dimensions that already exist.
