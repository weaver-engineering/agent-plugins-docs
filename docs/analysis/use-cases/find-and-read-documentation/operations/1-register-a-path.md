# 1 — Register A Path

The condition space of [find-and-read-documentation](../USE-CASE.md) step 1, and the states bracketing it: the
dimensions its fixtures must expose, the invariants they must witness, and the cells they combine into, each
with the state it establishes and the fixture exposing it.

## Context
* [find-and-read-documentation](../USE-CASE.md) - the use case whose step 1 this analyses
* [single-document](../fixtures/single-document/FIXTURES.md) - a path resolving to one document
* [many-documents](../fixtures/many-documents/FIXTURES.md) - the main scenario's own states
* [stale-registration](../fixtures/stale-registration/FIXTURES.md) - a registered document since deleted
* [unchanged-documents](../fixtures/unchanged-documents/FIXTURES.md) - a re-registration where most of the
  corpus did not change
* [unreadable-document](../fixtures/unreadable-document/FIXTURES.md) - one document unreadable inside a
  directory that is not
* [nested-directory](../fixtures/nested-directory/FIXTURES.md) - one corpus under three invocations
* [non-markdown-document](../fixtures/non-markdown-document/FIXTURES.md) - a path naming something that is not a
  document
* [path-absent](../fixtures/path-absent/FIXTURES.md) - nothing at the given path
* [path-unreadable](../fixtures/path-unreadable/FIXTURES.md) - present, but cannot be read
* @docs/standards/documentation-standards.md/§3 - Document Shape, the structure registration records
* @docs/standards/documentation-standards.md/§4 - Indexing, the word and TODO content registration holds and
  the Rationale/Appendix exclusion §5's first invariant turns on

## 1 Dimensions

Every dimension of this operation's condition space, in rank order.

| Rank | Dimension | Category |
|---|---|---|
| 1 | `path` | dependency |
| 2 | `corpus` | dependency |
| 3 | `recurse` | parameter |
| 4 | `document-readability` | dependency |
| 5 | `unchanged-documents` | dependency |
| 6 | `stale-registrations` | dependency |
| 7 | `report-rendering` | parameter |

**path** is ranked outermost because two of its three values end the operation before anything is read, and
**corpus** next because one of its four ends it before anything is registered — as ranked, each prunes a
subtree rather than repeating itself across one. **recurse** is ranked above the three dependencies that follow
it because it decides which documents are in scope at all; the three that follow are all questions about the
scope once settled, in the order each presumes the last: whether a document can be read at all, then whether
what was read matches what the registry already held, then — separately — whether anything the registry
already held has since disappeared.

## 2 Payload States

This operation has no payload dimension. What varies is what is *at* the path, never what the caller hands
over: the invocation carries a path and a flag, and everything else is a state of the corpus or of the registry.
The documents themselves appear as dependency fixtures, not payloads — see §3 and the Rationale.

## 3 Dependency States

What the operation's own dependencies present it with. Projection: `given`.

### 3.1 `path`

What is at the path the operation was given, before anything about its contents is asked.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `resolves` | something is there and can be read |
| 2 | `absent` | nothing at the given path |
| 3 | `unreadable` | present, but cannot be read |

Ordinals 2 and 3 each fail gracefully, with their own message (§6, extensions 1b and 1c).

### 3.2 `corpus`

What the resolved path turns out to be, and therefore which documents are in scope.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `single-document` | the path names one markdown document |
| 2 | `non-markdown-document` | the path names a file that is not a markdown document |
| 3 | `directory-flat` | a directory holding documents and no subdirectories |
| 4 | `directory-nested` | a directory holding at least one subdirectory |

Ordinal 2 fails gracefully (§6, extension 1a). Registering a single path registers exactly what is there;
there is no directory for a non-document to be filtered out of, which is what makes this a failure here and an
ordinary skip under ordinals 3 and 4 (§5).

### 3.3 `document-readability`

