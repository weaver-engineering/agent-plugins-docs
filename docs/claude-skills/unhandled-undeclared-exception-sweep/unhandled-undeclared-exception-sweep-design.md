# Unhandled/Undeclared Exception Sweep

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-112](https://linear.app/weaver-engineering/issue/WVR-112/skill-unhandledundeclared-exception-sweep) - the ticket this design fulfils
* @docs/workflows/feature-workflow/pseudocode-style.md/§3 - exception classes owned by the callee
* @docs/workflows/feature-workflow/pseudocode-style.md/§4 - the unhandled-and-undeclared rule this skill checks
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.1 - where this check runs

## 1 Purpose

A propagating exception is fine when it's declared on whatever function it propagates into — that's a legitimate
choice to let the caller decide. What's not fine is an exception that's neither caught locally nor declared
anywhere along the chain up to `IC-000`: a failure mode nobody has actually designed a response for, a direct
violation of "the system must behave gracefully at all times" that nothing else in the process specifically
checks for.

## 2 Trigger

Runs as part of the same §7.1 pass as the other mechanical reconciliation checks, over every function reachable
from a clean `SB-NNN`'s call tree.

## 3 Inputs

The `SB-NNN`'s own recorded bound pseudocode (§4.3), plus each External Dependency operation's own declared
error modes (the exception vocabulary a caller's `ON FAILURE` can reference).

## 4 Outputs And Effects

Read-only — produces a list of exceptions that are neither caught nor declared, each identified by where it
originates (a `RAISE`, or an uncaught propagation from a specific call) and which function's contract is missing
it. Does not add the missing `ON FAILURE` handling or declaration itself.

## 5 Algorithm

Walk the `SB-NNN`'s own bound pseudocode: collect every `RAISE` it contains, and every exception class any bound
call could produce (per that callee's own declared exception classes) that isn't caught by an `ON FAILURE`
clause at that point in the bound pseudocode. For each such exception, check whether the enclosing function's own
contract (what calls it) declares it as something it can produce. If neither caught here nor declared onward,
flag it. Repeat outward until reaching `IC-000` — an exception still neither caught nor declared once it would
propagate past the entry point itself is the clearest form of this finding.

## 6 Composition With Other Skills

Runs alongside [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md),
[unexpected-side-effect-scanner](../unexpected-side-effect-scanner/unexpected-side-effect-scanner-design.md), and
[thin-shim-consistency-checker](../thin-shim-consistency-checker/thin-shim-consistency-checker-design.md) in the
same §7.1 pass.

## 7 Cost/Benefit

A full sweep over every function in an operation's reachable graph, more exhaustive than the other three §7.1
checks but still mechanical — each exception's fate (caught, declared onward, or neither) is a lookup against
already-written contracts, not a fresh judgement. High benefit relative to cost: this is precisely the kind of
check that's tedious and error-prone for a human to do by hand across a graph of any real size (tracing every
propagation path manually), but cheap and reliable for a skill that's just walking declared data. Risk profile
is low — a flagged gap is objectively either caught-or-declared or it isn't; there's no ambiguous middle case
this skill has to interpret.

## 8 Open Questions

* Does this skill need its own graph traversal, or can it share call-tree-reconciler's or
  called-from-backward-walker's traversal machinery rather than reimplementing graph walking a third time in
  this family?
* Should a `RAISE` with no corresponding `ON FAILURE` anywhere *ever* be acceptable un-flagged (e.g. a truly
  unrecoverable condition, like an assertion failure, that's deliberately meant to propagate all the way to a
  generic top-level handler) — or does that case just need its own declared exception class at `IC-000`'s own
  contract, keeping the rule uniform?

# Built And Deployed

Built and deployed to `~/.claude/skills/unhandled-undeclared-exception-sweep/`, algorithm unchanged from this
proposal. Ran clean against real WVR-95 data throughout the project.
