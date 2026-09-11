# diagram-freshness

## Context
* [Workflow](../WORKFLOW.md) §4.8 - where this check is registered
* @docs/standards/design-layout-standards.md §6.1 - derived embedded diagrams and their metadata

## Purpose

Does every derived diagram still depict the design? Some derived views are most useful as pictures and are worth
having in the design for a human to review — an operation's call graph through the boundaries, the data model
reachable from one function. These are generated from the model, so they are subservient to the design's
claims, and once embedded in a document they can fall out of step with what they depict.

## Registration

| | |
|---|---|
| Stage | global |
| Model check | yes |
| Requires | [claim-competition](claim-competition.md) — a checksum over contested positions means nothing |

## What It Inspects

Every diagram carrying the two-field metadata in its own fenced-block frontmatter:

* a **key** — `{kind, target}` — naming what kind of diagram it is and the model address it was generated for;
* a **checksum** — a single aggregate over the claimed positions the generator read.

The generator resolves the key, reads the same positions again, and aggregates. A mismatch means the diagram no
longer depicts the design.

A diagram carrying no such metadata is an ordinary hand-drawn diagram — the design's own prose, authored like
any other content, never falsified against the model, and not inspected here.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `out-of-date-diagram` | a derived diagram's checksum no longer matches what it depicts | ● [regenerate](../resolutions/regenerate.md) |

**Global: it blocks nothing.** Whether a picture in a document still matches says nothing about whether the
design it depicts is complete or accurate.

## Settings

None.

## Notes For P6

**A single mechanical resolution, and nothing needs a human.** That is also why re-addressing may legitimately
trigger it — renaming an element changes the labels in the picture, so the picture really does need redrawing,
and redrawing costs nothing. This is the one place where the normalize-addresses-out rule does *not* apply, and
deliberately so.

**The positions are not fixed; the key is.** As the design evolves it may add a type to a signature or a
function to a path, so what the key resolves to changes — and the key never does. A manifest of positions would
have to be rewritten every time the design grew, and would be wrong in exactly the cases the checksum exists to
catch.

**This is not provenance, and the difference is directional.** Provenance points at prose and falsifies claims.
A derived diagram points at **claims** and falsifies **generated prose** — the picture itself. The metadata is
not a claim: it asserts nothing about the boundary, and it sits inside the fenced block so it cannot collide
with the document's `_claims` and a diagram can be moved between documents without disturbing either.
