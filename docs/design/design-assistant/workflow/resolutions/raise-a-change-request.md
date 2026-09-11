# raise-a-change-request

## Context
* [Workflow](../WORKFLOW.md) §2.5 - soft resolution, and blocked as a property of a finding
* [Decision Model](../../datamodel/decision-model.md) §4, §4.1 - the `ChangeRequest` and why it is deleted rather than resolved
* [Boundary Model](../../datamodel/boundary-model.md) §3.2 - authority

## Purpose

The fix belongs to another design target. A design target's operations and behaviors may only be changed by its
own design — if a boundary was complex enough to earn its own design, then changing what it promises is design
work on *that* boundary, not a side effect of work on a neighbour.

**This resolution is available to any finding**, not to a fixed list. Which findings turn out to need a change
this design cannot make is not knowable in advance.

## Applies To

Potentially any kind. Most commonly `unauthorized-change`, `mock-inconsistency`, `build-manifest-conflict`,
`nfr-conflict`, `satisfaction-failure`, `unstated-required-attributes`.

## What It Does

1. Establishes that the change genuinely belongs elsewhere — that this design has no authority over what would
   have to change.
2. Raises a ticket against the owning design target.
3. Records a `ChangeRequest`: who raised it, the `subject` address on the other target, the `change` needed and
   why this design needs it, the `ticket` as an `ExternalRef`, and the level it blocks.
4. Withdraws whatever this design had done in place of the change, where it had done anything.

## Mechanical

No.

## What Must Be True Afterwards

* the finding is **soft-resolved**: reported on every subsequent run as blocked, and not offered as work;
* the check that raised it is **not complete**, so anything requiring it is skipped and the level is not
  reached;
* other findings from the same check remain workable.

## Notes For P6

**A change request has no resolved state.** It exists, or it is gone. Once the change has been made it is
**deleted** — it explains nothing about the present, the change itself lives in the other design target, and the
reason that target made it is that target's own key decision. A withdrawn request goes the same way.

Nothing is lost by deleting it: when the other target's operation behavior changes, every fixture standing in
for it and every behavior traced against those fixtures invalidate by the ordinary rule. The audit trail — who
asked, for what, when — lives in the ticket and in version control, neither of which is the model's to
duplicate.

**Blocked is not failing.** The design is not complete, no further evolution of it is possible here, and nothing
is wrong. A whole project can legitimately sit blocked across every remaining design target. The resolution
prose should say so plainly, because a report that reads as an error invites someone to work around it — which
means making the change anyway, which is the thing authority exists to prevent.
