# 4 — Search The Registry

The condition space of [find-and-read-documentation](../USE-CASE.md) step 4, and the states bracketing it: the
dimensions its fixtures must expose, the invariants they must witness, and the cells they combine into, each
with the state it establishes and the fixture exposing it.

## Context
* [find-and-read-documentation](../USE-CASE.md) - the use case whose step 4 this analyses
* [1 — Register A Path](1-register-a-path.md) - the operation whose Result is this one's entry state; every
  corpus searched here was registered there
* @docs/standards/documentation-standards.md/§4 - Indexing, including the Rationale/Appendix exclusion §5's
  first invariant turns on and the aggregation §3.3 performs at query time

## 1 Dimensions

Every dimension of this operation's condition space, in rank order.

| Rank | Dimension | Category |
|---|---|---|
| 1 | `scope` | payload |
| 2 | `query` | payload |
| 3 | `scope-breadth` | payload |
| 4 | `match-shape` | dependency |
| 5 | `mode` | parameter |
| 6 | `result-limit` | parameter |
| 7 | `report-rendering` | parameter |

**scope** is ranked outermost because one of its two values ends the operation before any searching happens at
all, and **query** next because one of its three ends it with nothing to rank, preview or truncate — as ranked,
each prunes a subtree rather than repeating itself across one. Everything below **query** only means something
once there is a result set to have a shape.

## 2 Payload States

What varies in the operation's own input — the query and the scope the Agent hands over. Projection: `given`.

### 2.1 `scope`

Whether the scope the caller named can be resolved to registered locations at all, before anything is searched.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `resolves` | the scope names one or more locations the registry can find |
| 2 | `unresolvable` | the scope names something the registry has no way to interpret |

Ordinal 2 fails gracefully (§6, extension 4b). It is a different condition from a scope that resolves onto
nothing registered, and from one that resolves onto registered content the query misses — both of those are
ordinary empty results (§2.2), because the scope was right and the answer is simply "nothing here".

### 2.2 `query`

What the query's own terms find in the scope, stated as the outcome across the whole query.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `matches` | every term the query carries is found somewhere in scope |
| 2 | `matches-nothing` | no term is found anywhere in scope |
| 3 | `multi-term-partial` | the query carries several terms; at least one is found and at least one is not |

Ordinal 2 is an empty result and not an error (§6, extension 4a). Ordinal 3 is not a degraded version of
ordinal 1: it is the case that settles what an unmatched term does to a result some other term matched, which
§5's third invariant states and no other cell can show.

### 2.3 `scope-breadth`

How many registered locations the resolved scope covers.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `single-location` | the scope resolves to one registered location |
| 2 | `several-locations` | the scope resolves to more than one, searched together as one ranked set |

### 2.4 How A Scope Is Named Is A Route, Not A Dimension

Each value of **scope-breadth** is reachable two ways, and the operation does the same thing however it got
there — so these are routes, and they earn fixtures rather than cells
([Operation Fixtures §2](@docs/workflows/feature-workflow/operation-fixtures.md)).

`single-location` is reached by naming one location, or by naming no scope at all — in which case the search
runs from where the Agent already is. `several-locations` is reached by naming several, or by the reserved
specifier meaning every location the registry holds. A caller who names nothing and a caller who names their
own current location are asking the same question; so are a caller who lists every location by hand and one who
asks for all of them.

What a scope specifier actually looks like, and how it resolves to a location, is not settled here — that is
§7's first open question (where the registry lives) reaching into its own addressing. What this operation
requires is only that a scope resolves to some set of registered locations, or resolves to nothing at all.

## 3 Dependency States

What the registry presents the operation with. Projection: `given`.

### 3.1 `match-shape`

Where in a matching document the query's terms are found, and therefore how many results that one document
contributes.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `document-only` | the terms appear in the document's own prose but in none of its sections, so the document is the only result it yields |
| 2 | `document-and-section` | the terms appear in at least one section, so that section and the document containing it are both results |

