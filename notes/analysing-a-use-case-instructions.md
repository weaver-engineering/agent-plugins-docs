# Instructions — Analysing A Use Case

How to produce a use case's `ANALYSIS.md` by elicitation with the architect.

Three documents belong together, and this is the third:

| | |
|---|---|
| [Analysing A Use Case](analysing-a-use-case.md) | what must be true of an analysed use case |
| [the template](../docs/templates/USE-CASE-ANALYSIS-TEMPLATE.md) | the document that must exist once it is |
| **these instructions** | how to create it |

And one thing that is not a document but is the input to all three: **the use case's examples**. Without them
there is nothing to read a model off, which is why finding or writing them is the first question below rather
than a step of the analysis.

## Work The Document In Order

**The template's order is the work order.** §1 before §2, §2 before §3, and so on down.

It will feel wrong at times. You will be naming attributes before you are certain which the use case needs,
and dimensions before you have seen every space they have to separate. Do it anyway, because **getting it
wrong in this order makes the wrongness legible**: a goal that names no dimension, a dimension that partitions
nothing, a space that cannot be declared because the ordinals to declare it with do not exist. Each of those
reads as nonsense in the prose, and nonsense is what you take back to the architect.

**Going back and reworking is the method, not a failure of it.** Expect §3 to send you back to §2, and §5 to
send you back to §1. Say so when it happens, rework the implications, and carry on. The reason the work is cut
into *analyse a use case* and *analyse an operation* is exactly this: it keeps the blast radius of a
correction inside one document.

**Why the order matters beyond tidiness.** When a use case's analysis is true, every operation in it inherits
a contract — a start space, an end space, and which dimensions are in play — and analysing that operation
against its contract is sound and complete by construction, with their combination delivering the goal because
the spine says it does. Get the use case wrong and every operation analysis beneath it is wrong in a way no
amount of care at operation level will catch.

## How To Work

**Propose, do not interrogate.** At every step, draft an answer from what you already have and ask the
architect to correct it. *"I think these are the four types — what have I got wrong?"* gets a useful answer in
one exchange. *"What are the types?"* gets a paragraph you then have to interpret, and puts the work back on
the person who asked you to do it.

**Ask about one thing at a time.** A step here is one question or one draft. Batching four questions gets
three answered.

**Never invent state.** If you cannot tell what an operation changes, that is a question, not a gap to fill.
A wrong guess written confidently is worse than an open question, because it will be read as elicited.

**You do not approve anything.** The architect does. Your job ends at *here is what I have, here is what does
not yet check out*.

**Name no boundary, service, API or technology.** If one appears in your draft you have started designing.
What must exist to make the analysis true is architecture's question and comes after this.

## Verify At Every Step

**A section is a unit of work.** Draft it, and before moving on:

1. **Review it yourself** against the checks that apply to it. They are listed at each step below.
2. **Say what you think.** *"I believe this is sound"*, or *"these are the corrections I would make"*. Both are
   useful; silence is not.
3. **The architect asserts sound.** It is never your call whether something *is*. You propose, they decide, and
   the difference is not a formality — you are the one who wrote it, and you are the least able to see what is
   missing from it.
4. **On approval the section gains its lock**, and you move on.

## The Document Is Its Own State Engine

Once sections carry locks, the document says what to do next and you do not have to remember. Ask it, and act
on what it says:

| The section's lock | What it means | What to do |
|---|---|---|
| verifies | agreed, and agreed against what it currently rests on | nothing |
| its own content changed | it was edited since approval | review, propose, take it back for approval |
| its content is intact but its ground moved | something it depends on was edited or re-approved | take it back to be re-read in the new context |
| it depends on a section not yet agreed | it cannot be agreed either, whatever its own digests say | settle the section beneath it first |

**A section re-reviewed as sound with no edits updates its own lock and leaves everything downstream alone.**
That is the point of asking. The architect has asserted that the change beneath it does not alter it, so
nothing that depends on it needs re-reading — and a chain that re-opened every section below every change
would be a chain nobody used.

**Where a section's ground has moved, read it yourself first and bring an opinion.** *"§3 is unchanged and I
believe it still holds, because the attribute §1 gained is one no dimension varies"* is worth far more than
*"§3 needs re-reviewing"*. You may be wrong, and being wrong out loud is how that gets found.

