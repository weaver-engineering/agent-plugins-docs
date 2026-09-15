# Unreadable Document Fixtures

The states witnessing cell @`1.3.2` of [find-and-read-documentation](../../USE-CASE.md) — a directory that can
be listed holds a markdown document that cannot be opened, and registration warns about it rather than failing
or staying silent.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Many Documents Fixtures](../many-documents/FIXTURES.md) - cell @`1.3.1.1`, where a file that is not a
  document is skipped in total silence
* [Path Unreadable Fixtures](../path-unreadable/FIXTURES.md) - cell @`3`, the given path itself failing to
  enumerate at all

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`unreadable-document.corpus`](corpus) | @`1.3.2` · **corpus** | the one document that can be read |
| [`unreadable-document.layout`](layout.md) | @`1.3.2` · **document-readability** | the directory as it actually stands, with the document that cannot be opened named in place |
| [`unreadable-document.registered`](registered.md) | @`1.3.2` · **Result** | what the registry must be able to hand back afterward |
| [`unreadable-document.report`](report.txt) | @`1.3.2` · **Stdout** | the readable document registered and the other named in `warnings`, in the human rendering |
| [`unreadable-document.report`](report.json) | @`1.3.2` · **Stdout**, machine rendering | the same report for a caller that will parse it |

`secret.md` itself is not a fixture file — an actually-unreadable file checked into a fixtures directory would
be unreadable to the tooling that has to read this repository, which defeats the point of a fixture being a
real artefact. `layout.md` states the condition the same way
[path-unreadable](../path-unreadable/FIXTURES.md) states an unreadable path: as a fact about the tree, not a
file whose permission bits this repository could actually carry.

## 2 Why This Warns Rather Than Fails Or Stays Silent

Three responses were possible, and each was tried against what the Architect actually needs. Failing the whole
run would mean one bad file blocks every other document under a large corpus from being registered at all —
disproportionate, and it would recur every time the run was retried until the one file was fixed. Staying
silent, the way a non-markdown file is skipped, would mean a document the Architect believes exists is simply
missing from every future search with no record of why, discovered only by noticing an absence.

The warning is the position between those: everything that could be registered is, the Architect learns
exactly what could not be and why, and the remedy — fix the permission and register again — is available from
the report alone.

## 3 Why This Is Not The Same As A Non-Markdown File

`notes.txt` in [many-documents](../many-documents/FIXTURES.md) is not a document; there was never anything to
register and nothing was asked for. `secret.md` **is** a markdown document that satisfies every other condition
of being in scope, and the operation simply cannot open it. The first is answering the question correctly by
excluding something that was never part of it; the second is failing to answer a question it should have been
able to. Naming one and not the other is what keeps a caller from having to guess which kind of gap they are
looking at.

# Rationale

**Why the readable document is plain rather than carrying an appendix or a TODO of its own.** Every content
rule this operation has is already witnessed at @`1.3.1.1`. Repeating one here would multiply a rule this
fixture has nothing to say about, and would risk reading as though readability interacted with content, which
it does not.
