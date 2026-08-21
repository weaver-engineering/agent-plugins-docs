# Reconciliation Checksum Utility

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-113](https://linear.app/weaver-engineering/issue/WVR-113/skill-reconciliation-checksum-utility) - the ticket this design fulfils
* @docs/templates/SPECIFIC-BEHAVIOR-TEMPLATE.md - the `reconciliation:` block this utility reads and writes
* @docs/workflows/feature-workflow/design-feature-instructions.md/§7.1 - the Rationale entry "Why reconciliation: is checksums, not a checkbox"
* [pseudocode-subset-checker](../pseudocode-subset-checker/pseudocode-subset-checker-design.md), [unexpected-side-effect-scanner](../unexpected-side-effect-scanner/unexpected-side-effect-scanner-design.md), [thin-shim-consistency-checker](../thin-shim-consistency-checker/thin-shim-consistency-checker-design.md), [unhandled-undeclared-exception-sweep](../unhandled-undeclared-exception-sweep/unhandled-undeclared-exception-sweep-design.md) - the four checks that call this utility to record their combined result

## 1 Purpose

The small, shared mechanism that makes every other §7.1 check's result falsifiable rather than a one-shot
checkbox: compute a checksum of each relying use case's own Technical Interpretation slice, and of every
function's pseudocode or prose the `SB-NNN`'s bound pseudocode (§4.3) names; record them once all four §7.1
checks pass; and, on a later run, recompute and compare to detect whether anything the reconciliation relied on
has since changed — without re-reading or re-reasoning about content that hasn't actually moved. This is also
the comparison pseudocode-subset-checker runs first, before ever falling back to
[pseudocode-substitution-checker](../pseudocode-substitution-checker/pseudocode-substitution-checker-design.md)'s
more expensive judgement.

## 2 Trigger

Called by pseudocode-subset-checker, unexpected-side-effect-scanner, thin-shim-consistency-checker, and
unhandled-undeclared-exception-sweep once all four pass together for a given `SB-NNN`, to record the result. Also
called directly by `behavior-regeneration-checker` (added after WVR-130's §7.1/§7.2 rework — not originally
proposed here) to refresh checksums on a confirmed §7.2 match. Called by next-unit-of-work-detector's own §1
check, in compare mode, to decide whether an `SB-NNN`'s existing `reconciliation:` frontmatter is still current.
A new mode, `invalidate`, is called project-wide whenever a function's own pseudocode/prose changes.

## 3 Inputs

* Write mode: an `SB-NNN`'s relying use case(s), each with their own Technical Interpretation slice, and the
  full set of functions/prose its bound pseudocode names.
* Compare mode: an `SB-NNN`'s existing `reconciliation:` frontmatter, plus current access to the same content it
  originally checksummed.
* Invalidate mode (new, WVR-131): a project design root and a changed function's own address.

## 4 Outputs And Effects

The only skill in this family that writes to a design document — it populates or updates an `SB-NNN`'s own
`reconciliation:` block, now true YAML frontmatter (before the document title, documentation-standards.md §3),
not an embedded mid-body block as originally proposed: `checked_at`, `uc_technical_interpretation_checksums`,
`function_checksums` at the document level, and, per behavior, `reconciliation.behaviors.{id}.call_tree` and
`.reviewed` (`reviewed_by`/`reviewed_at`) — a genuine rework from the original single-document-level
`reviewed_by`/`reviewed_at` pair, needed because invalidating one behavior in a multi-behavior document must not
force re-review of every other, unaffected behavior in the same file. In compare mode it's read-only, returning
current-vs-stale. Invalidate mode is also read-only: it reports every behavior project-wide whose own recorded
`call_tree` (the concrete walk that behavior actually traced, not the abstract call graph) contains the given
function's address — clearing `reviewed` for exactly those behaviors is `behavior-regeneration-checker`'s own
action once regeneration confirms a real mismatch, never this utility's.

## 5 Algorithm

**Write:** compute one checksum per relying use case's own Technical Interpretation slice — keyed by that use
case's id, since a `SB-NNN` can name more than one (Specific Behaviors §3) and each is independently
falsifiable — and one per function/prose the bound pseudocode names; write all of them into the `SB-NNN`'s
`reconciliation:` frontmatter along with the current date. Per-behavior `reviewed` entries are untouched by this
mode — those are only ever written by the architect's own action, via `behavior-regeneration-checker`'s match
path or a direct confirm, never here.

**Compare:** recompute the same checksums against current content; report stale if any recomputed value doesn't
match what's recorded, current otherwise — and, on a stale `function_checksums` entry specifically, name which
function changed, since that's exactly what pseudocode-subset-checker needs to know which piece(s) to re-run
pseudocode-substitution-checker against, rather than re-deriving the whole bound pseudocode from scratch.

**Invalidate** (new mode, WVR-131 — not in the original proposal): walk every `SB-NNN` under every Feature
subdirectory in the given project design root; for each behavior's own recorded `call_tree`, check whether the
given function address appears anywhere in it. Report every match as a candidate needing §7.2 — this only
*identifies* candidates; clearing their `reviewed` entry is a separate, later action (`behavior-regeneration-checker`'s
own job, only once a real regenerate-and-compare mismatch is confirmed, not a consequence of this mode alone).

## 6 Composition With Other Skills

Downstream of all four §7.1 checks (only invoked in write mode once every one of them passes) and of
`behavior-regeneration-checker` (invoked in write mode directly on a confirmed §7.2 match — a call site added
after the original proposal). Upstream of next-unit-of-work-detector (invoked in compare mode as part of that
skill's own §1 check) and, via `invalidate`, upstream of `behavior-regeneration-checker`'s own project-wide
candidate discovery.

## 7 Cost/Benefit

Cheap per call (checksumming is fast, and only runs on already-identified content, not a search). High leverage
because it's shared: every other §7.1 skill and the router itself depend on this one utility's output staying
correct rather than each reimplementing its own staleness detection. Risk profile is the lowest in the family —
this is close to pure, deterministic computation with no judgement calls anywhere in it; a bug here would be a
straightforward implementation defect, not a debatable design choice.

## 8 Open Questions

* Does a stale `uc_technical_interpretation_checksums` entry ever need finer granularity than "this use case's
  slice changed" — e.g. flagging which step within it — or is routing the whole use case back through Gap
  Analysis's own re-classification always the correct response regardless?
* Compare mode already distinguishes which function's checksum went stale (§5) — should it go further and
  identify which specific piece(s) of the bound pseudocode that function was substituted for, or is leaving that
  lookup to pseudocode-subset-checker itself the right division of labor?

# Built And Deployed

Built and deployed to `~/.claude/skills/reconciliation-checksum-utility/`, with one significant, real bug found
and fixed on live data (WVR-150, Urgent): `write` mode silently corrupted a `SB-NNN`'s frontmatter the first
time it ran against a document whose checksums were still recorded in the pre-rework, multi-line block style —
every `SB-NNN` in the WVR-95 project, since none had ever been migrated to the newer flow-mapping style. The
underlying replace-logic only removed a checksum key's single header line, not its whole prior value, leaving
the old block's entries behind as orphaned, invalid YAML — while the tool's own return value still reported a
clean success. Caught by `design-assistant` diffing the written file directly rather than trusting that return
value; fixed by replacing the key's entire prior span, and flow-mapping was confirmed as the deliberate target
format going forward (matching what compare mode's own read side already assumed).
