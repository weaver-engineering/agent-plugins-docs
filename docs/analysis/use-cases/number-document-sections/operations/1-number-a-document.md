# 1 — Number A Document

The condition space of [number-document-sections](../USE-CASE.md) step 1, and the states bracketing it: the
dimensions its fixtures must expose, the invariants they must witness, and the cells they combine into, each
with the state it establishes and the fixture exposing it.

## Context
* [number-document-sections](../USE-CASE.md) - the use case whose step 1 this analyses
* [mixed-numbering](../fixtures/mixed-numbering/FIXTURES.md) - the main scenario's own states
* [shared-pseudo-number](../fixtures/shared-pseudo-number/FIXTURES.md) - duplicated numbers nothing points at
* [anchor-disambiguated](../fixtures/anchor-disambiguated/FIXTURES.md) - an anchor resolving into them
* [relative-target](../fixtures/relative-target/FIXTURES.md) - one payload under two filesystem layouts
* [dangling-reference](../fixtures/dangling-reference/FIXTURES.md) - a reference naming nothing
* [ambiguous-reference](../fixtures/ambiguous-reference/FIXTURES.md) - a reference naming more than one thing
* [document-absent](../fixtures/document-absent/FIXTURES.md) - nothing at the given path
* [document-not-writable](../fixtures/document-not-writable/FIXTURES.md) - present, readable, not writable
* @docs/standards/documentation-standards.md/§3 - the numbering convention the outputs satisfy
* @docs/standards/documentation-standards.md/§6 - the two reference forms §2.1 turns on

## 1 Dimensions

Every dimension of this operation's condition space, in rank order.

| Rank | Dimension | Category |
|---|---|---|
| 1 | `document` | dependency |
| 2 | `reference-resolution` | payload |
| 3 | `first-sibling-number` | payload |
| 4 | `figure` | payload |
| 5 | `local-target` | dependency |
| 6 | `unresolved-link-text` | payload |
| 7 | `report-rendering` | parameter |

**document** is ranked outermost because two of its three values end the operation before anything is read,
and **reference-resolution** next because its third and fourth values end it before numbering — as ranked,
each of those prunes a subtree rather than repeating itself across one. **local-target** ends nothing and
is irrelevant to most payloads, so it is ranked below the dimensions it would otherwise multiply.

## 2 Payload States

What varies in the document itself. Projection: `given`.

### 2.1 `reference-resolution`

What the document's own same-document references point at, stated as the **worst** outcome present: a
document with one dangling and one ambiguous reference is `4`. Only references carrying a section number
this operation would otherwise rewrite are counted — whether a link's *target* exists is not checked.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `none-present` | the document contains no same-document reference |
| 2 | `all-resolve` | every reference names exactly one heading or figure, in the body or in a named region |
| 3 | `some-dangling` | at least one reference names no heading or figure, and none names more than one |
| 4 | `some-ambiguous` | at least one reference names more than one |

### 2.2 `first-sibling-number`

Whether the first section, or the first subsection of a parent, opts itself into visible numbering.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `absent` | it carries no pseudo-number, so it takes a hidden `0` |
| 2 | `present` | it carries one, opting into visible numbering from `1` |

### 2.3 `figure`

Whether the document contains anything numbered on the figure rule rather than the heading rule.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `absent` | no pseudo-numbered fenced block |
| 2 | `present` | at least one, numbered `M.N.a` |

### 2.4 Pseudo-Number Collision Is A Route, Not A Dimension

Two headings carrying the same pseudo-number changes nothing on its own, because numbering comes from
position and depth. It is one of the ways **reference-resolution** reaches `4`, and it survives as a property
of *fixtures*: that value is exposed by two payloads, one where a `§` token meets a duplicated number and one
where an anchor meets a duplicated number *and* title.

### 2.5 `unresolved-link-text`

Whether the document contains a link whose target carries a protocol other than `file://` *and* whose text
contains a `§` token — a reference this operation declines to decide about.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `absent` | every `§` in link text belongs to a target the operation resolves |
| 2 | `present` | at least one does not, and is left as written **with a warning** |

**Why the operation declines, and why declining is right here.** Identity across a network boundary is not
defined for this operation. A document is edited before it is published, and publication may change it —
adding frontmatter, say — so the thing at `https://.../widget-store-guide` is not this document in any sense
this operation can check, even when it is "the same document" to a reader. The same content may equally sit
at two URLs. There is no question to answer, not merely an expensive one.

