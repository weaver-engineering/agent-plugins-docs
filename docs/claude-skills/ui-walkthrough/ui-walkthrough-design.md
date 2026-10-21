# UI Walkthrough

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-252](https://linear.app/weaver-engineering/issue/WVR-252) - the ticket this design fulfils
* dem-ambient's design-ui (WVR-253, WVR-254, WVR-255, in DEM's `dem-docs`) - the first consumer; it quotes the contract in §3
* [The skill's code](https://github.com/weaver-engineering/agent-plugins/tree/main/claude-skills/ui-walkthrough) - in `agent-plugins`, with its full reference, schemas and worked example (§3.9)

## 1 Purpose

Assembles a UI layout from wireframe **views** and renders one image per **step** of a use case, with a generated
markdown page per step that presents it in its use case's chain. A project's UI design is then shown as walkthroughs a
human reviews as a static document, readable in any markdown renderer. It is not a prototyper.

Three firm requirements shape everything below:

* **The skill reads only its own documents and writes only its own outputs.** Its inputs are files whose format the
  skill defines (§3). A consuming project's own documents, such as a view's design notes or its data model, are never
  read; an agent extracts the skill's inputs from them, or a tool such as DEM produces them mechanically from claims.
  Keeping the inputs consistent with the design is the producer's job, not the skill's.
* **A view's wireframe is written once and never copied.** The assembled HTML exists only in memory while a step
  renders.
* **It is generic.** No project's names, paths or views appear in the skill. DEM is only the first user.

## 2 Trigger

Used whenever a project's UI design changes a view, a step, or the chain between steps: render the affected steps,
then run `check`. `check` is also what a gate runs.

## 3 The Contract

Agreed with the architect on 21 October 2026, while designing DEM's UI. The skill's own documentation (§3.9) is the
full reference; this section is its design.

### 3.1 Configuration

One file, `ui-walkthrough.yaml`. The skill is run from where the use cases are and finds the nearest one on the path up
from the current directory, like git finds `.git`. Every path in it is relative to the directory holding it; step names
passed to `render` are relative to where the skill is run. A subdirectory with its own file lets a repo segregate its
walkthroughs, for instance one per Feature (architect, 20 October 2026):

```yaml
views: docs/design/ui/views
tokens: docs/design/ui/tokens.css
steps: docs/analysis/use-cases/*/walkthrough/*/STEP.yaml
viewports: { desk: 1440x900, tablet: 1024x768, tablet-portrait: 768x1024 }
```

A viewport is `WIDTHxHEIGHT`, width first.

### 3.2 Inputs and outputs

| File | Role | Written by |
|---|---|---|
| `ui-walkthrough.yaml` | configuration | the project |
| tokens stylesheet | shared styling | the project |
| `{views}/{VIEW-NAME}/VIEW.html` | the view's wireframe | the project |
| `{views}/{VIEW-NAME}/VIEW.yaml` | the view's data model, state, slots, components, bindings, descriptions | an agent or DEM |
| `{step}/STEP.yaml` | the step: its story, its chain, and how its screen is assembled | an agent or DEM |
| `{step}/STEP.png` | the rendered screen | the skill |
| `{step}/STEP.md` | the step as a static document in its use case's chain | the skill, entirely |

A view's directory may hold other files, such as the project's own `VIEW.md`; the skill ignores them. `VIEW.yaml` and
`STEP.yaml` are the persisted data the skill is called with, so any step can be regenerated from them alone.

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
types:                                   # the data model this view uses
  Card:
    name: string
    status: enum[draft, locked, archived]
    shared: boolean
state:
  mode: { type: "enum[default, selected]", default: default }
  card: Card
slots:
  BODY: { views: [DOC-DIFF, FILE-LIST], description: What the card shows when it is opened. }
components:
  TITLE: { text: card.name, description: The file's name. }
  OPEN:
    visible: card.status != archived
    enabled: card.status == draft
    description: Opens the file for review. Only a draft can be opened.
  SHARE: { description: Shares the file. }   # no bindings: as drawn unless a step overrides it
```

* `description` is optional on the view, each slot and each component. It is what `STEP.md` shows when a step
  describes or highlights the element (§4.5).
* `types` declares the record types the view's state uses (§3.5). A type used by several views must be declared
  identically in each (§4.7).
* `state` declares the view's state attributes, each a type or `{ type, default, description }`.
* `slots` declares each slot with the views it allows, and `many: true` if it holds a list of them. A slot may allow
  views not defined yet, or none yet (§4.11).
* `components` declares each component with optional bindings: `text` (a path), `visible` and `enabled` (predicates),
  per §3.6. Any component can be overridden by a step whether bound or not.

Slots and components must match `VIEW.html`'s `data-slot` and `data-component` names exactly.

### 3.5 Types and state

| Type | Values |
|---|---|
| `string`, `number`, `boolean` | as YAML |
| `enum[a, b, c]` | one of the names listed |
| `string<<stereotype>>`, e.g. `string<<card-ref>>` | a string; the stereotype is carried for the reader and not checked |
| `list<T>` | a list of `T`; may be declared and given, never read by a binding (§4.4) |
| a record type name, e.g. `Card` | a mapping of the record's fields |

Type names are UpperCamel, attribute and field names lower-kebab. Everything about a view is state, including its
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

### 3.7 STEP.yaml

A step is a directory under a use case's `walkthrough/`, named after the use case's numbering: main step 3 is `03-…`,
extension 3a is `03a-…`. The first step is `01-…`.

```yaml
title: Pick a file
narrative: |                              # markdown, copied into STEP.md as written
  The reviewer scans the matrix and picks the spec they were asked to review.
next:                                     # or, for a step that ends the use case:  end: the file is open
  - { step: 03-review, label: Open it }
  - { step: 02a-give-up, label: Give up }
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

* `title`, `narrative`, and exactly one of `next` or `end` are the step's story and chain.
* `viewport`, `root`, `slots`, `state`, `components` and `highlight` are its screen.
* Views are addressed by instance (§4.6): `CARD` when placed once, `CARD#n` when placed more than once.
* A slot has three meanings: bound to a view or a list, it shows them; bound to `null`, it is deliberately empty; left
  unbound, it shows its placeholder (§4.11).
* An override sets `visible` or `enabled` to `true`/`false`, or `text` to a string.
* A `describe` or `highlight` entry names a placed view instance, a slot `VIEW.SLOT`, or a component `VIEW.COMPONENT`.

### 3.8 STEP.md

Written by the skill from `STEP.yaml`, the `STEP.yaml` of the steps around it, and the descriptions in `VIEW.yaml`. It is
marked generated, and a hand edit is overwritten. Its layout:

```markdown
<!-- Generated by ui-walkthrough from STEP.yaml. Do not edit. -->
# 02 Pick a file

## Previous

* *Pick a file* from [01 Open the project](../01-open/STEP.md)

The reviewer scans the matrix and picks the spec they were asked to review.

![02 Pick a file](STEP.png)

## In this step

* **CARD#2.OPEN** (highlighted): Opens the file for review. Only a draft can be opened.
* **CARD-MATRIX.CARDS**: The files waiting for review.

## Next

* *Open it*: [03 Review the spec](../03-review/STEP.md)
* *Give up*: [02a Give up](../02a-give-up/STEP.md)
```

"Previous" and "Next" let a reviewer walk the use case forwards and backwards, every branch included, and approve
how the UI supports it step by step. "Previous" lists every step whose `next` leads here, ordered by step name, each with
the choice that leads here; the first step has none, and the section is left out. "Next" lists the step's `next` in its
order, each with its choice and the title of the step it leads to. A step that ends the use case has `**End:** {end}` in
place of "Next". "In this step" lists highlighted entries first, then described ones, each in the order the step gives them, and is left out
when there are none. An entry with no description shows its name alone. A slot showing its placeholder adds
*Not yet defined: shows a placeholder.* to its entry (§4.11).

### 3.9 The skill's documentation and worked example

The skill's directory carries its full documentation, because the installed copy is what an agent reads:

* [`SKILL.md`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/SKILL.md): when and how to run it.
* A complete reference for each of the skill's own files:
  * [`VIEW.html`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/view-html.md): the standards a wireframe follows;
  * [`VIEW.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/view-yaml.md): the data model, types, state, slots and components;
  * [bindings](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/bindings.md): paths and predicates;
  * [`STEP.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/step-yaml.md): the story, the chain, the screen, instance addresses, describe and
    highlight;
  * [`STEP.md`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/reference/step-md.md): the page the skill generates.
* JSON Schemas (§4.8): [`ui-walkthrough.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/schemas/ui-walkthrough.schema.json),
  [`VIEW.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/schemas/view.schema.json) and [`STEP.yaml`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/schemas/step.schema.json).
* [`example/`](https://github.com/weaver-engineering/agent-plugins/tree/main/claude-skills/ui-walkthrough/example): a fully worked use case with its own `ui-walkthrough.yaml`, views, steps and the rendered
  `STEP.png` and `STEP.md` of every step. It exercises the whole contract: nested slots, a slot holding many views,
  instance addresses, a record type, bindings, an override, `describe`, `highlight`, an extension and an end. It is also
  the test fixture (§4.9). Its first page is
  [`01-open/STEP.md`](https://github.com/weaver-engineering/agent-plugins/blob/main/claude-skills/ui-walkthrough/example/use-cases/UC-1-review-a-spec/walkthrough/01-open/STEP.md).

### 3.10 Modes

* `render <step>…` renders the steps named: each one's `STEP.png` if it is stale or missing (`--force` renders it anyway),
  then every `STEP.md` under the configuration that differs from what would be generated.
* `render --view NAME` does the same for every step that uses the view.
* `uses NAME` lists the steps that use a view, without rendering.
* `check` lists every problem, then everything pending (§4.11), and exits non-zero if there is any problem.
  `check --complete` also exits non-zero if anything is pending. The problems are:
  * a `VIEW.yaml`, `STEP.yaml` or configuration that breaks its schema;
  * a view problem (§5.1), or a type declared differently by two views (§4.7);
  * an assembly error (§5.2);
  * a `STEP.png` that is stale, missing or invalid;
  * a `STEP.md` that is missing or differs from what would be generated;
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

Reading a project's own documents, such as a view's `VIEW.md` or a hand-written step page, would couple the skill to
their format and let it drift from what they say elsewhere. So the skill's inputs are `VIEW.yaml` and `STEP.yaml`,
structured and defined here, and `STEP.md` is an output.

This puts the boundary where DEM already sits. A view's attributes and types are claims in DEM, so DEM can produce
`VIEW.yaml` mechanically and assert that its data model matches the design's data model documents. Without DEM, an
agent extracts the same file from the design natively. Either way, the skill checks only what it owns: its schemas,
its types, and the views and steps against each other.

### 4.3 Everything is state

A view's visual mode is not a separate concept: `mode: enum[default, selected]` is an attribute like `card: Card`. To
let a wireframe's CSS style its modes, the skill writes each **top-level enum or boolean** attribute that is set onto the
view's root element: an enum as `data-ATTR="value"`, a boolean as `data-ATTR` when true and nothing when false.
Records, strings and numbers are not written, so the root stays readable and CSS never depends on data.

### 4.4 Bindings and overrides, and why this is not a prototyper

Binding a component's text, visibility and enablement to the view's state states the design's rules once, in the view,
where a reviewer reads them as part of the design: "OPEN is enabled when the card is a draft." Steps then give data in
the use case's own terms and the screen follows; `check` catches a step that gives a value the data model does not
allow.

Every component can still be overridden in any step, bound or not, because this is a static document: a step may need
to show a combination the bindings would not produce, and saying so explicitly is clearer than bending the data.

Limits that keep it from becoming a prototyper:

* A predicate reads only its own view's state and literals (§3.6). A card does not work out from its parent whether it
  is selected; the step sets `mode: selected` on it, which is visible and checked.
* Data never creates views. A list of cards is `[CARD, CARD]` in the step's `slots`; a `list<T>` attribute may be
  declared, so a view's data model matches the design's, but nothing reads it.
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

Each `VIEW.yaml` carries the data model it uses, so a type such as `Card` is declared in every view that uses it. The
skill checks that every declaration of a type name is identical, field for field. DEM checks the views against the
design; the skill checks the views against each other, which costs it nothing and catches a view left behind when a type
changes.

### 4.8 The schemas ship with the skill and are what it validates against

The JSON Schemas are files in the skill's directory, and the skill validates its inputs with them (`ajv`) before its own
checks. So the schemas a producer validates against are exactly what the skill enforces, and cannot drift from it. What a
schema cannot express, such as a predicate's types or an instance address, the skill checks itself and its reference
documents.

### 4.9 The worked example is the test fixture

The example in the skill's documentation (§3.9) is what the tests run on. The tests render it and compare each generated
`STEP.md` with the committed one, and `check` must pass on it, which proves each committed `STEP.png` carries the hash of
its current inputs. So the example cannot fall behind the skill. Tests of individual problems derive their inputs from the
example by changing one file.

### 4.10 Other points

* **Invalid image** means not a PNG, or no hash in its metadata. It never means the pixels look wrong.
* **Viewport:** the screenshot is exactly the viewport size, not the full page.
* **Fonts:** the tokens stylesheet must not depend on a system font, or renders drift between machines.

### 4.11 Drawn a use case at a time: pending slots and placeholders

A design is drawn one use case at a time, so a view's slots are declared before the views that fill them exist: a shell's
navigation, main area and dock in the first increment, and the views that fill them over the increments after. So:

* A slot may allow views not defined yet, or none yet. Neither is a problem; each is **pending**.
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

A step uses a view if the view is its `root` or is bound in its `slots`, alone or in a list. `uses NAME` and
`render --view NAME` both use this and need no browser.

### 5.4 Input hash and staleness of STEP.png

SHA-256 over, in a fixed order and each length-prefixed: the skill's major version; the step's screen fields
(`viewport`, `root`, `slots`, `state`, `components`, `highlight`) as canonical JSON; for each placed instance, sorted
by address, its resolved state as canonical JSON, its `VIEW.html`, and its `VIEW.yaml` without descriptions as
canonical JSON; the tokens stylesheet; and the viewport as `WIDTHxHEIGHT`.

So a change to a step's narrative, chain or `describe`, or to any description, never stales an image; a change to
anything that can move a pixel always does. Only placed views count, so editing an unused view stales nothing. The
hash is written to a PNG text chunk when rendering. A step is stale when the hash in its `STEP.png` differs from the
one recomputed now, missing when there is no `STEP.png`, invalid per §4.10.

### 5.5 Generating STEP.md

`STEP.md` is a pure function of the step's `STEP.yaml`, the titles and `next` labels of its previous steps, the titles
of its next steps, and the descriptions of its described and highlighted entries, laid out per §3.8. `check`
generates it in memory and compares; `render` writes it when it differs.

### 5.6 The chain

From each use case's `STEP.yaml` files, reported by `check`:

* a `next` entry naming a step that does not exist in the use case;
* a step not reachable from step `01`;
* a step with neither `next` nor `end`, or with both.

## 6 Output

`render` writes `STEP.png` and `STEP.md` files and nothing else. `uses` prints step paths, one per line. `check` prints one
problem per line, then one line per pending item, each marked `pending:`; it exits non-zero if there are any problems, or
with `--complete` if anything is pending. Nothing writes a copy of any wireframe.

## 7 Parked

* Several renderings for one step (frames of a wizard): to be added if DEM's walkthroughs need it. If so, as a straight
  sequence of frames within a step, each a delta on the step's screen, never branching (branches are steps).
* Bindings beyond text, visibility and enablement: attributes, images, formatted text, views generated from lists.
* Checking a stereotyped string, such as that a `card-ref` names a card in the step.
* Interaction: images only, no clickable prototype.