**You do not calculate checksums, write frontmatter, or work out by hand what needs re-reading.** That is the
`analysis-lock` skill's job:

```
python3 ~/.claude/skills/analysis-lock/lock.py status <doc>               what holds, and what is next
python3 ~/.claude/skills/analysis-lock/lock.py stamp  <doc> <section>     on the architect's approval, and only then
```

Run `status` at the start of a session and after every approval. It reports each section as agreed, edited,
standing on ground that moved, or blocked behind something not yet agreed, and names the next unit of work.
Where it says `ground-moved` it names what moved, which is what you read the section against.

It also runs the structural checks the document type asks for — that the sections are the ones the type
declares, titled as it says, with subsections numbered without gaps and nothing left as an empty heading.
Those report beside the sections and count as work. They say nothing about whether a section is *right*: the
tool has no opinion on that, and neither do you.

An `ANALYSIS.md` is a `use-case-analysis` to it. It works that out from the section titles the first time and
records it when you stamp; pass `--type use-case-analysis` if it ever asks.

If the skill is unavailable, say so and record approvals in the pull request instead — but do not do its
arithmetic in your head and call the result a lock.

## Editing

Write into the `ANALYSIS.md` as you go, and **commit each turn's work separately**. The pull request is where
the architect reviews: separate commits answer *what changed this turn?* while the branch answers *what is the
state of the whole?* Squash only at a lock-in point, and only when asked.

---

## The First Question — Where Are The Examples?

