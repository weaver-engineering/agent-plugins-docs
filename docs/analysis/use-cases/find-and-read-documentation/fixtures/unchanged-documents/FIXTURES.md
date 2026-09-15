# Unchanged Documents Fixtures

The states witnessing cell @`1.3.1.2` of [find-and-read-documentation](../../USE-CASE.md) — a directory is
re-registered where most of its documents are byte-identical to what the registry already held for them, and
the report folds those into a count instead of naming each one.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case this cell belongs to
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space this cell sits in
* [Many Documents Fixtures](../many-documents/FIXTURES.md) - cell @`1.3.1.1.1`, the same shape of corpus on its
  first registration, when nothing could be unchanged yet
* [Stale Registration Fixtures](../stale-registration/FIXTURES.md) - cell @`1.3.1.1.2`, a re-registration where
  the change is a document vanishing rather than nothing changing

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`unchanged-documents.registered-before`](registered-before.md) | @`1.3.1.2` · **unchanged-documents** | what the registry already holds for `doc-a.md` and `doc-b.md`, byte-identical to their content now |
| [`unchanged-documents.corpus`](corpus) | @`1.3.1.2` · **corpus** | the directory as it now stands: two documents unchanged, one new |
| [`unchanged-documents.registered`](registered.md) | @`1.3.1.2` · **Result** | what the registry must be able to hand back afterward — full structure for all three, regardless of which are named in the report |
| [`unchanged-documents.report`](report.txt) | @`1.3.1.2` · **Stdout** | `doc-c.md` registered by name, the other two folded into `unchanged: 2` |
| [`unchanged-documents.report`](report.json) | @`1.3.1.2` · **Stdout**, machine rendering | the same report for a caller that will parse it |

## 2 What This Cell Proves, And What It Deliberately Does Not

The point of this cell is the gap between `Result` and `Stdout`. `registered.md` holds `doc-a.md` and
`doc-b.md` in exactly as much detail as `doc-c.md` — same fields, same shape, nothing missing and nothing
abbreviated. The report is where the difference actually shows: `doc-c.md` gets a line of its own, and the
other two are represented only by the number `2`. If `Result` ever shrank the way `Stdout` does, this cell
would be witnessing the wrong thing entirely — the registry would have stopped computing what it holds for
`doc-a.md` and `doc-b.md`, rather than merely stopped repeating it in the report.

This cell does not attempt to say *how* the registry decides two documents match — a content hash, a modified
time, a byte comparison — because that is exactly the kind of implementation detail §7's first open question
keeps out of this analysis. What it fixes is only the observable contract: given a corpus where two documents
are unchanged, the report names one and counts two.

## 3 Why Three Documents, And Why This Split

Two unchanged and one changed is the minimum shape that makes the point at all — a single unchanged document
would print as `unchanged: 1`, which reads as if it might be a coincidence of the report's format rather than a
deliberate fold. Two is enough to show the count is actually counting.

A real corpus this fixture is standing in for might have a few edited documents among many thousands unchanged
ones; three documents in a fixture cannot show that scale, only the shape scale would take. Trusting the reader
to extrapolate a count from `2` to `2,000` is the whole reason `unchanged-documents` is a count and not a list
in the first place (`operations/1-register-a-path.md` §3.4).

# Rationale

**Why `doc-c.md` is new here rather than changed.** "New under this path" and "present before, different now"
are the same fact from this dimension's own point of view — neither matches what the registry held, so both
register individually. Modelling a changed document as well would exercise nothing this fixture does not
already exercise with a new one, at the cost of a fourth document and a `registered-before.md` entry for
something that then gets overwritten anyway.

**Why `registered-before.md` doesn't attempt to represent the registry's actual comparison mechanism.**
Anything more concrete — a hash, a timestamp — would be exactly the kind of registry-implementation detail
`documentation-standards.md`'s own open question about where the registry lives is written to keep out of
Analysis. This fixture states only the fact a comparison must be capable of using: that two documents' content
now is identical to what was registered before.
