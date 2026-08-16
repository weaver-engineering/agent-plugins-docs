# Thin-Shim Consistency Checker

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-111](https://linear.app/weaver-engineering/issue/WVR-111/skill-thin-shim-consistency-checker) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-directory-and-hld.md/§3.4 - the `used_by:` list this skill compares
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.1 - where this check runs, as part of design review
* [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md) - a sibling §7.1 check
* [pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md) - a different kind of comparison from this skill's own — see §1

## 1 Purpose

An External Dependency document describes a thin shim — a narrow, system-specific translation of a third-party
API, not the API itself. A shim stays honest only if every use case's actual usage of it really is that thin.
This skill compares every relying use case's usage, recorded in an ED operation's own `used_by:` list, side by
side — catching a shim that's quietly stopped being a simple, one-for-one translation for one of them, something
invisible from any single use case's own point of view.

This is a different kind of comparison from
[pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md),
not an instance of it. That skill asks whether one candidate can stand in for one piece of pseudocode — a
one-to-one substitution question. This one asks whether several already-accepted usages, and the interface they
all rely on, are still mutually consistent — a uniformity question across a set, with no single candidate being
judged as a replacement for anything. Deliberately not built on the substitution primitive.

## 2 Trigger

Runs as part of the same §7.1 pass as the other mechanical reconciliation checks, for every External Dependency
operation involved in a clean `SB-NNN`'s call tree.

## 3 Inputs

An ED operation's own document (its declared interface, request/response shape, error modes) and its full
`used_by:` list — every use case currently recorded as relying on it.

## 4 Outputs And Effects

Read-only — produces a flagged inconsistency (a `used_by:` entry whose actual need exceeds what the shim's
declared interface can honestly give it) for human review. Does not edit the ED document or resolve the
inconsistency itself.

## 5 Algorithm

For every pair of entries in an ED operation's `used_by:` list, and each individually against the operation's
own declared interface: is what this use case actually needs from the operation something the declared,
one-for-one shim interface is actually capable of providing? Flag any entry that needs something subtly more —
a parameter the shim doesn't expose, a distinction between two use cases' needs the shim's current interface
can't tell apart.

## 6 Composition With Other Skills

Runs alongside [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md),
[unexpected-side-effect-scanner](../unexpected-side-effect-scanner/unexpected-side-effect-scanner-design.md), and
[unhandled-undeclared-exception-sweep](../unhandled-undeclared-exception-sweep/unhandled-undeclared-exception-sweep-design.md)
in the same §7.1 pass, feeding into
[reconciliation-checksum-utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md)
on a clean result.

## 7 Cost/Benefit

Runs once per ED operation involved in a reconciliation pass, cheap relative to a full pseudocode walk (it's
comparing declared interfaces and recorded usages, not tracing logic). Its value is specifically in catching
drift that accumulates gradually — no single use case's addition looks wrong on its own, which is exactly why
it needs a dedicated side-by-side comparison rather than relying on whoever adds the newest `used_by:` entry to
notice unassisted. Risk profile is low: a false flag costs a quick human look, a missed one lets a shim quietly
grow real complexity that the design's own documentation never admits to.

## 8 Open Questions

* Where exactly is the line between "the shim needs a genuinely new parameter" (a real Gap Analysis item, back
  to §3) and "this use case's need is close enough to already covered" — is that distinction this skill's job to
  draw, or always a human call once flagged?
* Should this check also run proactively during Gap Analysis (§3), when a new use case is first being classified
  against an existing ED operation, rather than only retrospectively at §7.1?