Cost is the lesser reason and was overstated in an earlier draft: only links whose *text* carries a `§`
would ever need resolving, and those are few.

**Why this operation warns rather than declining silently.** The rule is opinionated and will sometimes be
wrong — a published URL really can name this document — and a caller who never learns where the opinion was
applied has no way to check it.

## 3 Dependency States

The document store the operation reads from and writes to — named by the requirement, which says the operation
is invoked *against a document*. Projection: `given`.

### 3.1 `document`

| Ordinal | Value | Means |
|---|---|---|
| 1 | `readable-writable` | the document is there and can be written back |
| 2 | `absent` | nothing at the given path |
| 3 | `not-writable` | present and readable, but cannot be written |

Ordinals 2 and 3 each fail gracefully, with their own message (§6, extensions 1c and 1d).

### 3.2 `local-target`

Where the document's own locally-resolvable link targets land. The document's identity is never in doubt; a
*target's* is, and only the tree around the document settles it — so the same payload can be correct two
different ways.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `resolves-here` | a local target resolves to this document, so `§` tokens in its link text are rewritten |
| 2 | `resolves-elsewhere` | every local target resolves to some other document, so their link text is left alone |

Only `file://` targets and bare paths are resolved; anything carrying another protocol is not (§2.5). This
dimension is **irrelevant** to any payload with no locally-resolvable target, and collapses for those (§6).

## 4 Parameter Options

The knobs of the invocation. Projection: `when` — the entry state is identical and the call is different.

### 4.1 `report-rendering`

| Ordinal | Value | Means |
|---|---|---|
| 1 | `human` | the report is read by a person |
| 2 | `machine` | the caller declares it will parse the answer — hypothesised as `--json` |

This operation's human rendering is terse and line-oriented — a section head, one item per line, its
location, a short reason — which is what its Architect asked for, being a report they read at a glance
rather than one they study. Its machine rendering is compact JSON declaring `ok`.

Both renderings state the outcome, and this operation also exits with a code, so it has two channels saying
the same thing and they are required to agree. The code is not carried in the report.

## 5 Invariants

What this operation does regardless of any condition.

| Invariant | The rule it defines | Witnessed by |
|---|---|---|
| **`Context` is excluded at any depth** | a `Context` heading is never numbered and takes no position, at whatever depth it appears — so the first numbering-eligible heading beneath its parent is the first, not the second | @`1.2.1.2` — [`mixed-numbering.before`](../fixtures/mixed-numbering/before.md), which nests a `Context` under `Using The Store` and leaves `Errors` taking `1.0` regardless |
| **`Appendix` and `Rationale` are regions, numbered and addressed as such** | neither heading is numbered itself, but each opens a fresh sequence for the sections beneath it — body, `Appendix` and `Rationale` each count from `1` independently — and a reference into one is region-qualified: `§1.2` names the body's, `§Appendix.1.2` the appendix's. The qualification is what keeps the restart from making ids ambiguous | @`1.2.1.2` — [`mixed-numbering.before`](../fixtures/mixed-numbering/before.md), whose body reaches `1.1` while its `Appendix` runs `1`, `2` and its `Rationale` starts again at `1`, with a body reference `§Appendix.5` following the appendix's own renumbering to `§Appendix.1` |
| **`Context`, `Appendix` and `Rationale` match case-insensitively** | the three are recognised however they are cased, in a heading or in a reference — `# rationale` is the same heading as `# Rationale`, and `§aPpendix.1` the same reference as `§Appendix.1` | @`1.2.1.2` — [`mixed-numbering.before`](../fixtures/mixed-numbering/before.md), which writes its `Appendix` conventionally and its `rationale` in lower case, so the tolerance shows against the convention rather than replacing it |
| **Link text follows its target** | a `§` token in the *text* of a link is rewritten only when the link's target resolves to this document. `[model's own §2.3](widget-model.md)` is left alone; `[retry §2.1](widget-store-guide.md)` and `[retry again §2.1](./widget-store-guide.md)` are both rewritten. The target decides, never the text — and the target is resolved, never string-matched, since a document has more than one spelling of its own path | @`1.2.1.2` — [`mixed-numbering.before`](../fixtures/mixed-numbering/before.md), which carries all three path forms on adjacent lines: one resolving elsewhere and left alone, two spellings of this document and both rewritten |
| **A bare anchor is internal** | an anchor carrying no path names this document by definition, so it is rewritten with nothing resolved and no target consulted | @`1.2.2.1` — [`anchor-disambiguated.before`](../fixtures/anchor-disambiguated/before.md), whose `#3-1-retry` follows its target with no path to resolve |
| **Non-reference text is untouchable** | external `@{repo-slug}/{path}[/§M.N][/L1-L2]` references and number-like prose such as a version string are left exactly as they were | @`1.2.1.2` — [`mixed-numbering.before`](../fixtures/mixed-numbering/before.md), which carries an external reference and a version string, as does every other payload besides |