Whether every document that is in scope — after **corpus** and **recurse** have settled what that scope is —
can actually be read, stated as the worst outcome present across the scope.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `all-readable` | every in-scope document could be read |
| 2 | `some-unreadable` | at least one in-scope document exists and is a markdown document, but could not be read |

Ordinal 2 does not fail the run: the documents that could be read are registered and reported normally, and the
one that could not is named in a warning (§6). This is a different condition from **path** `unreadable` (§3.1),
which is the *given* path itself failing to enumerate — here the path resolves and lists its contents fine, and
one listed document individually will not open.

### 3.4 `unchanged-documents`

Whether any in-scope, readable document's content is identical to what the registry already held for it at its
last registration under this path.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `none` | every in-scope document is new, or has changed, since it was last registered |
| 2 | `some` | at least one in-scope document's content exactly matches its last registration |

This is a fact the *report* economises on, never the registry's own computation. Every in-scope document is
still registered in full regardless — see §6's own note on `Result` — and `some` only changes how many of them
the report names individually rather than folding into a single count. Without it, re-registering a large,
mostly-settled corpus after a handful of edits would report the entire corpus every time, drowning the few
lines that actually say something in however many thousand repeat what a caller already knew.

### 3.5 `stale-registrations`

What the registry already holds for documents under this path, stated only in terms of *what* it holds and
never *how* — §7's first open question stays open.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `none` | every document the registry holds under this path is still there |
| 2 | `present` | the registry holds a registration for a document no longer under the path |

### 3.6 What Is Not A Dimension

**Which documents the corpus holds, and what is in them.** Every document under a path is registered by the
same rule, and a second document exercises nothing a first one did not — so document *count* multiplies the
space without varying the operation. What each document contains is likewise not an axis: a Rationale zone, a
figure and a TODO marker are each recorded whenever present and absent otherwise, which is an invariant's shape
and not a dimension's (§5).

## 4 Parameter Options

The knobs of the invocation itself — same entry state, different call. Projection: `when`.

### 4.1 `recurse`

| Ordinal | Value | Means |
|---|---|---|
| 1 | `absent` | subdirectories of the given path are ignored; only documents directly under it are registered |
| 2 | `bounded` | hypothesised as `--depth N`; subdirectories are walked down to `N` levels and no further |
| 3 | `unbounded` | hypothesised as `--recurse`; subdirectories are walked to whatever depth they go |

`bounded` at `N` and `unbounded` differ only in where the walk stops — nothing about how a document already
within the walked depth is registered depends on which flag reached it, which is why one payload
([nested-directory](../fixtures/nested-directory/FIXTURES.md)) serves both. `absent` is the same as `bounded`
at `0`, stated as its own ordinal because it is the default a caller gets without naming either flag.

Irrelevant wherever there is no subdirectory to descend into — every value of **corpus** but `directory-nested`
— and collapses for those (§6).

### 4.2 `report-rendering`

| Ordinal | Value | Means |
|---|---|---|
| 1 | `human` | the report is read by a person |
| 2 | `machine` | the caller declares it will parse the answer — hypothesised as `--json` |

Every path in the report — registered, dropped, warned about, or named in an error — is absolute. A relative
path would read differently depending on the caller's own working directory at the moment it happened to
invoke the operation, which would make the report a fact about the invocation rather than a fact about the
registry.

The human rendering has four sections, each present only where it has something to say: `registered` — one
line per document, its path, how many sections it holds and the range they span, then the same for its
`APPENDIX` and `RATIONALE` where it has them, then its outstanding TODO count where it has any; `dropped` —
one line per document the registry no longer holds; `warnings` — one line per document that could not be read;
`unchanged` — a single count, never a list of paths, of how many in-scope documents were left out of
`registered` because their content had not changed. The machine rendering is compact JSON declaring `ok`,
carrying `registered`, `dropped` and `warnings` as named arrays and `unchanged` as a bare integer, all four
always present — the three arrays empty and the count `0` where there is nothing to report — so a caller
parsing the answer never has to tell "nothing happened here" from "this run does not report this".

