# Ambiguous Reference Fixtures

The states witnessing cell @`1.4` of [number-document-sections](../../USE-CASE.md) — a reference naming more
than one heading. The operation fails gracefully.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case this cell belongs to; extension 1b
* [Shared Pseudo-Number Fixtures](../shared-pseudo-number/FIXTURES.md) - duplicated numbers with nothing
  pointing at them, which renumber without incident
* [Anchor Disambiguated Fixtures](../anchor-disambiguated/FIXTURES.md) - duplicated numbers an anchor *can*
  resolve into, because there the titles differ
* [Dangling Reference Fixtures](../dangling-reference/FIXTURES.md) - the other way a reference is
  unresolvable, and the other message

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`ambiguous-reference.before`](before.md) | @`1.4` · **Payload** | one document carrying both routes to an unresolvable reference: `§3.1` where two headings share the number, and `#4-1-retry` where two share the number *and* the title |
| [`ambiguous-reference.error-report`](error-report.txt) | @`1.4` · **Stdout** | the failure, naming both references and every heading carrying each one's identity |
| [`ambiguous-reference.error-report`](error-report.json) | @`1.4` · **Stdout**, machine rendering | the same failure for a caller that will parse it |

There is no **Result** fixture. Nothing is written, so the document the Architect still has is
the payload — unchanged, and not a state this operation established.

## 2 Why One Payload And Not Two

An earlier version of this set had two payloads — one per route — both claiming to be cell @`1.4`'s entry
state. That is not possible. A cell has one payload fixture, because a cell is one entry state and a payload
is what makes that state concrete; two payloads are two entry states and therefore two cells.

Two cells would have been the alternative, and would have meant making reference *form* a dimension of its
own. It is not one: a `§` token and an anchor differ in what defeats them — a duplicated number alone
against a duplicated number and title — but not in what the operation then does. Same outcome, same
required effect, one cell.

So the two routes are carried by one document, which is the same thing
[mixed-numbering](../mixed-numbering/FIXTURES.md) does for the three path forms that *do* resolve. A value
reached two ways is witnessed by a payload exhibiting both.

# Rationale

**Why the report names both rather than stopping at the first.** The Architect's remedy is to edit the
document, and they would rather do it once. A report that stopped at `§3.1` would send them back for
`#4-1-retry` on the next run, and again for anything after that — turning one invalid document into as many
runs as it has faults.
