# Architect's Guide To Design Assistant

## Context
* [Design Assistant](design-assistant.md) - the sub-agent this guide is about working with; that document is the WHAT/WHY/HOW of its own construction, this one is the practical how-to
* [Design Assistant Persona](../../analysis/user-personas/design-assistant.md) - its role, goals, and frustrations
* Design Feature Instructions (@docs/workflows/feature-workflow/design-feature-instructions.md) - the process it drives; read this for the phases themselves, this guide is about the mechanics of directing it
* [Chunk Scope](@docs/workflows/feature-workflow/chunk-scope.md) - the artefact its §5.2/§7.2 work produces incrementally

This is a practical guide, not a process specification — everything here was learned by actually running Design
Assistant end to end against a real Feature ([WVR-95](https://linear.app/weaver-engineering/issue/WVR-95/design-the-doc-search-and-retrieval-mcp-server)),
not anticipated in advance. Where it disagrees with an earlier assumption, this guide reflects what actually
happened.

## 1 Installing It — There's No Releasable Plugin Yet

Cross-platform capability packaging (WVR-94) is still a placeholder — there's no build step that produces an
installable plugin for Claude Code, OpenCode, or anything else. Today, getting Design Assistant and its skill
family onto a machine is a manual copy from `agent-plugins`'s own canonical source into `~/.claude/`. This is a
real, standing gap, not a temporary inconvenience to work around silently — if you're setting up a new machine,
expect to repeat these steps by hand, and expect them to need repeating again every time the canonical source
changes.

**Prerequisite**: Node ≥22.6 with TypeScript type-stripping (every skill's own `check.ts` runs directly, no
build step of its own — `agent-plugins` itself pins Node 24 via `.nvmrc`). `gh` authenticated, for the
tracking-PR check (§3 below) to work at all.

### 1.1 The Sub-Agent Itself

The canonical source (`agent-plugins/sub-agents/design-assistant/design-assistant.md`) is body content only —
no YAML frontmatter. The deployed copy (`~/.claude/agents/design-assistant.md`, for Claude Code specifically)
needs that body plus a frontmatter header prepended once:

```yaml
---
name: design-assistant
description: Drives the Design The Feature workflow step for a given project's design directory - Technical Interpretation through Design Review - following next-unit-of-work-detector's own live, per-phase instructions. Invoke explicitly by name to work on a Feature's design; not for general-purpose delegated work.
tools: Read, Edit, Write, Bash, Grep, Glob, TaskCreate, TaskUpdate, AskUserQuestion
---
```

Re-sync whenever the canonical source changes — not automatically on every push, only on your own explicit
decision to pull a given PR's changes forward (this file's own header comment on both the canonical and deployed
copy documents this convention already).

### 1.2 The Skill Family

Each skill is a self-contained directory (`check.ts`, its own tests, `SKILL.md` with its own frontmatter already
included — no transformation needed, unlike the sub-agent above). Deploy by copying each one wholesale:

```
cp -r agent-plugins/claude-skills/{slug}/. ~/.claude/skills/{slug}/
```

...for every skill directory: `behavior-regeneration-checker`, `call-tree-reconciler`, `chunk-scope-utility`,
`gap-classifier`, `next-unit-of-work-detector`, `pseudocode-subset-checker`, `pseudocode-substitution-checker`,
`reconciliation-checksum-utility`, `specific-behavior-presenter`, `thin-shim-consistency-checker`,
`unexpected-side-effect-scanner`, `unhandled-undeclared-exception-sweep` — twelve, as of this writing (see the
[Agent Plugins index](../../agent-plugins.md) §5 for the current, authoritative list; `called-from-backward-walker`
is designed but not yet built, so has nothing to deploy).

`next-unit-of-work-detector`'s own directory also carries `instructions/{phase}.md` — the per-phase text it
attaches to its own output live. These deploy as part of the same `cp -r`, not a separate step.

### 1.3 Verifying It Landed Correctly

```
node ~/.claude/skills/next-unit-of-work-detector/check.ts <any-real-design-dir>
```

...should run and return a real phase/reason (or `complete: true`), not a "command not found" or a module-resolution
error. If it does, the rest of the family is almost certainly fine too, since they all deploy the same way.

## 2 Starting Or Resuming A Design Task

Invoke it with either a fresh assignment ("design UC-002, UC-003 for the {feature-slug} Feature") or, to
resume, just the ticket ref alone ("continue designing WVR-95") — it doesn't need the Feature slug or use case
list repeated; its own `--find-design-task {ref}` reverse lookup resolves that from the ref by itself.

Every session, cold-started or continued, starts the same way regardless of what you tell it: it calls
`next-unit-of-work-detector` against the design directory before doing anything else, and follows whatever
phase that returns. It never assumes it remembers where a previous session left off — document state is the only
source of truth, by design (this is what makes it resumable across a runtime restart, a cold start, or a
hand-off from a different session entirely — all three happened during WVR-95's own dogfooding, and it picked
up cleanly every time).

## 3 The Review Flow — What To Expect

Design Assistant stops and asks at named human-judgement points, never resolving one on its own:
per-gap ideation's "how might we" choice, the §5.1/§5.2 sanity checks on a freshly-derived behavior, an
unexpected side effect's resolution, and every §7.2 Human Review — including all three
`//REDESIGN_REQUIRED` resolutions (accept, reject, remove).

**"Presenting" means committed and pushed, not just described in chat.** Every judgement point is backed by a
real commit on its own tracking PR before it's ever raised with you — you're reviewing against that diff, not a
narration of working-tree state. If you want to look at the actual document yourself rather than trust a
chat-relayed summary, the PR is always there to check directly.

**A confirmation is a real decision, not a formality.** For most first-time reviews (a behavior that's never been
approved before — true for everything on a Feature's own first design task, since nothing has shipped yet for
anything to have been previously approved), Design Assistant will present full detail — the Given/When/Then, the
call tree, provenance for each condition — and wait for you to actually confirm it before `reviewed:` gets set.
A "match" from its own regenerate-and-compare step only means the recorded content is technically still
consistent with the current design; it never substitutes for you actually looking at it the first time.

**Presentation is one at a time, by default.** Design Feature Instructions is explicit about this — batching
dilutes review attention. The one exception seen in practice: a run of behaviors that are all, individually
verified, the exact same already-decided pattern repeating (a function gained a new internal call that changed
several call trees identically, but changed no actual behavior) is worth confirming as one batch rather than
re-litigating the same decision N times. Even then, Design Assistant asked before batching rather than assuming
it — expect it to ask you too, and treat a request to batch as something to actually weigh (has it verified each
one individually first, or is it just similar-looking?), not rubber-stamp.

## 4 Setting Up And Maintaining The Tracking PR

A design task's own branch needs a currently *open* PR against `main` at all times — this is how you watch
design docs change as they happen, and lock in progress by squashing whenever it feels sensible, rather than
finding out later that 90 commits of work sat unreviewed. `next-unit-of-work-detector` checks this on every call
(Step 0) and reports `error` if it's missing — Design Assistant will notice and open one itself, but it won't
happen silently; expect it to say so.

**A real trap, hit once already**: if a design task's original tracking PR was approved and merged early (a
squash-merge), then more work continued on the same branch for a long stretch with no new tracking PR, the
eventual "real" merge back to `main` can hit genuine conflicts — `main`'s squash-merged history and the branch's
own full granular history of that same earlier work look unrelated to git, even though the content mostly
agrees. If this happens: don't assume it's real, conflicting work. Check whether `main`'s version of each
conflicting file is simply an earlier, superseded snapshot of the branch's own progress (a `git diff` against an
earlier commit on the branch itself is the fastest way to confirm) — if so, a `git merge -X ours` (or resolving
each file explicitly to the branch's own version) is usually correct, verified file-by-file rather than assumed.

## 5 Chunk Scope's `new` vs. `mutated`

`mutated`/`deleted` only apply when the behavior being revised belongs to a *different*, already-shipped design
task — something that went through `Chunk The Design` previously and is now being invalidated by *this* task's
own change. Revising your own not-yet-shipped work, within the same still-open design task, always stays `new` —
there's nothing to "mutate" relative to, since nothing has shipped yet for this task to have disturbed. This
matters concretely on a Feature's first design task specifically: nothing in the whole Feature has ever shipped,
so nothing that task's own internal revisions touch can genuinely be `mutated` — if you see a `mutated` entry
show up for a behavior this same task derived, that's worth a second look, not an automatic accept.

## 6 Unexpected Skill Behavior Is A Hard Stop, Not A Bug Report To Ignore

Design Assistant is instructed to stop immediately — not retry, not silently work around it — the moment a
skill's output looks wrong, crashes, or produces a visible false positive/negative. Treat this exactly as
seriously as a finding against the design itself: five real defects in shipped skill code were caught this way
during WVR-95's own dogfooding, three of them silent data corruption or truncation bugs a skill's own test suite
hadn't exercised. If it reports one, the right response is usually: confirm the finding yourself if you can,
ticket the bug, get it fixed and redeployed, then tell it explicitly it's clear to retry — not "just work around
it for now."

## 7 Working Through A Relay vs. Directly

Both patterns work; which one fits depends on how much you want to see firsthand. Early in WVR-95's own
dogfooding, a separate supervising session relayed Design Assistant's findings and confirmations back and
forth — useful when you're also coordinating other concurrent work (a skill-builder session fixing bugs Design
Assistant found, in this case) and don't want to context-switch into the design session itself for every small
confirmation. Once the volume of individual behaviors needing review grew, engaging directly with Design
Assistant's own session became the better fit — you see its actual presentations firsthand rather than a
relayed summary, which matters most exactly when there's a lot of genuine review judgement to exercise in a
short stretch. Neither is more "correct"; switch when the friction of one becomes noticeable.
