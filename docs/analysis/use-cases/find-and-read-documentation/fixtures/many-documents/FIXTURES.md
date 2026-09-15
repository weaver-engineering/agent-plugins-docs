# Many Documents Fixtures

The states witnessing cell @`1.3.1.1.1` of [find-and-read-documentation](../../USE-CASE.md) — the main success
scenario, with every registration rule that has no condition of its own present at once.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to; the main success scenario
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Stale Registration Fixtures](../stale-registration/FIXTURES.md) - cell @`1.3.1.1.2`, this same directory after one
  of its documents has gone
* [Single Document Fixtures](../single-document/FIXTURES.md) - cell @`1.1`, a path naming one document instead
  of a directory
* @docs/standards/documentation-standards.md/§3 - the document shape `doc-b.md` satisfies
* @docs/standards/documentation-standards.md/§4 - the indexing rules the Appendix and Rationale rows of
  `registered.md` turn on

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`many-documents.corpus`](corpus) | @`1.3.1.1.1` · **corpus** | a directory holding two markdown documents and one file that is not one |
| [`many-documents.registered`](registered.md) | @`1.3.1.1.1` · **Result** | what the registry must be able to hand back afterward, stated without naming a storage form |
| [`many-documents.report`](report.txt) | @`1.3.1.1.1` · **Stdout** | what the operation reports having registered, in the human rendering |
| [`many-documents.report`](report.json) | @`1.3.1.1.1` · **Stdout**, machine rendering | the same report for a caller that will parse it |

`registered.md` and a report together witness one state. The report says which documents were registered and
how much of each; `registered.md` says what the registry can therefore be asked for. Neither on its own is the
operation's result: a report with nothing behind it would say a registration happened that nothing could use,
and a registration nobody was told about would leave the caller unable to check what they had just done.

## 2 What Registering Does Here

`doc-a.md` is the plain case — three sections, no appendix, no rationale, no TODO — and it is here so that
`doc-b.md`'s extra rows can be read as *extra* rather than as what every document carries.

`doc-b.md` carries seven things at once, and all seven are invariants this corpus exists to witness
([operations/1-register-a-path.md](../../operations/1-register-a-path.md) §5).

Its `Appendix` and `Rationale` are recorded with their headings, their nesting and their line ranges, and none
of them carries words. That is the whole of the exclusion as this operation can state it: the sections stay
addressable, so a reader can still be pointed at one and handed it, and nothing in them can be reached by
searching, because there is nothing recorded for a search to match. `§Rationale.1.1` and `§Rationale.1.2` are
there to show the exclusion is a zone rather than a heading: they are nested two deep inside `# Rationale` and
they carry no words either.

Four figures are recorded as figures and not as sections. Each has a position and a pseudo-number, so each can
be addressed and fetched like anything else, and all four are absent from the section total — `doc-b.md`
reports seven sections, which is what it has without counting any of them. A figure that counted would make the
reported extent of a document depend on how much of it happened to be code.

Each figure carries its pseudo-number a different way, and none of the three ways is the fenced block's own
info string carrying the number alone — the old convention this corpus used to follow, and the reason it had
to change:

* **`§2.1.a`** — a `*fig.* 2.1.a` caption line immediately above the fence. This is the only one of the three a
  reader actually sees rendered, and the only one whose fence is otherwise free to be a real language: this
  figure is a Mermaid diagram, and its fence reads `` ```mermaid `` with nothing else in it.
* **`§2.2.a`** — a bare numeric info string, `` ```2.2.a ``, and no caption. Fine here because this fence isn't
  a language that needs its info string for anything else; a diagram fence could not use this form without
  losing its own language tag, which is exactly the fault the old convention had.
* **`§2.3.a`** — a `fig: 2.3.a` key inside a `---`-delimited block written *inside* a `` ```mermaid `` fence,
  with no caption. This is the form that specifically rescues a language-tagged figure: the fence's info string
  stays exactly `mermaid`, so it renders, and the pseudo-number travels as data inside the block instead of
  contesting the one slot a renderer actually reads.
* **`§3.1.a`** — carries two markers at once, and they disagree on purpose: a `*fig.* 3.1.a` caption and a
  `fig: 3.1.b` key in the fence's own frontmatter. This is the fourth invariant's own witness — one figure, not
  two, and the caption wins because it is given first, ahead of anything the fence contains. `3.1.b` is not
  registered anywhere; there is no cell where the frontmatter's number would win, because nothing here ever
  omits a caption while also disagreeing with it.

The old convention is retired rather than merely avoided: no figure here uses it, and `§2.1.a`'s Mermaid diagram
is the figure that would have gone dark under it — a fenced block only reads as `` ```mermaid `` when nothing
else shares that slot with the word itself.

The two TODO markers are recorded with their text, their containing section and their line, and the count
reaches the report as `- todos 2`. `doc-a.md` has none and its line simply ends, which is what makes the
suffix readable as a fact about `doc-b.md` rather than a field every document carries. One marker names a
ticket and one does not, so the reference is recorded where there is one to record and the absence is not an
error.

`notes.txt` is registered nowhere and mentioned nowhere. It is in the directory precisely so that the
registration can be seen declining to treat it as a document — silently, with no entry, no warning and no
failure. Under a directory path, a file that is not a markdown document is simply not one of the documents the
caller asked to register.

The reports are the fixtures for what the operation *says*. The human one is one line per document; the
machine one is a single compact JSON document declaring `ok`, with nothing else on the stream.

The two renderings differ in what they do with nothing. Nothing was dropped here, nothing was warned about and
nothing was unchanged, so the human rendering simply has no `dropped`, `warnings` or `unchanged` section — a
person reading at a glance is not served by three headings announcing that nothing happened. The machine
rendering carries all four regardless, the arrays empty and the count `0`, because a caller parsing the answer
would otherwise have to tell "nothing was dropped" from "this run does not report dropping" — and the second is
indistinguishable from an older version of the tool. The same facts, rendered for two readers with opposite
needs.

# Rationale

**Why one directory rather than one document per rule.** Every rule here has to hold at the same time for the
registration to be witnessed honestly. A corpus exercising one at a time would let an implementation record
appendix structure correctly, and TODOs correctly, and still produce the wrong answer for a document that has
both — which is every real document in this repo.

**Why the plain document is kept even though it exercises nothing of its own.** It is what makes the corpus a
corpus rather than a document with a directory around it, and it is the only thing that shows a registration
of two documents is two independent registrations rather than one merged account of the directory.

**Why `notes.txt` has real content rather than being empty.** An empty file is skippable for a reason that has
nothing to do with the rule under test — an implementation that skipped every empty file and registered every
non-empty one would pass this fixture and be wrong. The content is there to make the skip attributable to the
file not being a markdown document, and nothing else.
