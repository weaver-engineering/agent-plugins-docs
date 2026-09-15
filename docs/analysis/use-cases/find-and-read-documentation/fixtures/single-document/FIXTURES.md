# Single Document Fixtures

The states witnessing cell @`1.1` of [find-and-read-documentation](../../USE-CASE.md) — the path names one
markdown document rather than a directory, and that document is registered.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Many Documents Fixtures](../many-documents/FIXTURES.md) - cell @`1.3.1.1.1`, the same operation given a directory
* [Non-Markdown Document Fixtures](../non-markdown-document/FIXTURES.md) - cell @`1.2`, the other thing a single
  path can name

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`single-document.document`](document.md) | @`1.1` · **corpus** | one markdown document, at the path the operation was given |
| [`single-document.registered`](registered.md) | @`1.1` · **Result** | what the registry must be able to hand back afterward |
| [`single-document.report`](report.txt) | @`1.1` · **Stdout** | the registration reported, in the human rendering |
| [`single-document.report`](report.json) | @`1.1` · **Stdout**, machine rendering | the same report for a caller that will parse it |

## 2 What This Cell Establishes, And What It Deliberately Does Not

A path naming one document registers that document and nothing else. The report has one line, and the `dropped`
set is empty and present.

The document carries no appendix, no rationale, no figure and no TODO — deliberately. Every content rule of
this operation is an invariant witnessed once at @`1.3.1.1.1`, and a second document carrying them here would
witness them twice, which
[Operation Fixtures §2](@docs/workflows/feature-workflow/operation-fixtures.md) treats as a sign the invariant
was drawn wrong rather than as extra assurance. What this cell has to show is the *shape* of the entry state —
a path that is a file, not a directory — and a plain document shows that without confusing it with anything
else.

# Rationale

**Why this is a cell rather than a route to the directory cell's value.** A file and a directory are not two
ways of reaching one entry state: one names the document to register, the other names a place to look for
documents, and only the second can come back with more or fewer than one. That difference is also where the
non-markdown case stops being a skip and becomes a failure (@`1.2`), which a route could not express.
