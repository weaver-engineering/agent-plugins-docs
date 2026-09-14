# Mixed Numbering Fixtures

The states witnessing cell @`1.2.1.2` of [number-document-sections](../../USE-CASE.md) — the main success
scenario, with every numbering condition the operation handles without incident present at once.

## Context
* [number-document-sections](../../USE-CASE.md) - the use case this cell belongs to; the main success scenario
* [Dangling Reference Fixtures](../dangling-reference/FIXTURES.md) - cell @`1.3`, this document plus a
  reference whose target is gone
* [Shared Pseudo-Number Fixtures](../shared-pseudo-number/FIXTURES.md) - cell @`1.1.2.1`, duplicated numbers with
  nothing pointing at them
* [Anchor Disambiguated Fixtures](../anchor-disambiguated/FIXTURES.md) - cell @`1.2.2.1`, an anchor resolving
  into duplicated numbers
* [Ambiguous Reference Fixtures](../ambiguous-reference/FIXTURES.md) - cell @`1.4`, a reference naming more
  than one heading
* @docs/standards/documentation-standards.md/§3 - the numbering convention `after.md` satisfies
* @docs/standards/documentation-standards.md/§6 - what counts as a reference, and what must never be touched

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`mixed-numbering.before`](before.md) | @`1.2.1.2` · **Payload** | a document with an unnumbered first section, a pseudo-numbered later sibling, an unnumbered first subsection, a figure, a reference that survives, an external reference, and a version string that only looks like one |
| [`mixed-numbering.after`](after.md) | @`1.2.1.2` · **Result** | the same document renumbered, with its reference rewritten to follow its target |
| [`mixed-numbering.change-report`](change-report.txt) | @`1.2.1.2` · **Stdout** | what the operation reports having done, in the human-readable form the Architect's own invocation produces |
| [`mixed-numbering.change-report`](change-report.json) | @`1.2.1.2` · **Stdout**, machine rendering | the same report for a caller that will parse it |

`after.md` and a change report together witness one state — the operation establishes both, and neither on
its own says the operation succeeded. The two report renderings are the same state seen through different
invocations (the parameter dimension), not two different outcomes: every fact in one is a fact in the other,
and holding both concretely is what makes that claim checkable rather than asserted.

## 2 What The Numbering Does Here

`Overview` and `Errors` are each the first of their siblings and carry no pseudo-number, so both take a hidden
id — `0` and `1.0`. `Using The Store` was pseudo-numbered `2` and is the first visible sibling, so it becomes
`1`, taking `Retry` to `1.1` and the figure to `1.1.a` with it. The reference `§2` follows its target to `§1`.
The external reference and `1.4.2` are left exactly as they were.

Four things are worth looking at twice, and all are invariants this payload exists to witness
([operations/1-number-a-document.md](../../operations/1-number-a-document.md) §5).

`Errors` is `1.0` even though a `Context` heading sits above it, nested under `Using The Store`. An excluded
heading takes no position, so it cannot push its siblings along, and the report says the `Context` was
skipped rather than leaving its absence from the renumbering to be inferred.

Lines 10 to 12 carry four `§` tokens in link text that look alike and get four treatments between them.
`§2.3` pointing at `widget-model.md` is left as written, because the target resolves to another document.
`§2.1` appears twice on line 11 — once targeting `widget-store-guide.md`, once `./widget-store-guide.md` —
and both follow their target to `§1.1`, because those spellings name the same document and the target is
resolved before it is compared rather than matched as a string. The `§2.1` on line 12 targets an `https://`
address, so it is neither resolved nor rewritten, and the report **warns** about it.

All four sit on adjacent lines rather than in separate fixtures. Apart, each looks like an ordinary
reference; together they are the only way to see that identical text is treated four ways, and that what
decides is always the target and never the text.

The document ends with an `# Appendix` and a `# rationale`, and those carry the last two invariants at
once. Neither heading is numbered, each starts its own sequence — the body reaches `1.1`, the appendix runs
`1`, `2`, and the rationale begins again at `1`.

The casing is deliberate and deliberately lopsided. `Appendix` is written the way the standard writes it
and `rationale` is not, so the payload shows the convention and the tolerance side by side. Casing both
oddly would have read as though the odd spelling were the expected one, which is the opposite of what the
invariant says.

Line 24 is what makes the restart safe to have: a body reference `§Appendix.5` follows the appendix's own
renumbering to `§Appendix.1`, and never touches the body's `§1`. Without the region qualifier the two
sequences would each own a section `1` and a bare `§1` would name both — the ambiguity that fails a run.

The reports are the fixtures for what the operation *says*. The human one is terse and line-oriented; the
machine one is a single compact JSON document declaring `ok`, with nothing else on the stream. Neither
carries the exit code — that is the other channel, and what matters is only that it agrees. Both
renderings are held here so the claim that they carry the same facts stays checkable.

The warning does not make this an extension. Renumbering is the use case's goal rather than a step toward
one, so the renumbered document and the report of what was done to it are together what the Architect asked
for — a fact about the run belongs in the report, and reading the report is the ordinary scenario's own
last step. What makes an extension is the operation not delivering the document at all.

Which is why the dangling reference that used to live in this payload now lives in
[its own fixture set](../dangling-reference/FIXTURES.md): it stops the run. Keeping it here made the main
scenario carry a condition that prevents a main scenario.

# Rationale

**Why one document rather than one per condition.** Every condition here has to hold simultaneously for the
operation to be witnessed honestly — a fixture exercising one at a time would let an implementation pass each
in isolation and still fail the combination. This is the same reasoning that makes a behavior's possible
fixture set a per-combination question rather than a per-value one.

**Why the reference that survives is kept even though nothing dangles here.** It is what distinguishes cell
@`1.2.1.2` from `1.1.x.x`: a document with no references at all would witness a different cell, and the
requirement that surviving references follow their targets would go unobserved.
