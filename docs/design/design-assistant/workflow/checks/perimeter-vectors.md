# perimeter-vectors

## Context
* [Workflow](../WORKFLOW.md) §4.7 - where this check is registered
* [Deployable Model](../../datamodel/deployable-model.md) §3 - the five vectors and their endpoint kinds
* [Deployable Model](../../datamodel/deployable-model.md) §3.1 - every vector assessed or exempted
* [Deployable Model](../../datamodel/deployable-model.md) §3.2 - host and kernel

## Purpose

Has every one of the five vectors been answered? The interface perimeter is the formal boundary around the
running process: every vector through which data, state, execution triggers, control signals or configuration
enter or leave. Completeness at `M5` means every vector has been **considered**, not that every vector is
populated — and "considered" has to leave a record or it is not a claim.

## Registration

| | |
|---|---|
| Stage | maturity — `M5` |
| Model check | yes |
| Requires | [operation-identity](operation-identity.md) — an endpoint on an invocable vector exposes an operation |

## What It Inspects

Each of the five vectors, for **declared endpoints** or a **recorded exemption with a reason**:

| Vector | Carries |
|---|---|
| `network-and-invocation` | external invocation and response |
| `configuration-and-environment` | operational context injected at startup or runtime |
| `system-signals` | host and orchestrator control of the process lifecycle |
| `streams-and-telemetry` | outbound diagnostics |
| `host-and-kernel` | implicit inputs from the host |

And every endpoint's own attributes: `slug`, `vector`, `protocol`, `address`, `kind`, `direction`, and `exposes`
on the invocable vectors.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unassessed-perimeter-vector` | a vector has neither declared endpoints nor a recorded exemption | [state-the-fact](../resolutions/state-the-fact.md) · [exempt](../resolutions/exempt.md) |
| `unstated-required-attributes` | an endpoint is missing what `M5` requires of it | [state-the-fact](../resolutions/state-the-fact.md) |

Blocks `M5`.

## Settings

None.

## Notes For P6

**The kinds are enumerated rather than described, because that is what makes elicitation systematic.** "What are
this service's endpoints?" is an open question and gets an incomplete answer; "does it take CLI arguments, does
it read mounted files, does it publish messages?" is a finite walk with an answer per item. A CLI tool whose
primary invocation vector is `cli-argument` is exactly the case an open question loses.

The model stops at the enumeration and leaves **how** to ask to this workflow — which means the resolution prose
is where the elicitation actually lives, and it should adapt to what the perimeter already has rather than
walking all five from scratch every time.

**`host-and-kernel` exposes no endpoints and is still assessed.** What it holds is declared implicit
dependencies — a clock, a filesystem path, a file descriptor — and each becomes a `dependency-state` dimension
in the condition spaces of the operations that read it. It is the vector most likely to be forgotten and most
likely to cause the failures hardest to reproduce; declaring the dependency is what brings it into the condition
space where it can be covered.
