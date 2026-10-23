# UI Walkthrough

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-252](https://linear.app/weaver-engineering/issue/WVR-252) - the ticket this design fulfils
* dem-ambient's design-ui (WVR-253, WVR-254, WVR-255, in DEM's `dem-docs`) - the first consumer; it quotes the contract in §3
* [The skill's code](https://github.com/weaver-engineering/agent-plugins/tree/main/claude-skills/ui-walkthrough) - in `agent-plugins`, with its full reference, schemas and worked example (§3.10)

## 1 Purpose

Assembles a UI layout from wireframe **views** and renders one image per **step** of a **walkthrough**, with a generated
markdown page per step that presents it in its walkthrough, under a diagram of the walkthrough with the step
highlighted. A project's UI design is then shown as walkthroughs a human reviews as a static document, readable in any
markdown renderer. It is not a prototyper.

A walkthrough is any sequence of screens a reviewer walks through, with its branches. It is analysis: what must be true
of the UI, not how the UI is built (§4.18). One may describe a use case, and the first consumer's mostly do, but a
walkthrough need not follow a use case's rules, so the skill never speaks of use cases; it only links to the page a
walkthrough says it describes.

Three firm requirements shape everything below:

* **The skill reads only its own documents and writes only its own outputs.** Its inputs are files whose format the
  skill defines (§3). A consuming project's own documents, such as a use case or a view's design, are never
  read; an agent extracts the skill's inputs from them, or a tool such as DEM produces them mechanically from claims.
  Keeping the inputs consistent with the design is the producer's job, not the skill's.
* **A view's wireframe is written once and never copied.** The assembled HTML exists only in memory while a step
  renders.
* **It is generic.** No project's names, paths or views appear in the skill. DEM is only the first user.

## 2 Trigger

Used whenever a project's UI design changes a view, a walkthrough's outline, or a step: render the walkthrough or the
affected steps, then run `check`. `check` is also what a gate runs.

## 3 The Contract

Agreed with the architect on 21 October 2026, while designing DEM's UI. The skill's own documentation (§3.10) is the
full reference; this section is its design.

### 3.1 Configuration

One file, `ui-walkthrough.yaml`. The skill is run from where the walkthroughs are and finds the nearest one on the path up
from the current directory, like git finds `.git`. Every path in it is relative to the directory holding it; step names
and walkthrough names passed to `render` are relative to where the skill is run. A subdirectory with its own file lets a repo segregate its
walkthroughs, for instance one per Feature (architect, 20 October 2026):

```yaml
views: docs/analysis/ui/views
tokens: docs/analysis/ui/tokens.css
walkthroughs: docs/analysis/ui/walkthroughs/*/WALKTHROUGH.yaml
viewports: { desk: 1440x900, tablet: 1024x768, tablet-portrait: 768x1024 }
```

A viewport is `WIDTHxHEIGHT`, width first. Walkthroughs, their views and the tokens are analysis, so they sit together
under it, a walkthrough describing a use case taking the use case's slug; the UI's design sits elsewhere and links to
them (§4.18; architect, 23 October 2026).

### 3.2 Inputs and outputs

| File | Role | Written by |
|---|---|---|
| `ui-walkthrough.yaml` | configuration | the project |
| tokens stylesheet | shared styling | the project |
| `{views}/{VIEW-NAME}/VIEW.html` | the view's wireframe | the project |
| `{views}/{VIEW-NAME}/VIEW.yaml` | what the wireframe needs to be drawn: types, state, slots, components, bindings, descriptions | an agent or DEM |
| `{walkthrough}/WALKTHROUGH.yaml` | the walkthrough's outline: its title, what it describes, and each step's title, narrative and chain | an agent or DEM |
| `{walkthrough}/{step}/STEP.yaml` | the step's screen, or screens: how each is assembled | an agent or DEM |
| `{step}/STEP.png` | the rendered screen; the first screen, when there are several | the skill |
| `{step}/STEP-{n}.png` | the rendered screen `n`, from 2, of a step with several | the skill |
| `{step}/STEP.md` | the step as a static document in its walkthrough | the skill, entirely |
| `{step}/FLOW.svg` | the walkthrough as a diagram, this step highlighted | the skill, entirely |
| `{walkthrough}/WALKTHROUGH.md` | the walkthrough's overview: its diagram and a link to every step | the skill, entirely |
| `{walkthrough}/WALKTHROUGH.svg` | the whole walkthrough as a large diagram, every step's narrative in its box | the skill, entirely |
| `{views}/{VIEW-NAME}/VIEW.png` | the view drawn alone, its slots showing their placeholders | the skill, entirely |
| `{views}/{VIEW-NAME}/VIEW.md` | the project's page for the view; the skill writes two marked blocks in it | the project, and the skill its blocks |

A view's directory may hold other files; the skill ignores them. Of the project's own `VIEW.md` it reads only the blocks
it writes (§4.16). `VIEW.yaml`,
`WALKTHROUGH.yaml` and `STEP.yaml` are the persisted data the skill is called with, so any step can be regenerated from
them alone.

### 3.3 VIEW.html

An HTML fragment that follows these standards, so the skill can assemble it:

* Its one root element is `<section data-view="VIEW-NAME">`, optionally preceded by one `<style>`. The name is the
  directory's, in UPPER-KEBAB case.
* No scripts, no external resources. Styling comes from the tokens stylesheet's custom properties plus the view's own
  `<style>`.
* A **slot** is an element marked `data-slot="SLOT-NAME"`. The views that fill it replace its content; it keeps the size
  its parent gives it. A slot holding many views lays them out with the view's CSS, e.g. `[data-slot="CARDS"] { display: grid; }`.
* A **component** is any element marked `data-component="COMPONENT-NAME"`: a button, a title, a banner.
* Each slot and component name appears once, and no name is both.
* The wireframe draws its own placeholder content, which is what a step shows wherever nothing binds or overrides it.
  Inside a slot that is a **slot placeholder**, drawn one way by every view: `<div data-placeholder>SLOT-NAME</div>`,
  which the skill styles as a box crossed corner to corner with the slot's name centred, in the tokens stylesheet's
  `--walkthrough-placeholder` (§4.11).
* **State hooks:** the skill writes the view's top-level enum and boolean state onto the root (§4.3), and the view's CSS
  selects on them: `[data-view="CARD"][data-mode="selected"]`, `[data-view="CARD"][data-shared]`.

### 3.4 VIEW.yaml

```yaml
description: One file, shown as a card in a matrix.
types:                                   # what the wireframe's state is made of
  Card:
    name: string
    status: enum[draft, locked, archived]
    shared: boolean
state:
  mode: { type: "enum[default, selected]", default: default }
  card: Card
  changes: { type: number, description: The changes since the last review. }
slots:
  BODY: { views: [DOC-DIFF, FILE-LIST], description: What the card shows when it is opened. }
components:
  TITLE: { text: card.name, description: The file's name. }
  OPEN:
    visible: card.status != archived
    enabled: card.status == draft
    description: Opens the file for review. Only a draft can be opened.
  SHARE: { description: Shares the file. }   # as drawn unless a step overrides it
image: { width: 300, state: { mode: selected } }   # how VIEW.png draws the view alone
```

* `description` is optional on the view, each slot and each component. It is what `STEP.md` shows when a step
  describes or highlights the element (§4.5).
* `types` declares the record types the view's state uses (§3.5). A type used by several views must be declared
  identically in each (§4.7).
* `state` declares the view's state attributes, each a type or `{ type, default, description }`; the two forms mean
  the same. They are what steps set and bindings read, modelling the wireframe, not the UI (§4.18).
* `slots` declares each slot with the views it allows, and `many: true` if it holds a list of them. A slot may allow
  views not defined yet, or none yet (§4.11).
* `components` declares each component with optional bindings: `text` (a path), `visible` and `enabled` (predicates),
  per §3.6. Any component can be overridden by a step whether bound or not.
* `image` says how `VIEW.png` draws the view alone: its `viewport`, its `width`, as the slot it sits in would give it,
  and its `state` (§4.16).

Slots and components must match `VIEW.html`'s `data-slot` and `data-component` names exactly. A state attribute's
`source` and a component's `unbound: true`, which §4.16 once asked for, are accepted and ignored (§4.18).

### 3.5 Types and state

| Type | Values |
|---|---|
| `string`, `number`, `boolean` | as YAML |
| `enum[a, b, c]` | one of the names listed |
| `string<<stereotype>>`, e.g. `string<<card-ref>>` | a string; the stereotype is carried for the reader and not checked |
| `list<T>` | a list of `T`; may be declared and given, never read by a binding (§4.4) |
| `map<K, V>`, e.g. `map<string <<Slug>>, string>` | a mapping of keys to values; `K` is `string` or a stereotyped string, `V` any type; like a list, declared and given, never read by a binding |
| a record type name, e.g. `Card` | a mapping of the record's fields |

Types are written as the design writes them: a stereotype is any name, with or without a space before `<<`, and
types nest. Type names are UpperCamel, attribute and field names lower-kebab. Everything about a view is state, including its
visual mode, which is an enum attribute such as `mode`.

An attribute's value in a step is the step's value, else its `default`, else **unset**. Values may be partial: a step
may give a record only the fields it cares about.

### 3.6 Bindings and predicates

A **path** names an attribute or a record field of the view's own state: `card.name`. A `text` binding is a path to a
string, number, enum or stereotyped string, shown as its value.

A **predicate**, for `visible` and `enabled`, is:

```
pred  := or
or    := and ("or" and)*
and   := unary ("and" unary)*
unary := "not" unary | "(" pred ")" | test
test  := path                                     (a boolean)
       | path ("==" | "!=") literal
       | path ("<" | "<=" | ">" | ">=") number    (a number)
       | path "in" "[" literal ("," literal)* "]"
```

A literal is a number, `true`, `false`, an enum value, or a quoted string. Every path and literal is type-checked
against the view's declared state when the view is loaded. A binding applies only when every path it reads is set;
otherwise the component stays as the wireframe draws it. Predicates read only the view's own state and literals: never
another view's state, never another attribute compared with this one.

### 3.7 WALKTHROUGH.yaml

A walkthrough is a directory holding its outline, `WALKTHROUGH.yaml`, and a directory per step beside it, named as the
outline keys it: main step 3 is `03-…`, extension 3a is `03a-…`, and the first step is `01-…` (§4.12).

```yaml
title: Review a spec
describes: [{ title: Review a spec, path: docs/analysis/use-cases/review-a-spec/USE-CASE.md }]
steps:
  01-open:
    title: Open the project
    narrative: The reviewer opens the project and sees the files waiting.    # markdown, copied into STEP.md as written
    next:
      - { step: 02-pick, label: Pick a file }
  02-pick:
    title: Pick a file
    narrative: |
      The reviewer scans the matrix and picks the spec they were asked to review.
    next:
      - { step: 03-review, label: Open it }
      - { step: 02a-give-up, label: Give up }
  02a-give-up: { title: Give up, end: the spec waits for the next session }
  03-review: { title: Review the spec, end: the spec is reviewed }
```

* `title` is the walkthrough's, at the top of every page.
* `describes`, optional, lists what the walkthrough describes, such as its use case, each a `title` and a `path` from
  the project's root. `WALKTHROUGH.md` links each under its title; one that does not exist is a problem (§4.18).
* Each step has a `title`, an optional `narrative`, and exactly one of `next` (the steps it leads to, each with the
  choice it stands for) or `end` (how the walkthrough ends there).
* Step `01` is always a way in, labelled *Start*. Any step may be another, by giving `entry: {label}`, such as
  `entry: Opens a saved project` (§4.13). Every step must be reachable through `next` from step `01` or another entry.
* A step may be a walkthrough of its own, by giving `walkthrough: {directory}`, the other walkthrough's directory from
  the project's root, such as `walkthrough: docs/analysis/ui/walkthroughs/approve-a-document` (§4.17).
* A step the outline names with no `STEP.yaml` yet is pending (§4.11): it gets its page and diagram, saying its screen is
  not yet drawn. A `STEP.yaml` in a directory the outline does not name is a problem.

### 3.8 STEP.yaml

The step's screen, or its screens, and nothing else:

```yaml
viewport: tablet
root: APP
slots:                                    # VIEW.SLOT → a view, a list of views (many: true), or null; unbound, its placeholder
  APP.MAIN: CARD-MATRIX
  CARD-MATRIX.CARDS: [CARD, CARD]
  CARD#1.BODY: null
  CARD#2.BODY: DOC-DIFF
state:                                    # instance → attribute values
  CARD#2: { mode: selected, card: { name: spec-v3.md, status: locked } }
  CARD#1: { card: { name: notes.md, status: draft } }
components:                               # overrides: these win over any binding
  CARD#2.OPEN: { visible: true, enabled: true }
  DOC-DIFF.SAVE: { text: Saved }
describe: [CARD-MATRIX.CARDS]             # level 1: description in STEP.md
highlight: [CARD#2.OPEN]                  # level 2: description in STEP.md, and outlined in STEP.png
```

* `viewport` and `root` are required. `viewport`, `root`, `slots`, `state`, `components` and `highlight` are what the
  image's hash covers (§5.4); `describe` reaches only `STEP.md`.
* Views are addressed by instance (§4.6): `CARD` when placed once, `CARD#n` when placed more than once.
* A slot has three meanings: bound to a view or a list, it shows them; bound to `null`, it is deliberately empty; left
  unbound, it shows its placeholder (§4.11).
* An override sets `visible` or `enabled` to `true`/`false`, or `text` to a string.
* A `describe` or `highlight` entry names a placed view instance, a slot `VIEW.SLOT`, or a component `VIEW.COMPONENT`.

A step whose story takes more than one screen lists the screens after the first under `screens` (§4.14). Each has a
caption, as the first screen then must, and gives only what changes from the screen before it:

```yaml
caption: The reviewer reads the spec        # the first screen's caption; required when screens is given
screens:                                    # screens 2, 3, … in order
  - caption: The reviewer approves it
    state: { DOC-REVIEW: { approved: true } }
    components: { DOC-REVIEW.APPROVE: { text: Approved } }
    highlight: [DOC-REVIEW.BANNER]
```

* An entry may give any screen field: `viewport`, `root`, `slots`, `state`, `components`, `describe`, `highlight`.
* `slots` merge by key; `state` by instance, then attribute; `components` by key, then property. `viewport` is kept
  unless given.
* `describe` and `highlight` are never carried over: each screen names what it draws attention to.
* An inherited slot, state or component entry for a view the screen no longer places is dropped; one the screen gives
  itself is still an error.
* An entry giving `root` starts afresh, keeping only the viewport.
* `caption` reaches only `STEP.md`, like `describe`.

### 3.9 STEP.md, FLOW.svg and the overview

Written by the skill from `WALKTHROUGH.yaml`, the step's `STEP.yaml`, the descriptions in `VIEW.yaml` and the tokens
stylesheet. Both are marked or known as generated, and a hand edit is overwritten. A reviewer pages through a
walkthrough's steps, which look alike, so each page first says where the reviewer is (§4.13):

```markdown
<!-- Generated by ui-walkthrough from WALKTHROUGH.yaml and STEP.yaml. Do not edit. -->
# Review a spec

↑ [The whole walkthrough](../WALKTHROUGH.md)

## 02 Pick a file

[![Where 02 Pick a file sits in Review a spec](FLOW.svg)](../WALKTHROUGH.md)

| Previous | Next |
|:---|---:|
| ← *Pick a file* from [01 Open the project](../01-open/STEP.md) | *Open it*: [03 Review the spec](../03-review/STEP.md) → |
|  | *Give up*: [02a Give up](../02a-give-up/STEP.md) → |

The reviewer scans the matrix and picks the spec they were asked to review.

![02 Pick a file](STEP.png)

**Views:** [APP](../../../views/APP/VIEW.md), [CARD-MATRIX](../../../views/CARD-MATRIX/VIEW.md), [CARD](../../../views/CARD/VIEW.md)

## In this step

* **CARD#2.OPEN** (highlighted): Opens the file for review. Only a draft can be opened.
* **CARD-MATRIX.CARDS**: The files waiting for review.
```

1. The walkthrough's title and a link to its overview, then the step's number and title.
2. `FLOW.svg`: the whole walkthrough as a diagram, the same layout on every page of it, with this step filled and the
   routes into and out of it drawn heavier, each in its own colour. It links to the overview too.
3. The navigation, between the diagram and the step's own content: the way back on the left, the ways on on the right.
   "Previous" lists a way in first, *Start* for step `01` or the step's `entry` label, then every step whose `next` leads
   here, ordered by step name, each with the choice that leads here. "Next" lists the step's `next` in its order, each with its choice and the step it leads to; a
   step that ends the walkthrough has `**End:** {end}`.
4. A step that is a walkthrough of its own says so, linked to that walkthrough's page (§4.17). Then the narrative, then
   the image, or, for a step with no `STEP.yaml` yet, a line saying its screen is not yet drawn, or, for one that is a
   walkthrough, that walkthrough's overview diagram, linked to its page. Every image is framed (§4.18). Under it,
   **Views** links the `VIEW.md` of each view the screen places, once each, in the order placed.
   A step of several screens shows each in order in place of 4's image and 5: a heading `### {n}. {caption}`, the
   screen's image and views, and its own entries, listed as in 5.
5. "In this step" lists highlighted entries first, then described ones, each in the order the step gives them, and is
   left out when there are none. An entry with no description shows its name alone. A slot showing its placeholder adds
   *Not yet defined: shows a placeholder.* to its entry (§4.11).

Beside each `WALKTHROUGH.yaml` the skill writes the walkthrough's overview (§4.15), from the outline and the tokens
stylesheet:

```markdown
<!-- Generated by ui-walkthrough from WALKTHROUGH.yaml. Do not edit. -->
# Review a spec

Describes [Review a spec](../../../use-cases/review-a-spec/USE-CASE.md).

![The whole of Review a spec](WALKTHROUGH.svg)

## Steps

* [01 Open the project](01-open/STEP.md): a way in, *Start*
* [02 Pick a file](02-pick/STEP.md)
* [02a Give up](02a-give-up/STEP.md): ends the walkthrough
* [03 Review the spec](03-review/STEP.md): ends the walkthrough; *not yet drawn*
```

What the walkthrough describes, if it says, then `WALKTHROUGH.svg`, then a link to each step's page in step order, saying which steps are ways in, which are
walkthroughs of their own, linked to them, which end the walkthrough and which have no `STEP.yaml` yet. A walkthrough
that is a step of others links up to each of those steps under its title, as each of its steps' pages does beside the
link to its overview (§4.17).

### 3.10 The skill's documentation and worked example

The skill's directory carries its full documentation, because the installed copy is what an agent reads:

* [`SKILL.md`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/SKILL.md): when and how to run it.
* A complete reference for each of the skill's own files:
  * [`VIEW.html`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/view-html.md): the standards a wireframe follows;
  * [`VIEW.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/view-yaml.md): the types, state, slots and components that drive the wireframe;
  * [bindings](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/bindings.md): paths and predicates;
  * [`WALKTHROUGH.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/walkthrough-yaml.md): the outline, the story and the chain;
  * [`STEP.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/step-yaml.md): the screen, instance addresses, describe and highlight;
  * [`STEP.md`, `FLOW.svg` and the overview](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/step-md.md): the pages and diagrams the skill generates;
  * [`VIEW.png` and the blocks in `VIEW.md`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/view-md.md): each view drawn alone, and what the skill writes on its page.
* JSON Schemas (§4.8): [`ui-walkthrough.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/schemas/ui-walkthrough.schema.json),
  [`WALKTHROUGH.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/schemas/walkthrough.schema.json),
  [`VIEW.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/schemas/view.schema.json) and [`STEP.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/schemas/step.schema.json).
* [`example/`](https://github.com/weaver-engineering/agent-plugins/tree/main/claude-skills/ui-walkthrough/example): a fully worked walkthrough with its own `ui-walkthrough.yaml`, views, outline, steps and
  the rendered `STEP.png`, `STEP.md` and `FLOW.svg` of every step, and its overview. It exercises the whole contract: nested slots, a slot holding many views,
  instance addresses, a record type, bindings, an override, `describe`, `highlight`, a step of two screens, an extension and an end. It is also
  the test fixture (§4.9). Its first page is
  [`01-open/STEP.md`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/example/analysis/ui/walkthroughs/review-a-spec/01-open/STEP.md).

### 3.11 Modes

* `render <step>…` renders the steps named: each screen's image if it is stale or missing (`--force` renders it anyway),
  removing the image of any screen the step no longer has, and every view's `VIEW.png` that is stale or missing; then
  every `STEP.md`, `FLOW.svg`, `WALKTHROUGH.md`, `WALKTHROUGH.svg` and `VIEW.md` block under the configuration
  that differs from what would be generated.
* `render --walkthrough DIR` does the same for every step of a walkthrough, so a whole walkthrough is one command.
* `render --view NAME` does the same for every step that uses the view; with `--force` it renders the view's own image
  too.
* `uses NAME` lists the steps that use a view, without rendering.
* `check` lists every problem, then everything pending (§4.11), and exits non-zero if there is any problem.
  `check --complete` also exits non-zero if anything is pending. The problems are:
  * a `WALKTHROUGH.yaml`, `VIEW.yaml`, `STEP.yaml` or configuration that breaks its schema;
  * a `STEP.yaml` in a directory its outline does not name;
  * a view problem (§5.1), or a type declared differently by two views (§4.7);
  * an assembly error (§5.2);
  * a screen's image that is stale, missing or invalid, or that belongs to a screen the step no longer has;
  * a step with `screens` whose first screen has no `caption`;
  * a `STEP.md`, `FLOW.svg`, `WALKTHROUGH.md` or `WALKTHROUGH.svg` that is missing or differs from what would be
    generated;
  * a view's `VIEW.png` that is stale, missing or invalid, or whose `image` settings cannot be drawn; a `VIEW.md` that
    is missing, lacks either block, or whose blocks differ from what would be generated; markers that are not one begin
    followed by one end (§4.16);
  * a page a walkthrough `describes` that does not exist;
  * a chain problem (§5.6).

## 4 Decisions

### 4.1 Rendering: HTML to PNG with Playwright, and an install step

HTML/CSS gives flow, flex and grid for free, and "the slot keeps the size its parent gives it" is plain CSS. SVG would
need every nested size and position computed by hand, is token-dense, and is less rich; the restraint it imposes on
wireframes is already provided by the tokens file and the `VIEW.html` standards.

The mechanical logic (§5) is Node with small pure-JavaScript dependencies: `yaml`, an HTML parser
(`node-html-parser`) and a JSON Schema validator (`ajv`). Only the renderer needs a browser, and it sits behind one
narrow interface: assembled HTML plus a viewport in, PNG bytes out. So `check` and `uses` need no browser and run in CI
without one; `check` compares hashes and never re-renders.

The browser is **Playwright** with its own pinned Chromium, not `puppeteer-core` against an installed Chrome: the PNGs
are committed and reviewed, and a re-render on another machine must not produce a visibly different image. (The hash
is over inputs, so determinism is not needed for staleness, only for review.)

This **ends the "no install step" convention for this skill.** The skill carries its own `package.json` with exact
versions, and a documented install step that is plain Node, identical under Claude, Codex or OpenCode:

```
cd ~/.claude/skills/ui-walkthrough && npm install && npx playwright install chromium
```

`npm install`, not `npm ci`: the deployed directory has no lockfile. `claude-skills/README.md` says a skill may
declare dependencies and must name its install command.

### 4.2 The skill reads only its own documents

Reading a project's own documents, such as a view's `VIEW.md`, a use case or a hand-written step page, would couple the skill to
their format and let it drift from what they say elsewhere. The one exception is the blocks the skill writes into
`VIEW.md` (§4.16), which it reads only to find its own markers. So the skill's inputs are `VIEW.yaml`,
`WALKTHROUGH.yaml` and `STEP.yaml`, structured and defined here, and `STEP.md` is an output.

This puts the boundary where DEM already sits. DEM can produce `VIEW.yaml` mechanically from its claims, or an agent
extracts it from the analysis natively. Either way, the skill checks only what it owns: its schemas, its types, and the
views and steps against each other. Whether the UI's design satisfies the walkthroughs is the design's to show, and the
project's to check (§4.18).

### 4.3 Everything is state

A view's visual mode is not a separate concept: `mode: enum[default, selected]` is an attribute like `card: Card`. To
let a wireframe's CSS style its modes, the skill writes each **top-level enum or boolean** attribute that is set onto the
view's root element: an enum as `data-ATTR="value"`, a boolean as `data-ATTR` when true and nothing when false.
Records, strings and numbers are not written, so the root stays readable and CSS never depends on data.

### 4.4 Bindings and overrides, and why this is not a prototyper

Binding a component's text, visibility and enablement to the view's state states the design's rules once, in the view,
where a reviewer reads them as part of the design: "OPEN is enabled when the card is a draft." Steps then give data in
the walkthrough's own terms and the screen follows; `check` catches a step that gives a value the data model does not
allow.

Every component can still be overridden in any step, bound or not, because this is a static document: a step may need
to show a combination the bindings would not produce, and saying so explicitly is clearer than bending the data.

Limits that keep it from becoming a prototyper:

* A predicate reads only its own view's state and literals (§3.6). A card does not work out from its parent whether it
  is selected; the step sets `mode: selected` on it, which is visible and checked.
* Data never creates views. A list of cards is `[CARD, CARD]` in the step's `slots`; a `list<T>` or `map<K, V>`
  attribute may be declared, so the wireframe's state can say what it shows, but nothing reads it.
* Nothing carries from one step to the next: each step gives its state in full, falling back only to the declared
  defaults.
* No formatting in text bindings: a path, shown as its value.

### 4.5 Describe and highlight

A step names what it is about at one of two levels:

1. `describe`: the entry's description is included in `STEP.md`.
2. `highlight`: the description is included, and the entry is outlined in `STEP.png`.

An entry may be in only one of the two lists. The outline is 3px around the element's bounding box, drawn as an overlay
measured after layout, so it takes no space and moves nothing. Its colour is `--walkthrough-highlight` from the tokens
stylesheet, with a fixed default; views never draw their own highlight. Highlighting a `null` slot is allowed: "this area is
deliberately empty" can be the point of a step. Highlighting an element that has no box in the rendering, such as a
hidden component, is a render error.

Only `highlight` changes the image, so it is in the input hash and `describe` is not.

### 4.6 Slots holding many views, and instance addresses

A slot declared `many: true` is bound to a list of views, `CARD-MATRIX.CARDS: [CARD, CARD, CARD]`, placed in order; the
view's CSS lays them out. A list names at least one view; `null` is the empty binding for any slot. A slot without
`many` takes one view or `null`. Every view placed in a slot must be one of the views it allows, and defined.

A view may be placed more than once, in a list or in different slots. Each placement is an **instance**:

* A view placed once is addressed by its name, `CARD`.
* A view placed more than once is addressed `CARD#1`, `CARD#2`, … in placement order: depth first from the root,
  through a view's slots in the order its `VIEW.yaml` declares them, and through a list in its order.
* The address is used everywhere a view is named: slot keys (`CARD#2.BODY`), `state`, `components`, `describe` and
  `highlight`. A slot of an instance left unbound shows its placeholder (§4.11).
* A bare `CARD` when several are placed is an assembly error, as is `CARD#n` when there is no nth `CARD`, and `CARD#1`
  when `CARD` is placed once.
* A view placed inside an instance of itself is a cycle and is rejected.

### 4.7 Shared types agree across views

Each `VIEW.yaml` carries the types its wireframe's state uses, so a type such as `Card` is declared in every view that
uses it. The skill checks that every declaration of a type name is identical, field for field, which costs it nothing
and catches a view left behind when a type changes.

### 4.8 The schemas ship with the skill and are what it validates against

The JSON Schemas are files in the skill's directory, and the skill validates its inputs with them (`ajv`) before its own
checks. So the schemas a producer validates against are exactly what the skill enforces, and cannot drift from it. What a
schema cannot express, such as a predicate's types or an instance address, the skill checks itself and its reference
documents.

### 4.9 The worked example is the test fixture

The example in the skill's documentation (§3.10) is what the tests run on. The tests render it and compare each generated
`STEP.md` with the committed one, and `check` must pass on it, which proves each committed `STEP.png` carries the hash of
its current inputs. So the example cannot fall behind the skill. Tests of individual problems derive their inputs from the
example by changing one file.

### 4.10 Other points

* **Invalid image** means not a PNG, or no hash in its metadata. It never means the pixels look wrong.
* **Viewport:** the screenshot is exactly the viewport size, not the full page, framed (§4.18).
* **Fonts:** the tokens stylesheet must not depend on a system font, or renders drift between machines.

### 4.11 Drawn a walkthrough at a time: pending steps, slots and placeholders

A design is drawn one walkthrough at a time, so a view's slots are declared before the views that fill them exist: a shell's
navigation, main area and dock in the first increment, and the views that fill them over the increments after. So:

* A slot may allow views not defined yet, or none yet. Neither is a problem; each is **pending**.
* A step the outline names may have no `STEP.yaml` yet; it is pending, and still gets its page and diagram (§4.12),
  unless it is a walkthrough of its own, which need draw no screen. A walkthrough a step is, not written yet, is
  pending (§4.17).
* A step leaves a slot unbound to show its placeholder, the content `VIEW.html` draws inside the slot element. `null`
  stays the deliberately empty slot, which is a design decision, not a gap. An unbound slot is pending.
* Binding a slot to a view not defined yet is an assembly error: the step leaves it unbound until the view exists.
* `STEP.md` never presents a placeholder as designed: a described or highlighted slot showing its placeholder says it is
  not yet defined.
* `check` lists what is pending after the problems, and passes while only pending remains. `check --complete` fails on
  anything pending, so a gate can demand a finished design when it should be one, and a forgotten slot is still caught.
* The placeholder is drawn one way by every view (§3.3), styled by the skill's own stylesheet in the assembled page, so
  its colour comes from the tokens stylesheet and its look cannot drift between views.

Whether a slot is bound is part of the step's screen fields, so binding a slot later stales the step's image (§5.4).

### 4.12 The walkthrough's outline is a document of its own

A walkthrough's story and chain were first kept in each step's `STEP.yaml`. They belong together instead, in one
`WALKTHROUGH.yaml` per walkthrough:

* The chain is one thing, and is now written in one place. The diagram, the navigation and the chain checks read it
  whole, rather than reassembling it from every step.
* The outline can be written first, as the bones of the walkthrough, and the whole walkthrough generated from it in one
  command (`render --walkthrough`). A step without a screen yet still gets its page, so the flow can be reviewed before
  any screen is drawn, and screens added step by step.
* `STEP.yaml` becomes only the screen, so everything in it but `describe` is what the image's hash covers.
* It is a walkthrough's outline, not a use case's: it carries a title, steps, narratives and choices, and nothing a use
  case's rules require.

The steps are keyed by their directory names, so a step's directory, its key and its number in the diagram are one name.

### 4.13 The diagram: a fixed picture with a moving highlight

Paging through a walkthrough, every page looks alike, so a reviewer loses their place. Each page therefore opens with
the walkthrough's title, the step's, and a diagram of the whole walkthrough with the step highlighted and its routes in
and out drawn distinctly, then the navigation, and only then the step's own content.

* **The layout is the same on every page of a walkthrough**, so the highlight is the only thing that moves: one column
  per step number, the main step on the top row and its extensions on the rows below (`02a` on row 1, `02b` on row 2).
  The layout comes from the step numbers alone, never from the current step.
* **Routes are square and leave and enter boxes only by their sides.** Every vertical stretch runs in the gap between
  two columns and every long horizontal stretch in the gap between two rows, each route in a lane of its own and with a
  port of its own on each box side, so no route crosses a box or runs along another. Forward routes leave by the right
  and enter by the left, running straight across to the next column on the same row; back routes leave by the left and
  enter by the right; routes down a column use the gap on its left, and routes up it, or back to the same step, the gap
  on its right. Each gap widens to hold the lanes run in it. Choices label their routes, each placed along its route
  where it overlaps no other label and no box and, where there is such a place, crosses no other route.
* **A box grows to hold its routes.** A step every other step returns to, such as curate-a-check-set's editor, can have
  twenty routes on one side, which at a fixed size spilled past its corners into the gaps, where they met other routes.
  So each box grows across the flow, about the middle of its row, until its outermost port keeps a clearance from its
  corners: taller in `FLOW.svg`, wider in the overview. Its row widens with it; the other boxes in the row keep their
  own size, centred.
* **Facing sides share their ports.** A box's right side and the left side of the box across the gutter from it each
  had ports spread about the same middle, so the short stretches from each to its gutter lane lay along one another.
  The two sides' ports are now one set of lanes, so no two stretches in a gutter share a line; a route straight across
  takes one port at both ends.
* **A step that repeats is drawn as a route back to itself**, since "this step repeats for each registry" is part of
  the flow a reviewer follows.
* **A walkthrough may have more than one way in.** A use case can be entered other than at its first step: changing a
  saved project starts from the projects list, not from starting a new one. Without a second entry the only way to make
  such a step reachable is an edge from a later step, and the diagram then shows a way in as a branch. So any step may
  give `entry: {label}`; step `01` is always an entry, as *Start*. Each entry is drawn as an arrow from a dot into its
  step's left side, on the topmost port there, its label ending at the dot, and the reachability check starts from all
  of them. The label is a string rather than a flag so that each way in says how the reviewer arrives, as each `next`
  says its choice.
* **It is an SVG the skill writes as text**, not a Mermaid block or a rendering through the browser: it shows in any
  markdown viewer, its layout is the skill's to keep fixed, and `check` compares it as text with no browser. An image
  cannot read the tokens stylesheet, so its colours (`--walkthrough-current`, `--walkthrough-in`, `--walkthrough-out`,
  `--walkthrough-flow`) are read from it when the diagram is written, with defaults.
* The navigation sits between the diagram and the step's content, previous on the left and next on the right, as a
  two-column table, the one layout markdown offers.

### 4.14 Several screens in one step: a straight sequence of changes

Some steps of a use case take more than one screen: a dialog filled in, then the list it adds to, then the dialog that
completes it. Splitting those into steps sharing a step number misrepresents the use case, whose step is one, and gives
the walkthrough branches it does not have. So a step may show several screens, on its one page.

* **A straight sequence, never branching.** Branches are steps, in `WALKTHROUGH.yaml`, where the diagram shows them.
  Within a step the screens are read in order; going back to an earlier screen is told in a caption or the narrative,
  since a static page has nothing to draw for it.
* **Each screen a change to the one before.** The screens of one step are mostly the same screen, so each later one
  says only what changes, as the step was told in the use case. Changes merge at the level a step writes them: a slot,
  an instance's attribute, a component's property. `describe` and `highlight` are not carried over, since what a
  screen draws attention to is what changed on it. Rebinding a slot removes the views it showed, so what the screen
  inherited for them is dropped rather than reported: otherwise every small change that swaps a view would have to be
  written out whole. Only inherited entries are dropped, so a typo in a screen's own entry is still caught. A new `root` makes every address on the screen before meaningless,
  so a screen giving one starts afresh rather than inheriting entries that would all be errors.
* **The first screen is the step's own fields.** A step of one screen is unchanged, and its image is still `STEP.png`;
  later screens are `STEP-2.png` on, so the names sort in reading order. Each image carries the hash of its own screen
  (§5.4), so changing screen 3 stales only screens 3 onward. An image left by a screen since removed is reported, and
  removed by `render`, as the skill owns every image it names.
* **Captions are required once there are several,** because the page needs a heading for each screen and the reviewer
  needs to know what changed between them.

### 4.15 The overview: the whole flow, readable in place

`FLOW.svg` keeps a reviewer's place, but at the top of a page it is small: a markdown page is laid out to its width, so
a diagram drawn across is shrunk to fit, and its boxes have room for a title only. A reviewer could not follow the flow
without clicking through it. So each walkthrough also gets an overview page, `WALKTHROUGH.md`, whose diagram is drawn to
be read where it is.

* **The same layout, turned a quarter.** One row per step number, top to bottom, the main step on the left and its
  extensions to its right; routes leave and enter a box only by its top and bottom, with the same lanes, ports and
  gaps as §4.13. A page scrolls down, so a diagram drawn downwards keeps its size.
* **Each box carries the step's whole narrative**, wrapped, with its title and how it ends, so the flow can be reviewed
  as a story without opening any step. Each row is as tall as its tallest box.
* **Routes are coloured by the step they leave**, their labels with them, so routes running side by side can be told
  apart. Nothing is highlighted.
* **Links live in the page, not the image.** A link inside an image shown in markdown cannot be followed, so the page
  lists every step with a link to its `STEP.md`. Every `STEP.md` links back, both from a line under the walkthrough's
  title and from its `FLOW.svg`.
* **It stays an SVG written as text, from the outline alone**, like `FLOW.svg` (§4.13): it is sharp at any size, and
  `check` compares it with no browser. A step's `STEP.yaml` does not reach it.

### 4.16 Each view reviewed on its own: VIEW.png and blocks in VIEW.md

A reviewer saw a view only as steps assembled it, filled with other views, so a view on its own could not be reviewed,
and nothing checked that a view's page said what its wireframe does. So each view gets an image of itself, and its page
a block generated from `VIEW.html` and `VIEW.yaml`.

* **`VIEW.png` draws the view alone**, every slot showing its placeholder whatever the wireframe draws in it, so each
  slot can be seen. Drawn at the viewport's width, a view that sits in a narrow slot would be stretched across the
  screen, and with its state unset it shows none of its states, so `VIEW.yaml` may give `image: { viewport, width,
  state }`. The image is cropped to the view. Its hash covers what a step's does (§5.4) and the width; `image` reaches
  no step's image.
* **A block in the project's `VIEW.md`, not a page of the skill's.** A project's `VIEW.md` carries what the skill
  cannot derive, in DEM the capabilities a view serves, the calls it makes, what updates it live, so the skill neither
  owns the page nor adds a second one beside it. It writes one block between markers: the image, the slots linked to
  the views they hold, and every step that places the view. The block first also listed the components, state and
  types, which §4.18 took out. The block goes wherever the project puts the markers; without them it is added at the end, and
  without a `VIEW.md` one is written. Markers it cannot read as one block are left for the project to put right.
* **The page leads with the view** (architect, 23 October 2026). With the image in the one block, at the end of DEM's
  pages, a page all about the view showed it only after four sections of prose. So the image moved to a second, **view
  block**, which leads the page: what the view is, from `VIEW.yaml`'s `description`, then `VIEW.png`. The project moves
  it under a heading of its own, DEM's unnumbered `## The View` between its Context and §1, and the rest of its page
  explains the view in more detail. The
  description is the one `STEP.md` shows when a step describes the view, so the page cannot say otherwise. A page
  without the view block's markers gets it under its `# ` title, so every existing page gains it on the next render;
  the block of slots and uses stays where it was.
* **Documenting a view moves no pixel.** Descriptions are left out of every hash, as are the sources and `unbound`
  marks now ignored, and an attribute is hashed by what it means, `{ type, default }`, however it is written, so
  writing `card: Card` out in full to describe it stales nothing.

### 4.17 Nested walkthroughs: a step that is a walkthrough

Use cases nest: a step of one is often a whole use case of its own, such as browsing for a path while setting up a
project, or curating a check set from its picker. The step and the walkthrough it is are linked both ways, so a reviewer
can go down into the detail and come back up to where they were.

* **The step names the walkthrough, not the other way round.** `walkthrough: {directory}` on the step, the directory
  `render --walkthrough` takes. The step is where the nesting is decided, and a walkthrough may be a step of several
  others; each finds its parents by every step naming it, so the link up is derived, never written twice.
* **The step keeps its place in its own chain.** It has its own title, narrative and `next` or `end`: how the outer
  flow continues is the outer walkthrough's to say. The nested walkthrough's ends are not mapped onto the outer step's
  `next`; the narrative says how it comes back.
* **A screen is optional.** With no `STEP.yaml` the step shows the nested walkthrough's overview diagram in place of a
  screen, and is not pending, since the walkthrough is where its screens are. With one, its screens are drawn as any
  step's, such as the screen the nested walkthrough starts from.
* **Links live in the pages.** Down: the step's `STEP.md` and its walkthrough's `WALKTHROUGH.md`. Up: the nested
  walkthrough's `WALKTHROUGH.md` and every one of its `STEP.md`s name each step it is. In both diagrams the step's box
  has a second border inside its first, and in `WALKTHROUGH.svg` it names the walkthrough, since a link in an image
  cannot be followed.
* **Written one at a time.** A walkthrough named but not found by the configuration's glob is not written yet: pending,
  named as such on the pages, so an outer walkthrough can be drawn before the ones it nests. A step naming its own
  walkthrough is a problem.
* **Only pages change.** Nesting is in the outline, which reaches no image (§5.4), so adding or moving it rewrites
  pages and diagrams only.

### 4.18 Analysis, not design: the wireframe model, framed images, and what a walkthrough describes

Reviewed on a big screen, a step's image was hard to tell from the page around it, and the view pages listed
components and state that a reviewer read as the UI's design (architect, 23 October 2026).

* **A walkthrough is analysis.** It says what must be true of the UI; the views it names are views the UI must have.
  How the UI makes it true, its components, state, types and where each value comes from, is design, written by a
  design pass of its own in the project's design, which links to the walkthroughs and views it satisfies. Analysis
  never links to design, and the skill neither reads nor writes it.
* **`VIEW.yaml` models the wireframe, not the UI.** Its components and state are whatever lets the wireframe behave as
  the UI must: DEM draws a split button that opens to a second action as two components shown one at a time, which no
  real UI need have. So the `VIEW.md` blocks leave out components, state and types, and the pending items §4.16 added,
  a component neither bound nor marked `unbound` and a state attribute without a `source`, are dropped: they asked for
  design in the wrong place. `source` and `unbound` stay valid and do nothing, so a project's existing views keep
  passing, and are left out of the hash, so removing them stales nothing.
* **Every image is framed.** `STEP.png`, `STEP-{n}.png` and `VIEW.png` have a 2px grey border with square corners, drawn
  into the PNG round the screenshot, so it shows in any markdown viewer; a style on the image would be stripped. The
  image is 4px larger each way than the viewport or view. The skill's major version was raised so every image is
  stale once, and one render draws the frames. The diagrams are not framed: they are the document's, not the UI's.
* **A step links its views.** Each screen of a `STEP.md` lists the views it places, linked to their `VIEW.md`, so a
  reviewer can go from a screen to each view on its own.
* **A walkthrough may say what it describes.** `describes` links the use case, or any page, a walkthrough describes from
  its `WALKTHROUGH.md`. It is optional, since a walkthrough can be drawn for any reason, and one-way: the use case may
  link to its walkthrough, as analysis links analysis, but the skill never writes into it.

## 5 Algorithm

### 5.1 Loading views

Each directory under `{views}` is a view. A view's problems are reported once, not once per step using it:

* a missing `VIEW.html` or `VIEW.yaml`, or a `VIEW.yaml` that breaks its schema;
* a `VIEW.html` that breaks §3.3: its root, a script, a name used twice or for both a slot and a component;
* slots or components that differ between `VIEW.yaml` and `VIEW.html`;
* an unknown type, a record type used before it is declared in the view, a default of the wrong type;
* a binding that does not parse, names an unknown path, or does not type-check (§3.6).

Then every type name declared by more than one view is compared (§4.7). A slot allowing a view not defined yet, or none,
is pending rather than a problem (§4.11).

### 5.2 Assembly

From the step's `root`, place each view depth first: number its instance (§4.6), resolve its state (step values over
defaults), write its state hooks (§4.3), apply its bindings and then the step's overrides to its components, then fill
each slot with the views bound to that slot's address, in order. Each instance's slots and components are found in its
own wireframe before the views filling its slots are inserted, so one view's names never reach into another's. Slots,
components and view roots are marked with their address for the highlight to find.

Rejected, with an error naming the step and the offender:

* a `STEP.yaml` that breaks its schema, or an unknown viewport;
* an unknown view, slot or component;
* a view a slot does not allow or that is not defined yet, a list in a slot without `many`, or an empty list;
* an ambiguous or unknown instance address, or a cycle;
* a state value that does not match its declared type, or an unknown attribute or field;
* an override of the wrong type;
* a `describe` or `highlight` entry that names nothing placed, or an entry in both;
* a problem with any view placed (§5.1).

The assembled document is the tokens stylesheet plus the nested fragments, held in memory and never written.

### 5.3 Uses

A step uses a view if, on any of its screens, the view is the `root` or is bound in `slots`, alone or in a list. `uses NAME` and
`render --view NAME` both use this and need no browser.

### 5.4 Input hash and staleness of STEP.png

One hash per screen. SHA-256 over, in a fixed order and each length-prefixed: the skill's major version, raised to 2
when every image was framed (§4.18); the screen's
fields (`viewport`, `root`, `slots`, `state`, `components`, `highlight`), after the changes from the screens before it
and without inherited entries it drops (§4.14), as canonical JSON; for each placed instance, sorted
by address, its resolved state as canonical JSON, its `VIEW.html`, and its `VIEW.yaml` without descriptions, sources,
`unbound` or `image`, each attribute and field in the form `{ type, default }`, as canonical JSON; the tokens
stylesheet; and the viewport as `WIDTHxHEIGHT`. A view's `VIEW.png` is hashed the same way, its screen being the view as
root with its `image` state, and its `image` width added (§4.16).

So a change to the outline, to a step's `describe` or `caption`, or to any description, never stales an image; a change to
anything that can move a pixel always does. Only placed views count, so editing an unused view stales nothing. The
hash is written to a PNG text chunk when rendering. A step is stale when the hash in its `STEP.png` differs from the
one recomputed now, missing when there is no `STEP.png`, invalid per §4.10.

### 5.5 Generating STEP.md, FLOW.svg and the overview

`STEP.md` is a pure function of the walkthrough's outline, the step, and the descriptions of its described and
highlighted entries, laid out per §3.9. `FLOW.svg` is a pure function of the outline, the step and the tokens
stylesheet's colours (§4.13). `check` generates both in memory and compares; `render` writes each when it differs. A
step's page is not generated while its `STEP.yaml` has problems; its diagram is, since it needs only the outline.
A step's page also links the views each screen places. `WALKTHROUGH.md` is a pure function of the outline and which
steps have a `STEP.yaml`, and `WALKTHROUGH.svg` of the
outline and the tokens stylesheet's colours (§4.15); both are compared and written the same way. A nested walkthrough's
title and directory reach the pages and overview of the steps that are it, and the titles of those steps and their
walkthroughs reach its pages (§4.17).

### 5.6 The chain

From each walkthrough's `WALKTHROUGH.yaml`, reported by `check`:

* a `next` entry naming a step that is not in the outline;
* a step reachable from neither step `01` nor any step giving `entry`, or no step `01`;
* a step with neither `next` nor `end`, or with both;
* a step naming its own walkthrough as the walkthrough it is.

## 6 Output

`render` writes `STEP.png`, `STEP-{n}.png`, `STEP.md`, `FLOW.svg`, `WALKTHROUGH.md`, `WALKTHROUGH.svg` and `VIEW.png`
files, and the blocks in each `VIEW.md`, and removes only a `STEP-{n}.png` of a screen
a step no longer has. `uses` prints step paths, one per line. `check` prints one
problem per line, then one line per pending item, each marked `pending:`; it exits non-zero if there are any problems, or
with `--complete` if anything is pending. Nothing writes a copy of any wireframe.

## 7 Parked

* Bindings beyond text, visibility and enablement: attributes, images, formatted text, views generated from lists.
* Checking a stereotyped string, such as that a `card-ref` names a card in the step.
* Interaction: images only, no clickable prototype.
