# number-document-sections — Number A Document's Sections

**Actor:** [The Architect](../../user-personas/architect.md) — primary. [The Agent](../../user-personas/agent.md)
is a supporting actor, invoking the same operation on the Architect's behalf as a step of
[document-a-concept](../document-a-concept/USE-CASE.md).
**Scope:** Numbers and re-links what is already in the document. It does not decide the document's structure
or content, and never touches external (`@{repo-slug}/{path}`) references. **This is renumbering, not link
validation**: a reference matters here only where it carries a section number the operation would otherwise
rewrite, so a broken link is none of its business unless its own numbering is — see §7.

## Context
* [Agent Plugins index](../../../agent-plugins.md) - root index for this repo
* [The Architect](../../user-personas/architect.md) - primary actor
* [The Agent](../../user-personas/agent.md) - supporting actor
* [document-a-concept](../document-a-concept/USE-CASE.md) - the use case whose authoring step invokes this one
* @docs/standards/documentation-standards.md/§3 - Document Shape, the numbering convention this satisfies
* @docs/standards/documentation-standards.md/§6 - Cross-References, the reference-rewrite rule this satisfies

## 1 Goal

Every section, subsection and figure in a document carries the number the documentation standard requires, and
every same-document reference to them still resolves — without the Architect maintaining any of it by hand.

Renumbering by hand is slow, and it is worse than slow: it is silently error-prone. A reference missed during a
restructure keeps pointing at a number that now names a different section, so the document stays readable while
saying something false. The Architect cannot tell the two apart by reading it back.

## 2 Trigger

A document's headings and figures are unnumbered, partially numbered, or need renumbering because sections were
added, removed or reordered.

## 3 Preconditions

* The document follows the general shape — Title, optional Context, then body headings — and may have zero, some
  or all of its headings and figures already numbered or pseudo-numbered.
* A pseudo-number matches `^\d+(\.\d+)*\.?$` (headings) or `^\d+(\.\d+)*\.[a-zA-Z]\.?$` (figures). Anything else,
  however number-like, is ordinary title text with no special meaning — not even as an opt-in signal.
* The first section, or the first subsection within a parent, defaults to the hidden id `0` unless it carries a
  valid pseudo-number, which opts it into visible numbering from `1`. Every later sibling is always numbered
  visibly, whether or not the author typed a number.

## 4 Main Success Scenario

