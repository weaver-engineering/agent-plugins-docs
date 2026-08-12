# CI/CD Pipeline & Branch Protection

AgentPlugins spans two repositories, each with its own GitHub Actions workflows and its own GitHub ruleset
(GitHub's current branch-protection mechanism, not the legacy per-branch settings). Neither was designed
specifically for AgentPlugins — both are inherited from patterns already established elsewhere in Weaver
Engineering, as noted in the [Architecture Definition Document](../architecture/architecture-definition-document.md), §6.

## Context
* [Architecture Definition Document](../architecture/architecture-definition-document.md) - §6 Codebase & Delivery Reference links here for full detail

## 1 agent-plugins-docs (Documentation)

A single workflow, `MainGate` (`.github/workflows/main-gate.yml`), triggers on every pull request targeting
`main`. It checks one thing: the head commit's message must start with a task reference (e.g. `WVR-93`) and
include a body description beneath the title. It reports the result as a `MainGate` commit status.

Branch protection is one GitHub ruleset, "Validate main commits", targeting `refs/heads/main`:
* requires a pull request (GitHub does not enforce a minimum approving-review count on this ruleset — `0` —
  though human review remains the practiced convention, not a mechanically enforced one)
* only the `squash` merge method is offered
* the `MainGate` status check must pass
* organization admins and repository admins can bypass, but only via the pull-request route, never a direct
  push to `main`

No branch-naming ruleset exists for this repo; any branch name may be created. This work uses `task/WVR-NNN`,
matching the convention observed elsewhere in this repo's history.

## 2 agent-plugins (Code)

This repo follows the same spec/test/build task-phases pipeline as the-loom itself, via two workflows:

* **Main Gate** (`.github/workflows/main-gate.yaml`) — triggers on pull requests targeting `main` from a
  `ready/{ref}` branch (full route: separate spec, test, and build commits) or a `task/{ref}` branch (quick
  route: a single commit). Runs `pnpm gate-check main-gate`, which validates commit structure, coverage
  thresholds, and a real `tsc` build.
* **Build Gate** (`.github/workflows/build-gate.yaml`) — triggers on pull requests targeting a `build/{ref}`
  branch from a `test/{ref}` branch. Runs `pnpm gate-check build-gate`, validating spec/test commit structure
  (including a fail-then-pass test progression), coverage, and build.

Both workflows are thin wrappers: the actual validation logic lives in the `gate-checks` CLI, not in the
workflow YAML.

Branch protection is three GitHub rulesets:
* **branch-naming-policy** — blocks creation of any branch whose name doesn't fall under `main`, `spec/**`,
  `test/**`, `task/**`, `build/**`, or `ready/**`. No one can bypass this rule.
* **build-protection** — targets `build/**`; requires a pull request with the `BuildGate` status check passing;
  only the `rebase` merge method is offered (not squash — `build/{ref}` accumulates the spec/test/build commit
  sequence that Main Gate later validates as a unit, so those commits must survive intact, not get squashed
  away before reaching `main`). Repository admins can always bypass.
* **main-protection** — targets `main`; requires a pull request with the `MainGate` status check passing; only
  the `squash` merge method is offered. Repository admins can always bypass.

**Known gap, as of this writing**: this repo does not vendor `gate-checks`/`task-phases` as its own packages —
per `agent-plugins/CLAUDE.md`, it expects them as global commands (`gate-checks`, `task`), the way every other
Weaver Engineering project is meant to consume them once WVR-53 ships them as installable packages. Until then,
neither command is available in this repo's CI, so `MainGate`/`BuildGate` will not actually pass here — a real,
currently open gap, not a hypothetical one.

## 3 Squash-On-Merge Enforcement

Enforced declaratively rather than procedurally: each ruleset's `allowed_merge_methods` setting restricts what
GitHub's own merge button will offer, so there is no separate enforcement step to design. `main-protection` and
`Validate main commits` (agent-plugins-docs) both allow only `squash`; `build-protection` allows only `rebase`,
for the reason given above.

## 4 Provisional Status

This entire setup is inherited precedent, not something designed specifically for AgentPlugins, and Weaver
Engineering intends to define an org-wide standard CI/CD pipeline (WVR-38, currently blocked on ADR-021) that
will supersede this project-specific one once it exists. This document is offered as seed content for that
effort — a real, currently operating (aside from the gate-checks gap noted above) instance of what "GitHub
Actions + gate-checks + rulesets" looks like in practice, for both a documentation-only repo and a code repo.
