# design-declaration

## Context
* [Workflow](../WORKFLOW.md) §4.1 - where this check is registered
* [Serialization](../../serialization/SERIALIZATION.md) §3 - the design directory and its marker
* @docs/standards/design-layout-standards.md §1.1 - what `DESIGN.yaml` declares

## Purpose

Is this a design directory, and does it say where and what the design is? Nothing can be parsed until the scope
is decidable, and nothing can be assessed until the design names what it is assessed against.

This is the first check in the default configuration because every other one presupposes its answer.

## Registration

| | |
|---|---|
| Stage | pre-parse |
| Model check | no — it reads a file, before any model exists |
| Requires | — |

## What It Inspects

* whether the directory holds a `DESIGN.yaml` at its root;
* whether that file declares the **namespace** the design's addresses root in;
* whether a **check configuration** resolves — declared inline, named by pointer, or found by walking outward to
  the containing design, its Product, or the organisation.

The walk resolves *which* configuration applies; it never assembles one. Whichever is found is used whole, so
this check has no merging to do and no order of precedence to apply beyond stopping at the first one it reaches.

It does not read the design's documents, and it does not validate the configuration's contents — that is
[check-configuration](check-configuration.md).

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `not-a-design-directory` | no `DESIGN.yaml` at the root | [declare-the-design](../resolutions/declare-the-design.md) |
| `undeclared-namespace` | `DESIGN.yaml` names no namespace | [declare-the-design](../resolutions/declare-the-design.md) |
| `missing-check-configuration` | the walk outward reaches no configuration | [declare-the-design](../resolutions/declare-the-design.md) |

All three block every level, because a design that cannot be assessed has no maturity to reset.

## Settings

None.

## Notes For P6

The layout standard currently frames a missing configuration as **not a finding** — "a directory that cannot be
assessed" rather than work inside a design. Having a pre-parse stage is what makes it expressible as a finding
without contradicting that: it is still not work *inside* the design, and it is now reportable as the next unit
of work rather than as an exception outside the system. The standard's wording needs to follow.

Inheritance resolution — walking outward to a containing design, a Product, or an organisation — happens here,
and a pointer that resolves to nothing is a `missing-check-configuration` like any other.