A section and its document are separate results, scored separately and ranked against each other on their own
merits — a document may rank above its own section or below it, and both are addressable.

**A section-only match cannot arise.** A document's own score is computed over its whole prose, its sections
included (§3.3), so a term found in any section is necessarily found in the document too. There is no
combination in which a section matches and its document does not, which is why this dimension has two values
and not three.

### 3.2 What Is Not A Dimension

**How many documents match, and how many locations they are spread across.** Every matching node is scored by
the same rule and ranked in the same set; a second match exercises nothing a first one did not.
**scope-breadth** is a dimension because the entry state genuinely differs — one registered location or several
— not because the count of results does.

### 3.3 Scoring Is A Query-Time Aggregation Over Prose

A score says how well one piece of prose answers the query, measured against that prose's own extent. It is a
property of the text, not of what contains it: the same section scores the same whether it sits in a
twenty-document repository or a two-document one, and whether it was reached by naming its location or by
asking for everything. That is what lets results from several locations be ranked against each other directly
rather than merged from separate rankings (§5).

Two things follow, and both are requirements rather than choices:

* A document's own score aggregates its whole prose, its sections included. Registration records each node's
  words where they textually appear and rolls nothing up (`documentation-standards` §4, which says explicitly
  that aggregation is the search tool's job at query time) — so this operation is where that aggregation
  happens. A document scored over only the prose outside its sections would rank on the length of its own
  title, which is an artifact and not relevance.
* Rationale and appendix prose is not part of any score, because it was never registered (§5).

Which function computes the score is not settled here, and neither are its defaults — see the use case's §7.
What §5's third invariant fixes is the one property of that function this operation actually depends on.

## 4 Parameter Options

The knobs of the invocation itself — same entry state, different call. Projection: `when`.

### 4.1 `mode`

| Ordinal | Value | Means |
|---|---|---|
| 1 | `list` | each result is an addressable reference and its score, and nothing else |
| 2 | `details` | each result additionally carries a short preview of its own opening lines |

`details` exists to make choosing cheap. The Agent's whole problem is that reading a document to find out
whether it was worth reading is the cost it cannot afford (use case §1); a handful of lines per hit either
answers the question outright or points firmly at which reference to fetch, for a fraction of what fetching
several would cost.

### 4.2 `result-limit`

| Ordinal | Value | Means |
|---|---|---|
| 1 | `under-limit` | fewer matches than the caller's limit allows, so every match is returned |
| 2 | `over-limit` | more matches than the limit, so the lowest-scoring are dropped |

Truncation takes the highest-scoring results and drops the rest — it never samples, and never truncates before
scoring. What the default limit is, and how long a preview runs by default, are the use case's §7 to settle.

### 4.3 `report-rendering`

| Ordinal | Value | Means |
|---|---|---|
| 1 | `human` | the results are read by a person |
| 2 | `machine` | the caller declares it will parse the answer |

Both renderings carry the same results in the same order. The machine rendering names every field it has,
present and empty where there is nothing to report, for the reason
[1 — Register A Path](1-register-a-path.md) §4.3 already gives.

## 5 Invariants

What this operation does regardless of any condition.

| Invariant | The rule it defines | Witnessed by |
|---|---|---|
| **No rationale or appendix content is ever returned, whatever the query** | no rationale or appendix section is ever a result, and no preview ever shows their content — their words were never registered, so there is nothing for a query to reach, and a preview of a document stops before them rather than running on | @`1.2.1.1.1` — the corpus carries a document whose `Rationale` and `Appendix` hold the query's own terms, and neither appears among the results |
| **A result carries a reference and a score, never document content** | what a result identifies is where to read, not what is there; the only text search ever returns is a preview the caller asked for, and a preview is a fixed few lines rather than the section it previews | @`1.2.1.1.1` — every result is a reference and a score, and this cell asked for no preview |
| **A term that matches nothing is neutral, never annihilating** | a query term found nowhere lowers no result's standing and removes no result another term matched; it contributes nothing rather than zeroing what its neighbours found | @`1.3` — a two-term query where one term is found and one is not, returning exactly what the found term alone would have |
| **A score is a property of prose, not of its container** | the same prose scores the same however it was reached — whichever location holds it, however many other documents share that location, and whether it was named directly or arrived at by asking for everything | @`1.2.2` — the same document scores identically searched alone and searched alongside a second location, and results from both interleave by score rather than grouping by location |

## 6 Output Fixtures

Every leaf has two further leaves under **report-rendering** — `.1` human and `.2` machine — carrying the same
results and differing only in how they are rendered, so they are not drawn. Both renderings are held concretely
for every leaf.

**This operation has no `Result`.** It writes nothing and changes nothing: the registry it reads is exactly as
it was afterward. Its whole deliverable is what it hands back, which is why every leaf below carries `Stdout`
and no leaf carries anything else. Its entry state is
[1 — Register A Path](1-register-a-path.md)'s own `Result` — the corpus fixtures here are that operation's
registrations, not a second description of the same documents.

Nothing here is **invalid** except the shape §3.1 rules out: a section matching while its document does not
cannot arise. Everything else pruned is **immaterial**: **scope-breadth**, **match-shape**, **mode** and
**result-limit** all collapse under `matches-nothing` and under `unresolvable`, because an empty result and a
failed one have no shape to vary; **match-shape** collapses under `several-locations`, which is exercising how
results from different locations rank together rather than what one document contributes; and **mode** and
**result-limit** are each witnessed once rather than again beneath every value they do not interact with.

An empty result is not an extension — the operation answered the question it was asked, and the answer is that
nothing matches. Only `unresolvable` is an extension, because only there does the Agent have something to fix
before asking again.

* 1 - **scope:** `resolves`
  * 1.1 - **query:** `matches-nothing`
    > Leaf. Everything below **query** *pruned, immaterial:* an empty result has no shape, no preview and
    > nothing to truncate.
    >
    > **Establishes:** an empty result set, reported as such — **extension 4a**
    >
    > **Payload:** [`no-match.query`](../fixtures/no-match/query.md)
    >
    > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md) — the registration
    > [1 — Register A Path](1-register-a-path.md)'s own main success scenario established
    >
    > **Stdout:** `no-match.results` — [txt](../fixtures/no-match/results.txt)
    > · [json](../fixtures/no-match/results.json)
  * 1.2 - **query:** `matches`
    * 1.2.1 - **scope-breadth:** `single-location`
      * 1.2.1.1 - **match-shape:** `document-and-section`
        * 1.2.1.1.1 - **mode:** `list`
          > Leaf. **result-limit** *pruned, immaterial:* truncation is witnessed at @`1.2.1.1.3`.
          >
          > **Establishes:** a section and the document holding it returned as two results, each with its own
          > score, ranked against each other — **the main success scenario**
          >
          > **Witnesses:** *No rationale or appendix content is ever returned* (§5), against a corpus whose
          > excluded zones hold the query's own terms
          >
          > **Witnesses:** *A result carries a reference and a score, never document content* (§5)
          >
          > **Payload:** [`section-and-document.query`](../fixtures/section-and-document/query.md)
          >
          > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
          >
          > **Stdout:** `section-and-document.results` — [txt](../fixtures/section-and-document/results.txt)
          > · [json](../fixtures/section-and-document/results.json)
        * 1.2.1.1.2 - **mode:** `details`
          > Leaf. **result-limit** *pruned, immaterial:* as @`1.2.1.1.1`.
          >
          > **Establishes:** the same results, each carrying a preview of its own opening lines — a section's
          > preview bounded by the section, a document's by the document, and both stopping short of content
          > the preview may not show
          >
          > **Witnesses:** *No rationale or appendix content is ever returned* — the preview half: the
          > document-level preview stops before its `Rationale` rather than running into it
          >
          > **Payload:** [`section-and-document.query-details`](../fixtures/section-and-document/query-details.md)
          >
          > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
          >
          > **Stdout:** `section-and-document.results-details` —
          > [txt](../fixtures/section-and-document/results-details.txt)
          > · [json](../fixtures/section-and-document/results-details.json)
        * 1.2.1.1.3 - **result-limit:** `over-limit`
          > Leaf. **mode** *pruned, immaterial:* what is dropped does not depend on whether what survives
          > carries a preview.
          >
          > **Establishes:** the highest-scoring results kept and the lowest dropped, with the drop counted so
          > the Agent knows the list was cut rather than exhausted
          >
          > **Payload:** [`section-and-document.query-limited`](../fixtures/section-and-document/query-limited.md)
          >
          > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
          >
          > **Stdout:** `section-and-document.results-limited` —
          > [txt](../fixtures/section-and-document/results-limited.txt)
          > · [json](../fixtures/section-and-document/results-limited.json)
      * 1.2.1.2 - **match-shape:** `document-only`
        > Leaf. **mode** and **result-limit** *pruned, immaterial:* as above.
        >
        > **Establishes:** one result for the document and none for any section — the terms are in the
        > document's own prose and in none of its sections, so there is no narrower reference to offer
        >
        > **Payload:** [`document-only.query`](../fixtures/document-only/query.md)
        >
        > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
        >
        > **Stdout:** `document-only.results` — [txt](../fixtures/document-only/results.txt)
        > · [json](../fixtures/document-only/results.json)
    * 1.2.2 - **scope-breadth:** `several-locations`
      > Leaf. **match-shape**, **mode** and **result-limit** *pruned, immaterial:* this cell exercises how
      > results from different locations rank together, which is independent of all three.
      >
      > **Establishes:** one ranked set drawn from two registered locations, interleaved by score rather than
      > grouped by where each hit came from
      >
      > **Witnesses:** *A score is a property of prose, not of its container* (§5) — a document appearing in
      > both this cell and @`1.2.1.1.1` carries the identical score in each
      >
      > **Payload:** [`several-locations.query`](../fixtures/several-locations/query.md)
      >
      > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md) and
      > [`nested-directory.registered-recursed`](../fixtures/nested-directory/registered-recursed.md) — two
      > registrations operation 1 established separately, searched together here
      >
      > **Stdout:** `several-locations.results` — [txt](../fixtures/several-locations/results.txt)
      > · [json](../fixtures/several-locations/results.json)
  * 1.3 - **query:** `multi-term-partial`
    > Leaf. Everything below *pruned, immaterial:* what an unmatched term does is independent of breadth,
    > shape, mode and limit.
    >
    > **Establishes:** the results the matched term alone would have produced, unchanged — the unmatched term
    > removes nothing and lowers nothing
    >
    > **Witnesses:** *A term that matches nothing is neutral, never annihilating* (§5)
    >
    > **Payload:** [`partial-match.query`](../fixtures/partial-match/query.md)
    >
    > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
    >
    > **Stdout:** `partial-match.results` — [txt](../fixtures/partial-match/results.txt)
    > · [json](../fixtures/partial-match/results.json)