A local CLI is the entry point in every product offering this use case is expected to reach — the first drop,
a local API or MCP server, and a remote one across teams and document domains — because the corpus is a git
working tree being edited locally, and that is where a human reviews what an agent produced. So this operation
has a rendering pair whatever else is later put in front of it.

## 5 Invariants

What this operation does regardless of any condition.

| Invariant | The rule it defines | Witnessed by |
|---|---|---|
| **Rationale and Appendix are recorded as structure, never as words** | each heading under `# Rationale` or `# Appendix`, and every heading nested beneath one, is recorded with its title, type and position so it stays addressable — and none of their words is recorded, so nothing in them can ever be matched by a search | @`1.3.1.1.1` — [`many-documents.registered`](../fixtures/many-documents/registered.md), whose `Appendix` and `Rationale` headings carry line ranges and no words, beside body sections that carry both |
| **A figure is recorded as structure, typed apart from a section** | a fenced code block carrying a pseudo-number is recorded with its own position and pseudo-number, addressable like a heading — and is never a section, so it never counts toward a document's reported section total | @`1.3.1.1.1` — [`many-documents.registered`](../fixtures/many-documents/registered.md), where `doc-b.md` holds four and still reports seven sections |
| **A caption line marks a figure** | a `*fig.* N` line immediately before a fence marks that fence as figure `N`, and the caption is part of the figure's own span | @`1.3.1.1.1` — `doc-b.md`'s `§2.1.a`, whose caption both marks it and renders visibly, unlike anything else that can mark a figure |
| **A bare numeric info string marks a figure** | a fence opened `` ```N `` with no language marks itself as figure `N` | @`1.3.1.1.1` — `doc-b.md`'s `§2.2.a`, a fence with no caption and no language, marked by its info string alone |
| **A frontmatter key marks a figure without disturbing a real language tag** | a `fig: N` key inside a `---`-delimited block within a fence marks that fence as figure `N`, and the fence's own info string is untouched — `` ```mermaid `` still reads as exactly `mermaid` | @`1.3.1.1.1` — `doc-b.md`'s `§2.3.a`, a Mermaid diagram marked this way and still a Mermaid diagram |
| **However many markers a figure carries, it is exactly one figure, and a disagreement resolves to whichever was given first** | multiple markers on one fence never register as more than one figure; where they name different numbers, the figure's id is the one given first in the document — the caption, when there is one, since it precedes the fence entirely | @`1.3.1.1.1` — `doc-b.md`'s `§3.1.a`, whose caption says `3.1.a` and whose frontmatter says `3.1.b`; registered once, as `3.1.a` |
| **Every outstanding TODO marker is recorded, and reported** | each `//TODO`-style marker is recorded with its text, containing section and line, and the count of them appears on the document's own report line — a document carrying TODOs registers normally, since an outstanding TODO is a smell and not a fault | @`1.3.1.1.1` — [`many-documents.report`](../fixtures/many-documents/report.txt), whose `doc-b.md` line ends `- todos 2` while `doc-a.md`, having none, ends without it |
| **Registering is absolute, never differential** | the registry's resulting *state* — the nodes it holds, for every in-scope document — depends only on what is under the path now, never on what it held before; a path registered for the first time and one re-registered after everything beneath it changed compute the identical result. What the *report* chooses to name individually is a separate question (`unchanged-documents`, §3.4) and does not bear on this | @`1.3.1.1.2` — [`stale-registration.registered`](../fixtures/stale-registration/registered.md), which is the registration of what is there now, with the vanished document's entry gone rather than amended |
| **A file that is not a markdown document takes no part in the registry** | under a directory path, anything that is not a markdown document is not a document: it is not registered, it is not reported, and it is not an error | @`1.3.1.1.1` — [`many-documents.registered`](../fixtures/many-documents/registered.md), whose corpus holds `notes.txt` beside two documents and whose registration names only the two |
| **An unreadable document is warned about, never registered and never failed** | a document that is a markdown document but cannot be read is named in the report's `warnings`, and every other in-scope document is registered exactly as it would be if the unreadable one were not there | @`1.3.2` — [`unreadable-document.report`](../fixtures/unreadable-document/report.txt), whose readable document registers normally while `secret.md` is named only in `warnings` |

