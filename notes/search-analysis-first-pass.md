<!--
NOT A LIVE DOCUMENT. Kept for the fixture types, their aspects and their example
fixtures, which are correct, and for the invariants, which are largely reusable.

Withdrawn from `operations/4-search-the-registry.md` on 2026-09-18 because most of
it analyses the solution rather than the behaviour. A use case operation may only
model the fixtures that cross its own step's boundary and the perceived state of
the other side of it. The Agent perceives the difference between the registry it
is standing in and one it named; it does not perceive a filesystem walk, a
configuration file, a registry root marker, or that a registry must be registered
before it can be searched. Registry Register, Registry Search, Registry Report and
Filesystem are all of them how, not what.

What survives the move: the Query fixture and its aspects, the Results and Failure
fixtures and theirs, the invariants over those, and the worked renderings.
-->

---
analysis_lock:
  aspects:
    own: "02a75ecfc8d170b5c402c29c42a04057e8b6e046fe51f072d60372de06d8a1d3"
  invariants:
    own: "f48521b13173e9eab02641df2ada31bf119fc3c7f937afa18d68a5f7f2883b76"
    composite: "fc4f5d78fbcc5df8c72f58932610d67fb5d494686b601153c7907d2182c32ca9"
  dimensions:
    own: "8d1aa298962fbb839e175b512c76332b44101b1861f302195be44c637fb78b72"
    composite: "d7b5d50440a682e521bcdaa2ef4ac842d7342b761df217e01fefebfe596c26ff"
  immaterial_rules:
    own: null
    composite: null
  orthogonal_rules:
    own: null
    composite: null
---
# 4 — Search The Registry

The condition space of [find-and-read-documentation](../USE-CASE.md) step 4, and the states bracketing it: the
dimensions its fixtures must expose, the invariants they must witness, and the cells they combine into, each
with the state it establishes and the fixture exposing it.

## Context
* [find-and-read-documentation](../USE-CASE.md) - the use case whose step 4 this analyses
* [1 — Register A Path](1-register-a-path.md) - the operation whose Result is this one's entry state; every
  corpus searched here was registered there
* [WeaverDocs Architecture](../../../architecture/weaverdocs/ARCHITECTURE.md) - §1.6 and §2.3, the registry
  boundary this operation crosses and the two implementations behind it
* @docs/standards/documentation-standards.md/§5 - Indexing, including the Rationale/Appendix exclusion §2's
  first invariant turns on and the aggregation §5.5 performs at query time

## 1 Fixtures And Their Aspects

> What the operation's fixtures are, and what separable parts each carries. Sketch each type in the section
> that describes it, and name its aspects as nested bullets — an aspect sits inside the one it is part of.
> Nothing here names a dimension: the aspects are what exist, and §3 is where what varies them is found.
> Claim here that the aspects are independent of one another; §9 is where that claim is paid for.

What this operation's fixtures are, and what separable parts each carries.

**These aspects are claimed to be independent of one another.** Whether a preview names what it withheld turns
on whether there is a preview at all and whether the content ran past its length. It does not turn on whether
the hit was a document or a section, on whether the list around it was cut, or on which encoding it was
written in — and the same holds the other way: the list overflow answers to the cap and not to previewing, the
ancestry block to the kind of match and to nothing beneath it.

### 1.1 The Fixture Types

> One row per artefact the operation is given or hands back. A dependency on a boundary is a crossing rather
> than a store: each distinct call is its own type, carrying **the call** and **the answer** as its two halves.
> Output the operation delivers and output it fails with are separate types, not one type with two moods.

| Fixture | Role | What it is | Sketched and broken down in |
|---|---|---|---|
| **Query** | payload | one invocation: what was searched for, where, and with which parameters | §1.2 |
| **Filesystem** | dependency | the locations the operation can reach before it can search anything: the configuration it finds among them, and the registry root it is standing in | §1.3 |
| **Registry Register** | dependency | one crossing that establishes an ambient registry before it is searched: the call, and what it did or could not establish | §1.4 |
| **Registry Search** | dependency | one crossing of the registry boundary: the call, and the matches it answers with | §1.5 |
| **Registry Report** | dependency | one crossing for one result's content: the call, its bound, and the content it answers with | §1.6 |
| **Results** | stdout | what came back when the operation delivered | §1.7 |
| **Failure** | stdout | what came back when it did not | §1.8 |

This operation does not read a corpus; it calls a boundary and is answered. The registry's own contents are
upstream of that: they are [1 — Register A Path](1-register-a-path.md)'s `Result`, which is this operation's
entry state, and what a search answer is, is that state seen through the boundary.

`search` is made once per registry in scope and returns no content; `report` is made once per surviving result
and returns nothing else (§1.6). A run may make the first and never the second.

`Results` and `Failure` share no aspect: a failure names the scope it could not resolve and why, and carries
no rows, no ancestry, no previews and no counts. Which of them a run produces is decided before anything is
searched, by whether the scope named resolves at all.

A malformed `.weaverdocs.yaml` does not make a second type of `Filesystem`: it keeps the whole spine — still a
path, with permissions, pointing at a file — and loses only its `registries`. An empty result is likewise a
`Results` and not a `Failure`; nothing matched, but the operation answered the question it was asked.

### 1.2 `Query` Fixtures

One invocation. A plain one — terms and a scope, every parameter unset. The form is the CLI's, taken from
`ARCHITECTURE.md` §2.3:

```
weaverdoc search "eviction policy" --scope @AgentPlugins
```

The same search asking for previews, a smaller list and longer previews, encoded for a parser:

```
weaverdoc search "eviction policy" --scope @ALL --details --max-results 2 --preview-lines 4 --json
```

Its aspects are siblings — a command line has no nesting — though what one of them means can depend on
another: a length flag bounds a preview only where a mode flag asked for previews at all.

#### 1.2.1 `Query` Aspects

* **terms:** - what is being searched for
* **scope specifier:** - which registries to search — one, several, or all of them
* **mode flag:** - whether previews are wanted
* **cap flag:** - how many results the caller will take
* **length flag:** - how much of each hit the caller will be shown
* **encoding flag:** - whether the answer is for a person or a parser

Every parameter is a flag a caller may or may not set, so each of these aspects has an unset form — four of
the six are unset in the first invocation above. A scope specifier may name one registry, several, every one
the configuration holds, or none at all; all four are the same aspect written differently.

### 1.3 `Filesystem` Fixtures

What the operation can reach before it can search anything, and the walk up from the working directory finds
two different things on it (`ARCHITECTURE.md` §1.1). A `.weaverdocs.yaml` says which registries exist and
where they live, which is what a named scope resolves against. A `.git/` marks a **registry root** — the
repository the working directory is inside — which is what a search with no scope resolves to. The two are
independent: a clone or a worktree of a registered repository is a registry root and is not the registered
registry, and searching it is a different question from searching the one it came from.

A walk that finds both:

```
/Users/simon/weaver-engineering/AgentPlugins/agent-plugins-docs/.git   the registry root, found here
/Users/simon/weaver-engineering/AgentPlugins/agent-plugins-docs        the working directory
/Users/simon/weaver-engineering/AgentPlugins
/Users/simon/weaver-engineering/.weaverdocs.yaml                       the configuration, found here
/Users/simon
```

The registry root is found at the working directory here, and the configuration two levels above it. Neither
stops the other: the walk runs until it has a configuration or runs out, noting the nearest root on the way.

```yaml
registries:
  AgentPlugins: /Users/simon/weaver-engineering/AgentPlugins
  TheLoom: /Users/simon/weaver-engineering/TheLoom
```

`.git/` is taken as the registry-root marker because it is the only one this design has a case for. If that
changes, this behaviour is revisited rather than quietly extended.

**A map keyed by slug, not a list of entries.** A scope specifier resolves a slug, so the slug is the key, and
keying it makes a slug naming two locations unwriteable rather than merely wrong. What a map cannot rule out is
the other duplication — two slugs on one location (§2).

**The paths are flat, not nested.** A directory's contents are not an aspect of that directory here, because
descending one changes nothing this operation does: the only filesystem fact its behaviour turns on is what
each path it touches points at.

An ambient registry is reached through the registry boundary (§1.5, §1.6), as a configured one is — the
operation does not touch the `.index/` behind either. What differs is only what draws that boundary: a
configured registry is drawn by the configuration, an ambient one by the root the walk found. Whether an
indexation is already sitting behind it changes nothing, because it cannot be trusted however recent it
looks and is established either way — so it is neither sketched above nor an aspect below.

#### 1.3.1 `Filesystem` Aspects

* **paths:** - which locations the operation touches at all: the walk up from the working directory, and then
  the locations the configuration it found names
  * **whether it can be read:** - a location may exist and still refuse to be opened
  * **what it points at:** - nothing, a directory, or a file
* **the configuration:** - the `.weaverdocs.yaml` the walk found, if it found one
  * **registries:** - the places a named scope can resolve to
    * **slug:** - the key: the name a scope specifier can use for one
    * **path:** - the location it lives at, which is one of the paths above
* **the ambient registry:** - the registry root the walk found at or above the working directory, if there was
  one

**Which locations there are and what each holds are two aspects, not one**, which is why `paths` is the set and
the two beneath it are of each member. The walk's own extent belongs to the set: it stops at the first
configuration it finds, so which locations are touched at all is a fact about the walk rather than about any
location on it.

The configuration is a sibling of the paths rather than nested beneath the one that held it. Its content is
the same whatever the walk it was reached by, so nesting it under a particular path would say the walk mattered
to what it contains, which it does not.

### 1.4 `Registry Register` Fixtures

A local search cannot be answered until the registry it is standing in has been established, so it crosses the
boundary a third time before it searches anything. The crossing is made only for a local search: a named scope
reaches registries somebody else has already registered, and this operation does not touch them.

```
registry.register("/Users/simon/weaver-engineering/AgentPlugins/agent-plugins-docs")
```
```yaml
registered: 34
dropped: 2
unreadable:
  - path: "…/docs/design/notes/private.md"
    reason: "permission denied"
```