1. Number the document

    **BOUNDARY:** the numbering tool, perceived as a CLI run against a path — the same surface The Agent
    invokes when it numbers a document as a step of larger delegated work, rather than a second one of its own.

    **STATES:** [operations/1-number-a-document.md](operations/1-number-a-document.md) — the entry states
    this step admits, the state each establishes, and the fixture exposing each.

    The tool reads the document once, recording every eligible heading — a heading-like line inside a fenced
    block is not a heading at all, which this use case's own fixtures depend on, being documents quoted
    inside documents — any pseudo-numbers the author typed, including on brand-new headings and figures, so
    a reference written in the same edit as its target resolves rather than reading as dangling; every
    fenced code block and whether it carries a pseudo-number, marking it a figure; and every `§M.N(.O)?`
    token or markdown-link anchor anywhere in the document.

    **Numbering comes from the document's own structure** — position and depth — never from what the author
    typed. A pseudo-number does only two things: it opts a first sibling into visible numbering rather than a
    hidden `0`, and it is what a reference resolves against. So the new number of a heading does not depend on
    whether any other heading was written with the same one.

    **`Context` is excluded at any depth**, and excluded means invisible to the computation rather than
    merely unnumbered: it takes no position, so a `Context` nested under a subsection does not make the
    heading after it the *second* subsection.

    **`Appendix` and `Rationale` are unnumbered but not excluded.** Neither heading takes a number, and
    each opens a fresh sequence for the sections beneath it — so a document's body, its `Appendix` and its
    `Rationale` each count from `1` independently.

    **A reference into a region is region-qualified.** `§1.2` names the body's section `1.2`;
    `§Appendix.1.2` names the appendix's. The qualifier is matched case-insensitively, like the heading it
    names. That qualification is what keeps restarting sequences from making ids ambiguous, and it is why
    the regions can be numbered at all rather than left unnumbered to avoid the collision.

    The qualifier sits inside the section component, so it composes with the rest of the reference grammar
    unchanged: `@{repo-slug}/{path}[/§M.N][/L1-L2]` becomes `@{repo-slug}/{path}/§appendix.1.2` for a
    region, with the leading `/` still separating the section component from the path exactly as it
    separates a line range from the section.

    All three are recognised **case-insensitively**: `# APPENDIX` and `# rationale` are the same headings
    as `# Appendix` and `# Rationale`, and are treated identically.

    **A `§` token in a link's text follows the link's target**, not its own appearance: rewritten where the
    link resolves to this document, left alone where it resolves anywhere else. `[model's own §2.3](other.md)`
    and `[the retry rules §2.1](this.md)` are indistinguishable as text and opposite in treatment.

    The target is **resolved** before it is compared, never matched as a string — `this.md` and `./this.md`
    are the same document, and a rule written against the spelling would rewrite one and not the other. A
    **bare anchor** has no path at all and is internal by definition, so it is rewritten with nothing to
    resolve.

    Whether a relative target names this document is a question about the tree, not about the text, so the
    same document is correct two different ways depending on where it sits.

    **Only `file://` targets and bare paths are resolved.** Anything carrying another protocol is left
    alone — not to save the cost of resolving it, but because the question has no answer: a document is
    edited before it is published, publication may change it, and the same content may sit at two URLs, so
    nothing at an `https://` address is *this document* in any sense checkable from here.

    **A machine rendering is held to more than a human one.** Where the caller has declared it will parse
    the answer, the report must be one parsable document and nothing else — no banner, no progress, no
    error prose sharing the stream — and must state whether the run succeeded rather than leaving it to be
    inferred. A caller that parses cannot recover from prose mixed into the answer, and cannot ask
    afterwards what happened.

    **Whichever rendering it is, the report's verdict and the exit code must agree.** Both are in front of
    the caller at once, so a disagreement is not a second opinion but an operation that cannot be believed
    on either channel. Why a run failed remains inferable from the report itself; what must never diverge
    is whether it failed.

    **Where that rule leaves a `§` in link text unresolved, the operation warns.** It is an opinionated rule
    and it will sometimes be wrong, since a published URL really can name this document. Declining silently
    would leave a reference quietly stale; saying so hands the judgement to the only party who can make it.
    A tool rewriting someone's prose on an opinion owes them notice of where the opinion was applied.

    **A reference must name exactly one heading or figure**, resolved against the original, unmodified
    document before anything else changes — so a reference can never later be mistaken for a match once
    renumbering is under way. There are two kinds, and they carry different amounts of identity:

    * a `§M.N` token names a **number** only;
    * a markdown anchor, `#{number}-{title}`, names a number **and** a title.

    Naming exactly one target, it is rewritten to that target's new id. Naming none (extension 1a) or more
    than one (extension 1b), it cannot be resolved and the operation fails without writing anything — so
    duplicated numbering defeats a `§` token, while an anchor survives it unless the titles match too.

    Only a reference carrying a section number this operation would otherwise rewrite can fail it. Whether
    a link's *target* exists is not checked and is not this operation's concern.

    Headings and figures are then rewritten to their computed ids and the surviving references to their
    targets' new ones, leaving `@{repo-slug}/{path}[/§M.N]` external references and non-reference
    `A.B.C`-shaped text untouched throughout. A change report states every item renumbered, every reference
    rewritten, and every one left unresolved, in a form usable by whoever invoked it.

2. The Architect confirms from the change report that the document's structure is what was intended, rather
   than re-reading the numbering itself.

## 5 Postconditions

* Every eligible heading and figure carries a correct, freshly computed number, or remains hidden `0` where
  intended.
* Every same-document reference and anchor points at what it pointed at before, under its new number; any
  the operation declined to resolve are reported as such. No reference was added, altered in meaning, or
  taken away.
* External references and non-reference number-like text are unchanged.
* A change report exists, in a form consumable by whichever actor invoked the tool.
* The Architect has nothing left to do but read it. Where that is not true, the operation declined to
  proceed at all and the run took an extension (§6) rather than this path.

