# Non-Markdown Document Fixtures

The states witnessing cell @`1.2` of [find-and-read-documentation](../../USE-CASE.md) — the operation is given
a path naming a file that is not a markdown document, and fails gracefully.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to; extension 1a
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Many Documents Fixtures](../many-documents/FIXTURES.md) - cell @`1.3.1`, where a file that is not a document
  is skipped instead of failing

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`non-markdown-document.target`](target.txt) | @`1.2` · **corpus** | the file the path names |
| [`non-markdown-document.error-report`](error-report.txt) | @`1.2` · **Stdout** | the failure, naming the path and what was wrong with it |
| [`non-markdown-document.error-report`](error-report.json) | @`1.2` · **Stdout**, machine rendering | the same failure for a caller that will parse it |

There is no Result fixture, because nothing was registered.

## 2 Why This Fails Where The Same File Is Skipped Elsewhere

`notes.txt` sits in @`1.3.1`'s corpus and is silently not registered. This file is the same kind of thing and
the run stops. The rule has not changed — only markdown documents are registered — but the *ask* has.

A caller naming a directory asks for whatever documents are inside it, and a file that is not one is simply
not among them; declining it silently is answering the question. A caller naming a file asks for that file,
and there is nothing else the request could have meant. Registering nothing and reporting success would tell
them a registration had happened when none had, and the first they would learn of it is a search that never
finds what they thought they had registered.

## 3 What Graceful Means Here

Nothing is registered, nothing is partly registered, and the report names the path and says what was wrong
with it. The remedy is the Architect's to apply — point at a document, or at the directory holding it — and
it is available from the report alone.

# Rationale

**Why the message says "not a markdown document" rather than "unsupported file type".** The remedy is to give
a different path, and the thing that makes this path wrong is what it names rather than some property of a
format the registry might later grow to support. A message about support invites waiting for support; a
message about what was asked for invites correcting the ask.