What comes back is not a report for a person to read — this run is incidental to the search that provoked it,
and its own report belongs to [1 — Register A Path](1-register-a-path.md). What this operation needs from it
is narrower: whether what it established can be searched, and what, if anything, it could not.

#### 1.4.1 `Registry Register` Aspects

* **the call:** - what was asked of the boundary, once, and only for a local search
  * **whether it is made at all:** - the crossing happens only where no scope was named
  * **the root named:** - the location to be established, which is the registry root the walk found
* **the answer:** - what the registration established, and what it did not
  * **what it established:** - the registrations a search over that root is then answered from
  * **what it could not:** - whatever the registration failed to establish, which is the difference between a
    search that can be trusted and one that cannot

A registration that partly succeeded is the case this fixture exists for. A run that establishes most of a
root and quietly drops the rest would answer a search from an index it has no reason to trust, and would look
exactly like one that succeeded.

### 1.5 `Registry Search` Fixtures

A `Registry` is a **boundary**, not a store. The same operations cross it whether what lies behind is the local
filesystem registry or a hosted enterprise one, and this operation is defined against the boundary rather than
either implementation (`ARCHITECTURE.md` §1.6). A scope resolves to a *set* of registries, and `search` is
called once against each, their answers ranked together afterwards.

The call carries the terms and a cap. What comes back is matches and no content at all:

```
registry.search("eviction policy", max-results: 2)
```
```yaml
matched: 14
matches:
- reference: "/docs/policies/eviction-policy"
  type: document
  title: "Company Eviction Policy"
  relevance: 0.6
  wordCount: 200
  document: { path: "…/policies/eviction-policy.md", title: "Company Eviction Policy", wordCount: 200 }
- reference: "/docs/procedures/eviction-procedures$2.1"
  type: section
  title: "Cache Eviction"
  relevance: 0.3
  wordCount: 50
  document:
    path: "…/procedures/eviction-procedures.md"
    title: "Eviction Procedures"
    wordCount: 150
    section: { number: "2", title: "Policies", wordCount: 80,
               section: { number: "2.1", title: "Cache Eviction", wordCount: 30 } }
```

A document match carries its own row and nothing beneath it; a section match carries the chain down to it,
each level with its own word count. The two kinds of match are not two shapes of the same row: one is a
reference, the other is a reference and the chain that places it.

The call and the answer are one fixture with two halves, and the aspects of the answer nest, because a match
is a thing with parts:

**The answer has to carry the total, and the sketched `Match[]` did not.** *A truncated list names what it did
not show* (§2) needs a number this operation cannot compute: having asked for two and been given two, nothing
in a bare list of matches says whether there was a third or a thirtieth. The count is a fact only the registry
holds, so the boundary has to hand it over — the sketch above now does, as `matched`, alongside the capped
`matches`.

#### 1.5.1 `Registry Search` Aspects

* **the call:** - what was asked of the boundary
  * **the registries called:** - one call per registry the specifier resolved to, or none at all where it
    resolved to nothing the registry knows
  * **the cap passed:** - the number of matches the call is willing to be answered with
* **the answer:** - the matches, and nothing of their content
  * **whether anything matched:** - whether the terms appear anywhere in scope
  * **the matches handed back:** - how many came back, which is as many as the call would take
  * **how many matched in all:** - the number the registry found, against the number it handed back
  * **a match:** - one matching node, and whether it is a document or a section within one
    * **its ancestry:** - for a section, the document and every section above it, each with its own word count

The cap the call passed and the overflow the answer came back with are separate facts: one is a number the
caller chose, the other is what happened to be there, and neither can be read off the other.

### 1.6 `Registry Report` Fixtures

**A preview is a second crossing, not part of the first.** Where the caller asked for details, the operation
calls `report` once per surviving result, bounded to the preview length — and where it did not, it makes no
such call at all (`ARCHITECTURE.md` §2.3's own sequence). That is why previewing cannot change which results
there are, and why truncation necessarily settles before any preview is fetched: there is nothing to preview
until the list is known.

The call carries one reference and a line bound. What comes back is that node's verbatim content, and only
that node's:

```
registry.report("/docs/procedures/eviction-procedures$2.1", to: 4)
```
```yaml
reference: "/docs/procedures/eviction-procedures$2.1"
type: section
parameters: { to: 4 }
lineCount: 9
content: |
  Blah blah blah evict
  Blah blah policy
  Blady blah blah
  Blah blah blah
```

**The same hole, in the same place, for the same reason.** *A preview names what it did not show* (§2) needs
the count of lines withheld, and a call bounded to four that comes back with four says nothing about whether a
fifth exists. `lineCount` in the sketch above is the node's own extent, which is what makes `... (5 more
lines)` computable. It is the same requirement the search answer carries: **a bounded answer must disclose
what the bound cost.**

A whole fixture of this type can be absent from a run: asking for previews or not decides first whether this
crossing happens at all, and what a preview looks like where it printed follows from that.

This crossing is also the only place the operation reads the corpus. Everything else it prints is answered from
what registration recorded, which is what lets it rank a repository nobody opened.

#### 1.6.1 `Registry Report` Aspects

* **the call:** - what was asked of the boundary, once per surviving result
  * **whether it is made at all:** - the crossing happens only where previews were asked for
  * **the bound passed:** - how many of the node's lines the call is willing to be answered with
* **the answer:** - that node's own opening lines, verbatim
  * **the lines handed back:** - as many of the node's opening lines as the call would take
  * **how many lines the node holds in all:** - the extent of the node, against the number it handed back

### 1.7 `Results` Fixtures

A `Results` fixture is not one indivisible thing. It is several separable parts, and a single fixture shows
many of them at once.

The first query of §1.2, in the human encoding — rows and ancestry only:

```
registered locations searched:
  @AgentPlugins

@AgentPlugins/docs/policies/eviction-policy            - 0.6 over 200 words
  - Company Eviction Policy
@AgentPlugins/docs/procedures/eviction-procedures$2.1  - 0.3 over 50 words
  - Eviction Procedures - 150 words
    - 2 Policies - 80 words
      - 2.1 Cache Eviction
```

The second, across two registries, with previews, a cut list and a cut preview:

```
registered locations searched:
  @AgentPlugins
  @TheLoom

@AgentPlugins/docs/policies/eviction-policy            - 0.6 over 200 words
  - Company Eviction Policy
@AgentPlugins/docs/procedures/eviction-procedures$2.1  - 0.3 over 50 words
  - Eviction Procedures - 150 words
    - 2 Policies - 80 words
      - 2.1 Cache Eviction
  Blah blah blah evict
  Blah blah policy
  Blady blah blah
  ... (5 more lines)

... (12 more matches)
```

The aspects nest, and the nesting is the artefact's own shape — the second sketch read as a structure:

#### 1.7.1 `Results` Aspects

* **result set:** - results, or an empty answer that is not an error
  * **searched locations:** - the registries the scope resolved to, named back
  * **result rows:** - one per matching node — its scope-qualified reference, its relevance and the word count
    that relevance was measured against — as many as the cap admits
    * **ancestry block:** - the document's title, and for a section match every section above it with its
      number, title and word count
    * **preview block:** - the opening lines of that hit's own content, fetched by `report` and as many as the
      length admits
      * **preview overflow:** - the count closing a preview that was cut — `... (5 more lines)`
  * **list overflow:** - the count closing a list that was cut — `... (12 more matches)`
* **warning:** - something the run noticed that did not stop it — a parameter that could not be used, a
  configuration worth remarking on — reported beside the results rather than instead of them
* **encoding:** - whether all of the above is written as prose for a person or as a document for a parser; it
  wraps the artefact rather than sitting anywhere inside it, and contains nothing

Nine aspects, and the second sketch shows all but the warning at once.

**The ancestry block is where the two kinds of match part company.** A document match carries its title and
nothing more; a section match carries the document and the whole chain down to it, each level with its own
word count. That is not decoration: a section returned on its own is prose without a home, and the chain is
what tells the Agent where the words it is about to fetch actually sit.

### 1.8 `Failure` Fixtures

What comes back when the scope names something the registry cannot resolve. Nothing was searched, so there is
nothing to report about what was found.

A scope the configuration cannot resolve — no `weaverdocs.yaml` above the working directory, or a slug that is
not one of its entries:

```
weaverdoc search "eviction policy" --scope @NoSuchProject
```

```
failed - scope unresolvable
nothing searched

scope
- @NoSuchProject - not a registry this configuration knows

