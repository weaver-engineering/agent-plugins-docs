# find-and-read-documentation — Find And Read The Documentation That Bears On A Task

**Actor:** [The Agent](../../user-personas/agent.md) — primary.
[The Architect](../../user-personas/architect.md) is a supporting actor: they author the documentation being
registered, and it is their instruction that starts the Agent working in the first place.
**Scope:** Covers reaching existing documentation — registering it, finding it, and reading the parts that matter.
It does not cover deciding what that documentation *says*
([document-a-concept](../document-a-concept/USE-CASE.md)) or how it is numbered
([number-document-sections](../number-document-sections/USE-CASE.md)) — see §7.

## Context
* [Examples](examples/EXAMPLES.md) - a corpus registered, searched and reported from, written down before
  analysis to expose how things vary; what the data model, dimensions and aspects are read off. Examples, not
  fixtures — they assert nothing
* [Agent Plugins index](../../../agent-plugins.md) - root index for this repo
* [The Agent](../../user-personas/agent.md) - primary actor; its memorylessness and context budget are why this
  use case exists
* [The Architect](../../user-personas/architect.md) - supporting actor
* [document-a-concept](../document-a-concept/USE-CASE.md) - the authoring use case whose output is registered here
* @docs/standards/documentation-standards.md/§3 - Document Shape, the structure registration records
* @docs/standards/documentation-standards.md/§4 - Indexing, the word and section content registration holds and
  the Rationale/Appendix exclusion steps 2 and 5 state, and §6's extension 7a turns on

## 1 Goal

The Agent reaches the current, curated truth on whatever subject its delegated work touches — and the
justification behind it where the work needs that too — by reading only the sections that actually bear on the
task, rather than reading whole documents, or guessing. **Where it cannot reach that truth, it learns what it
must fix in order to** — a path that is not there, a permission that blocks it — which is the same journey's
end by a different road rather than a failure of the use case.

Both halves of that are load-bearing, and they are separate problems (see
[The Agent §3](../../user-personas/agent.md)). The Agent cannot remember which document covers a subject, because
it remembers nothing between invocations. And it could not read them all even if it could remember them: its
context budget is finite, and every document read to find one relevant section is budget not spent on the work
itself. A capability that solved only recall would still leave it reading too much; one that only reduced reading
would still leave it reading the wrong things.

**The goal's closing clause — *learns what it must fix* — is a deliberate widening, recorded as one.** Without it, a registration that finds
nothing at the path is a dead end: no route to the goal, so by the method's own rule the use case may not name
it and nothing may be written about it. Those states are worth keeping, because they are where the applicable
stops being applicable and so are exactly what a condition space has to be drawn around. Widening the goal to
admit them is the honest way to keep them; the alternative is losing them here and rediscovering them at
design, after the analysis they should have informed was already written.

## 2 Trigger

The Agent is given work whose correct execution depends on documentation whose location it does not know.

## 3 Preconditions

* A corpus of documents complying with the documentation standard exists.
* A registry exists that can hold those documents' structure, their significant words, and their outstanding
  TODOs, and can return content located through it.

## 4 Main Success Scenario

1. Register a path

    **BOUNDARY:** the registry's registration surface, crossed with a path. Its shape is deliberately not
    guessed at: what invokes it — an actor, a commit hook, a watch on the corpus — is §7's second open
    question, and what it reaches is §7's first. Only the crossing itself is perceived here.

    **STATES:** [operations/1-register-a-path.md](operations/1-register-a-path.md) — the entry states this
    step admits, the state each establishes, and the fixture exposing each.

    The Architect, or The Agent on their behalf, authors or revises a document
    ([document-a-concept](../document-a-concept/USE-CASE.md)) and registers the path it lives under — one
    document, or a directory of them. The authoring half belongs to that use case, not this one: what this
    operation admits is the path, whatever produced what sits under it. Only markdown documents are registered;
    anything else under a directory path is not a document and takes no part in the registry, silently.

    **What is in scope is the caller's to say.** A directory's own subdirectories are descended into only when
    the caller asks, and then either to a depth they name or all the way down. Documents outside the scope that
    results are not registered, and that is the scope being honoured rather than anything going wrong.

    **Registering is absolute, never differential.** A path registered for the first time and one re-registered
    after every document beneath it changed are handled identically: what the registry *holds* afterward is
    computed from what is under the path now, never amended from what it held before. What the run *reports* is
    a separate question — it may say that a document has not changed since it was last registered, precisely so
    that re-registering a large, settled corpus does not report the whole of it back.

