# prune-the-cell

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* [Condition Model](../../datamodel/condition-model.md) §4.2 - the three ways a cell is pruned
* [Data Dictionary](../../datamodel/data-dictionary.md) §3.1 - presence and validity prune differently

## Purpose

Record that this combination does not arise. Pruning is what makes a condition space reviewable: an unpruned
space is the full product of every dimension's every value, most of which is mutually-exclusive nonsense, and no
architect can review it.

## Applies To

`uncovered-cell`, `no-suitable-fixtures`.

## What It Does

Establishes **which kind** of pruning this is, because they are not interchangeable:

| | Constrains | Prunes by |
|---|---|---|
| a **validity rule** on the input type | which combinations of values are possible | **impossibility** — the branch is removed |
| a **presence dependency** on a field | which fields exist in an instance | **irrelevance** — the subtree collapses and its parent becomes a leaf |
| an **architect exclusion** | this cell, by judgement | recorded with a reason |

The first two are written on the **type**, where they prune mechanically and re-derive. The third is written on
the cell, with its reason.

## Mechanical

No.

## What Must Be True Afterwards

* the cell's `status` is `pruned`;
* an architect exclusion carries a `pruneReason` — an exclusion with no reason is itself a finding;
* a rule-derived prune is expressed as a rule, so the same rule prunes the same branch again without anyone
  restating it.

## Notes For P6

**Prefer a rule to an exclusion wherever the reason is a general fact about the input.** A rule-derived prune is
re-derivable and converts a recorded judgement into something the model can check; an exclusion is not
re-derivable from anything, which is why it needs a reason at all. "Crypto payments cannot have manual capture"
is a validity rule, not an exclusion.

**This resolution can silently remove a requirement**, which is why it is offered alongside `state-the-fact`
rather than instead of it. A cell with no suitable fixtures may be a combination that cannot occur — or one
nobody has built a fixture for yet, and pruning it would quietly narrow what the design is claiming to cover.
The distinction is the whole judgement, and it should be asked before anything is written.