Eight of the ten are witnessed at the same cell, which is what makes `many-documents` the corpus it is: one
directory carrying every rule that has no condition of its own. The other two each need a condition the main
scenario cannot carry alongside the rest: a document having vanished since the last registration, and a
document existing but refusing to open.

## 6 Output Fixtures

Every leaf has two further leaves under **report-rendering** — `.1` human and `.2` machine — carrying the same
state and differing only in how the report is rendered, so they are not drawn. Both renderings are held
concretely for every leaf that produces one.

**Result** here is not a storage snapshot and names no storage form. It is what the registry must be able to
hand back afterward, whatever form it takes: the nodes registered, their titles, types and positions, which of
them carry words, and the TODOs found — each grouped under the absolute path of the document it belongs to,
never a path relative to wherever the operation happened to be invoked from. That is prescribable without
choosing between files, a database and a service, and it is exactly what steps 4 and 7 consume as their own
entry state (Rationale).

No node here is **invalid** except one: **stale-registrations** cannot arise under `single-document`, because
the only document under a single-document path is that document, and a path whose document is gone fails at
**path** instead. Everything else pruned is **immaterial**: **recurse** collapses wherever there is no
subdirectory to descend into; **document-readability** and **unchanged-documents** are each witnessed once, at
@`1.3.2` and @`1.3.1.2` respectively, and neither varies with nesting or with how far a walk goes, so both
collapse under `directory-nested` entirely; **stale-registrations** is witnessed once at @`1.3.1.1.2` rather
than again under a nesting, an unreadable document, or an unchanged one — none of which changes anything about
how a vanished registration is dropped.

Registration's deliverable is the registry's new state and the report of what went into it. Every failing leaf
below is an extension because it registers nothing; a document skipped for not being markdown, a subdirectory
not descended into because no recursion flag was given, a document warned about because it could not be read,
and a document folded into `unchanged` rather than named, are none of them extensions — each hands back exactly
the registration that was asked for, of exactly the scope that was asked for.

