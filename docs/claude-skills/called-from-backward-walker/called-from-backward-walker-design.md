# Called-From Backward Walker

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-114](https://linear.app/weaver-engineering/issue/WVR-114/skill-called-from-backward-walker) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§4.1 - the cascading-invalidation lookup this skill implements
* @docs/workflows/feature-workflow/design-directory-and-hld.md/§4.1 - `calls:`/`called_from:`, this skill's own data
* @docs/workflows/feature-workflow/design-directory-and-hld.md/§4.5 - the usage lists this walk terminates at
* [call-tree-reconciler](../call-tree-reconciler/call-tree-reconciler-design.md) - the reverse-consistency check this walker's correctness depends on

## 1 Purpose

When a Key Decision extends an existing Internal Component function, every other use case already relying on it
is now relying on pseudocode that's about to change — their existing `reconciliation:` blocks become stale the
moment the change is made. An `IC-000` function or an External Dependency operation names its relying use cases
directly (they carry usage lists); a non-entry-point function doesn't. This skill finds them anyway, by walking
`called_from:` backward instead of searching every `IC-000` function's own call tree forward for a path that
happens to reach the changed function.

## 2 Trigger

Called during per-gap-ideation (§4.1), the moment a gap is closed by extending an existing function, before the
change is actually made — so every use case that needs to know is identified up front, not discovered later by
accident.

## 3 Inputs

The address of the Internal Component function about to change.

## 4 Outputs And Effects

Read-only — produces the set of `IC-000` function(s) the changed function terminates at, and, via their own
usage lists, every use case and specific behavior now relying on pseudocode about to change. Does not itself
invalidate or touch any `reconciliation:` block — that's a consequence the next-unit-of-work-detector's own
checksum comparison picks up mechanically once the change is actually made.

## 5 Algorithm

From the changed function's own address, read its `called_from:` list. For each address in it, repeat: read
that address's own `called_from:`, continuing outward. Stop each branch of the walk once it reaches an `IC-000`
function (an entry point has no further `called_from:` to walk, by definition — nothing calls into it from
elsewhere in the graph, only from outside the system). Once every branch terminates, read each reached
`IC-000` function's own `used_by_steps:`/`used_by_behaviors:` lists — the union of those is every use case and
behavior now affected.

## 6 Composition With Other Skills

Depends on [call-tree-reconciler](../call-tree-reconciler/call-tree-reconciler-design.md)'s reverse check for its
own correctness — a `called_from:` entry that was never added is a branch this walker will silently never find.
Called by whatever performs per-gap-ideation (§4.1), not routed to by next-unit-of-work-detector directly, since
it's invoked at decision-time, before a change is made, not as a response to detecting one already happened.

## 7 Cost/Benefit

Runs only when a gap is closed by extending an existing function — infrequent relative to the per-`SB-NNN`
checks, but high-value exactly because it replaces something that would otherwise be either skipped (missing the
cascading invalidation entirely) or done as an expensive full-graph forward search every time. Pure graph
traversal, no judgement anywhere in it — risk is entirely in its dependency on `called_from:` actually being
accurate, not in this skill's own logic.

## 8 Open Questions

* If a `called_from:` branch appears broken (an address whose own document can't be found, or whose
  `called_from:` is empty when it plausibly shouldn't be), should this skill treat that as its own kind of
  flagged finding, or silently under-report and rely on call-tree-reconciler's separate reverse check to have
  already caught it?
* Does the walk need cycle detection, or is the call graph guaranteed acyclic by construction (a function can't
  transitively call itself) given nothing else in this process asserts that explicitly?
