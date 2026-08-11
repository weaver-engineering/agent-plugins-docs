# UC-{NNN} — {Title}

**Actor:** {link to the persona doc under `docs/analysis/user-personas/`}
**Scope:** {one or two lines on what this use case does *not* cover, with a
forward reference to §7 if there's a longer list}

## Context
* {links to the root index and any directly relevant docs, each with a one-line summary}

## 1 Goal

{what the actor is trying to achieve, in a sentence or two}

## 2 Trigger

{the event or condition that starts this use case}

## 3 Preconditions

{what must already be true for this use case to be invoked}

## 4 Main Success Scenario

{numbered steps. A step that relies on another use case's functionality
references it inline, by id, at that step — e.g. "...generates the section
index (UC-003)...". This is the only place dependencies are declared: no
separate "Depends On" summary field. Once the word-indexer (UC-004) exists,
a document's dependency set is mechanically recoverable anyway, by scanning
its own word index for `UC-\d+` tokens outside `## Context` — so a bespoke
field would just be a second place for the same information to drift out of
sync with the actual steps.}

## 5 Postconditions

{observable end state once the main scenario completes}

## 6 Extensions

{numbered-step branches, Cockburn-style: `<step><letter>` — e.g. `2a`, `4c` —
each naming the branching condition and what happens instead}

## 7 Open Design Questions (not resolved by this use case)

{things this use case deliberately leaves undecided, and why — scope
boundaries, not justification for what *is* decided; justification belongs
in a `# Rationale` section per the documentation standard, if one is needed}