2. > The registry records, for each document in scope: its sections and figures with their titles, types and
   > positions; the significant words in each of them; and every outstanding TODO marker. Rationale and appendix
   > sections — and everything nested beneath them — are recorded as structure but not as words: they stay
   > addressable, and nothing they contain is ever matched by a search. Registrations whose source document no
   > longer exists are dropped in the same pass, so the registry describes what is there now rather than what
   > once was. A document in scope that cannot be read is named in the run's report rather than registered — the
   > rest register regardless, and nothing about it is left behind describing a document nobody could open.

3. > The Architect instructs The Agent to carry out work. The Agent knows the subject it has been given and has
   > no memory of which documents cover it.

4. Search the registry

    **BOUNDARY:** the registry's search surface, crossed with a query and a scope. The Agent is a systematic
    actor, so whatever this surface is, it is callable rather than presented — a CLI or an API, not a UI.
    Which of those, and what sits behind it, are not settled here (§7).

    **STATES:** [operations/4-search-the-registry.md](operations/4-search-the-registry.md) — the entry states
    this step admits, the state each establishes, and the fixture exposing each.

    The Agent searches the registry: a query, and a scope to search within. The scope may name one registered
    location, several at once, or every one the registry holds; naming none searches from where the Agent
    already is. Whichever it is, what comes back is one ranked set rather than one per location.

5. > The registry returns the documents and sections whose registered words match, ranked by relevance, each as
   > an addressable reference. A section and the document containing it are separate results, scored separately
   > and ranked against each other on their own merits. The ranking is answered from what registration
   > recorded, not by reading the corpus — and where the Agent asks for them, a short preview of each hit's own
   > opening lines comes back with it, so that choosing what to fetch costs a few lines rather than a document.
   > No rationale or appendix section is ever among the results, or inside a preview, whatever the query: their
   > words were never registered (step 2), so there is nothing there for a query to match.

6. > The Agent judges which of those documents and sections are actually worth reading. The ranking informs that
   > judgement; it does not make it, and the Agent is free to fetch any returned reference, or none.

7. Fetch the chosen references

    **BOUNDARY:** the registry's retrieval surface, crossed with references the Agent already holds — ones
    search returned, or ones it derived from them (7a). Callable rather than presented, for the same reason
    as step 4. Whether retrieval is the same surface as search or a separate one is exactly the kind of merge
    or split `Architect Solution` decides: this use case perceives two crossings and commits to nothing about
    how many surfaces answer them.

    **STATES:** [operations/7-fetch-references.md](operations/7-fetch-references.md) — the entry states this
    step admits, the state each establishes, and the fixture exposing each.

    The Agent fetches the references it chose — one, or several in a single crossing.

8. > The registry returns their verbatim source text, each with its **context path** — the chain of ancestors
   > from the document down to the section returned — so a section read on its own carries where it sits in the
   > document it came from, rather than arriving as free-floating prose.

9. > The Agent carries out the delegated work from what it fetched, and can state which documents and sections
   > that work rests on.

## 5 Postconditions

* Every document the registration actually covered is findable by its content, and none of the registry's
  entries describe a document that is no longer there. A document under the path that was *not* covered — out
  of the scope the caller asked for, not a markdown document, or impossible to read — is not findable either,
  and the run's own report is what distinguishes those from an omission.
* The Agent has the content that bears on its task, and has read no source document in full to get it — or,
  where it could not, holds a statement of what to fix specific enough to act on, rather than an absence it
  has to diagnose.
* Returned content is verbatim source text, never reconstructed from what the registry holds about it.
* Every returned section carries its context path.
* What the Agent acted on is traceable to current registered documents, not to recall.

## 6 Extensions

* **1a.** The path resolves directly to a document that is not markdown → it fails gracefully, naming the path
  and saying it is not a document this registry can hold. Registering a single path is registering exactly what
  is there; there is no directory to filter it out of. Cell in
  [operations/1-register-a-path.md](operations/1-register-a-path.md).
