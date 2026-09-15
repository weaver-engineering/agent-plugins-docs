# Path Unreadable Fixtures

The states witnessing cell @`3` of [find-and-read-documentation](../../USE-CASE.md) — the path is there and
cannot be read, and the operation fails gracefully.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to; extension 1c
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Path Absent Fixtures](../path-absent/FIXTURES.md) - the other failure of the path itself

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`path-unreadable.layout`](layout.md) | @`3` · **path** | a tree where the given path exists and cannot be read |
| [`path-unreadable.error-report`](error-report.txt) | @`3` · **Stdout** | the failure, saying the path is there and could not be read |
| [`path-unreadable.error-report`](error-report.json) | @`3` · **Stdout**, machine rendering | the same failure for a caller that will parse it |

There is no corpus fixture. Whatever is behind the path could not be read, so there is nothing to state about
it — which is the condition rather than an omission.

## 2 Why The Message Says The Path Is There

Without that, the Architect cannot tell a permission problem from a path they typed wrongly, and the first
thing they would do is go and check a path that was correct all along. Saying the path was found and could not
be read points at the one thing that is actually wrong.

The layout shows a readable sibling directory beside the unreadable one on purpose: the failure is a property
of this path, not of the corpus being inaccessible in general, and a run against `/repo/docs/widgets/` would have
succeeded.

# Rationale

**Why unreadable is a state of the path rather than of each document under it.** A directory that cannot be
read cannot be enumerated, so there is no list of documents to have states. A document that individually cannot
be read inside an otherwise readable directory is a different condition, and one this analysis has not
modelled — see the use case's own open questions.
