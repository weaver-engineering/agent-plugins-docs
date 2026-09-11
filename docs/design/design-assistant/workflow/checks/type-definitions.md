# type-definitions

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Data Dictionary](../../datamodel/data-dictionary.md) §1, §2 - the dictionary's scope and what a type carries
* [Data Dictionary](../../datamodel/data-dictionary.md) §3, §4 - fields, presence dependencies and validity rules

## Purpose

Is every shape that crosses a boundary defined? The dictionary exists so that contracts are unambiguous and so
that condition dimensions can be derived from real value sets — and neither purpose is served by a type that is
only ever a name in a signature.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [function-placement](function-placement.md) — what crosses a boundary follows from visibility and interfaces |

## What It Inspects

Every type in the design target's dictionary — the view over every type defined in its own scope — for `slug`,
`purpose`, `kind`, and the attributes its kind implies: `fields` for a structure, `values` for an enum,
`elementType` for a collection, and `rules` where any apply.

Its obligation is scoped to what **crosses** a boundary: in and out through the design's own perimeter
operations, in and out through its dependency boundaries, and across the perimeters of its own contained
boundaries. Shapes used only by a boundary's `private` functions still have types; the dictionary makes no
completeness claim about them.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unstated-required-attributes` | a type that crosses a boundary is missing what `M2` requires of it | [state-the-fact](../resolutions/state-the-fact.md) · [take-a-decision](../resolutions/take-a-decision.md) |

Blocks `M2`.

## Settings

None.

## Notes For P6

An `external` type — one owned by a depended-on boundary and referenced rather than defined — is a complete
answer, not a gap. It states both facts that matter: the shape is known, and it is not ours to change.

Validity rules and presence dependencies are worth eliciting here rather than later, because they are what
prunes an operation's condition space. A prose constraint contributes nothing to the coverage claim: it cannot
prune anything. A field-local bound is the degenerate rule with an empty `if`, and there is deliberately no
separate per-field constraint type to state it twice, differently.
