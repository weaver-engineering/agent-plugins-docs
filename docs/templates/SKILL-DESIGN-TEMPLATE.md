# Skill Design Template

## Context
* Documentation Standards (@docs/standards/documentation-standards.md) - the document shape (Context, numbered sections, Rationale/Appendix) this template follows
* [Claude Skills](../claude-skills/) - where a design produced from this template is filed, one directory per skill

Template for a Claude Code Skill design write-up — one file per skill, filed as
`docs/claude-skills/{slug}/{slug}-design.md`. This is a design proposal for the architect to review for
plausibility and cost/benefit before a PR raises the skill's actual implementation — it is not the implementation
itself, and no `SKILL.md` is expected to exist yet when this document is written. The template itself is in the
Appendix below, since it's reference material to copy from, not indexed content in its own right.

# Appendix

```
# {Skill Name}

## Context
* {link to the Linear ticket this design fulfils}
* {link(s) to the source process document section(s) this skill implements — e.g. Design Feature Instructions §M[.N]}
* {links to any other skill-design docs this one composes with — calls into, or is called by}

## 1 Purpose

{the problem this skill solves, tied directly to its source section — quote or closely paraphrase the relevant process-doc text rather than re-describing it from scratch}

## 2 Trigger

{how this skill gets invoked: manually by the architect, chained automatically from the Next-Unit-Of-Work router, or called by another skill — name which one(s) if so}

## 3 Inputs

{concretely what gets handed to this skill to run — a design directory path, a specific SB-NNN id, a UC-NNN id, a changed function's address, etc. Specific enough that "could this actually be invoked" is answerable.}

## 4 Outputs And Effects

{what this skill produces, and whether it's read-only (a report or finding, for a human or another skill to act on) or mutates a document directly. Be explicit — this is one of the first things cost/benefit and risk review will ask.}

## 5 Algorithm

{the step-by-step logic, precise enough to assess plausibility. Draw this directly from the source process-doc section(s) named in Context — this section should read as an extraction, not a reinterpretation.}

## 6 Composition With Other Skills

{which other candidate skills this one calls into, or is called by — name them by slug. "None" is a valid, expected answer for a self-contained skill.}

## 7 Cost/Benefit

{expected invocation frequency in a real design cycle; what it saves compared to an agent reasoning the same thing out inline, unassisted, every time; its risk profile — mechanical/deterministic (a wrong output is a bug) versus judgement-assisting (a wrong output is a bad suggestion someone still has to catch)}

## 8 Open Questions

{genuine unresolved points for the architect to weigh — scope boundaries or design forks this write-up deliberately leaves open, not a hedge against having done the analysis}

# Rationale

{only if a shape or scoping choice in this design isn't self-justifying}
```

# Rationale

Eight required sections, not fewer, because the architect's own ask was specifically "plausibility and
cost/benefit" — Purpose and Algorithm establish plausibility (does this make sense, is the logic sound), Inputs
and Outputs And Effects establish exactly what's being proposed (not a vague capability), and Cost/Benefit and
Open Questions are what the review decision actually turns on. Trigger and Composition With Other Skills exist
because most of these candidates were identified as a family, several sharing inputs or feeding each other's
outputs (see @docs/workflows/feature-workflow/design-feature-instructions.md/§7.1) — reviewing one in isolation
from how it fits the others would miss exactly the kind of double-counted cost or hidden dependency this section
exists to surface.

Section 5, Algorithm, is required to read as an extraction from the source process document rather than a fresh
description, because the whole point of these skills is to implement a process that's already been designed and
agreed — a design write-up that quietly reinterprets its own source section is describing a different skill than
the one the ticket actually asked for, even if nobody notices until implementation.

This template has no numbered "0" section for a preamble paragraph before `## Context`, unlike some documents in
this family — every instance is expected to open directly with `## Context`, keeping the whole document inside
the standard's numbered-body convention from the first line.