Three of the four are witnessed at the same cell, which is what makes `mixed-numbering` the payload it is:
one document carrying every rule that has no condition of its own. The fourth needs a bare anchor, and the
main scenario's payload has none.

Non-reference text is carried by every payload here, not only the one that witnesses it: it costs nothing,
and it lets every fixture show that nothing else disturbed it.

`Context` never has subsections of its own. Nothing here supports one, and nothing here polices it either.

## 6 Output Fixtures

Every leaf has two further leaves under **report-rendering** — `.1` human and `.2` machine — carrying the
same state and differing only in how the report is rendered, so they are not drawn.

**Result** and **Stdout** are not the same thing here: a renumbered document is written, a report is
printed, and a run can produce one without the other — every failing leaf below does. Both the graceful
failures and the successes print to Stdout, because reporting that the document it was given is invalid
*is* this operation working; **Stderr** would be the tool itself failing, which is not a condition of this
space and has no leaf.

No node here is **invalid** — every combination of these dimensions is a document someone could write.
Seven are **immaterial**: **first-sibling-number** and **figure** each contribute a rule that varies with
nothing else, so their values are witnessed once rather than again under every other value, and
**local-target** collapses wherever a payload has no locally-resolvable target to be uncertain about.
**unresolved-link-text** is immaterial throughout — a warning interacting with nothing — so it is witnessed
at @`1.2.1.2` and not drawn elsewhere.

Renumbering is this use case's goal rather than a step toward one, so its report is part of what was asked
for: every failing leaf below is an extension because it delivers no renumbered document, and the warning
at @`1.2.1.2` is not one.

