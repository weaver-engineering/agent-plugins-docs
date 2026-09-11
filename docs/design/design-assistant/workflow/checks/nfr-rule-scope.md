# nfr-rule-scope

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §7.2 - rules are inherited, selections are not
* [Condition Model](../../datamodel/condition-model.md) §5 - what an `NfrRule` is

## Purpose

Which NFR rules is this design in scope of? The scope resolves by walking outward from the design's directory to
the Product that owns it and reading that Product's pointer to its rule definitions. Without an answer,
[nfr-assessment](nfr-assessment.md) has nothing to assess against — not because the design is wrong, but because
nobody has said what the rules are.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes — the scope reference is a fact the design records |
| Requires | [boundary-identity](boundary-identity.md) — the walk starts from an identified design target |

## What It Inspects

* whether the outward walk reaches a Product;
* whether that Product carries a pointer to its NFR rule definitions;
* whether the design defines rules of its own, or inherits any from a containing design target.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unresolved-nfr-scope` | the walk finds no Product, or a Product with no NFR rule pointer | [state-the-fact](../resolutions/state-the-fact.md) · [acknowledge](../resolutions/acknowledge.md) |

**Advisory.** An unresolvable scope must not block design: a boundary being designed ahead of the Product that
will own it is an ordinary state, and waiting for a pointer somebody else has to write would stop work for a
reason that has nothing to do with the design. What it may do is require an answer — supply the pointer, or
declare the rules this design applies, which may legitimately be none — and an acknowledgement records that the
declaration was made deliberately.

Left neither answered nor acknowledged, it blocks `M4` like any advisory finding.

## Settings

None.

## Notes For P6

A locally-declared rule set is a real answer and not a fallback. A design target may define rules of its own,
and those are in scope for anything it contains — so "there is no Product yet, and these are the rules I am
holding myself to" is a complete resolution.

The declaration is reconcilable from the Product's side later: when a Product does arrive with a rule catalog,
every design in scope acquires whatever it did not already assess, which surfaces through
[nfr-assessment](nfr-assessment.md) as ordinary work.
