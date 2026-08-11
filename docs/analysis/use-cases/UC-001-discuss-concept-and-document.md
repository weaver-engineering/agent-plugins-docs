# UC-001 — Discuss A Project Concept And Document It

**Actor:** [The Architect](../user-personas/architect.md)
**Scope:** Documentation only. Producing a specification or design from a
documented concept is out of scope — see §7.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [The Architect](../user-personas/architect.md) - the actor for this use case

## 1 Goal

Capture a concept that currently exists only in the architect's head as a
documented artifact in a project's docs repo, correctly linked into that
project's existing documentation, with a PR raised for review.

## 2 Trigger

The architect has a concept in mind, scoped to a specific project (e.g.
MagpieWeaver, TheLoom, AgentPlugins itself), that is undocumented or whose
documented understanding has evolved and gone stale, and that future use
cases, specs, or designs will need to reference for context. In practice
this is usually surfaced as a `//TODO` tag left in the docs at the relevant
location, plus a Linear issue referencing it (see §3) — e.g.
`workflows/feature-workflow/use-cases.md` in `weaver-engineering/docs`
currently reads `//TODO - Define what a use case is`.

## 3 Preconditions

* Either:
  1. the concept exists only informally (in the architect's head, or
     scattered across conversation/notes) — no documented artifact exists
     yet; or
  2. a documented artifact for the concept already exists, but the
     architect's understanding has evolved and the artifact is now stale.
* A Linear issue exists referencing the change — required by branch
  protection for any commit to a docs repo. The issue typically points to
  the `//TODO` tag from §2, which identifies both *what* concept is
  missing or stale and *where* it belongs; the full detail doesn't need to
  be captured in the issue since the elicitation dialogue (§4) draws it out.
* The target project's docs repo has an established structure to link into
  (at minimum a glossary and an index/overview doc — see `magpieweaver-docs`
  for the reference shape).

## 4 Main Success Scenario

1. Architect invokes the concept-capture tool/sub-agent with the Linear
   issue reference for the change (e.g. `WVR-83`).
2. Sub-agent resolves the issue to a target project and, where the issue
   references a `//TODO` tag, the specific location in the docs repo the
   concept belongs.
3. Sub-agent checks whether a documented artifact for the concept already
   exists at or near that location.
   1. If none exists, one will be created.
   2. If one exists, it will be updated in place rather than duplicated.
4. Sub-agent conducts an elicitation dialogue with the architect, drawing
   out the concept's current, evolved definition, boundaries, and
   relationships to existing documented terms and concepts.
5. Sub-agent drafts (or revises) the concept documentation artifact,
   resolving and removing the `//TODO` tag that identified the gap.
6. Sub-agent identifies related existing artifacts in the project's docs
   repo and:
   1. adds or updates the relevant Glossary entry;
   2. adds cross-reference links between the artifact and related
      artifacts (bidirectional — the artifact links out, and the related
      docs link back);
   3. registers the artifact in the project's index/overview doc, if not
      already registered.
7. Sub-agent generates the artifact's section index (UC-003) and word index
   (UC-004): `.index/<slug>.sections.yaml` and `.index/<slug>.words.yaml`.
8. Sub-agent commits the changes, referencing the Linear issue, on a branch
   in the project's docs repo.
9. Sub-agent raises a PR against the docs repo for the architect to review.

## 5 Postconditions

* The concept exists as a current, standalone documented artifact in the
  target project's docs repo — newly created, or updated in place if one
  already existed.
* The `//TODO` tag that identified the gap has been resolved and removed.
* The artifact is linked from, and links to, the relevant existing
  documentation (at minimum: Glossary, project index/overview doc; where
  applicable: related concept docs, ADRs, feature docs).
* A PR is open against the docs repo containing the change, referencing the
  Linear issue, awaiting human review. PR approval is always a human
  action, never automated (see the weaver-engineering workspace rule that
  agents may never approve PRs).
* The artifact's `.index/<slug>.sections.yaml` and `.index/<slug>.words.yaml`
  exist (see step 7).

## 6 Extensions

* **2a.** The architect's description conflicts with an existing glossary
  term or documented concept → sub-agent surfaces the conflict and asks the
  architect to resolve it (rename, merge, or explicitly supersede) before
  drafting continues.
* **4c.** No index/overview doc exists yet for the project → treated as a
  gap to fill as part of this run, not a blocker.
* **6a.** Nothing to change after elicitation (concept turns out to already
  be adequately covered) → sub-agent reports this and exits without
  committing.
* **7a.** UC-003/UC-004 tooling doesn't exist yet (true as of this writing)
  → `.index/` files are hand-written as a temporary substitute; still
  required, not skipped.

## 7 Open Design Questions (not resolved by this use case)

* **Cross-project references.** A concept may need to reference a concept
  documented in a *different* project (e.g. an AgentPlugins concept
  referencing something in MagpieWeaver). Each project's docs exist both as
  a local repo in the weaver-engineering workspace and in their canonical
  form on GitHub — a plain relative markdown link only resolves in one of
  those two contexts. Needs a resolution strategy before cross-project
  linking is attempted. The first implementation of this use case should
  assume same-project links only.
* **Where concept docs live.** Whether concepts get their own
  `docs/concepts/` area, live alongside architecture docs, or something
  else, is a design decision for the downstream design doc — not fixed
  here.
* **Producing specs/designs from a documented concept** is a separate,
  downstream use case; this one stops at "documented and linked."
* **Responding to PR review comments** on the PR raised in §4 step 9 is a
  distinct use case in its own right — this one's postcondition is "a PR is
  open," not "the PR is merged," and it ends there.
