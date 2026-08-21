# Call Tree Reconciler

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-108](https://linear.app/weaver-engineering/issue/WVR-108/skill-call-tree-reconciler-forward-and-reverse) - the ticket this design fulfils
* @docs/workflows/feature-workflow/design-feature-instructions.md/§6 - the forward check this skill implements
* @docs/workflows/feature-workflow/design-directory-and-hld.md/§4.1 - `calls:`/`called_from:`, the reverse check's own data
* [next-unit-of-work-detector](../next-unit-of-work-detector/next-unit-of-work-detector-design.md) - routes here when either check finds a gap

## 1 Purpose

Two related but distinct integrity checks over the same underlying graph data:

* **Forward** (§6): does a specific behavior's own call tree actually match what its nodes' own components
  declared they'd call? A tree that's drifted from the declared graph is describing a design that either never
  got decided or has since changed underneath it.
* **Reverse** (identified during skill-candidate review, not originally in §6): `called_from:` is maintained by
  hand, as the mirror of `calls:` — added at the target the same edit that adds it at the source. Nothing
  enforces that actually happened. Walking forward from every `IC-000` function and checking that each callee's
  `called_from:` lists the caller back catches the case where it didn't.

## 2 Trigger

Forward check: routed here by the next-unit-of-work-detector once a behavior has been derived (§5) but not yet
reconciled. Reverse check: run as routine hygiene — after any edit that adds or changes a `calls:` entry, and
periodically as a whole-graph sweep, since nothing else in the process specifically prompts it.

## 3 Inputs

* Forward: one derived specific behavior — its `call_tree:` read from `reconciliation.behaviors.{id}.call_tree`
  in the `SB-NNN` document's own YAML frontmatter (documentation-standards.md §3, WVR-130's rework — not an
  inline body block as originally proposed) — plus the `calls:` declarations of every `IC-NNN`/`ED-NNN` address
  it names.
* Reverse: no specific input beyond a project scope — it's a whole-graph walk starting from every `IC-000`
  function.

## 4 Outputs And Effects

Read-only in both directions — produces a list of mismatches for a human or another skill to triage, never
edits `calls:`, `called_from:`, or a call tree itself. Forward mismatches are handed off already labeled
"needs a decision" or "needs a doc fix" is *not* something this skill decides — see §5.

## 5 Algorithm

**Forward:** for every node in a behavior's call tree, confirm its address appears in the `calls:` list declared
by its parent node. For each mismatch, this skill reports it as a mismatch only — Design Feature Instructions §6
requires a human (or a follow-on judgement step) to triage it as either a genuine design gap (route to
per-gap-ideation) or a simple documentation error (fix `calls:` directly); this skill does not make that call
itself. Idempotent: re-running against an unchanged tree and an unchanged graph reports nothing.

**Reverse:** starting from each `IC-000 §M`, walk its `calls:` list. For each address reached, confirm that
address's own `called_from:` list includes the address just walked from. Recurse into each reached address's own
`calls:` list, continuing the same check outward across the whole graph. Report every address whose
`called_from:` is missing an entry that its own `calls:`-declaring caller says it should have.

## 6 Composition With Other Skills

Feeds discrepancies to a human (or, eventually, to per-gap-ideation for the design-gap case) rather than calling
another skill directly. The reverse check's output is exactly the data
[called-from-backward-walker](../called-from-backward-walker/called-from-backward-walker-design.md) depends on
being accurate — a `called_from:` gap this skill would have caught is a `called_from:` gap that walker will
silently under-report later.

## 7 Cost/Benefit

Forward: runs once per derived behavior, cheap and mechanical — a set-membership check, no judgement. Reverse:
whole-graph, more expensive per run, but doesn't need to run often (only when `calls:` actually changes, or as
periodic hygiene) — and its value compounds, since a `called_from:` gap left uncaught silently degrades
called-from-backward-walker's own correctness without either skill's own output ever surfacing that as the root
cause. Both are low-risk to run (a false mismatch report is a minor annoyance; a missed one is a latent
correctness gap elsewhere), which argues for running the reverse check more liberally than its cost alone would
suggest.

## 8 Open Questions

Resolved by build and use: the reverse check stays a separate, less-frequent sweep rather than part of every
forward invocation (its whole-graph cost doesn't scale with per-behavior frequency); forward-mismatch triage
stays entirely a human/per-gap-ideation call, never folded into this skill.

# Built And Deployed

Built and deployed to `~/.claude/skills/call-tree-reconciler/`. Both checks ran clean against the real WVR-95
design directory throughout its own dogfooding; the fence-blindness and dual-role heading-search bugs found in
this family's shared extraction helper (WVR-149, WVR-153) live in a different code path (behavior body/Then
extraction) this skill doesn't use — its own frontmatter-based `call_tree` read was unaffected.