* 2 - **scope:** `unresolvable`
  > Leaf; the run stops before any searching.
  >
  > **Establishes:** nothing searched; the report names the scope and says it could not be resolved —
  > **extension 4b**
  >
  > **Payload:** [`unresolvable-scope.query`](../fixtures/unresolvable-scope/query.md)
  >
  > **Stdout:** `unresolvable-scope.error-report` —
  > [txt](../fixtures/unresolvable-scope/error-report.txt)
  > · [json](../fixtures/unresolvable-scope/error-report.json)

## 7 Coverage

Eight leaves survive pruning, each with exactly one payload fixture.

Every value of every dimension is still exposed by a kept leaf: both values of **scope** at @`1` and @`2`; all
three of **query** at @`1.1`, @`1.2` and @`1.3`; both values of **scope-breadth** at @`1.2.1` and @`1.2.2`;
both values of **match-shape** at @`1.2.1.1` and @`1.2.1.2`; both values of **mode** at @`1.2.1.1.1` and
@`1.2.1.1.2`; both values of **result-limit** at @`1.2.1.1.1` and @`1.2.1.1.3`. Every invariant in §5 names the
leaf that witnesses it, and each of those leaves names the invariant back — four claims, agreeing from both
directions.

* **Every corpus here was registered by operation 1, not described again.** The `registry` line on each leaf
  points at that operation's own `Result`, which is what makes these two operations one chain rather than two
  analyses of the same documents. A search fixture that restated what is registered could drift from it; one
  that references it cannot.
