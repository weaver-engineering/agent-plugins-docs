# Shared Pseudo-Number Fixtures

The states witnessing cell @`1.1.2.1` of [number-document-sections](../../USE-CASE.md) — two headings the author
gave the same pseudo-number, which is exactly the fault this operation exists to correct.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case this cell belongs to
* [Ambiguous Reference Fixtures](../ambiguous-reference/FIXTURES.md) - duplicated numbers with a reference
  into them, which the operation cannot resolve and therefore fails on
* [Anchor Disambiguated Fixtures](../anchor-disambiguated/FIXTURES.md) - the same document plus an *anchor*,
  which resolves because it carries the title too
* [Mixed Numbering Fixtures](../mixed-numbering/FIXTURES.md) - the main scenario's own states

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`shared-pseudo-number.before`](before.md) | @`1.1.2.1` · **Payload** | a document with two subsections both pseudo-numbered `3.1`, and nothing referring to that number |
| [`shared-pseudo-number.after`](after.md) | @`1.1.2.1` · **Result** | both renumbered by position, @`1.1` and @`1.2` |
| [`shared-pseudo-number.change-report`](change-report.txt) | @`1.1.2.1` · **Stdout** | what the operation reports, with nothing rewritten or removed |
| [`shared-pseudo-number.change-report`](change-report.json) | @`1.1.2.1` · **Stdout**, machine rendering | the same report for a caller that will parse it |

## 2 Why This Is Not A Fault

Numbering comes from position and depth, not from what the author typed. A pseudo-number only signals that a
first sibling opts into visible numbering, and gives a reference something to resolve against. So two headings
both written `3.1` are not competing for an identity: the first takes `1.1`, the second `1.2`, and the document
comes out better numbered than it went in. That is the operation working, not tolerating a defect.

Two documents differ from this one by a single line. Add an anchor whose title distinguishes its target
([anchor-disambiguated](../anchor-disambiguated/FIXTURES.md)) and the operation succeeds; add `§3.1`, which
the titles cannot distinguish ([ambiguous-reference](../ambiguous-reference/FIXTURES.md)), and it fails.
Duplicate numbering is repairable. What may not be repairable is something pointing into it.

# Rationale

**Why this case is written as an extension at all, given that nothing exceptional happens.** It looks like a
fault and is not, and an earlier draft of this use case treated it as one — reporting a "duplicate identity"
and refusing to renumber. That was wrong about where the fault lies: the duplication is the defect being
corrected, and only a reference into it can defeat the operation. Keeping this as an extension records the
correction where someone would look for it — the question "what happens when two headings share a number" has
an answer, and the answer is "they are renumbered, like everything else."
