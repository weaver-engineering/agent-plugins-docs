# document-a-concept — Document A Project Concept

**Actor:** [The Architect](../../user-personas/architect.md) — primary; the concept being documented is theirs and
only they can settle what it means. [The Agent](../../user-personas/agent.md) is a supporting actor, conducting
the elicitation and doing the mechanical work that follows it.
**Scope:** Documentation only. Producing a specification or a design from a documented concept is a separate,
downstream use case — see §7.

## Context
* [Agent Plugins index](../../../agent-plugins.md) - root index for this repo
* [The Architect](../../user-personas/architect.md) - primary actor
* [The Agent](../../user-personas/agent.md) - supporting actor; performs the steps below on the Architect's behalf
* [number-document-sections](../number-document-sections/USE-CASE.md) - invoked at step 5
* [find-and-read-documentation](../find-and-read-documentation/USE-CASE.md) - the registration this use case's
  output feeds, and the search this use case's own step 3 relies on
* @docs/standards/documentation-standards.md/§2 - the structure a new document has to be filed into, and the
  glossary rule step 6 satisfies

## 1 Goal

A concept that exists only in the Architect's head — or whose documented form has gone stale as their
understanding moved on — exists as a current, standalone document, linked into the documentation around it, with a
PR open for review.

The Architect is not short of the understanding; they are short of the hours to write it down, link it up and
keep it consistent with everything already written, every time it changes. Undocumented, the concept is still
usable by the Architect and unusable by everyone and everything else: an agent cannot read what was never
written, and reconstructs it wrongly each time it needs it.

## 2 Trigger

The Architect has a concept in mind, scoped to a specific project, that is undocumented or whose documented form
has gone stale, and that future use cases, specifications or designs will need to reference. In practice this
usually surfaces as a `//TODO` marker left in the docs at the place the concept belongs, plus a tracked issue
referencing it.

## 3 Preconditions

* Either the concept exists only informally — in the Architect's head, or scattered across conversation and notes
  — with no document for it yet; or a document exists but no longer says what the Architect now understands.
* A tracked issue exists referencing the change, as branch protection requires for any commit to a docs repo. The
  issue typically points at the `//TODO` marker, which identifies both *what* is missing or stale and *where* it
  belongs; the full detail need not be in the issue, since the elicitation draws it out.
* The target project's docs repo has an established structure to link into — at minimum a glossary and an index
  document.

## 4 Main Success Scenario

1. The Architect invokes The Agent with the issue reference for the change.
2. The Agent resolves the issue to a target project and, where the issue references a `//TODO` marker, to the
   place in the docs repo the concept belongs.
3. The Agent establishes what is already documented at or near that place
   ([find-and-read-documentation](../find-and-read-documentation/USE-CASE.md)), so that an existing document is
   revised in place rather than duplicated alongside a second account of the same concept.
4. The Agent conducts an elicitation dialogue with the Architect, drawing out the concept's current definition,
   its boundaries, and its relationships to concepts and terms already documented.
5. The Agent drafts or revises the document, numbers its sections
   ([number-document-sections](../number-document-sections/USE-CASE.md)), and resolves and removes the `//TODO`
   marker that identified the gap.
6. The Agent links the document into what is already there: the glossary entry for the concept, cross-reference
   links to and from related documents, and registration in the project's index document.
7. The Agent registers the document
   ([find-and-read-documentation](../find-and-read-documentation/USE-CASE.md) step 1), so that what was just
   written is findable by the next agent that needs it — including, in a later session, itself.
8. The Agent commits the change on a branch, referencing the issue, and raises a PR.
9. The Architect reviews the PR. Approval is always theirs: no agent approves its own work.

## 5 Postconditions

* The concept exists as a current, standalone document in the target project's docs repo — newly created, or
  revised in place.
* The `//TODO` marker that identified the gap is resolved and removed.
* The document is linked from, and links to, the documentation around it: at minimum the glossary and the project
  index, and any related concept, decision or feature documents.
* The document is registered, and so is reachable by search rather than only by someone already knowing it exists.
* A PR is open against the docs repo, referencing the issue, awaiting human review.

## 6 Extensions

* **4a.** What the Architect describes conflicts with an existing glossary term or documented concept → The Agent
  surfaces the conflict and asks the Architect to resolve it — rename, merge, or explicitly supersede — before
  drafting continues. It is not the Agent's call to make, and quietly writing both leaves the corpus saying two
  things.
* **4b.** No index document exists yet for the project → treated as a gap to fill as part of this run, not a
  blocker.
* **6a.** Elicitation establishes the concept is already adequately documented → The Agent reports that and exits
  without committing.
* **7a.** Registration tooling does not exist yet (true as of this writing) → the document is left unregistered
  rather than registered by hand. Hand-written entries are discarded by the first full re-registration the tooling
  performs, so the effort buys nothing
  (@docs/standards/documentation-standards.md/§4).

## 7 Open Design Questions (not resolved by this use case)

* **Cross-project references.** A concept may need to reference one documented in a different project. Each
  project's docs exist both as a local repo in the workspace and canonically on GitHub, and a plain relative link
  resolves in only one of those. Needs a resolution strategy before cross-project linking is attempted; the first
  implementation assumes same-project links only.
* **Where concept documents live** — their own directory, alongside architecture documents, or elsewhere — is a
  design decision, not fixed here.
* **Producing specifications or designs from a documented concept** is a separate, downstream use case.
* **Responding to review comments** on the PR raised at step 8 is a use case in its own right. This one's
  postcondition is that a PR is open, not that it is merged, and it ends there.
* This use case's Technical Interpretation has not yet been written — see
  [find-and-read-documentation §7](../find-and-read-documentation/USE-CASE.md) for why the whole set is
  outstanding.
