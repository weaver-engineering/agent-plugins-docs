# Path Absent Fixtures

The states witnessing cell @`2` of [find-and-read-documentation](../../USE-CASE.md) — the operation is invoked
against a path with nothing at it, and fails gracefully.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to; extension 1b
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Path Unreadable Fixtures](../path-unreadable/FIXTURES.md) - the other failure of the path itself, and the
  reason each carries its own message

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`path-absent.layout`](layout.md) | @`2` · **path** | a tree with nothing at the path the operation was given |
| [`path-absent.error-report`](error-report.txt) | @`2` · **Stdout** | the failure, naming the path and what was wrong with it |
| [`path-absent.error-report`](error-report.json) | @`2` · **Stdout**, machine rendering | the same failure for a caller that will parse it |

There is no corpus fixture, because there is no corpus. The entry state is entirely the state of the path,
which is true of this cell and @`3` and of no other cell in this operation.

## 2 What Graceful Means Here

Nothing is registered, and the report names the path and says nothing was found there. The Architect's next
action — correct the path — is available from the report alone.

This cell is one of the three the enumeration found. The use case's narrative described registering a path and
never asked what happens when there is nothing at it; writing out the path's own states is what surfaced the
question, and extension 1b is the answer.

# Rationale

**Why this is a separate message from the unreadable case rather than one "cannot access" failure.** The two
have different remedies: a wrong path is corrected by typing a different one, an unreadable one by changing a
permission. A shared message would name the condition the operation detected rather than the thing the
Architect has to do about it, which is the half that matters to them.