* **@`1.2.1.2` is the only cell that proves a document is addressable on its own.** Every other matching cell
  yields a section too, and a reader could otherwise take the document-level result to be an artifact of having
  a section beneath it rather than a result in its own right.
* **@`1.2.2` reuses a corpus rather than inventing a second one**, for the same reason its invariant needs: the
  claim is that a document's score does not move when the scope around it widens, and that is only checkable if
  the document is literally the same one, with the same registration, in both cells.
* **Two ways of naming a scope reach each of @`1.2.1` and @`1.2.2`.** Each carries a second payload fixture
  rather than a second cell (§2.4) — naming nothing beside naming one location, and asking for everything
  beside naming several.
* **Nothing here is read from the corpus except previews.** Every other result is answered from what
  registration recorded. That is the whole reason this operation can rank a repository the Agent has never
  opened, and the reason a preview is capped rather than complete.

# Rationale

**Why an unresolvable scope fails while an empty scope does not.** Both hand the Agent nothing, and the
difference is what it should do next. A scope that resolved onto nothing registered, or onto content the terms
missed, is an answer: the Agent re-queries, widens, or accepts that the documentation does not cover this. A
scope the registry cannot interpret is not an answer at all — nothing was searched, and re-querying would fail
the same way forever. Reporting them alike would leave the Agent retrying terms against a scope that was never
going to work.

