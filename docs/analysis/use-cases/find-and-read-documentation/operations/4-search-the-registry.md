# 4 — Search The Registry

The condition space of [find-and-read-documentation](../USE-CASE.md) step 4: what the Agent may vary in its
request, what states the registry may be in when it arrives, and what must be true of the answer for each
combination of the two.

**This is an analysis of behaviour, not of mechanism.** The step's boundary is the registry's search surface.
What crosses it is a request; what lies beyond it is a registry in some state. How the registry comes to be in
that state — what it reads, what it indexes, what it has to establish first — is on the far side of the
boundary and is not perceived here. Where the Agent does perceive a difference it is modelled, and the
difference between searching a registry it named and searching the one it is standing in is perceived, because
the Agent chose between them.

## Context
* [find-and-read-documentation](../USE-CASE.md) - the use case whose step 4 this analyses
* [1 — Register A Path](1-register-a-path.md) - the operation whose Result is this one's entry state; every
  registry searched here holds what that operation put in it
* [WeaverDocs Architecture](../../../architecture/weaverdocs/ARCHITECTURE.md) - §1.6 and §2.3, the registry
  boundary this step crosses
* @docs/standards/documentation-standards.md/§5 - Indexing, including the Rationale/Appendix exclusion §5's
  first invariant turns on

## 1 The Payload

What the Agent hands across the boundary: one search request. Its terms, and where to look.

### 1.1 `Query` Fixture

One invocation. The form is the CLI's, taken from `ARCHITECTURE.md` §2.3; what matters to the analysis is what
it carries, not how it is written.

A search of registries the Agent names:

```
weaverdoc search "eviction policy" --scope @AgentPlugins
```

A search of the registry the Agent is standing in, naming no scope at all:

```
weaverdoc search "eviction policy"
```

Every registry the Agent can reach:

```
weaverdoc search "eviction policy" --scope @ALL
```

#### 1.1.1 `Query` Aspects

* **terms:** - what is being searched for
* **scope specifier:** - which registries to search, or none at all

The parameters a request may also carry are §2's, and are not aspects of this fixture: they change how an
answer is presented rather than what was asked for.

### 1.2 Payload Dimensions

| Dimension | What it settles | Varies aspect |
|---|---|---|
| `term` | whether there is anything to report at all | terms |
| `scope` | which registries the search runs against, and how the answer names them | scope specifier |