* 1 - **document:** `readable-writable`
  * 1.1 - **reference-resolution:** `none-present`
    * 1.1.1 - **first-sibling-number:** `absent`
      > *pruned, immaterial:* the hidden-`0` rule is witnessed at @`1.2.1.2` and does not vary with
      > **reference-resolution**
    * 1.1.2 - **first-sibling-number:** `present`
      * 1.1.2.1 - **figure:** `absent`
        > **Establishes:** renumbered from position, visible from `1`; nothing to rewrite
        >
        > **Payload:** [`shared-pseudo-number.before`](../fixtures/shared-pseudo-number/before.md)
        >
        > **Result:** [`shared-pseudo-number.after`](../fixtures/shared-pseudo-number/after.md)
        >
        > **Stdout:** `shared-pseudo-number.change-report` — [txt](../fixtures/shared-pseudo-number/change-report.txt)
        > · [json](../fixtures/shared-pseudo-number/change-report.json)
      * 1.1.2.2 - **figure:** `present`
        > *pruned, immaterial:* adds a figure only
  * 1.2 - **reference-resolution:** `all-resolve`
    * 1.2.1 - **first-sibling-number:** `absent`
      * 1.2.1.1 - **figure:** `absent`
        * 1.2.1.1.1 - **local-target:** `resolves-here`
          > **Establishes:** the `§` in the local target's link text follows it to the target's new id
          >
          > **Payload:** [`relative-target.before`](../fixtures/relative-target/before.md)
          >
          > **local-target:** [`relative-target.layout-resolves-here`](../fixtures/relative-target/layout-resolves-here.md)
          >
          > **Result:** [`relative-target.after-resolves-here`](../fixtures/relative-target/after-resolves-here.md)
          >
          > **Stdout:** `relative-target.change-report-resolves-here` —
          > [txt](../fixtures/relative-target/change-report-resolves-here.txt)
          > · [json](../fixtures/relative-target/change-report-resolves-here.json)
        * 1.2.1.1.2 - **local-target:** `resolves-elsewhere`
          > **Establishes:** the same payload, that `§` left exactly as written
          >
          > **Payload:** [`relative-target.before`](../fixtures/relative-target/before.md)
          >
          > **local-target:** [`relative-target.layout-resolves-elsewhere`](../fixtures/relative-target/layout-resolves-elsewhere.md)
          >
          > **Result:** [`relative-target.after-resolves-elsewhere`](../fixtures/relative-target/after-resolves-elsewhere.md)
          >
          > **Stdout:** `relative-target.change-report-resolves-elsewhere` —
          > [txt](../fixtures/relative-target/change-report-resolves-elsewhere.txt)
          > · [json](../fixtures/relative-target/change-report-resolves-elsewhere.json)
      * 1.2.1.2 - **figure:** `present`
        > **Establishes:** renumbered; first section hidden `0`; the figure renumbered `M.N.a`; every
        > reference rewritten to its target's new id; one unresolved link text warned about — **the main
        > success scenario**
        >
        > **Witnesses:** **unresolved-link-text** `present` — immaterial everywhere, so witnessed only here
        >
        > **Witnesses:** *`Context` is excluded at any depth* (§5), by nesting one under `Using The Store`
        > and leaving `Errors` as the first subsection
        >
        > **Witnesses:** *`Appendix` and `Rationale` are regions, numbered and addressed as such* (§5) —
        > the body reaches `1.1`, the `Appendix` runs `1`, `2`, the `Rationale` starts again at `1`, and a
        > body reference `§Appendix.5` follows the appendix to `§Appendix.1`
        >
        > **Witnesses:** *`Context`, `Appendix` and `Rationale` match case-insensitively* (§5), by writing
        > `# Appendix` conventionally and `# rationale` in lower case beside it
        >
        > **Witnesses:** *Link text follows its target* (§5), in all three path forms on adjacent lines
        >
        > **Witnesses:** *Non-reference text is untouchable* (§5)
        >
        > **Payload:** [`mixed-numbering.before`](../fixtures/mixed-numbering/before.md)
        >
        > **Result:** [`mixed-numbering.after`](../fixtures/mixed-numbering/after.md)
        >
        > **Stdout:** `mixed-numbering.change-report` — [txt](../fixtures/mixed-numbering/change-report.txt)
        > · [json](../fixtures/mixed-numbering/change-report.json)
    * 1.2.2 - **first-sibling-number:** `present`
      * 1.2.2.1 - **figure:** `absent`
        > **Establishes:** as @`1.2.1.2` without the hidden first section or the figure. Kept rather than
        > pruned because the two reference forms resolve by different keys, and both must be witnessed
        > resolving as well as failing.
        >
        > **Witnesses:** *A bare anchor is internal* (§5) — the one reference form that needs nothing
        > resolved
        >
        > **Payload:** [`anchor-disambiguated.before`](../fixtures/anchor-disambiguated/before.md)
        >
        > **Result:** [`anchor-disambiguated.after`](../fixtures/anchor-disambiguated/after.md)
        >
        > **Stdout:** `anchor-disambiguated.change-report` — [txt](../fixtures/anchor-disambiguated/change-report.txt)
        > · [json](../fixtures/anchor-disambiguated/change-report.json)
      * 1.2.2.2 - **figure:** `present`
        > *pruned, immaterial:* adds a figure only
  * 1.3 - **reference-resolution:** `some-dangling`
    > Leaf; the run stops before numbering.
    >
    > **Establishes:** nothing renumbered, nothing written; the report names the reference and says nothing
    > in the document carries that number — **extension 1a**
    >
    > **Payload:** [`dangling-reference.before`](../fixtures/dangling-reference/before.md)
    >
    > **Result:** none — the document is left exactly as it arrived
    >
    > **Stdout:** `dangling-reference.error-report` — [txt](../fixtures/dangling-reference/error-report.txt)
    > · [json](../fixtures/dangling-reference/error-report.json)
  * 1.4 - **reference-resolution:** `some-ambiguous`
    > Leaf; the run stops before numbering.
    >
    > **Establishes:** nothing renumbered, nothing written; the report names the reference and every heading
    > carrying its identity — **extension 1b**
    >
    > **Payload:** [`ambiguous-reference.before`](../fixtures/ambiguous-reference/before.md)
    >
    > **Result:** none — the document is left exactly as it arrived
    >
    > **Stdout:** `ambiguous-reference.error-report` — [txt](../fixtures/ambiguous-reference/error-report.txt)
    > · [json](../fixtures/ambiguous-reference/error-report.json)
