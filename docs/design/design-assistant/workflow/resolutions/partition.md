# partition

## Context
* [Workflow](../WORKFLOW.md) §7 - the standard resolutions
* @docs/standards/design-layout-standards.md §2.1, §2.2 - the containment rule and what earns another document
* @docs/standards/design-layout-standards.md §4 - naming, and the rename that is the whole mechanism of a split
* [Anchoring](../../serialization/anchoring.md) §4 - granularity as the lever on re-judgement precision

## Purpose

Split a boundary's content across the documents the layout standard would give it. A boundary occupies a
directory of its own as soon as more than one document describes it, and stays a single document while one
suffices.

## Applies To

`boundary-over-budget`.

## What It Does

1. Decides **where the seam is** — a data model outgrowing what fits inline, a function intricate enough to want
   its own document, a contained boundary that by its own existence produces a second document.
2. Moves the prose and the claims that index it.
3. Renames as the standard requires: `{slug}.md` becomes `BOUNDARY.md` once it owns a directory, and `X.md`
   earning a directory becomes `X/X.md`.
4. States the disposition of every claim the split disturbs — which side each claim's anchors go to.

## Mechanical

No. Where the seam falls is the judgement, and no threshold in the standard forces one.

## What Must Be True Afterwards

* the same claims stand, targeting the same addresses;
* nothing is invalidated and no review is cleared — **splitting a document changes nothing about the model**;
* the spend is reduced, or the remaining spend is acknowledged.

## Notes For P6

**A move is a deletion and a creation the fold does not notice.** A document is prose and the claims that index
it, so moving claims between documents is placement, never authorship: anchors are document-local and digests
are over span content, so the same claims reappear attributed to a new path.

**Splitting is the mechanism for tightening invalidation, not only an editing convenience.** An anchor covers
every section nested beneath it, so a claim anchored at a broad section is re-judged whenever anything under it
changes. Well-structured prose is rewarded with less spurious re-judgement, with nothing to configure.

**A function moves out on its own account.** One function becoming intricate does not oblige its siblings to
move with it, and a boundary holding most of its functions inline and one or two separately is the normal state
rather than a stage on the way to somewhere.

The standard's own reason for caring is worth carrying into the prose: artefacts already in their own directory
make a later promotion nearly free, where interleaved ones have to be untangled first.