## 6 Extensions

A condition is written here when **the Architect has to do something different as a result** — not merely when
the flow differs. Conditions that leave them with the document they asked for, however differently the
operation reached it, belong to the operation's condition space
([operations/1-number-a-document.md](operations/1-number-a-document.md)) and not here: duplicated
pseudo-numbers with nothing pointing at them are renumbered like anything else, an anchor whose title
distinguishes its target resolves like any other reference, and a caller declaring it will parse the answer
gets the same states with the report rendered differently. Each of those is a cell, not a path.

**A fact in the report is never an extension.** Renumbering is this use case's goal, not a step toward some
larger one, so the renumbered document and the report of what was done to it *are* the deliverable, and
reading the report is step 2 of the ordinary scenario. A warning that the operation declined to resolve a
reference is therefore neither a defect nor work — it is part of what the Architect asked for.

**What makes an extension is the operation not delivering.** Every branch below ends without a renumbered
document, which is the one thing that leaves the Architect with something to do. All four fail gracefully:
nothing is written, nothing is partially written, and the report names what was wrong in terms of what they
have to do about it. Each carries its own message rather than a shared one, because the conditions differ
in remedy and the remedy is the half that matters to them.

* **1a.** A reference names no heading or figure at all → it cannot be resolved, and **the operation fails
  gracefully**. The document was handed over in an invalid state: it points at a section that is not there,
  which numbering cannot repair and only its author can.

    The operation did not create the dangling reference and does not remove it. Deleting the author's text
    to tidy away a fault it neither caused nor was asked to fix would be a larger intervention than
    numbering has any business making — and leaving it in place is unsafe, because after renumbering some
    heading may genuinely become `§9`, turning a visibly broken reference into a plausibly wrong one. The
    answer to that is to stop.

    The states, and the fixtures exposing them, are cell `1.3` in
    [operations/1-number-a-document.md](operations/1-number-a-document.md).

* **1b.** A reference names more than one heading or figure → it cannot be resolved, and **the operation
  fails gracefully**. The document was handed over in an invalid state: it contains a reference that names
  two things, which no numbering can repair and only its author can. Nothing is renumbered and nothing is
  written.

    Two ways in, one condition: a `§` token is defeated by a duplicated number alone, since it names only a
    number; an anchor survives that and is defeated only when the titles match too, since it names both.

    The author's intent exists and the document does not record it. Renumbering what can be resolved and
    reporting the rest would leave the reference ambiguous *and* stale — pointing at whatever came to occupy
    its old number — and the Architect would have to reconstruct the original numbering to recover what they
    meant. This is the one condition where the operation declines to improve a document it could partly
    improve.

    Instead of a renumbered document, the report names the reference and every heading carrying its identity.
    The states, and the fixtures exposing them, are cell `1.4` in
    [operations/1-number-a-document.md](operations/1-number-a-document.md).

* **1c.** Nothing exists at the path the operation was given → it fails gracefully, naming the path and
  saying nothing was found there. The Architect's remedy is to correct the path, and the report is enough
  to tell them so. Cell `2`; states and fixtures in
  [operations/1-number-a-document.md](operations/1-number-a-document.md).

* **1d.** The document is there and readable, but cannot be written back → it fails gracefully, and the
  message says the document *was* read and can be renumbered. That distinction is the point of giving this
  its own message: without it the Architect cannot tell a permissions problem from a document the operation
  could not make sense of, and would go looking at their own prose first. Cell `3`.

## 7 Open Design Questions (not resolved by this use case)

* Exact CLI flags, exit-code values and report formats are a design-phase concern. The `--json` by which a
  caller declares it will parse the answer is a hypothesis about the shape of a boundary this use case also
  only hypothesises, recorded because it is worth `Architect Solution` having a starting position to confirm
  or replace. What is *not* deferred is that the machine rendering parses cleanly, that both renderings
  state their own success, and that the exit code agrees — those are requirements, and only the values and
  the flag's spelling are a design choice.
* Whether numbering is ever triggered by the document changing rather than by an actor invoking it is the same
  open question registration carries in
  [find-and-read-documentation §7](../find-and-read-documentation/USE-CASE.md), and is deliberately left open in
  the same way.
