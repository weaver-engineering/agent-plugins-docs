# Relative Target Fixtures

The states witnessing cells @`1.2.1.1.1` and @`1.2.1.1.2` of
[number-document-sections](../../USE-CASE.md) — one payload, two filesystem layouts, two different correct
outputs.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case these cells belong to
* [Mixed Numbering Fixtures](../mixed-numbering/FIXTURES.md) - the main scenario, whose link targets resolve
  unambiguously and which therefore witnesses neither of these cells

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`relative-target.before`](before.md) | @`1.2.1.1.1` and @`1.2.1.1.2` · **Payload** | a document containing `[retry §2.1](../dir/widget-store-guide.md)` — a relative target whose meaning is not decidable from the text |
| [`relative-target.layout-resolves-here`](layout-resolves-here.md) | @`1.2.1.1.1` · **local-target** | the tree in which that path resolves to this document |
| [`relative-target.layout-resolves-elsewhere`](layout-resolves-elsewhere.md) | @`1.2.1.1.2` · **local-target** | the tree in which it resolves to a different document of the same name |
| [`relative-target.after-resolves-here`](after-resolves-here.md) | @`1.2.1.1.1` · **Result** | `§2.1` in the link text follows its target to `§1.1` |
| [`relative-target.after-resolves-elsewhere`](after-resolves-elsewhere.md) | @`1.2.1.1.2` · **Result** | the same `§2.1` left exactly as written |
| [`relative-target.change-report-resolves-here`](change-report-resolves-here.txt) · [.json](change-report-resolves-here.json) | @`1.2.1.1.1` · **Stdout** | two rewrites reported |
| [`relative-target.change-report-resolves-elsewhere`](change-report-resolves-elsewhere.txt) · [.json](change-report-resolves-elsewhere.json) | @`1.2.1.1.2` · **Stdout** | one rewrite, one deliberate non-rewrite |

## 2 Why This Set Exists

`before.md` is one payload. Read it as text and there is no fact in it that decides whether `§2.1` should be
rewritten: `../dir/widget-store-guide.md` might be this very document reached the long way round, or a
different document that happens to share its name. Only the tree around it says which.

That is what makes it a **dependency state** rather than a payload condition. The two layout fixtures are the
dependency's two states, and the two `after` documents are what the same input produces under each. Nothing
about the document changed between them.

It is also why the operation classifies by rule before it resolves anything: a target carrying any protocol
other than `file://` is external without being checked, and only `file://` and bare paths are resolved
locally. Resolving every hyperlink in a large document to find out what it points at would cost more than
the question is worth, and a protocol is decidable from the text.

# Rationale

**Why the same payload rather than two payloads.** Two documents differing in their link paths would witness
the same two outputs and teach the wrong lesson — that the text decides. Holding the payload fixed and
varying only the dependency is the whole demonstration: identical input, identical rules, two correct and
different answers.

**Why the layouts are described rather than built.** A dependency fixture states the state the dependency is
in. For a filesystem that is a tree, and a tree is a thing to write down — building it would make these
fixtures executable, which they do not need to be to say what state the operation is entitled to assume.
