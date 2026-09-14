# Dangling Reference Fixtures

The states witnessing cell @`1.3` of [number-document-sections](../../USE-CASE.md) — a same-document reference
whose target does not exist. The operation fails gracefully.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case this cell belongs to; extension 1a
* [Mixed Numbering Fixtures](../mixed-numbering/FIXTURES.md) - the same document without the dangling
  reference, which is the main success scenario
* [Ambiguous Reference Fixtures](../ambiguous-reference/FIXTURES.md) - the other way a reference can be
  unresolvable, and the other message

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`dangling-reference.before`](before.md) | @`1.3` · **Payload** | the main scenario's document plus `The retired behaviour was described in §9.` |
| [`dangling-reference.error-report`](error-report.txt) | @`1.3` · **Stdout** | the failure, naming the reference and why nothing can follow it |
| [`dangling-reference.error-report`](error-report.json) | @`1.3` · **Stdout**, machine rendering | the same failure for a caller that will parse it |

There is no **Result** fixture. Nothing is written, so the document the Architect still has is
the payload — unchanged, and not a state this operation established.

## 2 One Sentence Is The Whole Difference

`before.md` is [mixed-numbering's](../mixed-numbering/before.md) document plus `The retired behaviour was
described in §9.` Everything else is identical. Without that sentence the document is renumbered; with it
nothing is.

## 3 Why Nothing Is Removed

An earlier version of this use case had the operation strip `§9` and carry on, leaving *"the retired
behaviour was described in ."* — a sentence with a hole in it. Two things were wrong with that.

The operation did not create the dangling reference; the document arrived carrying it. Deleting the
author's text to tidy away a fault the operation neither caused nor was asked to fix is a larger
intervention than numbering has any business making.

And it was the wrong remedy for the right worry. Leaving `§9` alone is unsafe — after renumbering some
heading may genuinely become `§9`, turning a visibly broken reference into a plausibly wrong one. But the
answer to that is to stop, not to edit around it.

# Rationale

**Why this is not link validation.** The operation cares about a broken reference only where it carries a
section number it would otherwise have rewritten. A link whose target document does not exist, or whose text
holds no `§` token, is not this operation's concern however broken it is — checking that is a different job,
and taking it on here would make every run an audit of the whole document rather than a renumbering of it.
