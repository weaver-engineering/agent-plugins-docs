# Chunk Scope Utility

## Context
* [WVR-139](https://linear.app/weaver-engineering/issue/WVR-139/new-skill-chunk-scope-utility-shared-readwrite-primitive-for-chunk) - the ticket this design fulfils
* @docs/workflows/feature-workflow/chunk-scope.md - the artefact shape and incremental-recording model this skill implements
* [Reconciliation Checksum Utility](../reconciliation-checksum-utility/reconciliation-checksum-utility-design.md) - the shared-primitive precedent this skill's own architecture follows
* [Behavior Regeneration Checker](../behavior-regeneration-checker/behavior-regeneration-checker-design.md) - calls `append` on a `//REDESIGN_REQUIRED` resolution
* [design-assistant](../../sub-agents/design-assistant/design-assistant.md) - calls `init`/`append` directly at each §5.2 first derivation

## 1 Purpose

A design task's own `{design-task-ref}-chunk-scope.yaml` is written incrementally throughout Design — a behavior
recorded `new` the moment §5.2 first derives it, `mutated`/`deleted` the moment a `//REDESIGN_REQUIRED`
resolution decides it — never computed in one pass at the end (Chunk Scope §2). This skill is the shared
primitive that owns all read/write of that one artefact, the same architectural role
`reconciliation-checksum-utility` already plays for `reconciliation:` — one tool, called from multiple places,
rather than each caller reimplementing the file's own shape.

## 2 Trigger

Called directly by `design-assistant` (`init` once, `append` at each §5.2 first derivation) and by
`behavior-regeneration-checker` (`append` when a `//REDESIGN_REQUIRED` resolves as `mutated` or `deleted`) — not
routed here by `next-unit-of-work-detector`, since chunk scope plays no role in reaching design completion
itself (Chunk Scope §1); it's a pure consequence of reaching it, recorded along the way.

## 3 Inputs

* `init <chunk-scope-path> <feature> <hld> <delivers-list>` — the path, and `feature`/`hld`/`delivers`, all
  already known from the Design Task's own HLD entry and supplied by the caller (never derived by this tool).
* `append <chunk-scope-path> <address> <new|mutated|deleted>` — an `SB-NNN §id` address and its decided status.
* `get-feature` / `get-hld` / `get-delivers` / `get-modifies` / `get-behaviors <chunk-scope-path>` — just the
  path; each returns one field.

## 4 Outputs And Effects

`init` creates the file (throws if it already exists). `append` mutates it: appends `{address, status}` to
`behaviors`, and also maintains `modifies` automatically — reads the address's own `SB-NNN` document's
document-level `**Realizes:**` (Specific Behaviors §3/§4, already-recorded, mechanical to read) to find which
UC(s) rely on it, and for any UC not already in `delivers`, adds it under that UC's own Feature slug in
`modifies` (a project-wide lookup, since the affected UC can belong to any Feature, not just this task's own).
Getters are read-only, one field each.

## 5 Algorithm

Straight read/write against the fixed YAML shape Chunk Scope §4/§5 defines — no judgement calls anywhere in this
skill. The one piece of derived logic is `modifies` maintenance: given an address, resolve its own `SB-NNN`
document, read its `**Realizes:**` line for the relying UC id(s), resolve each UC's own Feature slug (the same
lookup `next-unit-of-work-detector`'s WVR-138 same-Feature check needs — kept as this skill's own private copy,
not a cross-skill import), and append any UC not already in `delivers` to `modifies`, grouped by that Feature
slug. If the address's own `SB-NNN` document can't be found project-wide, `append` still records the behavior
itself but skips `modifies` maintenance for it — a missing document is a genuine data problem this tool can't
paper over, not something to guess past.

## 6 Composition With Other Skills

Called by `design-assistant` directly (no other skill owns the §5.2 first-derivation call site) and by
`behavior-regeneration-checker` on a `//REDESIGN_REQUIRED` accept/remove resolution. Shares the
Feature-slug-for-a-UC lookup with `next-unit-of-work-detector`'s own same-Feature check (WVR-138) — each keeps
its own private copy, the same no-code-level-imports composition every skill in this family follows.

## 7 Cost/Benefit

Cheap per call — targeted parsing/serialization of one small, fixed YAML shape, never a general library, only
ever touching content the caller already identified. High leverage because it's shared: every caller (design-
assistant's own §5.2 step, `behavior-regeneration-checker`'s resolution paths, and eventually `Chunk The Design`
reading the finished file) depends on this one utility's read/write staying correct rather than each
reimplementing the shape and the `modifies` lookup independently. Lowest risk profile in the family — pure,
deterministic read/write with no judgement calls; a bug here is a straightforward implementation defect, not a
debatable design choice.

## 8 Open Questions

None outstanding at design time — built and deployed (WVR-139), and has run clean through WVR-95's entire
project, including its first project-wide §7.2 pass (see Validated Against Real Data, `SKILL.md`).

# Rationale

**Why `append` maintains `modifies` automatically rather than requiring a separate call.** The caller appending
a behavior already knows its address and status — asking it to also work out which UC that behavior's own
relying function ultimately serves, and which Feature that UC lives under, would just be this same lookup done
badly, once per caller, instead of once here. The relying UC is already recorded (a `SB-NNN`'s own document-level
`**Realizes:**`) — reading it is mechanical, not a judgement call, so there's no reason to make it a second,
separately-forgettable step.

**Why getters return one field each, not the whole parsed document.** A plain "read the whole file back"
operation has little value once callers can ask for exactly the field they need — every known caller (design-
assistant, behavior-regeneration-checker, the eventual Chunk The Design reader) wants one specific thing, not
the whole shape re-parsed on their own end.