**Why `multi-term-partial` is a value of `query` rather than an invariant on its own.** The rule it exercises
is an invariant — an unmatched term is neutral — but a rule about what happens when a term fails needs a query
where a term fails, and no other value of this dimension has one. `matches` has every term found by
definition, and `matches-nothing` has none found, so neither can show a term failing beside a term succeeding.

**Why the score is required to be about prose and not about its container.** This is the one property of the
relevance function this operation actually rests on, and it is what makes searching several locations a single
question rather than several. If a score encoded anything about the document or the repository around a piece
of prose, results from different locations could only be ranked by merging separate lists, and the Agent would
have to reason about where a result came from before it could judge whether the result was any good. Requiring
a self-contained score is what keeps `several-locations` from needing a different answer than
`single-location`.

**Why a bare product across terms is ruled out.** §5's third invariant is not a preference about tie-breaking,
it is a constraint on the shape of any function that may be chosen: a term matching nowhere must contribute
nothing rather than annihilate. Multiplying per-term scores would make one absent term zero a result that
another term matched strongly, which is exactly the outcome the invariant forbids. Everything else about the
function — how coverage across several terms weighs against frequency within one, phrases, negation,
conjunction — is left open.

**Why the old design's document-level scoring is not carried forward.** Its worked behaviours scored a
document against only the prose outside its sections, which made a short title dominate: a document scored
`0.5` on a two-word root while its own longer, richer section scored `0.333`. That ranks documents by how
little text sits above their first heading. It is corrected here rather than raised elsewhere because that
design is the thing this analysis exists to replace — it was never pressure-tested, and finding this is what
the exercise is for.

**Why `details` is a mode rather than a separate operation.** It answers the same question against the same
entry state and returns the same results in the same order; what changes is how much of each one the caller
asked to see. Splitting it out would duplicate every cell above it to say nothing new, and would invite a
design where the two can disagree about what matched.
