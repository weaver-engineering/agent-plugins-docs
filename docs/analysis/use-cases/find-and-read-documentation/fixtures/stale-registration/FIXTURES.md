# Stale Registration Fixtures

The states witnessing cell @`1.3.1.1.2` of [find-and-read-documentation](../../USE-CASE.md) — a path is
re-registered after one of the documents under it has been deleted, and that document's registration is
dropped in the same pass.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to; extension 2a
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Many Documents Fixtures](../many-documents/FIXTURES.md) - cell @`1.3.1.1.1`, this same path before `doc-b.md`
  was deleted

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`stale-registration.registered-before`](registered-before.md) | @`1.3.1.1.2` · **stale-registrations** | what the registry already holds for this path when the run begins |
| [`stale-registration.corpus`](corpus) | @`1.3.1.1.2` · **corpus** | the directory as it now stands, with `doc-b.md` gone |
| [`stale-registration.registered`](registered.md) | @`1.3.1.1.2` · **Result** | what the registry must be able to hand back afterward |
| [`stale-registration.report`](report.txt) | @`1.3.1.1.2` · **Stdout** | what was registered and what was dropped, in the human rendering |
| [`stale-registration.report`](report.json) | @`1.3.1.1.2` · **Stdout**, machine rendering | the same report for a caller that will parse it |

This is the only cell of this operation with a **stale-registrations** fixture, because it is the only one
where what the registry already held is not simply consistent with what is there.

## 2 What Is Actually Being Witnessed

The observable outcome — `doc-b.md` gone from the registry — is the easy half, and on its own it would be
satisfied by an implementation that compared old against new and deleted the difference. That implementation
would be wrong, and nothing downstream would ever catch it.

What the invariant requires is that no comparison happens at all. The registration written here is the
registration of what is under the path *now*. `doc-b.md` is absent from it for the same reason a document that
never existed is absent from it: it was not found. That the registry previously held something for that path is
not an input to the computation, and `registered-before.md` exists to be the thing the operation is seen *not*
to consult.

The distinction matters beyond tidiness. A differential registration has to be right about what changed, which
means it can be wrong about it — a moved file, a renamed directory, or a run interrupted halfway leaves the
registry describing a corpus that never existed. An absolute one cannot drift: the registry after any run is a
function of the corpus at that moment, and re-running it is always a repair.

## 3 Why The Report Says "dropped" Rather Than Staying Silent

The Agent is memoryless and the Architect is not watching. A registration that quietly stopped describing a
document would be indistinguishable, afterward, from one that never described it — and the difference matters,
because the first means something was deleted and the second means something was never there. Naming the
dropped path is what lets a reader tell a deliberate deletion from an accident, at the only moment either is
visible.

This is the one cell where the human rendering actually shows a `dropped` section, because it is the one cell
with something to drop. Where there is nothing, the human rendering omits the heading entirely — the machine
rendering still carries `dropped` as an empty array, so a caller parsing the answer never has to tell "nothing
was dropped" from "this run does not report dropping".

# Rationale

**Why the deleted document is the one with everything in it.** `doc-b.md` carried the appendix, the rationale,
the figure and both TODOs at @`1.3.1.1.1`. Dropping the richest registration rather than the plainest is what makes
the drop observable as a whole registration going rather than a few rows being tidied — and it is the case
where a differential implementation has the most to get wrong.