remedy
- check the scope name, or the weaverdocs.yaml it should be registered in
```

#### 1.8.1 `Failure` Aspects

* **the scope named:** - the specifier as the caller gave it, so they can see what was not understood
* **the reason:** - that it could not be resolved, as against resolving onto nothing registered
* **encoding:** - whether both of the above are written as prose for a person or as a document for a parser;
  it wraps the artefact rather than sitting anywhere inside it, and contains nothing

Nothing of §1.7's nesting appears here — no rows, no ancestry, no counts — because this is a different
artefact and not an emptier one. What the caller named and why it was not understood are the whole of what
this type contains; the third aspect says only how those two are written down, exactly as it does for a
`Results`.

## 2 Invariants

> What the operation does that does not vary. An invariant is a feature of an aspect, so it belongs to the one
> fixture type that aspect is part of, and the sections below are grouped accordingly. **Invariants are
> conditional**: one holds regardless of anything varying *inside* its region, not regardless of everything.
> That region is **the aspect it names**, and it is asserted wherever that aspect is present. Which cells
> those are follows from §1's nesting and needs no naming here, which is why an invariant names no dimension
> and this section can be read before §3 — or before any tree is drawn. Every fixture carrying the aspect
> checks the invariant, and that is what constrains the behaviour to be invariant. Which cell *witnesses* each
> one is a fact about the tree and is recorded with the tree, in §9.

What this operation does that does not vary.

### 2.1 `Filesystem`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **The walk goes up and never down** | from the working directory toward the root, and never into anything beneath it. Neither a `.weaverdocs.yaml` nor a `.git/` below the working directory is found, and neither is meant to be: the walk's extent has to be decidable from the working directory alone, or two runs in the same place could search different things | paths |
| **The nearest configuration wins outright** | the walk stops at the first `.weaverdocs.yaml` it finds; one further up is shadowed and never merged into it. Merging would make the set of available registries depend on how deep the working directory happens to sit, which is the one thing the walk must not do | the configuration |
| **A location that cannot be read is never reported as absent** | the two hand the operation the same nothing and need different remedies — fix a permission against fix a path — which is the same distinction the use case draws at its own extensions 1b and 1c | paths / whether it can be read |
| **A named scope resolves only against the configuration** | nothing outside it is reachable by naming, which is what makes `@ALL` definite and an unknown slug unresolvable rather than empty. The ambient registry is reached by naming no scope at all and by nothing else — it has no slug, so no specifier can ask for it | the configuration / registries |
| **A slug names exactly one location** | a scope specifier resolves to one location or to none, never ambiguously to several. Keying the configuration by slug is what makes this structural rather than checked — and a parser that silently takes the last of two identical keys has reintroduced the ambiguity the key was meant to remove | the configuration / registries / slug |
| **A configured registry always has a path** | an entry with a slug and nothing against it is not a registry that resolves to nowhere, it is a configuration that cannot be used. A key with no value is the one shape a map makes easy to write by accident | the configuration / registries |
| **A location configured under several slugs is searched once, and said so** | two slugs may name one location, which no key can prevent. Searching it per slug would return every match as many times as it was configured, and ranking would interleave a result with itself. The run searches it once and warns, which costs nothing: the duplicate is visible from the configuration before anything is searched | the configuration / registries / path |
| **The nearest registry root wins outright** | the walk takes the first `.git/` it finds and no other. A repository inside a repository — a submodule, a worktree, a vendored clone — is its own registry, and the one containing it is not searched as well. Same reason as the configuration: which registry an unscoped search reaches has to follow from where the caller is standing, not from how far up the tree something else happens to sit | the ambient registry |
| **An ambient registry is reindexed before it is answered from** | whatever indexation is already there says nothing about how stale it is, and nothing on the filesystem can be asked. Reindexing is mechanical and idempotent, so it costs a run rather than a decision — and an index taken on trust is the one way a search can report nothing and be wrong about it | the ambient registry |
| **A search that cannot trust its index fails rather than answering** | where the reindex does not complete, no result set comes back — not a partial one, and not one that hopes. An answer drawn from an index the run could not establish is indistinguishable from an answer drawn from a good one, which is exactly what makes it unusable | the ambient registry |

### 2.2 `Registry Register`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A register answer states what it could not establish** | never only what it did. A registration that succeeded in part and said nothing would be indistinguishable from one that succeeded entirely, and the search that follows would be answered from an index nobody had reason to trust. It is the same requirement the other two crossings carry, in the one place where the operation is asking for state to be made rather than read | the answer / what it could not |

### 2.3 `Registry Search`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A matched search answers with a reference, a type, a score, a word count and a document** | five things for every match, never four. The reference says what to fetch, the type what kind of node it is, the score how well it matched, the word count what that score was measured against, and the document which file it lives in — a match missing any of them cannot be acted on without another crossing | the answer / a match |
| **A document always provides a path and a word count** | every match carries its document, and every document carries where it is and how big it is. For a whole-document match those are the match's own; for a section match they are the file the section sits in | the answer / a match |
| **A section always provides a number and a word count** | every section in the chain is numbered and measured. The number is what makes it addressable and the word count is what makes its share of the document legible — a chain of titles alone would say where a match sits but not how much of the document it is | the answer / a match / its ancestry |
| **A search answer states how many matched in all** | the count the registry found, alongside the matches it handed back — never only the matches. A capped answer carrying nothing but what survived the cap cannot say how much it withheld, and the operation cannot compute it: how many matched is a fact only the registry holds | the answer / how many matched in all |

### 2.4 `Registry Report`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A matched report answers with a reference, a type, a line count and content** | the reference and type say what was fetched, the line count how much there is of it, and the content is the prose itself — verbatim, never reconstructed from what the registry holds about it | the answer |
| **A report answer states how many lines the node holds** | the node's own extent, alongside the lines within the bound — never only the lines. Asked for four and given four, nothing else in the answer says whether a fifth exists, and a preview that cannot say what it withheld is a teaser rather than a steer | the answer / how many lines the node holds in all |

### 2.5 `Results`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A result set names every location it searched, by slug where it has one and by path where it does not** | the run always knows which registries it searched and always says so, whether anything was found in them or not. A configured registry is named by its slug because that is what identifies it; an ambient registry has no slug (§2.1), so its full path is what there is. An empty answer that did not say where it looked is indistinguishable from one that looked in the wrong place | result set / searched locations |
| **No rationale or appendix section is ever a result** | whatever the query, no rationale or appendix section is ever among what search hands back — their words were never registered, so there is nothing there for a query to reach | result set / result rows |
| **A result always carries a reference, a score, and a word count** | every result names what to read, how well it matched, and how much of it there is — the three facts the Agent needs to choose between results without reading any of them. A preview, where one was asked for, is carried in addition to these and never in place of any of them | result set / result rows |
| **A score is a property of prose, not of its container** | the same prose scores the same however it was reached — whichever location holds it, however many other documents share that location, and whether it was named directly or arrived at by asking for everything | result set / result rows |
| **An ancestry block carries the whole chain down to the matched node** | the document, then every section above the match, each with its own word count — complete, never partial, and for a whole-document match that chain is the document alone. It is what lets the Agent judge where the words sit and how much of the document they are before fetching any of them; a narrower result handed back without it would be prose with no home | result set / result rows / ancestry block |
| **No preview ever shows rationale or appendix content** | a preview of a document stops where its excluded zones begin rather than running on into them — and it stops there even when the caller asked for more lines than that leaves, because the exclusion outranks the request. Content that cannot be searched for cannot be read by accident either | result set / result rows / preview block |
| **A preview names what it did not show** | a preview runs to the caller's length and stops; where the content continues past it, the preview states how many lines it withheld, so how much is there is known without fetching it. Content that fits is shown whole, with nothing to state | result set / result rows / preview block |
| **A truncated list names what it did not show** | where more results matched than the caller's limit admits, the list ends in a count of the matches it did not name — so a list that was cut is never mistaken for one that was exhausted, which is the difference between having the answer and having the top of a pile | result set / list overflow |
| **Truncation ranks before it cuts** | the whole matching set is scored and ranked, and only then are the lowest-scoring dropped. It never samples, and never cuts before scoring, so what survives a cap is always the best of what matched rather than the first of it | result set / list overflow |
| **A parameter that cannot apply is reported, never obeyed and never fatal** | the deliverable result comes back in full, with a warning naming the parameter that was not used. Failing would withhold a result over something that changed nothing about it, and silence would leave the caller believing it applied | warning |
| **Both renderings carry the same results in the same order** | the encoding changes how an answer is written down and nothing about what it is: the same results, the same ranking, the same counts. A caller choosing a rendering is choosing a format, never a different question | encoding |
| **The machine rendering names every result field it has** | reference, score, word count, ancestry, preview — present and empty where there is nothing to report, for the reason [1 — Register A Path](1-register-a-path.md) §6.3 already gives: a parser that must distinguish "absent" from "empty" is a parser that breaks on the empty case | encoding |

### 2.6 `Failure`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A failure names the scope and says it could not be resolved** | never reported as nothing found. The two hand the Agent the same emptiness and need different remedies — correct the scope, against re-query or accept that the documentation does not cover this — and only the failure says which | the scope named<br>the reason |
| **Both renderings carry the same failure and the same reason** | a failure encoded for a parser says exactly what the one encoded for a person says. A caller that can read only one of the two must not be told a different story by it | encoding |
| **The machine rendering names every failure field it has** | the scope named and the reason, present and empty on the same terms. A failure is the answer a caller is least able to guess at, so it is the last place to leave a field out | encoding |

## 3 Dimensions

> Found by asking of each aspect in §1 what makes it come out differently. §3.1 collects them and checks them
> against the aspects; §3.2 ranks and categorises the same set once they are all in hand.

Fifteen dimensions, every one of them binary. Each is named as a condition, so that its name followed by
**yes** reads as a true statement and its ordinals need no vocabulary of their own — `max-results-exceeded`
• `yes` says what it means without a table to look it up in.

### 3.1 What Varies, And The Aspects It Varies

> A dimension naming no aspect is not a dimension. An aspect no dimension names means a dimension is missing.
> Aspects are listed under the fixture type carrying them, nested as they are nested in §1. **What it settles**
> is what the operation does differently — never a restatement of the dimension's own ordinals, and never what
> caused the dimension to take a value.

| Dimension | What it settles | Varies aspect |
|---|---|---|
| `scope-is-local` | whether the run searches the registry it is standing in or one the caller named | • `Query`<br>&nbsp;&nbsp;– scope specifier<br>• `Registry Register`<br>&nbsp;&nbsp;– the call<br>&nbsp;&nbsp;&nbsp;&nbsp;– whether it is made at all<br>• `Registry Search`<br>&nbsp;&nbsp;– the call<br>&nbsp;&nbsp;&nbsp;&nbsp;– the registries called<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– searched locations<br>• `Failure`<br>&nbsp;&nbsp;– the scope named |
| `path-unreadable` | whether a location on the walk is reported as unreadable rather than treated as absent | • `Filesystem`<br>&nbsp;&nbsp;– paths<br>&nbsp;&nbsp;&nbsp;&nbsp;– whether it can be read |
| `configuration-found` | whether any named scope can be resolved at all | • `Filesystem`<br>&nbsp;&nbsp;– paths<br>&nbsp;&nbsp;&nbsp;&nbsp;– what it points at<br>&nbsp;&nbsp;– the configuration |
| `registry-root-found` | whether a local search has anything to run against | • `Filesystem`<br>&nbsp;&nbsp;– the ambient registry<br>• `Registry Register`<br>&nbsp;&nbsp;– the call<br>&nbsp;&nbsp;&nbsp;&nbsp;– the root named<br>• `Failure`<br>&nbsp;&nbsp;– the reason |
| `registration-failed` | whether a local search answers or fails, once it has a root to answer from | • `Filesystem`<br>&nbsp;&nbsp;– the ambient registry<br>• `Registry Register`<br>&nbsp;&nbsp;– the answer<br>&nbsp;&nbsp;&nbsp;&nbsp;– what it established<br>&nbsp;&nbsp;&nbsp;&nbsp;– what it could not<br>• `Failure`<br>&nbsp;&nbsp;– the reason |
| `search-target-available` | whether a named scope reaches registered locations or fails naming itself | • `Filesystem`<br>&nbsp;&nbsp;– the configuration<br>&nbsp;&nbsp;&nbsp;&nbsp;– registries<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– slug<br>• `Registry Search`<br>&nbsp;&nbsp;– the call<br>&nbsp;&nbsp;&nbsp;&nbsp;– the registries called<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– searched locations<br>• `Failure`<br>&nbsp;&nbsp;– the scope named<br>&nbsp;&nbsp;– the reason |
| `location-configured-twice` | whether the run searches a location once and warns, or once and says nothing | • `Filesystem`<br>&nbsp;&nbsp;– the configuration<br>&nbsp;&nbsp;&nbsp;&nbsp;– registries<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– path<br>• `Results`<br>&nbsp;&nbsp;– warning |
| `query-matched` | whether there is any result to report, or an empty answer | • `Query`<br>&nbsp;&nbsp;– terms<br>• `Registry Search`<br>&nbsp;&nbsp;– the answer<br>&nbsp;&nbsp;&nbsp;&nbsp;– whether anything matched<br>• `Results`<br>&nbsp;&nbsp;– result set |
| `match-is-a-section` | what a result carries beyond its reference — a title alone, or the chain of ancestors placing a section in its document | • `Registry Search`<br>&nbsp;&nbsp;– the answer<br>&nbsp;&nbsp;&nbsp;&nbsp;– a match<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– its ancestry<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– result rows<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– ancestry block |
| `max-results-exceeded` | whether the list ends in a count of the matches it did not name | • `Registry Search`<br>&nbsp;&nbsp;– the answer<br>&nbsp;&nbsp;&nbsp;&nbsp;– how many matched in all<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– list overflow |
| `max-results-given` | which cap the list is cut against — the caller's number or the default | • `Query`<br>&nbsp;&nbsp;– cap flag<br>• `Registry Search`<br>&nbsp;&nbsp;– the call<br>&nbsp;&nbsp;&nbsp;&nbsp;– the cap passed<br>&nbsp;&nbsp;– the answer<br>&nbsp;&nbsp;&nbsp;&nbsp;– the matches handed back<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– result rows |
| `details-requested` | whether a result is a pointer alone or carries a preview with it | • `Query`<br>&nbsp;&nbsp;– mode flag<br>• `Registry Report`<br>&nbsp;&nbsp;– the call<br>&nbsp;&nbsp;&nbsp;&nbsp;– whether it is made at all<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– result rows<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– preview block<br>&nbsp;&nbsp;– warning |
| `preview-length-exceeded` | whether a preview ends in a count of the lines it did not show | • `Registry Report`<br>&nbsp;&nbsp;– the answer<br>&nbsp;&nbsp;&nbsp;&nbsp;– how many lines the node holds in all<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– result rows<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– preview block<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– preview overflow |
| `preview-length-given` | which length each preview is cut against — the caller's number or the default | • `Query`<br>&nbsp;&nbsp;– length flag<br>• `Registry Report`<br>&nbsp;&nbsp;– the call<br>&nbsp;&nbsp;&nbsp;&nbsp;– the bound passed<br>&nbsp;&nbsp;– the answer<br>&nbsp;&nbsp;&nbsp;&nbsp;– the lines handed back<br>• `Results`<br>&nbsp;&nbsp;– result set<br>&nbsp;&nbsp;&nbsp;&nbsp;– result rows<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;– preview block<br>&nbsp;&nbsp;– warning |
| `machine-rendering` | whether the same answer is encoded for a person or for a parser | • `Query`<br>&nbsp;&nbsp;– encoding flag<br>• `Results`<br>&nbsp;&nbsp;– encoding<br>• `Failure`<br>&nbsp;&nbsp;– encoding |

A preview block is varied both by whether previews were asked for and by how long they run; no aspect here is
varied by *another aspect's* dimensions (§1).

**The first six settle whether there is anything to search at all**, and nothing below them can be asked until
they have. A run either names a scope or does not; a named one has to resolve against a configuration that was
itself found; a local one has to stand in a registry root, and that root has to register. Only then is there
somewhere for a query to look.

**Six of the fifteen appear on a `Query` aspect, then on a crossing, then on the output** — a knob travelling
the whole way through. Four appear only on a crossing's answer and on the output: nobody set them, they were
found. And `machine-rendering` is the only one that never reaches a crossing at all — it changes how an answer
is written down and nothing about what was asked or returned.

**Each cap is two dimensions because it is two facts in two places.** `max-results-given` sits in the search
call and `max-results-exceeded` in its answer; `preview-length-given` sits in the report call and
`preview-length-exceeded` in its answer.

### 3.2 Rank And Category

> Rank by how much of the answer each dimension decides: one ranks above another when the second only has
> something to say once the first has gone a particular way. Category is where a dimension's value comes from
> — the payload, the dependencies, or the invocation's own knobs.

| Rank | Dimension | Category | Decides |
|---|---|---|---|
| 1 | `scope-is-local` | payload | which registry |
| 2 | `path-unreadable` | dependency | what |
| 3 | `configuration-found` | dependency | whether |
| 4 | `registry-root-found` | dependency | whether |
| 5 | `registration-failed` | dependency | whether |
| 6 | `search-target-available` | dependency | whether |
| 7 | `location-configured-twice` | dependency | what |
| 8 | `query-matched` | dependency | whether |
| 9 | `match-is-a-section` | dependency | what |
| 10 | `max-results-exceeded` | dependency | what |
| 11 | `max-results-given` | parameter | what |
| 12 | `details-requested` | parameter | what |
| 13 | `preview-length-exceeded` | dependency | what |
| 14 | `preview-length-given` | parameter | what |
| 15 | `machine-rendering` | parameter | how |

`scope-is-local` is the only payload dimension, and it outranks everything because it decides which of two
quite different routes the run takes — against a registry the caller named, or against the one it is standing
in. Whether the caller wrote `@AgentPlugins`, several slugs, or `@ALL` does not (§4.2); whether they wrote
anything at all does.

**Within each cap pair, the outcome outranks the knob.** Under-limit collapses the knob entirely, because a
number nothing reached is a number that changed nothing, while over-limit is exactly where whose number it was
becomes visible.

`machine-rendering` decides neither — it changes how the same answer is encoded and nothing about what it is,
which is why no node draws it and the only rule reaching it declares it orthogonal to everything.

## 4 Payload States

> The dimensions whose values come from what the operation was asked to do. Projection: `given`.

What varies in the operation's own input — the one thing the Agent decides before anything is looked up.

### 4.1 `scope-is-local`

Whether the run names no scope at all, and so searches the registry it is standing in.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | a scope was named, and the run searches whatever the configuration resolves it to |
| 2 | `yes` | no scope was named, and the run searches the registry root it is standing inside |

A local search and a named one are not the same search run over different locations. A named scope resolves
against the configuration and comes back identified by its slug; a local one resolves to the root the walk
found and comes back identified by its path, because it has no slug for a specifier to have asked for (§2).
The two also fail in different ways and for different reasons, which §5 separates out.

`@ALL` is a named scope, not a local one. It reaches every registry the configuration holds, and the registry
the caller happens to be standing in is among them only if it was configured.

### 4.2 How Many Locations A Named Scope Reaches Is A Route

A named scope may reach one registered location, several, or every one the configuration holds. All three
reach the same behaviour, so none of them is a dimension
([Operation Fixtures §3](@docs/workflows/feature-workflow/operation-fixtures.md)).

It is the whole content of *A score is a property of prose, not of its container* (§2.4). A score measures
prose against its own extent and carries nothing about what contains it, so a document scores what it scores
whether it was reached alone or alongside twenty others. Searching several locations is therefore not a
different operation with a merge on the end — it is the same operation over a larger set, returning one ranked
list in which results from different locations interleave by score like any others. Nothing downstream of the
query needs to know how wide the search was.

So breadth earns fixtures rather than cells: the main success scenario's own registry spans two registered
locations, which is where that invariant is witnessed, and naming a scope three different ways gives three
payloads against the same behaviour rather than three branches.

**Naming none is not among them**, and that is `scope-is-local` rather than a fourth route. It resolves
somewhere else entirely, is reported differently, and fails differently. Where the three above differ in how
many locations one behaviour runs over, that one differs in what it runs over at all.

What a scope specifier actually looks like, and how it resolves to a location, is not settled here — that is
the use case's own first open question (where the registry lives) reaching into its addressing.

## 5 Dependency States

> The dimensions whose values come from what the operation finds rather than from what it was told.
> Projection: `given`.

What the filesystem and the registry present the operation with. The first six of these settle whether there
is anything to search; the rest shape what comes back once there is.

### 5.1 `path-unreadable`

Whether a location the walk touches exists and refuses to open.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | every location the walk touches either opens or is not there at all |
| 2 | `yes` | a location exists and cannot be read, which is reported as such and never as absence |

Fixing a permission and fixing a path are different remedies, which is why the two are never reported alike
(§2.1) — the same distinction the use case draws at its own extensions 1b and 1c.

### 5.2 `configuration-found`

Whether the walk up from the working directory reached a `.weaverdocs.yaml`.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | no configuration anywhere on the walk, so no named scope can resolve to anything |
| 2 | `yes` | a configuration was found, and its registries are what a named scope resolves against |

A local search needs no configuration at all: it resolves to the root it is standing in, and never consults
one. So this dimension bites only where a scope was named, which is what makes it rank below
`scope-is-local` rather than above it.

### 5.3 `registry-root-found`

Whether the walk found a registry root at or above the working directory.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | nothing on the walk holds a `.git/`, so a local search has nowhere to run |
| 2 | `yes` | a root was found, and it is the registry a local search runs against |

Only the nearest counts (§2.1). A repository inside a repository is its own registry, and the one containing
it is not searched as well.

### 5.4 `registration-failed`

Whether registering the ambient registry root completed.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the root registered, and the search is answered from what that established |
| 2 | `yes` | registration did not complete, and the run fails rather than answering from an index it cannot trust |

Registration is not conditional on an index being absent. Whatever is already there says nothing about how
stale it is, and it is established on every local run because doing so is mechanical and idempotent (§2.1).
What varies is only whether that succeeded.

### 5.5 `search-target-available`

Whether the scope the caller named resolves to registered locations at all, before anything is searched.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the scope names something the configuration does not hold, and the run fails naming it |
| 2 | `yes` | the scope names one or more locations the configuration holds |

Failing here is a different condition from a scope that resolves onto nothing registered, and from one that
resolves onto registered content the query misses — both of those are ordinary empty results (§5.7), because
the scope was right and the answer is simply "nothing here". The use case's §6 extension 4b is this
dimension's `no`.

### 5.6 `location-configured-twice`

Whether two slugs in the configuration name one location.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | every configured location is named once, and the run says nothing about it |
| 2 | `yes` | one location is configured under several slugs, and the run searches it once and warns |

A map keyed by slug cannot prevent this, only its inverse (§1.3). The check costs nothing — the duplicate is
visible in the configuration before anything is searched — and without it every match from that location
would come back as many times as it was configured.

### 5.7 `query-matched`

What the query's own terms find in whatever is being searched, stated as the outcome across the whole query.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the query finds nothing, which is an empty result and not an error |
| 2 | `yes` | the query finds something |

`no` is the use case's §6 extension 4a.

**How a query is written is not this operation's concern.** Whether it carries one term or several, whether
some of its terms match and others do not, and what phrases, negation or conjunction might mean are all
questions about the relevance function and the query language it implies — a design in their own right, and
left open as one (the use case's §7). What this operation settles is what happens to what was found: whether
anything was, what kinds of node, and what is then done with them.

### 5.8 `match-is-a-section`

What a matching node is, and therefore what its result carries with it.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the node is a whole document; its result carries its title and nothing beneath |
| 2 | `yes` | the node is a section; its result carries the document above it and every section down to it, each with its own word count |

Both are returned by the same search and ranked against each other on their own merits — a document may rank
above a section of another document or below it, and each is separately addressable. Relevance concentrated in
one section is best answered by that section; relevance spread thinly across a document is best answered by
the document, which is the only node that sees all of it.

What a section result carries is the chain that places it, which is why the two are worth telling apart at all
rather than folding every match into its document (§2).

### 5.9 `max-results-exceeded`

Whether the matches found exceed the limit the search was run under.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | every match fits inside the limit, so every match is returned |
| 2 | `yes` | more matched than the limit admits, so the lowest-scoring are dropped |

Truncation takes the highest-scoring and drops the rest (§2).

### 5.10 `preview-length-exceeded`

Whether a previewed node's content exceeds the preview's own length. A run that previews nothing has no such
node to ask about.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the content fits, and the preview shows all of it |
| 2 | `yes` | the content runs past the length, and the preview is cut |

### 5.11 What Is Not A Dimension

**How many documents match, how many locations they are spread across, and how many locations a named scope
reached.** Every matching node is scored by the same rule and ranked in the same set; a second match
exercises nothing a first one did not, and neither does a second location (§4.2).

### 5.12 Scoring Is A Query-Time Aggregation Over Prose

A score says how well one piece of prose answers the query, measured against that prose's own extent. It is a
property of the text, not of what contains it: the same section scores the same whether it sits in a
twenty-document repository or a two-document one, and whether it was reached by naming its location or by
asking for everything. That is what lets results from several locations be ranked against each other directly
rather than merged from separate rankings (§2).

Two things follow, and both are requirements rather than choices:

* A document's own score aggregates its whole prose, its sections included. Registration records each node's
  words where they textually appear and rolls nothing up (`documentation-standards` §5, which says explicitly
  that aggregation is the search tool's job at query time) — so this operation is where that aggregation
  happens. A document scored over only the prose outside its sections would rank on the length of its own
  title, which is an artifact and not relevance.
* Rationale and appendix prose is not part of any score, because it was never registered (§2).

Which function computes the score is not settled here, and neither are its defaults — see the use case's §7.
What *A score is a property of prose, not of its container* (§2.4) fixes is the one property of that function
this operation actually depends on.

## 6 Parameter Options

> The dimensions the caller sets on the invocation itself — same entry state, different call. Projection:
> `when`.

The knobs of this operation's own invocation. Each is a flag, and `yes` is the caller having set it.


### 6.1 `details-requested`

Whether the caller asked for previews, so that a result carries its own opening lines rather than a pointer

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | each result is an addressable reference, its score, and the word count that score was computed against |
| 2 | `yes` | each result additionally carries a preview of its own opening lines |

`details` exists to make choosing cheap. The Agent's whole problem is that reading a document to find out
whether it was worth reading is the cost it cannot afford (use case §1); a handful of lines per hit either
answers the question outright or points firmly at which reference to fetch, for a fraction of what fetching
several would cost.

A preview runs to the caller's own length and no further, and where the content runs past it the preview says
how much it withheld — the opening lines, then a count of the rest:

```
/repo/docs/widgets/doc-b.md §2 Configuration  - score 0.6 - words 25
  Configuration is read once at startup.
  The host, the port and the timeout.
  ... (12 lines)
