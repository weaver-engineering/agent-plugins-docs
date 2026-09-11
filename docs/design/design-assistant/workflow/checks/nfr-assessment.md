# nfr-assessment

## Context
* [Workflow](../WORKFLOW.md) §4.3 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §7.3 - assessment or exemption, and why there is no third state
* [Boundary Model](../../datamodel/boundary-model.md) §7.1 - rules and the associations that apply them
* [Condition Model](../../datamodel/condition-model.md) §5 - a rule as a generator into the condition space

## Purpose

Is every rule in scope applied or exempted? A design with no auth boundary and a design that has decided none of
its functions need one are indistinguishable if silence is permitted, and the difference is the whole point of
the assessment.

This is also what makes a Product adding a rule propagate mechanically: every design in scope acquires an
unassessed rule, which surfaces here as work rather than relying on anyone remembering to revisit designs that
were finished.

## Registration

| | |
|---|---|
| Stage | maturity — `M1` |
| Model check | yes |
| Requires | [nfr-rule-scope](nfr-rule-scope.md) · [element-identity](element-identity.md) — the rules to assess, and the cross-cutting boundaries that apply them |

## What It Inspects

For every rule in the design's scope, that the design either

* **applies** it — a cross-cutting boundary of the rule's own kind declares it in `applies`; or
* **exempts** itself — an explicit record that no function in this design is on that boundary, with a reason.

And that every `NfrRule` the design defines itself carries its `slug`, `kind`, `description`, the dimensions it
contributes and the required effects it contributes.

It does not check that the selector reaches real functions — functions are `M2`, and that is
[selector-resolution](selector-resolution.md).

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unassessed-nfr-rule` | a rule in scope is neither applied nor exempted | [state-the-fact](../resolutions/state-the-fact.md) · [exempt](../resolutions/exempt.md) |
| `unstated-required-attributes` | a locally-defined rule, or a cross-cutting boundary, is missing what `M1` requires of it | [state-the-fact](../resolutions/state-the-fact.md) |

Blocks `M1`.

## Settings

None.

## Notes For P6

**Rules inherit; selections never do.** A design inherits the *definitions* of `auth` and `2fa-auth` from its
Product and must then decide, locally and explicitly, which of its own functions those rules apply to. Nothing
about the inherited rule tells it.

An exemption is a claim, not a silence — reviewable and falsifiable, so a Product can later read every design's
exemptions together and find the ones that have stopped being true.

A design target may declare **several cross-cutting boundaries of the same kind** — `public.auth` and
`public.2fa-auth` are two security boundaries applying different rule sets to different function sets. That is a
design statement, not a duplication, and the resolution must not push toward one boundary per kind.
