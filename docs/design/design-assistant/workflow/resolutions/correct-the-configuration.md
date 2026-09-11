# correct-the-configuration

## Context
* [Workflow](../WORKFLOW.md) §3.3 - required checks as a configuration constraint
* [Workflow](../WORKFLOW.md) §2.2 - model checks and non-model checks

## Purpose

Fix the check configuration so it can be run. A configuration is data a project writes, so it can be wrong in
ways that have nothing to do with the design being assessed — and every one of those faults would otherwise
surface as a confusing result from some later check.

## Applies To

`invalid-check-configuration`.

## What It Does

Corrects whichever fault was reported:

| Fault | Fix |
|---|---|
| a named check does not resolve | correct the name, or install the package providing it |
| a required check is not registered | register it |
| a required check is registered **later** | move it earlier |
| `requires` has a cycle | break it — one of the two checks does not actually depend on the other |
| a **model check** is registered pre-parse | move it into a maturity stage, or replace it with a non-model equivalent |
| the configuration both declares its structure and references another | drop one; the structure is taken whole |
| the `reference` chain does not resolve, or cycles | correct the pointer, or break the cycle |
| a setting path collides with the configuration's own fields | move the setting under a path of its own |
| two checks declare one path with different types | give them separate paths, or reconcile the types |
| a required setting has no value anywhere in the chain | set it in the nearest configuration |
| a value has the wrong type, or reads a path no check declares | correct it, or register the check that reads it |

## Mechanical

No. Each fault has an obvious shape and a judgement about which end to change.

## What Must Be True Afterwards

* every registered check resolves, with its requirements registered earlier and no cycle;
* the pre-parse stage holds only non-model checks;
* the registration order is itself a valid order, so the sequence a reader sees is the sequence that runs.

## Notes For P6

**A cycle in `requires` is the one fault that is usually a modelling error rather than a typo.** Two checks that
each need the other's answer generally means one of them is doing two jobs, and the fix is to split it rather
than to break the edge arbitrarily.

The ordering rule is deliberately stricter than the dependency graph requires: a topological sort would accept
more configurations, and would let a reader see one order while another ran. Legibility is most of what makes a
configuration reviewable, so the stricter rule is the point rather than an implementation convenience.