```

That count is what makes the preview a steer rather than a teaser. Two hits whose first two lines read alike
are a very different proposition when one of them is three lines long and the other is two hundred, and the
Agent has to make that call without fetching either.

### 6.2 `max-results-given`

Whether the caller named a cap on how many results to be given.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the caller names no cap, and the list is cut against whatever the default is |
| 2 | `yes` | the caller names one, and the list is cut against that |

As with `preview-length` (§6.3), `default` is not "no cap" — a caller who names nothing still gets a bounded
list, so **a default must exist**, and design owes a number. Truncation happens against whichever number is in
force, not against a built-in one the caller thought they had overridden.

Where anything is dropped the list says how many, in the same form a capped preview uses (§6.1): the results it
kept, then a count of the matches it did not name.

```
/repo/docs/widgets/doc-b.md §2 Configuration  - score 0.6 - words 25
/repo/docs/widgets/doc-b.md                   - score 0.5 - words 98
... (12 more matches)
```

Both counts answer the same question in their own register — "how much did you not show me" — and the Agent
needs both to spend its budget well. Without the list's count it cannot tell a query that found three things
from one that found thirty and showed three, which is the difference between having the answer and having the
top of a pile.

### 6.3 `preview-length-given`

Whether the caller named a length for each preview.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the caller names no length, and each preview is cut against whatever the default is |
| 2 | `yes` | the caller names one, and each preview is cut against that |

`default` is not "no preview". A caller who asks for details and names no length still gets one, of some
length, which means **a default must exist**. That it must exist is settled here. What it is, is not — and
unlike the questions this operation leaves open because they may reasonably stay open, this one cannot: nothing
can be built until a number is chosen. Design owes a value, not a decision about whether to have one. The same
is true of `max-results` (§6.2).

A given length reaches the only case where a preview stops for a reason other than running out of lines: asked
for more lines than a document holds before its `Rationale`, it stops at the `Rationale` and not at the count,
because the exclusion outranks the request.

`preview-length` and `mode` are independent knobs, so naming a length while asking for a list is an ordinary
thing for a caller to do and the operation has to answer it, with a warning rather than a refusal (§2).

### 6.4 `machine-rendering`

Whether the caller declared it will parse the answer rather than read it.

| Ordinal | Value | Means |
|---|---|---|
| 1 | `no` | the answer is written to be read by a person |
| 2 | `yes` | the caller declares it will parse the answer |

What either rendering contains is the same answer; the choice is a format and not a different question (§2).


## 7 Condition Rules

> Pruning declared as rules over the dimensions rather than inferred from the tree that results. Each rule
> names where it applies in a first table — rows read together, the ordinals against one dimension
> alternatives — and in a second what has nothing to say there. State the least condition that makes the claim
> true: a rule naming the whole path to a cell is naming conditions its claim does not rest on.

**These rules predate six of §3's fifteen dimensions and do not yet account for them.** They were written
against nine, and `scope-is-local`, `path-unreadable`, `configuration-found`, `registry-root-found`,
`registration-failed` and `location-configured-twice` are unmentioned by any of them. Every count below is
therefore of the space as it was. Rewriting them is the next stage's work and is deliberately not done here,
since the dimensions are what is under review.

Three of the four kinds prune inside a region — a combination that cannot arise, a dimension with nothing to
say, a dimension whose variation changes nothing. The fourth says that two regions do not interact, which is
what turns a cross-product into a covering.

### 7.1 Invalid

> The cells in this region cannot be invoked.

No combination of §3's ordinals is impossible. Every one of them is a search somebody could run.

The impossibility this operation does have — a section matching while its document does not — removes a *value*
rather than a combination, so it is ruled out at §5.1's ordinal list and there is nothing left here to exclude.

### 7.2 Not Applicable

> The cells in this region cannot be reached, so the dimension needs no behaviour there. Derive them from §1's
> nesting rather than judging them one at a time, three ways: an aspect removed takes everything beneath it,
> and a dimension governing only those has nothing left to vary; a fixture absent from the run takes all of its
> aspects at once, which a call never placed does; and a dimension that selects between **fixture types**
> silences every dimension governing no aspect of the type it selected. All three are read off §3.1 and checkable
> against it — a rule naming a different set from the one the aspects imply is wrong in one of the two places.

§1.7's nesting is what these rules say in the vocabulary of dimensions:

| Remove | and these go with it | leaving nothing for |
|---|---|---|
| result rows — nothing matched | ancestry block, preview block, preview overflow | `match-is-a-section`, `details-requested`, `preview-length-given`, `preview-length-exceeded` (§7.2.2) |
| preview block — no previews asked for | preview overflow | `preview-length-exceeded` (§7.2.3) |

The first row is not quite the whole of §7.2.2: `max-results-given` and `max-results-exceeded` are silenced there
too, but by there being no matches to cap rather than by anything being removed from the tree. Containment
accounts for most of that rule and not all of it, which is worth saying rather than rounding up.

**Both rows have a second derivation on the dependency side, and it is the stronger one.** A whole fixture can
be absent as easily as an aspect can: where `details-requested` is `no`, or where nothing matched, no `Registry Report`
crossing is made at all (§1.6), so that fixture does not exist for the run and neither of the dimensions it
carries has anything to vary. Read that way, §7.2.3 is not a fact about the rendered output at all — it is a
call that was never placed, and the missing preview block is the consequence rather than the cause.

**§7.2.1 is not in this table because it derives another way, not because it does nothing.** It is the
hardest-working rule in this document: it collapses 128 combinations to one, and no other rule can reach that
region, because §7.2.2 needs a `query-matched` value and §7.2.3 a `details-requested` value and §7.2.1 is
precisely the claim that
neither has one. Removing it would leave the whole of that region standing.

What it derives from is **type selection** rather than containment. `search-target-available` decides which
artefact type comes
back (§3), and a `Failure` carries three aspects — what was named, why it was not understood, and how those
are written down. Every dimension §7.2.1 names is therefore exactly a dimension that varies no aspect of a
`Failure`, which is readable straight off §3.1 rather than judged. That is why it cannot be got wrong: not
because it prunes nothing, but because what it prunes is computed rather than decided.

**Running that check on all three rules.** State which aspects the condition kills, exclude the rule's own
condition dimension and the payload — a `Query` always carries every flag, so it can silence nothing — and the
dimension list follows. §7.2.1 and §7.2.3 come out exactly as declared. §7.2.2 does not:

| Rule | derived | declared |
|---|---|---|
| §7.2.1 | seven dimensions | the same seven |
| §7.2.3 | `preview-length-exceeded` | the same |
| §7.2.2 | five dimensions | those five **and** `max-results-given`, `details-requested`, `preview-length-given` |

**§7.2.2 claims three dimensions are meaningless that the aspects say are still live**, and the claim is left
standing here rather than fixed, because the rules are what is under review. The cap was still passed in a
call that was still made (`the cap passed`), so `max-results-given` has a live aspect; and a length named alongside
a list still earns its warning whether or not anything matched, so `details-requested` and
`preview-length-given` do too. Whether
those are genuinely meaningless, or merely immaterial, or the rule should name fewer dimensions, is a question
for review and not one this check can answer on its own.

#### 7.2.1 Nothing Was Searched

When

| | Dimension | Ordinals |
|---|---|---|
| - | `search-target-available` | • `no` |

then

| Dimension |
|---|
| `query-matched` |
| `match-is-a-section` |
| `max-results-exceeded` |
| `max-results-given` |
| `details-requested` |
| `preview-length-exceeded` |
| `preview-length-given` |

are **meaningless**.

The run stopped before anything was searched, and what comes back is a `Failure` rather than a `Results`
(§1.1). Its two aspects both answer to `search-target-available`; every dimension named above governs some
aspect of a `Results`,
and a `Failure` has none of them. `machine-rendering` is not in this list, because a `Failure` is still encoded
for a person or for a parser like anything else.

This rule records what the tree does at that cell rather than constraining it. Nothing in it could be got
wrong once `Failure` is a type of its own — which is the point of its being one.

#### 7.2.2 An Empty Result Has No Shape

When

| | Dimension | Ordinals |
|---|---|---|
| - | `query-matched` | • `no` |

then

| Dimension |
|---|
| `match-is-a-section` |
| `max-results-exceeded` |
| `max-results-given` |
| `details-requested` |
| `preview-length-exceeded` |
| `preview-length-given` |

are **meaningless**.

A shape is a property of results, a cap bounds them, a preview previews one; with no results, all of them are
questions about nothing.

#### 7.2.3 No Preview To Overflow

When

| | Dimension | Ordinals |
|---|---|---|
| - | `details-requested` | • `no` |

then

| Dimension |
|---|
| `preview-length-exceeded` |

is **meaningless**.

Nothing is previewed, so whether content would have run past a preview is a question about nothing.
`preview-length-given` is deliberately not here: a caller may name a length while asking for a list, which is an
ordinary invocation the operation answers with a warning (§6.3), not a condition that cannot arise.

### 7.3 Immaterial

> The cells in this region exhibit behaviour that does not vary across them, so it needs defining once.
> Immaterial means immaterial to the **behaviour**, not to the fixtures: a dimension belongs here only where
> varying it leaves what the operation does unchanged, never where varying it would produce something another
> cell happens to have shown already.

#### 7.3.1 A Cap Nothing Reached Is A Cap That Did Nothing

When

| | Dimension | Ordinals |
|---|---|---|
| - | `query-matched` | • `yes` |
| & | `max-results-exceeded` | • `no` |

then

| Dimension |
|---|
| `max-results-given` |

is **immaterial**.

Every match fits, so every match is returned, and the caller's number changes nothing about what comes back —
a cap of twenty and a cap of fifty produce the same list when eleven things matched. Whose number it was only
becomes visible when something is actually dropped against it.

#### 7.3.2 A Bound Nothing Reached Is A Bound That Did Nothing

When

| | Dimension | Ordinals |
|---|---|---|
| - | `details-requested` | • `yes` |
| & | `preview-length-exceeded` | • `no` |

then

| Dimension |
|---|
| `preview-length-given` |

is **immaterial**.

The content fits, so the preview shows all of it, and the caller's number changes nothing about what comes
back — a bound of five lines and a bound of fifty show the same three lines, with nothing withheld to declare.
Whose number it was only becomes visible when something is actually cut, which is §7.3.1's argument applied to
the other cap.

**Two things about the pair, both left for review.**

The first row of each rule is implied by its second. `max-results-exceeded` only has a value where the query
matched, and `preview-length-exceeded` only where previews were asked for — §7.2.2 and §7.2.3 are what make
that so. Under this section's own least-condition rule both first rows could go, leaving each rule naming the
outcome alone. They are written out here because §7.3.1 was written that way.

Both rules are immaterial to what the operation *delivers* and not to what it *does*. Varying the cap still
varies `Registry Search / the call / the cap passed`, and varying the bound still varies
`Registry Report / the call / the bound passed`: a different call is made, and the same answer comes back from
it. That is the one live aspect either dimension has in its region, and it is the same aspect in both — so it
is a property of the pair rather than a fault in one of them. Whether **immaterial** should mean immaterial to
the delivered output, with a differing dependency call allowed, is a question for §7.3's own definition.

### 7.4 Orthogonal

> The dimensions in each group below compose with those in every other group: the behaviour of a combination is
> the behaviour of each part, and nothing arises from putting them together. Groups that compose need
> **covering, not crossing** — every state of every group must appear somewhere, not once per combination. This
> is §1's independence claim expressed over dimensions instead of aspects, and it is falsifiable the same way:
> a combination that behaves differently from the composition of its parts refutes the declaration.

The other three kinds prune inside a region. None of them says that two regions do not interact, and without
that the space stays multiplied: §7.1 to §7.3 leave 32 cells standing, of which 30 are a pure cross-product.

#### 7.4.1 What Matched, How Much Was Kept, And How Much Was Shown

When

| | Dimension | Ordinals |
|---|---|---|
| - | `query-matched` | • `yes` |

then

| | Group | Dimensions |
|---|---|---|
| - | match shape | • `match-is-a-section` |
| & | the cap | • `max-results-exceeded`<br>• `max-results-given` |
| & | the preview | • `details-requested`<br>• `preview-length-exceeded`<br>• `preview-length-given` |

are **orthogonal**.

Capping ranks the whole set and cuts it; what each surviving row then carries, and how much of each hit is
shown beneath it, are decided afterwards and separately. A document match is capped exactly as a section match
is, and previewed exactly as a section match is — the preview is of the matching node's own opening lines
whichever kind of node it was.

The declared rules already respect this grouping, which is the evidence for it rather than an argument about
it. Every rule that *shapes* an answer lives strictly inside one group: §7.3.1 within the cap, §7.2.3 and
§7.3.2 within the preview. The only rules spanning groups are §7.2.1 and §7.2.2, and those are gates that
silence everything below rather than relating one group to another.

After §7.1 to §7.3, the three groups carry 2, 3 and 5 states. Crossed that is 30; covered it is 5.

#### 7.4.2 Encoding Composes With Everything

Unconditionally — in every region, including those where nothing was searched —

| | Group | Dimensions |
|---|---|---|
| - | the encoding | • `machine-rendering` |

is **orthogonal** to every other dimension.

Both values are held concretely at every leaf and neither is drawn as a node (§8). This was stated as *Drawn
Compactly* before the kind had a name, and it is an instance of it rather than a special case: `machine-rendering`
changes how an answer is written down and nothing about what the answer is, so it composes with everything and
needs covering rather than crossing like any other orthogonal group.

### 7.5 Consistency Of The Tree With These Rules

**Not currently consistent, and the tree is what is wrong.** §8 draws ten leaves; these rules leave far more
standing, because two rules that were holding the tree down have been withdrawn as untrue:

* *A lone document is capped and previewed like any other result* claimed that capping and previewing were
  immaterial under a `no` match. They are not. A document match and a section match differ in what they
  carry — a title alone, against the whole chain down to the section with each level's own word count — and
  capping and previewing then act on different things. Both dimensions change the answer under either type, so
  neither is immaterial to it.
* *Both disclosures hold everywhere* claimed that `details-requested`, `preview-length-exceeded` and
`preview-length-given` were
  immaterial once the list had been truncated. They are not: details mode previews the survivors, and that is
  a different answer. The argument that carried it — that both disclosures are invariants already witnessed —
  is an argument about what needs *drawing*, and this section is not about drawing.

A third went with them, unflagged in review but false for the same reason: *a cut preview is cut at whichever
length was in force* claimed `preview-length-given` was immaterial once a preview overflowed. It is not — a preview
cut at five lines and one cut at ten show different amounts of the same section. That the cut is *declared* is
invariant; how much survives it is not.

**What the rules now predict.** Expanding §3's nine dimensions and applying §7.1 to §7.3 leaves 32 cells.
Applying §7.4 to those replaces the 30-cell cross-product with 5 covering cells, leaving **7**: five under a
query that matched, one empty result, one unresolvable scope.

Seven is a floor and not a target. Covering is one obligation on the tree; witnessing is another, and §2's
invariants need particular cells to stand on — a corpus whose excluded zones hold the query's own terms, a
registry spanning two locations, a document that matches where none of its sections do. Where witnessing
demands a cell that covering would have folded away, the cell is drawn and says which invariant it is there
for. Redrawing §8 is owed against both obligations, and is deliberately not done here while the rules are
under review.

## 8 Output Fixtures

> The cells that survive §7's pruning, each with the state it establishes and the fixtures exposing it. Its job
> is to identify which fixtures presenting which aspect-variants are required, not to enumerate a
> cross-product: independent aspects need covering, not crossing.

Every leaf has two further leaves under **report-rendering** — `.1` human and `.2` machine — carrying the same
results and differing only in how they are rendered, so they are not drawn. Both renderings are held concretely
for every leaf.

**This operation has no `Result`.** It writes nothing and changes nothing: the registry it reads is exactly as
it was afterward. Its whole deliverable is what it hands back, which is why every leaf below carries `Stdout`
and no leaf carries anything else. Its entry state is
[1 — Register A Path](1-register-a-path.md)'s own `Result` — the corpus fixtures here are that operation's
registrations, not a second description of the same documents.

Which cells are drawn, and why every other combination is not, is §7's — not restated here.

An empty result is not an extension — the operation answered the question it was asked, and the answer is that
nothing matches. Only `no` is an extension, because only there does the Agent have something to fix
before asking again.

* 1 - **search-target-available:** `yes`
  * 1.1 - **query-matched:** `no`
    > Leaf. Everything below **query** *pruned, meaningless:* §7.2.2.
    >
    > **Establishes:** an empty result set, reported as such — **extension 4a**
    >
    > **Witnesses:** *The machine rendering names every result field it has* (§2) — the hardest case for
    > it, since here every field there is has nothing in it
    >
    > **Payload:** [`no-match.query`](../fixtures/no-match/query.md)
    >
    > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
    >
    > **Stdout:** `no-match.results` — [txt](../fixtures/no-match/results.txt)
    > · [json](../fixtures/no-match/results.json)
  * 1.2 - **query-matched:** `yes`
    * 1.2.1 - **match-is-a-section:** `yes`
      * 1.2.1.1 - **results:** `no`
        > **max-results** *pruned, immaterial:* §7.3.1.
        * 1.2.1.1.1 - **details-requested:** `no`
          > **preview-length-exceeded** *pruned, meaningless:* §7.2.3.
          * 1.2.1.1.1.1 - **preview-length-given:** `no`
            > **Establishes:** a section and the document holding it returned as two results, each with its own
            > score and word count, ranked against each other — **the main success scenario**
            >
            > **Witnesses:** *The walk goes up and never down* (§2) — the configuration
            > sits above the working directory, and nothing beneath it is consulted
            >
            > **Witnesses:** *The nearest configuration wins outright* (§2) — the walk stops at the first one
            > it finds, and that one is the whole of what is available
            >
            > **Witnesses:** *A named scope resolves only against the configuration* (§2) — the scope names a
            > configured slug, and nothing outside the configuration is reachable by naming
            >
            > **Witnesses:** *A slug names exactly one location* (§2) — two distinct slugs, each resolving to
            > exactly one location
            >
            > **Witnesses:** *A configured registry always has a path* (§2) — each slug has a location against
            > it, neither left empty
            >
            > **Witnesses:** *A matched search answers with a reference, a type, a score, a word count and a
            > document* (§2) — two matches, each carrying all five
            >
            > **Witnesses:** *A document always provides a path and a word count* (§2) — a document match and a
            > section match, each naming the file it lives in and its size
            >
            > **Witnesses:** *A section always provides a number and a word count* (§2) — the section match's
            > chain numbers and measures every level of it
            >
            > **Witnesses:** *No rationale or appendix section is ever a result* (§2), against a corpus whose
            > excluded zones hold the query's own terms
            >
            > **Witnesses:** *An ancestry block carries the whole chain down to the matched node* (§2) — the
            > section result carries the document and every section above it, each with its own word count
            >
            > **Witnesses:** *Both renderings carry the same results in the same order* (§2) — both are held
            > concretely against this one result set
            >
            > **Witnesses:** *A score is a property of prose, not of its container* (§2) — this cell's registry
            > spans two registered locations, and their results interleave by score rather than grouping by
            > where each came from
            >
            > **Payload:** [`section-and-document.query`](../fixtures/section-and-document/query.md)
            >
            > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md) and
            > [`nested-directory.registered-recursed`](../fixtures/nested-directory/registered-recursed.md) — two registrations operation 1 established
            > separately, searched together here
            >
            > **Stdout:** `section-and-document.results` — [txt](../fixtures/section-and-document/results.txt) · [json](../fixtures/section-and-document/results.json)
          * 1.2.1.1.1.2 - **preview-length-given:** `yes`
            > **Establishes:** the same results, in full, with a warning that the length was not used — a
            > parameter that cannot apply is reported rather than obeyed or refused
            >
            > **Witnesses:** *A parameter that cannot apply is reported, never obeyed and never fatal* (§2)
            >
            > **Payload:** [`section-and-document.query-length-ignored`](../fixtures/section-and-document/query-length-ignored.md)
            >
            > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
            >
            > **Stdout:** `section-and-document.results-length-ignored` —
            > [txt](../fixtures/section-and-document/results-length-ignored.txt) · [json](../fixtures/section-and-document/results-length-ignored.json)
        * 1.2.1.1.2 - **details-requested:** `yes`
          * 1.2.1.1.2.1 - **preview:** `no`
            * 1.2.1.1.2.1.1 - **preview-length-given:** `no`
              > **Establishes:** each result carrying a preview of its own opening lines, every one of them
              > shorter than the length and so shown whole, with nothing withheld to declare
              >
              > **Witnesses:** *A matched report answers with a reference, a type, a line count and content*
              > (§2) — a preview fetched for each result, its content and its extent coming back together
              >
              > **Witnesses:** *A result always carries a reference, a score, and a word count* (§2) — each
              > result carries all three and a preview besides, which is what shows the preview to be carried
              > in addition to them rather than in place of any
              >
              > **Payload:** [`section-and-document.query-details`](../fixtures/section-and-document/query-details.md)
              >
              > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
              >
              > **Stdout:** `section-and-document.results-details` —
              > [txt](../fixtures/section-and-document/results-details.txt) · [json](../fixtures/section-and-document/results-details.json)
            * 1.2.1.1.2.1.2 - **preview-length-given:** `yes`
              > **Establishes:** previews at the length the caller named — longer where there is content to
              > reach, and stopping short of it where an excluded zone comes first
              >
              > **Witnesses:** *No preview ever shows rationale or appendix content* (§2) — the document-level
              > preview is asked for more lines than the document holds before its `Rationale`, and stops at
              > the `Rationale` rather than at the count
              >
              > **Payload:** [`section-and-document.query-details-long`](../fixtures/section-and-document/query-details-long.md)
              >
              > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
              >
              > **Stdout:** `section-and-document.results-details-long` —
              > [txt](../fixtures/section-and-document/results-details-long.txt) · [json](../fixtures/section-and-document/results-details-long.json)
          * 1.2.1.1.2.2 - **preview:** `yes`
            > Leaf. **preview-length** was pruned by a rule since withdrawn (§7.5).
            >
            > **Establishes:** a hit whose section runs past the preview, cut at the length and ending in a
            > count of the lines it did not show
            >
            > **Witnesses:** *A preview names what it did not show* (§2)
            >
            > **Witnesses:** *A report answer states how many lines the node holds* (§2) — the node's
            > full extent comes back with the lines that fit, which is what makes the count computable
            >
            > **Payload:** [`section-and-document.query-details-cut`](../fixtures/section-and-document/query-details-cut.md)
            >
            > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
            >
            > **Stdout:** `section-and-document.results-details-cut` —
            > [txt](../fixtures/section-and-document/results-details-cut.txt) · [json](../fixtures/section-and-document/results-details-cut.json)
      * 1.2.1.2 - **results:** `yes`
        > **mode**, **preview-length-exceeded** and **preview-length** were pruned by a rule since
        > withdrawn (§7.5).
        * 1.2.1.2.1 - **max-results-given:** `no`
          > **Establishes:** the highest-scoring results kept and the lowest dropped against the default cap
          >
          > **Witnesses:** *Truncation ranks before it cuts* (§2) — more matched than the cap admits, and what
          > survives is the best of them rather than the first of them
          >
          > **Witnesses:** *A truncated list names what it did not show* (§2) — the list ends in a count of the
          > matches it did not name, the same convention a capped preview follows (§6.1)
          >
          > **Witnesses:** *A search answer states how many matched in all* (§2) — the count of
          > what matched comes back from the registry alongside the matches that fit
          >
          > **Payload:** [`section-and-document.query-limited`](../fixtures/section-and-document/query-limited.md)
          >
          > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
          >
          > **Stdout:** `section-and-document.results-limited` —
          > [txt](../fixtures/section-and-document/results-limited.txt) · [json](../fixtures/section-and-document/results-limited.json)
        * 1.2.1.2.2 - **max-results-given:** `yes`
          > **Establishes:** the same matches cut against the caller's own number rather than the default —
          > fewer kept, and a correspondingly larger count of those not named
          >
          > **Payload:** [`section-and-document.query-limited-given`](../fixtures/section-and-document/query-limited-given.md)
          >
          > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
          >
          > **Stdout:** `section-and-document.results-limited-given` —
          > [txt](../fixtures/section-and-document/results-limited-given.txt) · [json](../fixtures/section-and-document/results-limited-given.json)
    * 1.2.2 - **match-is-a-section:** `no`
      > Leaf. Everything below *pruned, immaterial:* §7.3.1.
      >
      > **Establishes:** one result for the document and none for any section — the terms are in the document's
      > own prose and in none of its sections, so there is no narrower reference to offer
      >
      > **Payload:** [`document-match.query`](../fixtures/document-match/query.md)
      >
      > **registry:** [`many-documents.registered`](../fixtures/many-documents/registered.md)
      >
      > **Stdout:** `document-match.results` — [txt](../fixtures/document-match/results.txt)
      > · [json](../fixtures/document-match/results.json)
* 2 - **search-target-available:** `no`
  > Leaf; the run stops before any searching.
  >
  > **Establishes:** nothing searched; a `Failure` naming the scope and why it could not be resolved — the
  > only cell of this operation that produces one — **extension 4b**
  >
  > **Witnesses:** *A failure names the scope and says it could not be resolved* (§2)
  >
  > **Witnesses:** *Both renderings carry the same failure and the same reason* (§2)
  >
  > **Witnesses:** *The machine rendering names every failure field it has* (§2) — the scope and the reason,
  > each named rather than implied
  >
  > **Payload:** [`unresolvable-scope.query`](../fixtures/unresolvable-scope/query.md)
  >
  > **Stdout:** `unresolvable-scope.failure` — [txt](../fixtures/unresolvable-scope/failure.txt)
  > · [json](../fixtures/unresolvable-scope/failure.json)

## 9 Coverage

> Why this set of cells is enough: every ordinal of every dimension reached somewhere, every invariant
> witnessed, and every variant of every aspect appearing in some fixture.

Ten leaves survive pruning, each with exactly one payload fixture.

**Every invariant in §2 names one cell, and that cell names it back.** Witnessing is the second obligation
on the tree and a different one from covering: a cell may exist because covering needs a variant shown, or
because an invariant needs somewhere it is hardest to satisfy. The mapping lives here rather than in §2 so
that §2 can be read and agreed before any tree is drawn.

| Fixture type | Invariant | Witnessed by |
|---|---|---|
| Filesystem | *The walk goes up and never down* | @`1.2.1.1.1.1` — a configuration found above the working directory, with none below it consulted |
|  | *The nearest configuration wins outright* | @`1.2.1.1.1.1` — the nearest configuration is the whole of what is available, and the walk stops there |
|  | *A location that cannot be read is never reported as absent* | **owed** — no cell yet puts an unreadable location on the walk, and none can until §8 is redrawn (§7.5) |
|  | *A named scope resolves only against the configuration* | @`1.2.1.1.1.1` — two registries configured, both searched, and nothing else reachable |
|  | *A slug names exactly one location* | @`1.2.1.1.1.1` — two distinct slugs, each resolving to exactly one location |
|  | *A configured registry always has a path* | @`1.2.1.1.1.1` — two registries configured, each with a location against its slug |
|  | *A location configured under several slugs is searched once, and said so* | **owed** — no cell yet configures one location twice, and none can until §8 is redrawn (§7.5) |
|  | *The nearest registry root wins outright* | **owed** — no cell yet stands inside a registry root (§7.5) |
|  | *An ambient registry is reindexed before it is answered from* | **owed** — no cell yet searches without a scope (§7.5) |
|  | *A search that cannot trust its index fails rather than answering* | **owed** — no cell yet fails to reindex an ambient registry (§7.5) |
|  | *A matched search answers with a reference, a type, a score, a word count and a document* | @`1.2.1.1.1.1` — two matches, each carrying all five |
|  | *A document always provides a path and a word count* | @`1.2.1.1.1.1` — a document match and a section match, each naming the file it lives in and its size |
|  | *A section always provides a number and a word count* | @`1.2.1.1.1.1` — a section match whose chain numbers and measures every level |
| Registry Register | *A register answer states what it could not establish* | **owed** — no cell yet registers an ambient registry, let alone one that partly fails (§7.5) |
| Registry Search | *A search answer states how many matched in all* | @`1.2.1.2.1` — more matched than the cap admits, and the count of those not named comes back with them |
|  | *A matched report answers with a reference, a type, a line count and content* | @`1.2.1.1.2.1.1` — a preview fetched for each result, content and extent together |
| Registry Report | *A report answer states how many lines the node holds* | @`1.2.1.1.2.2` — a section running past the preview, its full extent returned with the lines that fit |
| Results | *A result set names every location it searched, by slug where it has one and by path where it does not* | **owed** — the slug half is drawn at the main scenario, but no cell searches ambiently, so the path half of the claim has nowhere to stand (§7.5) |
|  | *No rationale or appendix section is ever a result* | @`1.2.1.1.1.1` — the corpus carries a document whose `Rationale` and `Appendix` hold the query's own terms, and neither appears among the results |
|  | *A result always carries a reference, a score, and a word count* | @`1.2.1.1.2.1.1` — every result carries all three, and a preview alongside them rather than instead of any |
|  | *A score is a property of prose, not of its container* | @`1.2.1.1.1.1` — the main scenario's own registry spans two registered locations, and results from both interleave by score rather than grouping by where each came from |
|  | *An ancestry block carries the whole chain down to the matched node* | @`1.2.1.1.1.1` — a section result carrying the document and every section above it, each with its word count |
|  | *No preview ever shows rationale or appendix content* | @`1.2.1.1.2.1.2` — a preview asked for more lines than the document has before its `Rationale`, stopping at the `Rationale` rather than at the count |
|  | *A preview names what it did not show* | @`1.2.1.1.2.2` — a hit whose section runs past the preview, cut at the length and ending in a count of the lines it did not show |
|  | *A truncated list names what it did not show* | @`1.2.1.2.1` — twelve matches beyond the limit, named as a count rather than silently absent |
|  | *Truncation ranks before it cuts* | @`1.2.1.2.1` — more matched than the cap admits, and the highest-scoring are what come back |
|  | *A parameter that cannot apply is reported, never obeyed and never fatal* | @`1.2.1.1.1.2` — a length named alongside a list, warned about and the results returned whole |
|  | *Both renderings carry the same results in the same order* | @`1.2.1.1.1.1` — both renderings held concretely against one result set |
|  | *The machine rendering names every result field it has* | @`1.1` — an empty result, where every field there is has nothing in it |
| Failure | *A failure names the scope and says it could not be resolved* | @`2` — the scope named back, with why it could not be understood |
|  | *Both renderings carry the same failure and the same reason* | @`2` — both renderings held concretely against one unresolvable scope |
|  | *The machine rendering names every failure field it has* | @`2` — the scope and the reason, each named rather than implied |

**Coverage is not currently claimable, and §1's independence claim is undischarged until it is.** This section
is where that claim is paid for: if the aspects were not independent, covering each variant somewhere would
not be enough and the argument below would not close. §7.5 records that §8's tree no longer derives from §7's rules, and
until it is redrawn there is no settled set of leaves to check every ordinal against. What can be said is that
the witness table below agrees from both directions wherever a cell exists to agree with, and that none of the
three withdrawn rules was carrying an invariant, so none lost its witness.

* **Every corpus here was registered by operation 1, not described again.** The `registry` line on each leaf
  points at that operation's own `Result`, which is what makes these two operations one chain rather than two
  analyses of the same documents. A search fixture that restated what is registered could drift from it; one
  that references it cannot.
* **The main scenario searches two registered locations, not one.** Breadth is a route rather than a dimension
  (§4.2), so rather than a cell of its own it is folded into the cell that has most to gain from it: the same
  corpus that witnesses the content rules also witnesses that results from two locations rank against each
  other directly. A narrower main scenario would have left that claim needing a branch to stand on.
* **@`1.2.2` is the only cell that proves a document is addressable on its own.** Every other matching cell
  yields a section too, and a reader could otherwise take the document-level result to be an artifact of having
  a section beneath it rather than a result in its own right.
* **Capping is drawn twice because it is two mechanisms, not one.** A result list and a preview are capped
  independently, by different numbers, against different things — @`1.2.1.2` cuts a list of matches,
  @`1.2.1.1.2.2` cuts the text of one. Each discloses what it withheld, and neither can stand in for the other.
* **A score without a word count is not actionable, so no result carries one.** A density says how concentrated
  a match is and nothing about how much there is to read; the two shortest results in §5.1's example are the
  highest-scoring and the least worth fetching. Both numbers travel together at every leaf that returns a
  result, and the count costs nothing to produce — the score was computed from it.
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

**Why the score is required to be about prose and not about its container.** This is the one property of the
relevance function this operation actually rests on, and it is what makes searching several locations a single
question rather than several. If a score encoded anything about the document or the repository around a piece
of prose, results from different locations could only be ranked by merging separate lists, and the Agent would
have to reason about where a result came from before it could judge whether the result was any good. Requiring
a self-contained score is what keeps `several-locations` from needing a different answer than
`single-location`.

**Why the old design's document-level scoring is not carried forward.** Its worked behaviours scored a
document against only the prose outside its sections, which made a short title dominate: a document scored
`0.5` on a two-word root while its own longer, richer section scored `0.333`. That ranks documents by how
little text sits above their first heading. It is corrected here rather than raised elsewhere because that
design is the thing this analysis exists to replace — it was never pressure-tested, and finding this is what
the exercise is for.

**Why `yes` is a mode rather than a separate operation.** It answers the same question against the same
entry state and returns the same results in the same order; what changes is how much of each one the caller
asked to see. Splitting it out would duplicate every cell above it to say nothing new, and would invite a
design where the two can disagree about what matched.
