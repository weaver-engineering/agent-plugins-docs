# Document Absent Fixtures

The states witnessing cell @`2` of [number-document-sections](../../USE-CASE.md) — the operation is invoked
against a path with nothing at it, and fails gracefully.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case this cell belongs to; extension 1c
* [Document Not Writable Fixtures](../document-not-writable/FIXTURES.md) - the other failure of the document
  store, and the reason each carries its own message

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`document-absent.layout`](layout.md) | @`2` · **document** | a tree with nothing at the path the operation was given |
| [`document-absent.error-report`](error-report.txt) | @`2` · **Stdout** | the failure, naming the path and what was wrong with it |
| [`document-absent.error-report`](error-report.json) | @`2` · **Stdout**, machine rendering | the same failure for a caller that will parse it |

There is no payload fixture, because there is no document. The entry state is entirely a dependency state,
which is the only cell of this operation where that is true.

## 2 What Graceful Means Here

Nothing is written, nothing is partially written, and the report names the path and says what was wrong with
it. The Architect's next action — correct the path — is available from the report alone, without their
having to work out what the operation was trying to do when it stopped.

# Rationale

**Why this is a separate message from the unwritable case rather than one "cannot access" failure.** The two
have different remedies: a wrong path is corrected by the Architect typing a different one, a read-only file
by changing something about the file. A shared message would name the condition the operation detected
rather than the thing the Architect has to do about it, which is the half that matters to them.