How a query is written is not this operation's concern. Whether it carries one term or several, and what
phrases, negation or conjunction might mean, belong to the relevance function and the query language it
implies — a design in its own right, left open as one (the use case's §7). What is settled here is only
whether what the Agent asked for is in the corpus.

#### 1.2.1 `term` Ordinals

| Id | Value | Means |
|---|---|---|
| `term.1` | `does-not-match` | nothing registered in the scope answers the term |
| `term.2` | `matches` | something does |

`does-not-match` is an empty answer and not a failure (the use case's §6, extension 4a).

#### 1.2.2 `scope` Ordinals

| Id | Value | Means |
|---|---|---|
| `scope.1` | `none-named` | the request names no scope, and the search runs against the registry the Agent is standing in, which the answer names by its location because the Agent gave it no name |
| `scope.2` | `some-named` | the request names one or more registries, and the answer names them back by the names it was given |
| `scope.3` | `all-named` | the request asks for every registry the Agent can reach, and the answer names each of them back |

`all-named` is distinct from `some-named` because the Agent did not name what it got: the answer has to say
which registries the request reached, and that set is the registry's to know rather than the request's.

### 1.3 Pruning Rules

A rule reads **when** a condition holds **then** the dimensions named have no state to take. A condition is
ordinals joined by `·` for *or* and clauses joined by `&` for *and*; `all others` means every dimension the
document declares apart from those in the condition. Expanding the full product and applying every rule must
leave exactly the space §4 draws — which is what makes the pruning checkable rather than asserted.

None. Every combination of a term and a scope is a request somebody could make.

## 2 The Parameters

What a request may set alongside its payload. Each is a dimension of the condition space, and each of its
values is an ordinal.

| Parameter | What it controls | Type | Default |
|---|---|---|---|
| `mode` | whether a result is a pointer alone or carries the prose behind it | enum | `references` |
| `max-results` | how many results the answer carries | integer | a number design owes |
| `preview-length` | how many lines of a result's own prose a preview shows | integer | a number design owes |
| `rendering` | whether the answer is written for a person or for a parser | enum | `human` |

**Both integers have defaults that must exist, and design owes two numbers.** A caller who names no cap still
gets a bounded answer, and one who asks for previews and names no length still gets a preview of some length.
Neither is "unbounded", and that much is settled here.

### 2.1 `mode` Values

| Id | Value | Means |
|---|---|---|
| `mode.1` | `references` | each result is an addressable reference, its relevance and the word count that relevance was measured against |
| `mode.2` | `preview` | each result additionally carries the opening lines of its own prose |

`preview` exists to make choosing cheap. The Agent's whole problem is that reading a document to find out
whether it was worth reading is the cost it cannot afford (use case §1); a handful of lines per hit either
answers the question outright or points firmly at which reference to fetch.

### 2.2 `max-results` Values

| Id | Value | Means |
|---|---|---|
| `max-results.1` | `absent` | the caller names no cap, and the answer is bounded by the default |
| `max-results.2` | `<1` | a cap below one — a request for no results, which is not a search |
| `max-results.3` | `given` | a cap within range, and the answer is bounded by that |
| `max-results.4` | `>100` | a cap above the maximum the operation will honour |

### 2.3 `preview-length` Values

| Id | Value | Means |
|---|---|---|
| `preview-length.1` | `absent` | the caller names no length, and each preview is bounded by the default |
| `preview-length.2` | `<1` | a preview of no lines, which is a preview the caller did not ask for |
| `preview-length.3` | `given` | a length within range, and each preview is bounded by that |
| `preview-length.4` | `>10` | a length above the maximum the operation will honour |

### 2.4 `rendering` Values

| Id | Value | Means |
|---|---|---|
| `rendering.1` | `human` | the answer is written to be read |
| `rendering.2` | `machine` | the caller declares it will parse the answer |

### 2.5 Pruning Rules

| Rule | When | Then | are |
|---|---|---|---|
| **2.5.a** | `max-results` • `max-results.2` · `max-results.4` | all others | meaningless |
| **2.5.b** | `preview-length` • `preview-length.2` · `preview-length.4` | all others | meaningless |

**A number outside its range is refused, not clamped**, which is why those two rules silence everything rather
than only what the number would have bounded. Clamping would hand the caller an answer bounded by a number
they did not choose and could not see, which is the one thing a bounded answer must never do. The request ends
before anything is reached, so nothing else has a state.

**A length named without previews is not a rule**, because it prunes nothing. `preview-length` and `mode` are
independent knobs, so naming a length while asking for references is an ordinary thing for a caller to do. The
results come back in full, with a warning that the length was not used — failing would withhold a deliverable
answer over a parameter that changed nothing about it, and silence would leave the caller believing it
applied.

Those are the only interactions between the four.

## 3 The Dependencies

What lies beyond the boundary when the request arrives: a corpus of registered documents. Every state below is
one the Agent can perceive from its own side — what a registry had to do to reach it is not modelled here.

| Dependency | What it settles |
|---|---|
| `target` | whether the scope reaches a registry that can be searched at all |
| `shape` | what kind of node answered, and so what its result carries |
| `volume` | whether the answer is cut, against the cap the request carried |
| `extent` | whether a preview is cut, against the length the request carried |

### 3.1 `Document` Fixture

The corpus is expressed as records of one shape. A registration by
[1 — Register A Path](1-register-a-path.md) is what puts documents in it; this fixture describes what is there
afterwards, in the terms a search perceives.

```yaml
- registry: AgentPlugins
  path: /docs/procedures/eviction-procedures.md
  title: Eviction Procedures
  length: 240
  preview-lines: ["Eviction is covered in two places.", "This document is the procedural half."]
  word-count: 150
  relevance: null
  sections:
    - id: "2"
      title: Policies
      start-line: 40
      end-line: 120
      preview-lines: ["Policies are set centrally."]
      word-count: 80
      relevance: null
      sections:
        - id: "2.1"
          title: Cache Eviction
          start-line: 60
          end-line: 95
          preview-lines: ["Blah blah blah evict", "Blah blah policy", "Blady blah blah"]
          word-count: 30
          relevance: 0.3
    - id: rationale
      title: Why Eviction Is Centralised
      start-line: 200
      end-line: 240
      word-count: 90
      relevance: null
```

**Only what a result needs is required.** `registry` and `path` alone describe a document that is registered
and answers nothing, which is all it takes to show that unanswering documents are not returned:

```yaml
- registry: AgentPlugins
  path: /docs/unrelated.md
  relevance: null
```

Four such records with lower relevances than three others are all it takes to show that a cap of three returns
the best three. A record needs a `length` only where a preview has to run past it, an `end-line` only where a
preview has to stop short of one, and a `rationale` or `appendix` section only where the exclusion is what is
being shown.

**A document that answers is best given twice**: as a record, and as the document itself, so that the record's
`start-line`, `end-line`, `preview-lines` and `word-count` can be read against real prose rather than asserted.
The worked corpus [1 — Register A Path](1-register-a-path.md) already carries is where those come from.

#### 3.1.1 `Document` Aspects

* **registry:** - which registry holds it; empty means the registry the Agent is standing in. The set of
  values across the corpus is what registries there are to reach
* **path:** - where it lives — the only aspect every record must carry
* **title:** - what it is called
* **length:** - how many lines of prose it holds
* **preview lines:** - its own opening lines, which a preview of the whole document shows
* **word count:** - how much prose it holds, which is what a relevance was measured against
* **relevance:** - how well it answers a hypothetical term; empty means it does not answer
* **sections:** - the nodes within it, `appendix` and `rationale` among them
  * **id:** - `appendix`, `rationale`, or a section number
  * **title:** - what it is called
  * **start line:** - where its prose begins, which is what a preview of it opens at
  * **end line:** - where its prose ends, which is what a preview of it stops at however many lines were asked for
  * **preview lines:** - its own opening lines
  * **word count:** - how much prose it holds
  * **relevance:** - how well it answers a hypothetical term; empty means it does not answer
  * **sections:** - the nodes within it, nested the same way and to any depth

**`start line` and `end line` are what make two awkward cases expressible.** A preview of a document whose
`rationale` begins before the preview length runs out has to stop at the `rationale` rather than at the count;
a preview of a section shorter than the length asked for has to stop at the section. Both are questions about
where a node's prose ends, and neither can be asked of a record that does not say.

### 3.2 `target` States

| State | Means |
|---|---|
| `target.1` | `available` | the scope reaches one or more registries that can be searched |
| `target.2` | `unavailable` | it does not — a named scope no registry answers to, or no searchable registry where the Agent is standing |

`unavailable` is not an empty answer. A scope that reaches a registry holding nothing relevant is `available`
and answers `term` • `does-not-match`; the Agent's remedy there is to re-query. `unavailable` means the search
never ran, and the remedy is to correct the scope or to stand somewhere else.

### 3.3 `shape` States

| State | Means |
|---|---|
| `shape.1` | `document` | a whole document answers, carrying a relevance, and none of its sections answers separately |
| `shape.2` | `section` | a section answers, and carries the document and every section above it |

Both are returned by the same search and ranked against each other on their own merits. Relevance concentrated
in one section is best answered by that section; relevance spread thinly across a document is best answered by
the document, which is the only node that sees all of it.

### 3.4 `volume` States

| State | Means |
|---|---|
| `volume.1` | `within` | everything that answered fits the cap in force |
| `volume.2` | `beyond` | more answered than the cap admits, so the lowest-scoring are dropped |

### 3.5 `extent` States

| State | Means |
|---|---|
| `extent.1` | `within` | an answering node's prose ends before the preview length in force |
| `extent.2` | `beyond` | it runs past that length |

A node's prose ends where its `end line` says, which for a document may be where its `rationale` begins rather
than where the file does.

### 3.6 Pruning Rules

| Rule | When | Then | are |
|---|---|---|---|
| **3.6.a** | `target` • `target.2` | `term`, `shape`, `volume`, `extent` | meaningless |
| **3.6.b** | `term` • `term.1` | `shape`, `volume`, `extent` | meaningless |
| **3.6.c** | `mode` • `mode.1` | `extent` | meaningless |

**3.6.a** — nothing is searched where the target is unavailable, so there is nothing to match against, nothing
to shape, nothing to count and nothing to measure.

**3.6.b** — nothing is shaped, counted or measured where nothing answered.

**3.6.c** — `extent` is a question about previewed prose, so it has no state where the request asked for
references. It is the one rule that reaches across from a parameter to a dependency, which is why it lives
here rather than in §2.5: what it silences is a state of the corpus, not a knob.

Neither `max-results` nor `preview-length` is silenced by any of these. A cap and a length are in force
whatever the corpus holds; what varies with the corpus is only whether anything reached them, and that is
`volume` and `extent`.

## 4 The Condition Space

The product of §1, §2 and §3 once §1.3, §2.5 and §3.6 have pruned it.

### 4.1 Dimension Rank

Ranking can only happen here, because it is a judgement about all ten together and none of §1, §2 or §3 can
see the others. One dimension ranks above another when the second has something to say only once the first has
gone a particular way.

| Rank | Dimension | From | Ordinals |
|---|---|---|---|
| 1 | `max-results` | parameter | 4 |
| 2 | `preview-length` | parameter | 4 |
| 3 | `scope` | payload | 3 |
| 4 | `target` | dependency | 2 |
| 5 | `term` | payload | 2 |
| 6 | `shape` | dependency | 2 |
| 7 | `volume` | dependency | 2 |
| 8 | `mode` | parameter | 2 |
| 9 | `extent` | dependency | 2 |
| 10 | `rendering` | parameter | 2 |

The two integer parameters outrank everything because a request naming a number out of range never reaches a
registry: §2.5 silences all others under them, and a rule that silences everything must be asked first.
`scope` then outranks `target` because what the request named decides what "reachable" even means, and
`target` outranks `term` because there is nothing to match against until something is reachable.

`mode` sits between `volume` and `extent` rather than with the other parameters, because `extent` is a
question only a previewed answer can be asked (§3.6.c). The full cross product is
4 × 4 × 3 × 2 × 2 × 2 × 2 × 2 × 2 × 2 = **6144 combinations**.

### 4.2 Held Rather Than Drawn

Three dimensions earn fixtures rather than cells. Each is a claim that varying it changes nothing about what
the answer *is*, so drawing it would double the tree to say the same thing twice.

| Dimension | Held because |
|---|---|
| `rendering` | both values carry the same answer in the same order (§6.1); only the encoding differs |
| `max-results` | `max-results.1` and `max-results.3` differ only in whose number is in force, and a number nothing reached changed nothing — so it is held wherever `volume` • `volume.1` |
| `preview-length` | the same, wherever `extent` • `extent.1`, or wherever `mode` • `mode.1` |

`shape` is **not** held, and that is a claim worth reading carefully: a document answer and a section answer
carry different things — a title alone against the whole chain down to the section, each level with its own
word count — so the two are different answers and not one answer twice.

### 4.3 The Space

A node carrying `&` has the dimensions beneath it still to settle; a node carrying `-->` is a leaf, and names
the result §5 requires of it.

* **max-results**: *<1* · *>100* --> `refused`
* **preview-length**: *<1* · *>10* --> `refused`
* **max-results**: *absent* · *given* & **preview-length**: *absent* · *given* &
  * **scope**: *none-named* &
    * **target**: *unavailable* --> `no local registry`
    * **target**: *available* & *the answer names the registry by its location, and continues as below*
  * **scope**: *some-named* · *all-named* &
    * **target**: *unavailable* --> `unreachable scope`
    * **target**: *available* &
      * **term**: *does-not-match* --> `empty answer`
      * **term**: *matches* &
        * **shape**: *document* &
          * **volume**: *within* &
            * **mode**: *references* --> `answer`
            * **mode**: *preview* &
              * **extent**: *within* --> `answer, previewed`
              * **extent**: *beyond* --> `answer, previewed and cut`
          * **volume**: *beyond* &
            * **mode**: *references* --> `answer, truncated`
            * **mode**: *preview* &
              * **extent**: *within* --> `answer, truncated and previewed`
              * **extent**: *beyond* --> `answer, truncated, previewed and cut`
        * **shape**: *section* & *the same eight, each answer carrying the chain that places the section*

**Twenty-one leaves.** A leaf drawn under `max-results` • *absent* · *given* stands for both, as §4.2 says;
so does a leaf under `shape` • *section*, which repeats the eight drawn above it rather than adding new ones.

### 4.4 Reconciliation

Expanding the 6144 combinations and applying §2.5's and §3.6's five rules in §4.1's rank order leaves **390
cells**. Every one of those reaches exactly one of §5's ten result shapes, and every one of the ten is
reached:

| Result shape | Cells |
|---|---|
| `answer` · `answer, previewed` · `answer, previewed and cut` | 48 each |
| `answer, truncated` · `answer, truncated and previewed` · `answer, truncated, previewed and cut` | 48 each |
| `empty answer` | 48 |
| `unreachable scope` | 32 |
| `no local registry` | 16 |
| `refused` | 6 |

That much is checkable from the tables alone and holds. What does not yet close is the step from those 390
cells to §4.3's 21 leaves: §4.2's holds account for most of the difference and the tree's grouped ordinals for
the rest, but neither is stated precisely enough to be applied mechanically. Closing that is owed, and until
it is, the tree is a reading of the rules rather than a derivation from them.

**A length named without previews adds a warning, not a leaf.** `preview-length` • *given* with `mode`
• *references* carries a warning alongside whatever result its leaf already names (§2.5).

**What this space still owes.** `volume` and `extent` are relations between what the corpus holds and what the
request asked for rather than states the corpus has on its own, which is why they are drawn beneath the
parameters they answer to. Whether that is the right shape, or whether each pair should be one dimension with
the relation as its ordinals, is the question §4.1's ranking makes visible and does not settle.

## 5 The Results

What must be true of the answer at each leaf. Ten shapes, and nothing else is admissible.

| Result shape | What it represents |
|---|---|
| **answer** | the registries searched, named back, and every node that answered, ranked, each with its reference, its relevance and the word count that relevance was measured against |
| **answer, truncated** | the same, cut to the cap, ending in a count of what it did not name |
| **answer, previewed** | the same, each result carrying the opening lines of its own prose |
| **answer, previewed and cut** | the same, each cut preview ending in a count of the lines it did not show |
| **answer, truncated and previewed** | both bounds reached at once: a cut list of previewed results |
| **answer, truncated, previewed and cut** | both bounds reached and both declared |
| **empty answer** | the registries searched, named back, and nothing answered in them — not an error |
| **unreachable scope** | the scope as it was given, and that it could not be reached; nothing was searched |
| **no local registry** | that there is no searchable registry where the Agent is standing; nothing was searched |
| **refused** | the parameter that was out of range, and the range it is out of; nothing was searched |

### 5.1 `answer` Fixture

```
registries searched:
  @AgentPlugins

@AgentPlugins/docs/policies/eviction-policy            - 0.6 over 200 words
  - Company Eviction Policy
@AgentPlugins/docs/procedures/eviction-procedures$2.1  - 0.3 over 50 words
  - Eviction Procedures - 150 words
    - 2 Policies - 80 words
      - 2.1 Cache Eviction
```

#### 5.1.1 `answer` Aspects

* **registries searched:** - every registry the scope reached, named back — by the name the request gave, or
  by location where the request gave none
* **result rows:** - one per answering node, carrying its reference, its relevance and the word count that
  relevance was measured against
  * **ancestry:** - the document the node sits in and every section above it, each with its own word count
* **encoding:** - whether all of the above is written for a person or for a parser

### 5.2 `answer, truncated` Fixture

```
registries searched:
  @AgentPlugins
  @TheLoom

@AgentPlugins/docs/policies/eviction-policy            - 0.6 over 200 words
  - Company Eviction Policy

... (12 more matches)
```

#### 5.2.1 `answer, truncated` Aspects

Everything `answer` carries, and:

* **the count withheld:** - how many answering nodes the cap did not admit

### 5.3 `answer, previewed` And `answer, previewed and cut` Fixtures

```
@AgentPlugins/docs/procedures/eviction-procedures$2.1  - 0.3 over 50 words
  - Eviction Procedures - 150 words
    - 2 Policies - 80 words
      - 2.1 Cache Eviction
  Blah blah blah evict
  Blah blah policy
  Blady blah blah
  ... (5 more lines)
```

#### 5.3.1 Preview Aspects

Everything `answer` carries, and:

* **preview:** - the opening lines of that node's own prose
  * **the count withheld:** - how many lines the preview did not show, where it was cut

### 5.4 `empty answer` Fixture

```
registries searched:
  @AgentPlugins

nothing answered "eviction policy"
```

#### 5.4.1 `empty answer` Aspects

* **registries searched:** - as `answer`, because where it looked is what makes an empty answer actionable
* **encoding:** - as `answer`

### 5.5 `unreachable scope` And `no local registry` Fixtures

```
weaverdoc search "eviction policy" --scope @NoSuchProject
```
```
failed - scope unreachable
nothing searched

scope
- @NoSuchProject - not a registry this Agent can reach

remedy
- check the scope name
```

```
weaverdoc search "eviction policy"
```
```
failed - no registry here
nothing searched

remedy
- name a scope, or work somewhere a registry covers
```

#### 5.5.1 Failure Aspects

* **what was asked for:** - the scope as the request gave it, or that none was given
* **the reason:** - that it could not be reached, as against reaching a registry that answered nothing
* **encoding:** - as `answer`

### 5.6 `refused` Fixture

```
weaverdoc search "eviction policy" --max-results 0
```
```
failed - max-results out of range
nothing searched

max-results
- 0 given, must be between 1 and 100

remedy
- name a number in range, or none at all
```

#### 5.6.1 `refused` Aspects

* **the parameter named:** - which one was out of range, and what the caller gave for it
* **the range:** - what it must be between, so the remedy needs no documentation to find
* **encoding:** - as `answer`

## 6 Invariants

What must be true of the answer whatever the condition. Each is a feature of an aspect above, and is asserted
wherever that aspect is present.

### 6.1 `answer`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **An answer names every registry it searched** | by the name the request gave, or by location where it gave none. An answer that did not say where it looked is indistinguishable from one that looked in the wrong place | registries searched |
| **A result always carries a reference, a relevance and a word count** | what to read, how well it answered, and how much of it there is — the three facts needed to choose between results without reading any of them. A preview, where one was asked for, is carried in addition to these and never in place of any | result rows |
| **A relevance is a property of prose, not of its container** | the same prose scores the same however it was reached — whichever registry holds it, however many others were searched alongside, and whether it was named or arrived at by asking for everything | result rows |
| **An ancestry carries the whole chain down to the answering node** | the document, then every section above it, each with its own word count — complete, never partial, and for a whole-document answer that chain is the document alone | result rows / ancestry |
| **No rationale or appendix section ever answers** | whatever the query, their words were never registered, so there is nothing there for a query to reach | result rows |
| **Both renderings carry the same answer in the same order** | the encoding changes how an answer is written down and nothing about what it is | encoding |
| **The machine rendering names every field it has** | present and empty where there is nothing to report: a parser that must tell "absent" from "empty" is a parser that breaks on the empty case | encoding |

### 6.2 `answer, truncated`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A truncated answer names how many it did not show** | so an answer that was cut is never mistaken for one that was exhausted, which is the difference between having the answer and having the top of a pile | the count withheld |
| **Truncation ranks before it cuts** | everything that answered is ranked, and only then are the lowest dropped. It never samples, so what survives a cap is the best of what answered rather than the first of it | the count withheld |

### 6.3 Previews

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A preview names how many lines it did not show** | a preview runs to the length in force and stops; where the prose continues past it, the preview says how much it withheld, so how much is there is known without fetching it | preview / the count withheld |
| **No preview ever shows rationale or appendix content** | a preview stops where an excluded zone begins even when the caller asked for more lines than that leaves, because the exclusion outranks the request | preview |

### 6.4 `empty answer`

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **An empty answer is an answer** | it names where it looked and reports that nothing answered. It is not a failure, and the Agent's remedy is to re-query rather than to correct anything | registries searched |

### 6.5 Failures

| Invariant | The rule it defines | Aspect |
|---|---|---|
| **A failure says nothing was searched** | never a partial answer, and never an empty one. An answer drawn from a search that did not run is indistinguishable from one drawn from a search that did | the reason |
| **A failure names what it could not reach** | the scope as it was given, or that none was given — so the Agent can see what was not understood | what was asked for |
| **A refusal names the range it refused against** | a caller told only that a number was wrong has to guess twice; one told what it must be between has to guess once. The range is the operation's to know and costs nothing to say | the range |

## 7 Coverage

**Not yet claimable.** §4 records that its tree is owed, and until it is drawn there is no settled set of cells
to check every ordinal against, nor any cell for an invariant to be witnessed at. What can be said is that
every result shape in §5 is reached by some leaf of the sketch, and that every invariant in §6 is a feature of
an aspect some result shape carries.

# Rationale

**Why this document was rewritten.** Its first pass modelled the filesystem the CLI walks, the configuration
it reads, the registry root it looks for and the three calls it makes across the registry boundary. All of
that is how the behaviour is realised, and none of it is perceived by the Agent at step 4. An operation's
condition space is what may be varied in the request and what states the other side of the boundary may be
in — analysis is what must be true, not how it comes to be true. The withdrawn version is kept at
`notes/search-analysis-first-pass.md` for its fixtures and aspects, which were right about the artefacts even
where they were wrong about which artefacts belonged.

**Why a local search is a dimension and not a route.** The Agent chooses between naming a registry and
searching the one it is standing in, and it perceives the difference: a named registry is named back, a local
one has no name to give and is reported by its location. The two also fail differently and for different
reasons. What the Agent does not perceive is anything about how the local registry is found or made ready.

**Why an unreachable scope fails while an empty answer does not.** Both hand the Agent nothing, and the
difference is what to do next. A scope that reached a registry holding nothing relevant is an answer: re-query,
widen, or accept that the documentation does not cover this. A scope that could not be reached is not an answer
at all — nothing was searched, and re-querying would fail the same way forever.

**Why relevance is required to be about prose and not about its container.** It is what makes searching
several registries a single question rather than several. If relevance encoded anything about the document or
the registry around a piece of prose, results from different registries could only be ranked by merging
separate lists, and the Agent would have to reason about where a result came from before judging whether it
was any good.