* 1 - **path:** `resolves`
  * 1.1 - **corpus:** `single-document`
    > Leaf. **recurse** is immaterial — there is no directory to descend into — and
    > **stale-registrations** cannot arise (above).
    >
    > **Establishes:** the one document registered, its sections recorded and reported
    >
    > **corpus:** [`single-document.document`](../fixtures/single-document/document.md)
    >
    > **Result:** [`single-document.registered`](../fixtures/single-document/registered.md)
    >
    > **Stdout:** `single-document.report` — [txt](../fixtures/single-document/report.txt)
    > · [json](../fixtures/single-document/report.json)
  * 1.2 - **corpus:** `non-markdown-document`
    > Leaf; the run stops before registering anything.
    >
    > **Establishes:** nothing registered; the report names the path and says it is not a document this
    > registry can hold — **extension 1a**
    >
    > **corpus:** [`non-markdown-document.target`](../fixtures/non-markdown-document/target.txt)
    >
    > **Result:** none — nothing was registered
    >
    > **Stdout:** `non-markdown-document.error-report` —
    > [txt](../fixtures/non-markdown-document/error-report.txt)
    > · [json](../fixtures/non-markdown-document/error-report.json)
  * 1.3 - **corpus:** `directory-flat`
    > **recurse** is immaterial throughout — there is no subdirectory to descend into.
    * 1.3.1 - **document-readability:** `all-readable`
      * 1.3.1.1 - **unchanged-documents:** `none`
        * 1.3.1.1.1 - **stale-registrations:** `none`
          > **Establishes:** every document directly under the path registered, each with its sections, its
          > `APPENDIX` and `RATIONALE` extents where it has them, and its outstanding TODO count — **the main
          > success scenario**
          >
          > **Witnesses:** *Rationale and Appendix are recorded as structure, never as words* (§5), by holding
          > their headings with line ranges and no words beside body sections carrying both
          >
          > **Witnesses:** *A figure is recorded as structure, typed apart from a section* (§5) — `doc-b.md`
          > holds four and still reports seven sections
          >
          > **Witnesses:** *A caption line marks a figure*, *a bare numeric info string marks a figure*, *a
          > frontmatter key marks a figure without disturbing a real language tag*, and *however many markers a
          > figure carries it is exactly one, resolved to whichever was given first* (§5) — `doc-b.md`'s four
          > figures, one per form and one carrying two markers that disagree
          >
          > **Witnesses:** *Every outstanding TODO marker is recorded, and reported* (§5), in `doc-b.md`'s two
          > against `doc-a.md`'s none
          >
          > **Witnesses:** *A file that is not a markdown document takes no part in the registry* (§5), in the
          > `notes.txt` sitting beside the two documents
          >
          > **corpus:** [`many-documents.corpus`](../fixtures/many-documents/corpus)
          >
          > **Result:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
          >
          > **Stdout:** `many-documents.report` — [txt](../fixtures/many-documents/report.txt)
          > · [json](../fixtures/many-documents/report.json)
        * 1.3.1.1.2 - **stale-registrations:** `present`
          > **Establishes:** the surviving document registered and the vanished one's registration dropped in
          > the same pass, so nothing the registry holds describes a document that is no longer there —
          > **extension 2a**
          >
          > **Witnesses:** *Registering is absolute, never differential* (§5) — what is written is the
          > registration of what is there now, not an amendment of what was held before
          >
          > **stale-registrations:** [`stale-registration.registered-before`](../fixtures/stale-registration/registered-before.md)
          >
          > **corpus:** [`stale-registration.corpus`](../fixtures/stale-registration/corpus)
          >
          > **Result:** [`stale-registration.registered`](../fixtures/stale-registration/registered.md)
          >
          > **Stdout:** `stale-registration.report` — [txt](../fixtures/stale-registration/report.txt)
          > · [json](../fixtures/stale-registration/report.json)
      * 1.3.1.2 - **unchanged-documents:** `some`
        > Leaf. **stale-registrations** *pruned, immaterial:* dropping a vanished registration is witnessed at
        > @`1.3.1.1.2` and does not vary with some other document in scope being unchanged.
        >
        > **Establishes:** the one document that is new or has changed registered individually; the two whose
        > content matches their last registration registered exactly as fully, but folded into a single count
        > rather than named
        >
        > **unchanged-documents:** [`unchanged-documents.registered-before`](../fixtures/unchanged-documents/registered-before.md)
        >
        > **corpus:** [`unchanged-documents.corpus`](../fixtures/unchanged-documents/corpus)
        >
        > **Result:** [`unchanged-documents.registered`](../fixtures/unchanged-documents/registered.md)
        >
        > **Stdout:** `unchanged-documents.report` — [txt](../fixtures/unchanged-documents/report.txt)
        > · [json](../fixtures/unchanged-documents/report.json)
    * 1.3.2 - **document-readability:** `some-unreadable`
      > Leaf. **unchanged-documents** and **stale-registrations** *pruned, immaterial:* an unreadable document
      > cannot be compared to anything, so whether some *other* document in scope is unchanged or vanished is
      > witnessed at @`1.3.1.2` and @`1.3.1.1.2` respectively and does not vary with this one being unreadable.
      >
      > **Establishes:** the readable document registered exactly as it would be alone; the unreadable one
      > registered nowhere and named once, in `warnings`
      >
      > **Witnesses:** *An unreadable document is warned about, never registered and never failed* (§5)
      >
      > **corpus:** [`unreadable-document.corpus`](../fixtures/unreadable-document/corpus), plus
      > [`unreadable-document.layout`](../fixtures/unreadable-document/layout.md) for the file that is there
      > and cannot be opened
      >
      > **Result:** [`unreadable-document.registered`](../fixtures/unreadable-document/registered.md)
      >
      > **Stdout:** `unreadable-document.report` — [txt](../fixtures/unreadable-document/report.txt)
      > · [json](../fixtures/unreadable-document/report.json)
  * 1.4 - **corpus:** `directory-nested`
    > **document-readability** is immaterial throughout — witnessed at @`1.3.2`, and nesting or depth changes
    > nothing about how an unreadable document is handled. **unchanged-documents** likewise — witnessed at
    > @`1.3.1.2`, and nesting or depth changes nothing about how an unchanged document is folded into a count.
    * 1.4.1 - **recurse:** `absent`
      > Leaf. **stale-registrations** *pruned, immaterial:* as @`1.3.1.1.2`, and does not vary with nesting.
      >
      > **Establishes:** only the documents directly under the path registered; the subdirectory is not
      > descended into, and the documents in it are neither registered nor reported
      >
      > **corpus:** [`nested-directory.corpus`](../fixtures/nested-directory/corpus)
      >
      > **Result:** [`nested-directory.registered-shallow`](../fixtures/nested-directory/registered-shallow.md)
      >
      > **Stdout:** `nested-directory.report-shallow` —
      > [txt](../fixtures/nested-directory/report-shallow.txt)
      > · [json](../fixtures/nested-directory/report-shallow.json)
    * 1.4.2 - **recurse:** `bounded`
      > Leaf. **stale-registrations** *pruned, immaterial:* as @`1.4.1`.
      >
      > **Establishes:** the corpus walked one level down and no further — the document directly under the
      > path and the one immediately beneath it registered, the one below that neither registered nor
      > reported, exactly as if it were not there
      >
      > **corpus:** [`nested-directory.corpus`](../fixtures/nested-directory/corpus)
      >
      > **Result:** [`nested-directory.registered-bounded`](../fixtures/nested-directory/registered-bounded.md)
      >
      > **Stdout:** `nested-directory.report-bounded` —
      > [txt](../fixtures/nested-directory/report-bounded.txt)
      > · [json](../fixtures/nested-directory/report-bounded.json)
    * 1.4.3 - **recurse:** `unbounded`
      > Leaf. **stale-registrations** *pruned, immaterial:* as @`1.4.1`.
      >
      > **Establishes:** the same corpus walked to its full depth — every document at every level registered,
      > with nothing about a document's registration depending on how deep it sat
      >
      > **corpus:** [`nested-directory.corpus`](../fixtures/nested-directory/corpus)
      >
      > **Result:** [`nested-directory.registered-recursed`](../fixtures/nested-directory/registered-recursed.md)
      >
      > **Stdout:** `nested-directory.report-recursed` —
      > [txt](../fixtures/nested-directory/report-recursed.txt)
      > · [json](../fixtures/nested-directory/report-recursed.json)
