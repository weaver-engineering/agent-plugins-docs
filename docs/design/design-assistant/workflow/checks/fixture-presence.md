# fixture-presence

## Context
* [Workflow](../WORKFLOW.md) §4.5 - where this check is registered
* [Behavior Model](../../datamodel/behavior-model.md) §3 - what a fixture is and what it attaches to
* [Condition Model](../../datamodel/condition-model.md) §2.1 - `fixtures` as the authored direction

## Purpose

Does every condition value that needs a fixture have one? A fixture is the concrete state that makes a condition
value real enough to trace against and, later, to test against. Without one there is nothing for a trace to run
against, which is why fixtures are required from `M3` and reconciliation is not meaningfully possible before
them.

## Registration

| | |
|---|---|
| Stage | maturity — `M3` |
| Model check | yes |
| Requires | [condition-space](condition-space.md) — fixtures attach to condition values |

## What It Inspects

* every condition value that needs a fixture names at least one;
* every fixture carries `slug`, `kind` (`seed`, `stub` or `mock`), `content`, and `standsFor` where its kind is
  `stub` or `mock`.

**The relationship is many-to-many and the value claims its fixtures.** One fixture exposes several values
across several dimensions — a single sample order payload exhibits a value of `order-value`, of
`customer-state` and of `payment-method` at once — and one value is exposed by several fixtures. The fixture
carries no pointer back.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `missing-fixture` | a condition value that needs a fixture has none | [state-the-fact](../resolutions/state-the-fact.md) |
| `unstated-required-attributes` | a fixture is missing what `M3` requires of it | [state-the-fact](../resolutions/state-the-fact.md) |

Blocks `M3`.

## Settings

None.

## Notes For P6

This is the **value-level** check. [fixture-suitability](fixture-suitability.md) is the combination-level one,
and it can fire while every value here is individually covered — which is why both exist.

The fixture claim and the fixture content live in different places: the claim belongs with whatever defines the
condition, and the content is a file the design points at with a checksummed reference rather than parses. A
file carrying no claims is data with a schema of its own, and nothing is written into it.

Reuse is the normal case rather than a sign of redundancy. Fixtures are shared across values *precisely because*
they carry the same characteristics, so the resolution should look for an existing fixture that already exhibits
the value before authoring a new one.
