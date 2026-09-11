# check-configuration

## Context
* [Workflow](../WORKFLOW.md) §3.3 - required checks as a configuration constraint
* [Workflow](../WORKFLOW.md) §4.1 - where this check is registered
* [design-declaration](design-declaration.md) - the configuration this check validates

## Purpose

Is the configuration itself runnable? A configuration is data a project writes, so it can be wrong in ways that
have nothing to do with the design — and every one of those faults would otherwise surface as a confusing
result from some later check rather than as the configuration error it is.

## Registration

| | |
|---|---|
| Stage | pre-parse |
| Model check | no — it reads the configuration, not the design |
| Requires | [design-declaration](design-declaration.md) — there is no configuration to validate until one is found |

## What It Inspects

* every check named by the configuration resolves to a check that exists;
* every check's `requires` are registered, and registered **earlier** in the sequence;
* `requires` contains no cycle;
* no **model check** is registered pre-parse ([Workflow](../WORKFLOW.md) §2.2);
* the configuration declares its own checks and levels **or** references another's, never both;
* the `reference` chain resolves and contains no cycle;
* no setting path begins with a field the configuration itself defines — `pre-parse-checks`, `maturity-levels`,
  `global-checks`, `reference` ([Workflow](../WORKFLOW.md) §3.4);
* two registered checks declaring the **same** path agree on its type;
* every setting a registered check declares **without a default** has a value somewhere in the chain;
* every value in the chain is of the declared type, and names a path some registered check actually reads.

It does not police anything else in `DESIGN.yaml`. The file may carry further attributes its product requires,
and those are outside this contract.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `invalid-check-configuration` | any of the above fails | [correct-the-configuration](../resolutions/correct-the-configuration.md) |

One finding per fault, each naming the registration at issue. Blocks every level.

## Settings

None.

## Notes For P6

This is the check that makes `requires` worth having: without configuration-time validation, a missing
prerequisite would only show up as a check being skipped forever, which reads as "nothing to do here" rather
than as a mistake.

The ordering rule is deliberately stricter than the dependency graph needs — a topological sort would accept
more configurations. Requiring the registration order to already be a valid order means the sequence a reader
sees in the configuration is the sequence that runs, which is most of what makes the configuration legible.