* 2 - **path:** `absent`
  > Leaf; the run stops before reading.
  >
  > **Establishes:** nothing registered; the report names the path and says nothing was found there —
  > **extension 1b**
  >
  > **path:** [`path-absent.layout`](../fixtures/path-absent/layout.md)
  >
  > **Result:** none — nothing was read, so nothing is registered
  >
  > **Stdout:** `path-absent.error-report` — [txt](../fixtures/path-absent/error-report.txt)
  > · [json](../fixtures/path-absent/error-report.json)
* 3 - **path:** `unreadable`
  > Leaf; the run stops before reading.
  >
  > **Establishes:** nothing registered; the report says the path is there and could not be read, so the fault
  > is a permission and not a missing path — **extension 1c**
  >
  > **path:** [`path-unreadable.layout`](../fixtures/path-unreadable/layout.md)
  >
  > **Result:** none — nothing was read, so nothing is registered
  >
  > **Stdout:** `path-unreadable.error-report` — [txt](../fixtures/path-unreadable/error-report.txt)
  > · [json](../fixtures/path-unreadable/error-report.json)

## 7 Coverage

Eleven leaves survive pruning, each with exactly one corpus fixture where it has a corpus at all.

Every value of every dimension is still exposed by a kept leaf: all three of **path** on the spine; all four of
**corpus** at @`1.1`, @`1.2`, @`1.3` and @`1.4`; all three of **recurse** beneath @`1.4`; both values of
**document-readability** at @`1.3.1` and @`1.3.2`; both values of **unchanged-documents** at @`1.3.1.1` and
@`1.3.1.2`; both values of **stale-registrations** at @`1.3.1.1.1` and @`1.3.1.1.2`. Every invariant in §5 names
the leaf that witnesses it, and each of those leaves names the invariant back — ten claims, agreeing from both
directions.

