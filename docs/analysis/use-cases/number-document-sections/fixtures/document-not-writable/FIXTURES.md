# Document Not Writable Fixtures

The states witnessing cell @`3` of [number-document-sections](../../USE-CASE.md) — the document is there and
could be renumbered, but the result cannot be written back, so the operation fails gracefully.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case this cell belongs to; extension 1d
* [Document Absent Fixtures](../document-absent/FIXTURES.md) - the other failure of the document store
* [Mixed Numbering Fixtures](../mixed-numbering/FIXTURES.md) - the payload reused here, unchanged

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`mixed-numbering.before`](../mixed-numbering/before.md) | @`3` · **Payload** | the main scenario's own payload; nothing about the document is at fault |
| [`document-not-writable.layout`](layout.md) | @`3` · **document** | the store state: present, readable, not writable |
| [`document-not-writable.error-report`](error-report.txt) | @`3` · **Stdout** | the failure, naming the path and what was wrong with it |
| [`document-not-writable.error-report`](error-report.json) | @`3` · **Stdout**, machine rendering | the same failure for a caller that will parse it |

The payload is referenced rather than copied. Reusing the main scenario's document is the point: the same
input that succeeds elsewhere fails here, and only the dependency differs.

## 2 What Graceful Means Here

Nothing is written and nothing is partially written. The report says the document was read and *can* be
renumbered — which is worth saying, because it tells the Architect the failure is about the file's
permissions rather than anything they wrote.

# Rationale

**Why the report says the renumbering would have worked.** Without it, a read-only failure is
indistinguishable to the Architect from a document the operation could not make sense of, and they would
reasonably go looking at their own prose first. Naming what was fine is what points them at the thing that
was not.