* **1b.** Nothing exists at the given path → it fails gracefully, naming the path and saying nothing was found
  there, which is the Agent learning what it must fix (§1). Cell in
  [operations/1-register-a-path.md](operations/1-register-a-path.md).
* **1c.** The path exists but cannot be read → it fails gracefully, and the message says so rather than
  reporting it as absent — the Architect's remedy (fix a permission) is different from 1b's (fix a path), and
  naming which is owed is what makes both routes to §1's goal rather than dead ends. Cell in
  [operations/1-register-a-path.md](operations/1-register-a-path.md).
* **2a.** A source document under the path has been deleted → its registration is removed, not left stale to be
  returned as a search result pointing at nothing.
* **4a.** The query matches nothing in scope → an empty result, not an error. The Agent re-queries with different
  terms or a wider scope rather than falling back to reading documents at random.
* **4b.** The scope names something the registry cannot resolve to any location at all → it fails gracefully,
  naming the scope. The Agent's remedy is to correct the scope, which is a different remedy from 4a's: there,
  the scope was right and the terms found nothing. Cell in
  [operations/4-search-the-registry.md](operations/4-search-the-registry.md).
* **7a.** The Agent needs justification rather than fact → it fetches the rationale by addressing it from the
  section that justifies it, rather than choosing it from among what search returned. Search never hands back a
  rationale reference (step 5), so what is fetched here is a reference the Agent derived from a returned section,
  not one it was offered.
* **8a.** A fetched reference no longer resolves, because the source document changed after it was registered →
  the fetch fails with the closest surviving match rather than a bare error, and the path is re-registered before
  the Agent proceeds.

## 7 Open Design Questions (not resolved by this use case)

* **Where the registry actually lives.** Files beside the documents they describe, a database, or a service
  another product calls — this use case requires a registry, not any particular one. That choice is exactly what
  varies between this product's own consumers and an enterprise deployment, and settling it here would foreclose
  the variation.
* **What triggers registration.** An actor invoking it, a commit hook, or a watch on the corpus. Step 1 says the
  path is registered, not who or what noticed it needed to be.
* **How far a bounded recursion can actually go.** Registration can descend not at all, to a caller-given
  depth, or without limit (`operations/1-register-a-path.md` §4.1). Whether a depth counts from something other
  than the registered path, and whether `unbounded` needs a cap against a real, possibly enormous tree, are not
  settled here.
* **Which relevance function, and its defaults.** A score measures how well one piece of prose answers the
  query, against that prose's own extent — so it says nothing about the document or the scope containing it,
  and scores from anywhere are ranked against each other directly
  (`operations/4-search-the-registry.md` §5). That much is required. Which function computes it is not: a
  starting point is matched words against total words, but a result matching several query terms is worth more
  than one matching a single term many times, and weighing coverage against frequency is left open. So are
  phrase matching, negation and conjunction, whether a caller may select between functions, and what the
  default result count and preview length actually are. One constraint on whatever is chosen: a term the query
  carries and the corpus does not must not annihilate a result some other term matched — it should count for
  nothing rather than reduce what its neighbours found, which rules out multiplying per-term scores together.
* **How much context path is enough** — ancestor titles, ancestor numbers, or both.
* **Step Contracts and operation condition spaces.** The second pass over these steps
  (@docs/workflows/feature-workflow/use-cases.md/§2.1) — which steps cross a boundary, and the condition space
  and fixtures each of those points at — is the gap WVR-203 closes for this use case; the other two still
  outstanding are `document-a-concept` and `evolve-a-design-to-maturity`. This supersedes the **Technical
  Interpretation** this bullet used to promise: WVR-202 retired that artefact in favour of Step Contracts stated
  on the steps themselves. The Technical Interpretations that existed before this rewrite were written in the
  vocabulary of one particular registry implementation (files named `.index/<slug>.words.yaml`), which is a
  solution and not a requirement — carrying them forward would have reintroduced under the Analysis label the
  very decision §7's first question exists to keep open. They were deleted rather than restored, and nothing
  written to close this gap may reintroduce that vocabulary.