* **Leaves @`1.4.1`, @`1.4.2` and @`1.4.3` are one corpus under three invocations**, and the only set here that
  cannot be told apart by looking at the corpus. That is what earns **recurse** a parameter rather than an
  invariant: the same tree is registered three legitimately different ways, and only the call says which.
* **@`1.4.1` is kept rather than pruned into @`1.3.1.1.1`.** A flat directory has no subdirectory to skip, so it
  cannot show that one *was* skipped. Only a nested corpus registered without descending witnesses that
  descending is a choice rather than a default, which is the whole point of the flag having a default at all.
  @`1.4.2` earns its own leaf the same way: a walk that stops at a bound is not observable from a walk that
  never started, or from one that never stopped.
* **@`1.3.2` is a directory-flat cell, not a directory-nested one.** An unreadable document and a subdirectory
  are unrelated conditions, and combining them would leave it ambiguous which one the leaf was exercising.
  Placing it beside @`1.3.1` keeps it doing one thing.
* **The enumeration's own findings are @`1.2`, @`2` and @`3`.** None of the three appeared anywhere in the use
  case until this dimension table was written out; all three turned out to be ordinary conditions of being
  invoked against a path, and all three now fail gracefully with their own messages. They are extensions 1a,
  1b and 1c, added to the use case by this pass.
* **A second document earns no cell, and the main scenario has three files anyway.** Count is not a dimension
  (§3.6), but the main scenario's corpus holds two documents and a non-document regardless — because seven of
  the eight invariants witnessed here need a document with something in it, and one needs a file that is not a
  document at all.
* **`unchanged-documents` sits under `all-readable`, not as a sibling of `document-readability`.** An unreadable
  document cannot be compared to what the registry held for it — there is nothing to compare, only an absence —
  so asking whether it is unchanged is not a question with an answer until it is readable. Nesting it beneath
  keeps the dimension meaningful everywhere it is enumerated, rather than needing its own "not applicable" value
  wherever readability has already failed.
* **@`1.3.1.2`'s corpus is plain, not the rich one.** Two of its three documents carry nothing but the fact of
  being unchanged; wiring them to also witness the figure and TODO invariants would leave a reader unable to
  tell which rule the fixture was actually there to show, the same reasoning that keeps `doc-a.md` plain at
  @`1.3.1.1.1`.
* **`doc-b.md` carries four figures rather than one.** Four of this operation's invariants are each a different
  fact about how a figure is marked, and no single figure can carry more than two markers at once without
  becoming the fifth invariant's own witness rather than its own. Four figures is the minimum that shows all
  four without any one of them doing double duty by coincidence.
* **Nothing here reads anything back.** Every leaf's Result says what the registry must be able to return; no
  leaf demonstrates it returning any of it. That is steps 4 and 7's to witness, against these same fixtures.

# Rationale

**Why this operation has no payload dimension.** The invocation carries a path and its flags, and a path is not
a payload in any sense that varies: every difference that matters is a difference in what the path *finds*. The
documents are therefore dependency fixtures — the corpus the operation reads — rather than payloads it was
handed. Modelling them as payloads would say the caller supplied the documents, which is precisely what
`document-a-concept` does and this operation does not.

