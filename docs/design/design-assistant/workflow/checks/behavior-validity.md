# behavior-validity

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §1.1 - validity is a property of fit, not only of contents
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §3.2 - what `invalid-behavior` catches
* [Reconciliation Model](../../datamodel/reconciliation-model.md) §6.4 - its two resolutions

## Purpose

Does every behavior still fit the cell it sits at? This is the one check in the model that compares an
**authored** artefact against the **structure** it depends on, and it exists because the ordinary invalidation
rule cannot reach that comparison by construction.

A required effect carries sourcing, not provenance, so no checksum ties it to the cell it was judged at. Narrow
a value's predicate, or insert a dimension above it, and the requirement was judged against a condition that no
longer obtains — while every provenance in sight is still fresh.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [cell-coverage](cell-coverage.md) — a cell with no behavior has nothing whose fit could be wrong |

## What It Inspects

For every behavior, whether it reconciles with:

* **the dimensions of its cell's condition space** — is the condition it was judged against the condition the
  cell now expresses;
* **its fixtures** — do they still expose the values its cell selects.

The fixture half is inert until fixtures exist at `M3`, and becomes live without the check being re-registered.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `invalid-behavior` | a behavior does not reconcile with its cell's dimensions or its fixtures | [re-express](../resolutions/re-express.md) · [remove-the-element](../resolutions/remove-the-element.md) |

Blocks `M1` — the checkpoint at which a behavior's own content becomes required.

## Settings

None.

## Notes For P6

**Never mechanical.** Which of the two resolutions is right is a judgement rather than a derivation, and both
leave the behavior `pending`: re-expression records something nobody has confirmed yet, so it cannot return
straight to approved.

**An approved behavior that becomes invalid loses its approval.** What the human agreed to was a behavior at a
cell that supported it, and the cell no longer does. That is not a fourth review state — the finding carries the
detail, and `pending` already says that nothing stands confirmed.

**Removal is the only route where the cell has ceased to exist**, pruned by a validity rule added later. It
inherits the higher confirmation bar: an unambiguous statement naming exactly what is being removed, never a
general nod at a batch — and it bites harder here, because the cell a removal frees may itself be gone.

This condition and `redesign-required` can hold at once and must not be collapsed: that one says the design
moved, this one says the requirement's context moved.
