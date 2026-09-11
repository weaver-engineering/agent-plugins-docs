# cell-exclusions

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Condition Model](../../datamodel/condition-model.md) §4.2 - the three ways a cell is pruned

## Purpose

Does every cell the architect excluded say why? A cell pruned by a validity rule or by a presence dependency is
re-derivable — the rule is in the model and will prune the same branch again. An architect's exclusion is not
re-derivable from anything, so without a recorded reason it is indistinguishable from a branch nobody has looked
at yet.

That difference is the whole of what a coverage claim rests on.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [condition-space](condition-space.md) — the cells to inspect |

## What It Inspects

Every cell whose `status` is `pruned` by architect exclusion rather than by a validity rule or a presence
dependency, and whether it carries a `pruneReason`.

Rule-derived and irrelevance-derived prunes are not inspected: they are mechanical, and their reason is the
rule.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unexplained-exclusion` | a cell is excluded by the architect with no recorded reason | [state-the-fact](../resolutions/state-the-fact.md) · [correct-the-design](../resolutions/correct-the-design.md) |

Blocks `M1`.

## Settings

None.

## Notes For P6

`correct-the-design` is the route where the exclusion turns out to be wrong — the combination does arise, and
the cell should be valid and covered rather than pruned. The resolution should offer that as a real alternative
rather than assuming the exclusion stands and only its reason is missing.

Where the reason turns out to be a general fact about the input rather than a judgement about this cell, it
belongs in a validity rule on the type instead, which prunes mechanically and re-derives. That converts a
recorded judgement into something the model can check, and is the better outcome wherever it is available.
