# declare-the-design

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Serialization](../../serialization/SERIALIZATION.md) §3 - the design directory and its marker
* @docs/standards/design-layout-standards.md §1.1 - what `DESIGN.yaml` declares

## Purpose

Write the `DESIGN.yaml` that says where and what this design is. Scope must be decidable **before** parsing —
parsing is defined over a scope, so a scope inferred from parsed content would be circular — and the same is
true of the check configuration, which decides what the positions in a design even mean.

## Applies To

`not-a-design-directory`, `undeclared-namespace`, `missing-check-configuration`.

## What It Does

Creates or completes the `DESIGN.yaml` at the directory's root, declaring:

* the **namespace** the design's addresses are rooted in;
* the **check configuration** the design is assessed against — stated inline, named by pointer, or left for the
  walk outward to resolve against the containing design, its Product, or the organisation.

**The structure is taken whole.** A configuration declares its own checks and levels or references another's,
never both, so this resolution never assembles one from a container's plus some local additions.

**Moving a threshold does not need a fork.** Where all a design wants is a different budget, the configuration
it declares is a `reference` to the one it would otherwise have resolved plus the settings it overrides — three
lines, and the design is still assessed by exactly the same checks and levels as everything else under that
configuration ([Workflow](../WORKFLOW.md) §3.4).

## Mechanical

No — though the ordinary case is nearly so, because a contained design usually needs to say nothing at all and
lets the walk find its container's.

## What Must Be True Afterwards

* the directory is a design directory, and the scope walk stops at any subdirectory holding its own
  `DESIGN.yaml`;
* the configuration resolves, and [check-configuration](../checks/check-configuration.md) can validate it;
* the file makes **no claims** — it is a support file, read as configuration before parsing begins, and never
  assessed.

## Notes For P6

**Neither declaration can be a claim, and both are circular in the same way.** The namespace is what every
claim's address resolves against, so a claim declaring it would need an address in the namespace that same claim
is establishing. The configuration determines which checks run, and the checks are what give positions their
meaning, so a claim declaring it would sit at a position the configuration has not yet licensed.

Keeping the file outside the claim mechanism entirely is what stops this being a special case in the parser —
and it removes the bootstrapping question of how the file defining a design's scope comes to be attested.

**No configuration is a failure, not a default.** A design directory that does not say what it is checked
against cannot be assessed at all, and inventing a default here would produce a maturity claim whose real
content nobody can recover.

This is the first resolution most new designs will meet, so its prose is effectively the front door of the whole
workflow.