**Why `Result` is prescribable without choosing a storage form.** An earlier draft of this document omitted
`Result` entirely on the grounds that the registry's form is §7's first open question, so nothing concrete
could be written. That was wrong, and wrong in a way worth recording: what a storage form must be able to
*provide* is fully determined by what was registered, and stating it commits to nothing about how it is held.
Each `registered.md` is that statement — the nodes, their types, positions and titles, which carry words, and
the TODOs found — and it is the same artefact steps 4 and 7 take as their own entry state, which is how a
search result's shape and contents come to be determined by what was registered rather than by the design that
later stores it.

**Why a non-markdown file is a failure at a single path and a skip under a directory.** Both are the same rule
— only markdown documents are registered — meeting two different asks. A caller naming a directory asks for
whatever documents are in it, and a file that is not one is simply not among them. A caller naming a file asks
for *that* file, and there is nothing else the request could have meant, so declining silently would report
success having registered nothing.

**Why `recurse` is a parameter rather than a second corpus value.** Whether a directory has subdirectories is a
fact about the corpus; whether they are descended into is a fact about the call. Folding them together would
make `directory-nested` mean two different things depending on an invocation the dimension does not mention,
and would lose the one thing @`1.4.1` exists to show — that a tree can be registered shallowly on purpose.

**Why `bounded` and `unbounded` are two ordinals of one dimension rather than a depth-valued dimension of its
own.** What varies the operation is where the walk stops, and that is a single question with an integer answer
at one end and "never" at the other — modelling every depth as its own ordinal would multiply the space to
observe a rule that does not change between depths one and two. `bounded` is witnessed at one depth because
one depth already shows the walk stopping partway; a second depth would show the same rule stopping at a
different number.

**Why an unreadable document is a dependency dimension and not folded into `corpus`.** `corpus` answers what
kind of thing the path is; readability answers whether what is there can actually be opened, which is a
question corpus does not reach — a directory is `directory-flat` whether or not everything in it can be read.
Keeping them apart is also why the flag stays a warning rather than a failure: `corpus` failing (`path`
`unreadable`) means nothing could be enumerated at all, and `document-readability` failing means enumeration
worked and one specific document did not open, which the operation can route around and the caller can act on
individually.

**Why `unchanged-documents` is a dependency and not a parameter of `report-rendering`.** It looks like a
rendering choice — how verbose the report is — but it isn't one the caller makes: whether a document happens to
match its last registration is a fact the corpus and the registry's own history present, not a flag anyone
passes. `report-rendering` governs how the same facts are *encoded*; this dimension governs which facts about
scope there are to encode in the first place, the same role `document-readability` and `stale-registrations`
already play.

**Why an outstanding TODO does not make registration an extension.** A TODO marker is a smell and not a fault:
the document is registered exactly as any other would be, and the count on its report line is a fact about what
was registered rather than a refusal to register it. `operation-fixtures.md` §5 is explicit that a fact in the
report is never an extension — what makes one is the operation not delivering.

**Why the four figure-marking invariants are stated here rather than only cited.** `documentation-standards.md`
is where a figure's pseudo-number notation belongs, and normally this document would cite it the way it cites
§3 and §4 rather than restate it. Its own worked example currently specifies a notation that breaks against a
Mermaid diagram — the fenced block's info string has to read as exactly `mermaid` to render, and the old
convention wrote the pseudo-number into that same slot — found while writing this fixture and fed back rather
than silently worked around (WVR-206, which owns changes to that standard). Until that lands, this operation's
own Result depends on figures being recognised correctly regardless, so the rule is stated here in full, against
the four figures in `doc-b.md` built to need it. Once the standard states this itself, this table should
shrink back to a citation the way §3 and §4 already are — carrying it twice from here on would be exactly the
drift `operation-fixtures.md`'s own no-methodology rule exists to prevent.

**What this analysis still does not settle about recursion.** `depth` is modelled as counting levels below the
given path, starting from `1` for its immediate children — @`1.4.2`'s fixture registers the path itself and one
level down. Whether a caller can ask for a depth relative to something other than the path it named, and
whether there is any cap on how deep `unbounded` is actually allowed to go against a real, possibly enormous
tree, are not settled here.
