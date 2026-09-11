# runtime-manifest

## Context
* [Workflow](../WORKFLOW.md) §4.7 - where this check is registered
* [Deployable Model](../../datamodel/deployable-model.md) §2 - the runtime manifest as an extension of the build manifest

## Purpose

Is every runtime setting stated or exempted? The `RuntimeManifest` **extends** the build manifest rather than
repeating it: what a codebase is written in, built with, constrained to and tested by is settled at `M2`,
because a Library needs all of it and is never deployed. What remains here is everything that only means
something for a **running process**.

## Registration

| | |
|---|---|
| Stage | maturity — `M5` |
| Model check | yes |
| Requires | [build-manifest](build-manifest.md) — this manifest extends that one |

## What It Inspects

Every `SettingKind` in the runtime enumeration:

| Dimension | Settings |
|---|---|
| `runtime` | `runtime-version`, `base-image` |
| `execution` | `execution-paradigm` |
| `frameworks` | `core-framework` |
| `wiring-and-infrastructure` | `persistence-driver`, `config-mechanism`, `observability-sdk` |
| `operational-scaffold` | `build-output-target`, `container-build-stages`, `healthcheck-command` |

Each stated or exempted. `ExecutionParadigm` is `long-running-server`, `ephemeral-worker`, `event-consumer`,
`scheduled-job`, or `wasm-module`.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unassessed-manifest-setting` | a runtime setting is neither stated nor exempted | [state-the-fact](../resolutions/state-the-fact.md) · [exempt](../resolutions/exempt.md) |

Blocks `M5`.

## Settings

None.

## Notes For P6

**Registered only for a `DeployableBoundary`.** None of these settings has a referent on a Library: there is no
image to base, no paradigm to execute under, nothing to wire to infrastructure and no health to probe. They are
not attributes a Library leaves blank — a Library is not a degenerate Service.

The manifest is authored, not derived. It is a set of decisions, and each dimension's content traces to the key
decision that made it.