* 2 - **document:** `absent`
  > Leaf; the run stops before reading.
  >
  > **Establishes:** nothing written; the report names the path and says nothing was found there —
  > **extension 1c**
  >
  > **Payload:** none — there is no document to carry one
  >
  > **document:** [`document-absent.layout`](../fixtures/document-absent/layout.md)
  >
  > **Result:** none — nothing was read, so nothing is written
  >
  > **Stdout:** `document-absent.error-report` — [txt](../fixtures/document-absent/error-report.txt)
  > · [json](../fixtures/document-absent/error-report.json)
* 3 - **document:** `not-writable`
  > Leaf; the run stops before reading.
  >
  > **Establishes:** nothing written; the report says the document was read and can be renumbered, so the
  > fault is the file's and not the prose's — **extension 1d**
  >
  > **Payload:** [`mixed-numbering.before`](../fixtures/mixed-numbering/before.md) — the main scenario's
  > own, reused because nothing about the document is at fault
  >
  > **document:** [`document-not-writable.layout`](../fixtures/document-not-writable/layout.md)
  >
  > **Result:** none — the store would not accept one
  >
  > **Stdout:** `document-not-writable.error-report` — [txt](../fixtures/document-not-writable/error-report.txt)
  > · [json](../fixtures/document-not-writable/error-report.json)

## 7 Coverage

Eight leaves survive pruning, each with exactly one payload fixture where it has a payload at all.

Every value of every dimension is still exposed by a kept leaf: **first-sibling-number** `absent` at
@`1.2.1.2` and `present` at @`1.1.2.1`; **figure** `present` at @`1.2.1.2` and `absent` at @`1.1.2.1`; both
values of **local-target** beneath @`1.2.1.1`; all four values of **reference-resolution** and all three of
**document** on the spine. Every invariant in §5 names the leaf that witnesses it, and each of those leaves
names the invariant back — six claims, agreeing from both directions.

* **Leaf @`1.4` carries both routes in one payload** — a `§` token defeated by a duplicated number, an
  anchor defeated only when the titles match too. They are two ways to reach one value, not two values: the
  forms differ in what defeats them and not in what the operation then does. A cell has one payload
  fixture, so a value reached two ways is witnessed by a payload exhibiting both, exactly as
  @`1.2.1.2` does for the three path forms that resolve.
* **Reference form is therefore a route, not a dimension.** It changes what counts as resolvable, which
  looks dimension-shaped, but it changes nothing about the outcome — and a dimension whose values share an
  outcome is two cells that immaterial pruning would collapse back into one. Keeping @`1.2.2.1` beside
  @`1.2.1.2` is the same point from the resolving side: both forms must be seen resolving as well as
  failing.
* **Leaves @`1.2.1.1.1` and @`1.2.1.1.2` are one payload under two dependency states**, and the only pair here that
  cannot be told apart by reading the document. That is what earns **local-target** a dimension rather than an
  invariant: the same input is correct two different ways, and only the tree around it says which.
* **Four of the eight leaves are graceful failures**, and the symmetry is the point: a reference naming
  nothing, a reference naming two things, a path with no document, and a document that cannot be written
  are all conditions the operation cannot resolve and must hand back. Each carries its own message because
  each has its own remedy; none writes anything.
* **Leaves @`2` and @`3` were the enumeration's own finding.** Neither condition appeared anywhere in the use case
  until the dependency's states were written out, and both turned out to be ordinary conditions of being
  invoked against a path. They now fail gracefully with their own messages, which is the whole return on
  enumerating a dependency nobody had thought to enumerate.

# Rationale

**Why `reference-resolution` takes the worst outcome present rather than being split per reference.** A
document has many references and one outcome, and the operation's response is decided by the worst of them:
one ambiguous reference stops the run however many others resolve cleanly. Modelling it per reference would
make the dimension's values neither mutually exclusive nor exhaustive over a document, which is what a
dimension's values have to be.

**Why `document` is a dependency state here at all.** The requirement names it — the operation is invoked
*against a document* — so the store it is read from and written to is part of what the use case describes
rather than something the design will discover later. That is also why its two failure values count as a gap
in the use case rather than an omission from this analysis.

**Why `figure` is a dimension while a heading's depth is not.** A figure is numbered on its own rule, taking
a letter suffix, so a document containing one exercises something a document of headings alone does not.
Depth exercises nothing new: a third-level heading is numbered the same way a second-level one is, with one
more component.
