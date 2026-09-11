# documents-parseable

## Context
* [Workflow](../WORKFLOW.md) §4.1 - where this check is registered
* [Parse Contract](../../serialization/parse-contract.md) §1 - per-file purity, and what a parse may fail on
* [Serialization](../../serialization/SERIALIZATION.md) §3 - which files are in scope

## Purpose

Is every file the parse will read well-formed? The parse contract says a parse never fails on a file for being
the wrong shape, only on one that is malformed as YAML or markdown — and a parse that fails is not a finding
anybody can act on. Asking the question before the parse turns it into ordinary work.

## Registration

| | |
|---|---|
| Stage | pre-parse |
| Model check | no — it reads bytes |
| Requires | [design-declaration](design-declaration.md) — scope is undecidable until the design directory is |

## What It Inspects

Every `*.md` and `*.yaml` within scope: the design directory and its subdirectories, stopping at any
subdirectory that is a design directory of its own. Every other file is out of scope and is never read.

Well-formedness only — that the frontmatter is YAML and the document is markdown. Whether the frontmatter says
anything sensible is a question for the fold, not for this check.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `malformed-document` | a file in scope cannot be parsed as its own format | [correct-the-design](../resolutions/correct-the-design.md) |

Blocks every level: the model would be missing whatever that file contributes, and the model has no way to know
what that was.

## Settings

None.

## Notes For P6

Report per file with the parser's own position and message. A malformed document is almost always a hand edit
or a merge artefact, and the fastest resolution is nearly always reading the error.