**Ask this before anything else, and do not start §1 without an answer.** It is
[the method's §1](analysing-a-use-case.md), and this is how it is carried out.

Nobody can name a data model, a dimension or an aspect out of the air. They are read off something concrete:
*these* documents in *this* state, *this* request against them, *this* answer back. An analysis begun without
that is an agent inventing a domain it has no knowledge of and presenting the invention as elicitation — the
single most expensive way this work goes wrong, because everything downstream inherits it and nothing
downstream contradicts it.

**What the examples are for is exposing variation**, and nothing else. You cannot say what must be true of how
a thing changes until you can see how it might change: empty, enormous, absent, cut, not the kind of thing
expected at all. That is what you are looking for in them, and what you take into §2.

**Every one of them must be something that could be true.** An example is an instance of a fixture the
analysis might end up asserting, so it has to be drawn from the same world. Never write data that could not
exist — not a malformed record, not an impossible combination, **not even to show that it would be
rejected**. An invalid combination has no instance to show, which is what makes it invalid.

**What cannot exist gets stated in the analysis, not exhibited in an example.** The `ANALYSIS.md` draws the
boundary by writing down things that are true — *this parameter exists, it has these values, it is not valid
when that one is set* — and the last of those rules a possibility out by being true about the boundary. This
state could exist; this possibility cannot, and the two are said in completely different ways.

**Which unwelcome states get examples: the ones the use case names, and no others.** A use case is the happy
path, and the exceptions it names are the ones with a way round to the goal. Each of those needs an example
just as the main route does, because each is a route to the goal. Everything else on the unhappy path needs
none to start — it is not part of what must be true for the actor to get there. Go through the use case's
extensions, work out which survive the minimum, and say which you covered.

**Where an extension turns out to be a dead end, raise it rather than quietly keeping it.** An exception with
no way round is not an extension at all, however useful it looks. Take it to the architect and let them decide
what happens to it; do not keep the example and hope nobody checks.

### Three Ways This Goes

| The examples | What you do |
|---|---|
| **exist** | read them, then confirm with the architect that they are this use case at the minimum you are analysing. Examples carrying behaviour the minimum cuts pull dimensions into §2 that nothing needs |
| **do not exist, and the architect gives you a seed** | write them from it, and take them back before §1. A seed is the shape of the input, the kind of request, roughly what comes back. It need not be much, and it has to be theirs |
| **do not exist, and there is no seed** | **stop and ask for one.** Say plainly that you cannot write them yourself because you have no knowledge of the domain outside what you have been told. Do not improvise, and do not start §1 anyway |

That third row is the one that matters. You have no context beyond what is in front of you, and a corpus you
invented will read exactly like a corpus somebody chose — right down to the confident file names.

### What Counts As Enough

Examples are indexed by **fixture type per operation** — what the operation is handed, what parameterises it,
the state it acts on, and each shape of result it can produce.

| | |
|---|---|
| **Minimum** | one of every fixture type of every operation, covering the happy path and every exception the use case names; for a state, one of what it could be before and one of what it could be after. None of them related |
| **Better** | several per fixture type, chosen to expose the edges of how that fixture varies. Still unrelated |
| **Better still** | several per fixture type, exposing edges, some of them related |
| **Platinum** | several exposing edges, **and** one fully worked example end to end |

**The minimum is the gate — do not start §1 without it**, and say which rung you are on when you hand the
examples over. A fixture type with no example is an artefact nobody has looked at, and the analysis will
either skip it or invent it.

**Do not aim at platinum.** It is there to be recognised, not targeted, and reaching for it is how examples
become the burden below. Rungs above the minimum get reached by adding one example when elicitation turns up
an edge worth showing.

### Writing Them, If That Falls To You

They live in `examples/` in the use case's own directory, beside `fixtures/` and never inside it, with an
`EXAMPLES.md` as the spine.
[find-and-read-documentation](../docs/analysis/use-cases/find-and-read-documentation/examples/EXAMPLES.md) is
the shape to copy.

**Pick each one because it varies something.** One where a bound is reached, one where nothing comes back, one
where something present can never be reached. Make each as accurate as you reasonably can — accuracy is worth
having where it is cheap — and do not spend effort making them line up into a single run-through. They are
not a story, and coherence exposes nothing. Where two of them *are* related, the pair has to be a combination
that could really have arisen: a state that could not have come from the call beside it is not two examples,
it is one contradiction.

**Stop early.** Examples must not become a burden, and an example worked hard enough to assert something is a
fixture written before the analysis that earns it. Enough to show how things vary is enough.

**An example is not a fixture, and that is why they are filed apart.** A fixture in `fixtures/` witnesses a
cell of a condition space; it exists because analysis found that cell, and it asserts. An example exists
before there is a condition space at all and asserts nothing — it says *this is roughly how this varies*.
Never cite one as a requirement.

### They Change Once, Then They Are Done

Elicitation on top of the examples evolves the model, and that is where an example that was wrong shows up.
Fix it then, out loud, with the architect — that is the one moment examples change. After that the work moves
to aspects, which expose the rough edges of the model itself, and the examples' job is finished. Do not go
back to tidy them. Adding a *new* example later to make a point is cheap and worth doing.

## Step 0 — Read Before You Ask

Read, in this order:

1. The use case's own `USE-CASE.md` — the actor, the goal in prose, the steps, the existing extensions. **This
   is the narrative.** You are not eliciting the story; you are eliciting what must be true for it to hold.
2. **The examples**, in full, including the corpus and every output file. This is where §1's types and §5's
   aspects come from; reading the narrative alone leaves you guessing at both.
3. [Analysing A Use Case](analysing-a-use-case.md), in full.
4. The template, in full.
5. The parent use case's `ANALYSIS.md`, if this use case expands one of its operations. Its types, and the
   operation's start and end space, are your inheritance.
6. Any other `ANALYSIS.md` sharing a type with this one, for what it already declares.

**Do not ask the architect anything you could have read.**

## Step 1 — The Model  *(§1)*

Draft the types the narrative touches, and for each, the attributes it needs. **Minimal, not descriptive** —
an attribute earns its place by being something the story turns on, and you will not be sure which those are
until §2. Draft what you can defend and expect to revise.

**Read them off the examples, not off the narrative.** The state the examples show is a populated instance of
the model you are drafting: every column in it is a candidate attribute, every distinct kind of thing a
candidate type, and anything they never show is an attribute you are about to invent. Where you do add one,
say so out loud — it is either something the examples are missing or something the model does not need, and
the architect is the one who knows which.

For each type, check the analysis type catalog: one already named there keeps that name and its primary key,
neither of which is yours to change. One not there is new, and you are proposing an addition.

**Do not limit yourself to attributes that sound like stored fields.** A modelled attribute only has to be
derivable from whatever design builds; the one the narrative actually turns on is very often not physical at
all — how many are in the list, whether the thing is populated, how well the prose answers. Those are good
attributes.

**An attribute that comes from other data says so in its description, as **derived from**.** Naming it
derived does not oblige the model to carry what derives it — if behaviour only changes on the size of the
list, declare the size and leave the members out, and every fixture is that much cheaper. Name the sources
this model carries; describe the ones it does not. Where the model *does* carry both a collection and
something derived from it, check they agree: a model that contradicts itself cannot produce a true example or
a true fixture.

Write the class diagram and the attribute tables. A foreign key names its target as **link-to**:
`{TypeName}`.

**Ask:** which of these types already exists elsewhere under another name? A type nobody else has named is
either genuinely new or a synonym, and only the architect knows which.

## Step 2 — Ordinals And Validity Rules  *(§1.{n}.1, §1.{n}.2)*

For every attribute, its discrete values. **`not-set` is always one of them.**

Then the validity rules over those ordinals:

* **Which attributes are required?** An unconditional rule ruling `not-set` invalid is how that is said, and
  several attributes can share one rule. There is no separate notion of required.
* **Which are required only sometimes?** That is the conditional form, and it is the one people reach for a
  flag to express and cannot.

Name each rule, because §2.{n+1} cites them.

## Step 3 — The Dimensions  *(§2, §2.{n}, §2.{n}.1)*

Which variations does this use case's narrative turn on? Draft them from the story, one dimension per thing
that changes the telling.

For each: its ordinals, and at §2.{n}.1 **how the aspect's physical values partition into them** — completely,
without overlap. This is where a half-modelled dimension shows itself. Ask what happens at the values nobody
mentioned.

Run the both-ends check with the architect:

* Every dimension varies an aspect of §1. One that varies nothing is not a dimension.
* Every aspect §1 declares is varied by a dimension, or is marked `INVARIANT`. Ask why an `INVARIANT` one is
  declared at all.

**Expect this to send you back to §1**, either for an attribute a dimension needs or to delete one nothing
varies.

## Step 4 — Invalidity Rules  *(§2.{n+1})*

Combinations this use case will not accept, from two sources, each saying which:

* **From the model** — extracted from a validity rule, citing it.
* **From the use case** — a state the model permits and this use case will not start from, giving a reason.

Ask for the second kind explicitly. It is easy to miss, because nothing in the model says it and the architect
may not think to volunteer it.

## Step 5 — The State Spaces  *(§3)*

**§3.1 first, the entry space:** what states may this use case validly start from? **Do not accept "any" by
default.** Whatever the entry space admits, the first operation must answer for, and a wide entry is the
single most expensive thing in a use case. If it really is any state, that should be said out loud.

Then every other space the narrative names, declared as not-applicable rules over §2, in the actor's
vocabulary — **loaded**, **jammed**, **summed**.

**A space's name is its identity.** Where two points in the story produce the same thing they carry the same
name; where you cannot tell whether two are the same, that is the question, and the answer decides whether an
operation later faces one space or a union.

**Expect this to send you back to §2**: a space you cannot declare is usually a dimension you have not named.

## Step 6 — The Spine  *(§4, §4.1, §4.2)*

Draw the graph. Every edge is named after the state space it carries.

Then §4.1's transitions and §4.2's transformations. For each operation, say **what it does to the state and
what drives it** — *for every order line, reduce that product's stock by the line item count*. That sentence
is what tells a reader whether the operation is one thing or several.

**Checks, each a question rather than a fix:**

* Does every transition name a space declared at §3?
* Does each operation's in-space follow from its predecessor's out-space?
* Does any operation change nothing? A smell with three causes — a verbose use case, a wasteful process, or an
  incomplete analysis — and which one it is has to be asked.

Leave §4.2's last column empty until Step 8.

## Step 7 — The Extensions  *(§4.3)*

For each operation ask: **what can go wrong here that the actor works around?** Only those.

A use case has no dead ends. An exception is declared only where there is a way round to the same goal —
jiggle the doodah, not burn the computer. A failure the actor cannot work around is not part of the use case,
and the operation will owe graceful failure for it regardless.

The `USE-CASE.md`'s existing extensions are candidates, not answers. Expect several not to survive: one whose
only remedy is *stop* is not an extension.

**An extension always has somewhere to go.** Its destination defaults to whatever follows the operation it
extends — the next operation, or **the goal** where it extends the last. Naming a destination is how it goes
somewhere else instead, usually back. There is no such thing as an extension with no destination, so do not
check for one.

So an extension of the last operation may name nothing and simply be that operation done another way, or it
may name an earlier one and send the actor round again. The peg board has both shapes available at operation
4; it happens to use the second.

**Checks:**

* Does its end space contain the start space of whatever it goes to — the next operation's, or the goal where
  it reaches the goal?
* Where it returns to an earlier operation, does that operation now face a wider entry space? It does, and
  Step 8 is where that is paid for.

## Step 8 — What Is Owed A Full Analysis  *(§4.2's last column)*

The cost of an operation is the product of its entry space and what may be done with it, and both are in the
row already. Three signals:

* its entry space is wide — usually the first operation
* an extension returns to it, so its entry space is a union
* its end space names something its entry space and payload cannot account for, which means it **creates**
  that state

An operation with none of them still gets the claim that its transformation is unconditional, which is worth
being wrong about in public.

## Step 9 — The End State And The Goal  *(§5)*

Write the comparison: every dimension, at entry and at end.

Then ask the architect to mark **the goal** — which of the changed dimensions the actor came for. Only now can
it be enumerated, because only now do the dimensions exist to enumerate it with. §5.2 and §5.3 follow from it
and are written out rather than left derived.

**Checks:**

* At least one dimension is marked the goal.
* Every dimension so marked changed between the columns. One that did not was already true.
* A dimension unconstrained at both ends is not an invariant. It is one the use case does not need, and it
  should be released for an operation to claim — ask before deleting it.
* If nothing changed at all, the goal is a state reached partway and the use case has been drawn too long, or
  the model is missing what the actor came for.

**If the goal reads as nonsense here, the fault is upstream.** A goal that names no dimension, or names one
whose ordinals do not describe what the actor wanted, is §2 or §1 being wrong — and it is meant to surface
here, which is why the goal is last.

## Step 10 — Open Questions, The Checks, And Hand Over  *(§6)*

Write §6: what is genuinely unresolved. A dimension whose ordinals do not yet partition their aspect. A type
whose primary key the analysis has not had to settle. A step that cannot be shown to matter and has not been
chased down. Not a hedge against having done the work.

Then go through these with the architect, reporting what does not hold rather than fixing it quietly:

| | Check |
|---|---|
| 1 | Every dimension varies an aspect of the model; every aspect is varied or `INVARIANT` |
| 2 | Every dimension's ordinals partition its aspect completely and without overlap |
| 3 | Every invalidity rule cites a validity rule or gives a reason |
| 4 | Every transition names a space declared at §3 |
| 5 | Every extension returns to an operation whose start space its end space contains |
| 6 | At least one dimension is the goal, and every goal dimension changed |
| 7 | No dimension is unconstrained at both entry and end |
| 8 | The model uses the catalog's type names and primary keys, and adds nothing it does not need |
| 9 | Nothing in the document names a boundary, a service or a technology |
| 10 | Every type and attribute in §1 appears in the examples, or is named as something the examples do not carry |
| 11 | Every variation the examples expose is either varied by a dimension or declared `INVARIANT` |
| 12 | Every fixture type of every operation has at least one example, and every example is something that could be true |

Then stop. Say what is written, what checks out, what does not, and what you asked that was not answered.
**The architect approves it; you do not.**

## When You Get Stuck

| Symptom | What it usually means |
|---|---|
| A dimension you cannot tie to the model | the model is missing an attribute, or the dimension is really two |
| A space you cannot declare | a dimension is missing, or its ordinals do not cover the case |
| Two operations' spaces do not join up | a step is missing, or one operation does more than its sentence says |
| A step that changes nothing | verbose use case, wasteful process, or incomplete analysis — ask which |
| An extension with nowhere to return | not an extension; the use case cannot complete there |
| A goal that reads as nonsense | §1 or §2 is wrong; this is where that surfaces |
| The end state equals the entry state | the goal is a state reached partway, or the model is missing what the actor came for |
| Every operation looks expensive | the entry space is too wide, and constraining it is the cheaper fix |
| You want to name a service | you have crossed into architecture; write what must be true instead |
| You are inventing corpus, payloads or results to reason about | there are no examples, or you have gone past the ones there are — stop and ask |
| An example shows something the analysis cannot express | one of the two is wrong; take both to the architect rather than choosing |
| You are tidying the examples | their work is done; go back to the analysis |
