# find-and-read-documentation — Find And Read The Documentation That Bears On A Task

**Actor:** [The Agent](../../user-personas/agent.md) — primary.
[The Architect](../../user-personas/architect.md) is a supporting actor: they author the documentation being
registered, and it is their instruction that starts the Agent working in the first place.
**Scope:** Covers reaching existing documentation — registering it, finding it, and reading the parts that matter.
It does not cover deciding what that documentation *says*
([document-a-concept](../document-a-concept/USE-CASE.md)) or how it is numbered
([number-document-sections](../number-document-sections/USE-CASE.md)) — see §7.

## Context
* [Agent Plugins index](../../../agent-plugins.md) - root index for this repo
* [The Agent](../../user-personas/agent.md) - primary actor; its memorylessness and context budget are why this
  use case exists
* [The Architect](../../user-personas/architect.md) - supporting actor
* [document-a-concept](../document-a-concept/USE-CASE.md) - the authoring use case whose output is registered here
* @docs/standards/documentation-standards.md/§3 - Document Shape, the structure registration records
* @docs/standards/documentation-standards.md/§4 - Indexing, the word and section content registration holds and
  the Rationale/Appendix exclusion §6's extension 6b turns on

## 1 Goal

The Agent reaches the current, curated truth on whatever subject its delegated work touches — and the
justification behind it where the work needs that too — by reading only the sections that actually bear on the
task, rather than reading whole documents, or guessing.

Both halves of that are load-bearing, and they are separate problems (see
[The Agent §3](../../user-personas/agent.md)). The Agent cannot remember which document covers a subject, because
it remembers nothing between invocations. And it could not read them all even if it could remember them: its
context budget is finite, and every document read to find one relevant section is budget not spent on the work
itself. A capability that solved only recall would still leave it reading too much; one that only reduced reading
would still leave it reading the wrong things.

## 2 Trigger

The Agent is given work whose correct execution depends on documentation whose location it does not know.

## 3 Preconditions

* A corpus of documents complying with the documentation standard exists.
* A registry exists that can hold those documents' structure, their significant words, and their outstanding
  TODOs, and can return content located through it.

## 4 Main Success Scenario

1. The Architect, or The Agent on their behalf, authors or revises a document
   ([document-a-concept](../document-a-concept/USE-CASE.md)) and registers the path it lives under — one document
   or a directory of them.
2. The registry records, for each document under that path: its sections and figures with their titles, types and
   positions; the significant words in each of them; and every outstanding TODO marker. Registrations whose source
   document no longer exists are dropped in the same pass, so the registry describes what is there now rather than
   what once was.
3. The Architect instructs The Agent to carry out work. The Agent knows the subject it has been given and has no
   memory of which documents cover it.
4. The Agent searches the registry: a query, and a scope to search within.
5. The registry returns the documents and sections whose registered words match, ranked by relevance, each as an
   addressable reference — without any source document having been read.
6. The Agent judges which of those documents and sections are actually worth reading. The ranking informs that
   judgement; it does not make it, and the Agent is free to fetch any returned reference, or none.
7. The Agent fetches the references it chose.
8. The registry returns their verbatim source text, each with its **context path** — the chain of ancestors from
   the document down to the section returned — so a section read on its own carries where it sits in the document
   it came from, rather than arriving as free-floating prose.
9. The Agent carries out the delegated work from what it fetched, and can state which documents and sections that
   work rests on.

## 5 Postconditions

* Every document under a registered path is findable by its content, and none of the registry's entries describe
  a document that is no longer there.
* The Agent has the content that bears on its task, and has read no source document in full to get it.
* Returned content is verbatim source text, never reconstructed from what the registry holds about it.
* Every returned section carries its context path.
* What the Agent acted on is traceable to current registered documents, not to recall.

## 6 Extensions

* **1a.** The path has never been registered → no different from re-registering a changed one; registration
  computes what is true now rather than diffing against what it held before.
* **2a.** A source document under the path has been deleted → its registration is removed, not left stale to be
  returned as a search result pointing at nothing.
* **4a.** The query matches nothing in scope → an empty result, not an error. The Agent re-queries with different
  terms or a wider scope rather than falling back to reading documents at random.
* **4b.** The scope spans repos with no shared relevance baseline — very different document sizes or densities →
  results are still returned, but scores are not comparable across them. Not resolved here (§7).
* **6a.** The Agent needs justification rather than fact → rationale is deliberately excluded from what search
  matches on, so it is never *found* by searching. It is reached by fetching it from the section it justifies,
  which is why registration records the structure of rationale sections even though it excludes their words.
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
* **Relevance.** Which algorithm ranks results, whether the caller can select between algorithms, and how many
  results and how much preview a search returns by default.
* **Cross-scope comparability** (extension 4b) — whether scores from different repos can be made comparable at
  all, or whether the honest answer is to rank within each and merge.
* **How much context path is enough** — ancestor titles, ancestor numbers, or both.
* **Technical Interpretation.** Not yet written, here or for the other two use cases. The versions that existed
  before this rewrite were written in the vocabulary of one particular registry implementation (files named
  `.index/<slug>.words.yaml`), which is a solution, not a requirement — carrying them forward would have
  reintroduced under the Analysis label the very decision §7's first question exists to keep open. They are to be
  rewritten, not restored.
