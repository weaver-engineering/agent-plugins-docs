# Nested Directory Fixtures

The states witnessing cells @`1.4.1`, @`1.4.2` and @`1.4.3` of
[find-and-read-documentation](../../USE-CASE.md) — one corpus with subdirectories, registered three ways:
without descending, descending to a bound, and descending without one.

## Context
* [find-and-read-documentation](../../USE-CASE.md) - the use case these cells belong to
* [1 — Register A Path](../../operations/1-register-a-path.md) - the condition space they sit in
* [Many Documents Fixtures](../many-documents/FIXTURES.md) - cell @`1.3.1.1.1`, a directory with no subdirectory
  to descend into at all

## 1 The Fixtures

| Fixture | Witnesses | What it is |
|---|---|---|
| [`nested-directory.corpus`](corpus) | @`1.4.1`, @`1.4.2` and @`1.4.3` · **corpus** | one document at the top, one a level down, one two levels down |
| [`nested-directory.registered-shallow`](registered-shallow.md) | @`1.4.1` · **Result** | what the registry holds when no subdirectory was descended into |
| [`nested-directory.report-shallow`](report-shallow.txt) | @`1.4.1` · **Stdout** | the one document registered, in the human rendering |
| [`nested-directory.report-shallow`](report-shallow.json) | @`1.4.1` · **Stdout**, machine rendering | the same report for a caller that will parse it |
| [`nested-directory.registered-bounded`](registered-bounded.md) | @`1.4.2` · **Result** | what the registry holds when the walk stopped one level down |
| [`nested-directory.report-bounded`](report-bounded.txt) | @`1.4.2` · **Stdout** | two documents registered, the third excluded, in the human rendering |
| [`nested-directory.report-bounded`](report-bounded.json) | @`1.4.2` · **Stdout**, machine rendering | the same report for a caller that will parse it |
| [`nested-directory.registered-recursed`](registered-recursed.md) | @`1.4.3` · **Result** | what the registry holds when the walk went all the way down |
| [`nested-directory.report-recursed`](report-recursed.txt) | @`1.4.3` · **Stdout** | all three documents registered, in the human rendering |
| [`nested-directory.report-recursed`](report-recursed.json) | @`1.4.3` · **Stdout**, machine rendering | the same report for a caller that will parse it |

**One corpus, three invocations.** All three cells share a single corpus fixture and differ only in the call,
which is what makes `recurse` a parameter rather than anything the corpus could have told you. This is the
only set in this operation that cannot be told apart by looking at what is on disk.

## 2 What Each Cell Establishes

Without any recursion flag, `index.md` is registered and `onboarding/` is not descended into. Neither document
below it is registered, reported, or treated as an error — the same treatment a non-markdown file gets under a
directory path, for the same reason: they are outside the scope the caller named.

With `--depth 1`, the walk goes one level down: `index.md` and `setup.md` are registered, `editors.md` — two
levels down — is not. This is the cell that actually distinguishes a bound from either extreme: it proves the
walk stops on a number and not merely on "no subdirectories left" or "no flag given".

With `--recurse`, all three are registered. `editors.md` sits two levels below the registered path
deliberately: one level would not distinguish a real walk from a single extra step, and the requirement is
that the walk keeps going rather than that it goes once.

The three `registered` fixtures also settle something the reports cannot show. Each document's registration is
identical in kind however deep it sat and however it got there — same node types, same line ranges, same
words. Depth and the flag together decide which documents are in scope; neither touches how one is registered
once it is, which is why `setup.md`'s own registration is byte-identical whether it arrived via `--depth 1` or
via `--recurse`.

## 3 A Note On The Report's Wording

`editors.md` has one section, and its line reads `1 section` rather than `1 sections`. The human rendering is
prose a person reads at a glance and it is worth being correct; the machine rendering carries the count as a
number and has no such problem.

# Rationale

**Why the shallow cell is kept rather than pruned into @`1.3.1.1.1`.** A flat directory establishes that
documents directly under a path are registered. It cannot establish that a subdirectory was *skipped*, because
it has none to skip. Only a corpus that visibly contains more than was registered shows that descending is a
choice — and without that, an implementation that always recursed would satisfy every other cell in this
operation.

**Why the bounded cell is kept rather than pruned into either extreme.** `1.4.1` shows nothing descended into;
`1.4.3` shows everything did. Neither shows a walk that started and then stopped on its own terms, which is the
one thing `--depth` actually adds over having only an on/off switch — and it is only visible with a corpus that
has somewhere further to go than the bound reaches.

**Why the default is not to recurse.** This analysis does not decide that; the use case does, by describing a
path as "one document or a directory of them". What this fixture set does is make the three behaviours
separately witnessable, so that whichever way the default falls, the other two are still described, required
behaviours rather than accidents of a flag's absence.
