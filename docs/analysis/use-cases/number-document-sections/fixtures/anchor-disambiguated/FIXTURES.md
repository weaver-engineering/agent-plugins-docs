# Anchor Disambiguated Fixtures

The states witnessing cell @`1.2.2.1` of [number-document-sections](../../USE-CASE.md) — duplicated pseudo-numbers
that a *markdown anchor* can still resolve into, because an anchor carries the title as well as the number.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case this cell belongs to
* [Ambiguous Reference Fixtures](../ambiguous-reference/FIXTURES.md) - where a reference into duplicated
  numbering cannot resolve, by either route
* @docs/standards/documentation-standards.md/§6 - the `[§3.2](#3-2-title)` anchor form

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`anchor-disambiguated.before`](before.md) | @`1.2.2.1` · **Payload** | two subsections both pseudo-numbered `3.1` but titled differently, and an anchor link to `#3-1-retry` |
| [`anchor-disambiguated.after`](after.md) | @`1.2.2.1` · **Result** | both renumbered, and the anchor following its target to `#1-1-retry` |
| [`anchor-disambiguated.change-report`](change-report.txt) | @`1.2.2.1` · **Stdout** | the anchor rewrite reported alongside the renumbering |
| [`anchor-disambiguated.change-report`](change-report.json) | @`1.2.2.1` · **Stdout**, machine rendering | the same report for a caller that will parse it |

## 2 Why The Anchor Resolves Where A `§` Would Not

An anchor is `#{number}-{title}`, so `#3-1-retry` names `3.1` **and** `retry`. Only one heading carries both,
so there is exactly one target and it is rewritten like any other reference.

Replace that anchor with `§3.1` and the same document becomes unresolvable
([ambiguous-reference](../ambiguous-reference/FIXTURES.md)): the number alone is carried twice, and a `§`
carries nothing else to tell them apart. This document, that one, and
[shared-pseudo-number](../shared-pseudo-number/FIXTURES.md) differ *only* in what refers to the duplicated
heading — nothing, an anchor, or a `§` token — which is what makes the rule legible: what matters is not
the duplication but whether anything points into it, and with what.

# Rationale

**Why this case is worth a fixture of its own rather than a sentence.** It is the counter-example that stops
the rule being read as "duplicated numbers plus any reference means failure". Duplicated numbers are fine;
duplicated numbers with an anchor whose title distinguishes them are fine too. Only a reference that cannot
name one target fails. A sentence saying so would be believed; a fixture saying so can be checked.
