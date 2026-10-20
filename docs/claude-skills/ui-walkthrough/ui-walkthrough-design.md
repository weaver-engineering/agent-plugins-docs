# UI Walkthrough

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo, §5 Claude Skills
* [WVR-252](https://linear.app/weaver-engineering/issue/WVR-252) - the ticket this design fulfils
* dem-ambient's design-ui (WVR-253, WVR-254, WVR-255, in DEM's `dem-docs`) - the first consumer; it quotes the contract in §3

## 1 Purpose

Assembles a UI layout from wireframe **views** and renders one image per **step** of a use case. A project's UI
design is then shown as walkthroughs: one markdown page per step, readable in any markdown renderer.

Two firm requirements shape everything below:

* **A view's wireframe is written once and never copied.** The assembled HTML exists only in memory while a step
  renders; only the image is written. Generated HTML could be edited on its own and bloats reviews.
* **It is generic.** No project's names, paths or views appear in the skill. DEM is only the first user.

## 2 Trigger

Used whenever a project's UI design changes a view, a step's layout, or the link graph between steps: render the
affected steps, then run `check`. `check` is also what a gate runs.

## 3 The Contract

Agreed with the architect on 19 October 2026. Unchanged by the decisions in §4 except where §4 says so.

### 3.1 Configuration

One file at the consuming repo's root, `ui-walkthrough.yaml`:

```yaml
views: docs/design/ui/views
tokens: docs/design/ui/tokens.css
steps: docs/analysis/use-cases/*/walkthrough/*/step.yaml
viewports: { desk: 1440x900, tablet: 1024x768, tablet-portrait: 768x1024 }
```

A viewport is `WIDTHxHEIGHT`, width first.

### 3.2 A view

A view lives at `{views}/{VIEW-NAME}/`, the name in UPPER-KEBAB case.

* `wireframe.html` is an HTML fragment with root `<section data-view="VIEW-NAME">`.
  * Its styling comes from the tokens stylesheet, plus an optional `<style>` of its own.
  * A **slot** is `<div data-slot="SLOT-NAME"></div>`. The view that fills it goes inside the div, and the div
    keeps the size its parent gives it.
  * A **state** is `data-state="…"` on the root element, which the view's CSS selects on.
  * Wireframes carry their own placeholder content. Steps supply none.
* `VIEW.md` frontmatter declares `slots: [...]` and `states: [...]`, the first state being the default. Its body is
  the consuming project's own; the skill reads only the frontmatter.

### 3.3 A step

A step is a directory under a use case's `walkthrough/`, named after the use case's numbering: main step 3 is
`03-…`, extension 3a is `03a-…`.

* `STEP.md` is hand-written and never written by the skill. It holds the step's description, `![…](step.png)`, and
  one or more links to the steps it leads to, each labelled with the choice it stands for. A step that ends the use
  case is marked `**End:**`.
* `step.yaml`:

  ```yaml
  root: APP
  viewport: desk
  slots:                       # VIEW.SLOT → view, so slot names never collide
    APP.BROWSER: FILE-BROWSER
    FILE-BROWSER.FILES: FILE-LIST
    APP.DOCUMENT: DOC-DIFF
    APP.SIDE: null             # deliberately empty
  states:
    FILE-BROWSER: collapsed-to-changed
  highlight: [APP.DOCUMENT]    # optional: outline what the step is about
  ```

* `step.png` is written beside `step.yaml`. Its PNG text metadata carries a SHA-256 over its inputs (§5.3).

### 3.4 Modes

* `render <step>…` renders the steps named.
* `render --view NAME` re-renders every step that uses the view.
* `uses NAME` lists the steps that use a view, without rendering.
* `check` exits non-zero and lists every problem. A problem is any of:
  * a step whose image is stale, missing or invalid;
  * an assembly error (§5.1);
  * a `STEP.md` link to a step that doesn't exist;
  * a step that can't be reached from step `01`;
  * a step with no link onward that isn't marked `**End:**`.

## 4 Decisions

### 4.1 Rendering: HTML to PNG with Playwright, and an install step

HTML/CSS gives flow, flex and grid for free, and "the slot div keeps the size its parent gives it" is plain CSS.
SVG would need every nested size and position computed by hand, is token-dense, and is less rich; the restraint it
imposes on wireframes is already provided by the tokens file and the view conventions.

The mechanical logic (§5) is pure Node with no dependencies. Only the renderer needs a browser, and it sits behind
one narrow interface: assembled HTML plus a viewport in, PNG bytes out. So `check` and `uses` need no browser and
run in CI without one; `check` compares hashes and never re-renders.

The browser is **Playwright** with its own pinned Chromium, not `puppeteer-core` against an installed Chrome: these
PNGs are committed and reviewed, and a re-render on another machine must not produce a visibly different image.
(The hash is over inputs, so determinism is not needed for staleness, only for review.)

This **ends the "no install step" convention for this skill.** The skill carries its own `package.json`, and a
documented install step is plain Node, identical under Claude, Codex or OpenCode:

```
cd ~/.claude/skills/ui-walkthrough && npm ci && npx playwright install chromium
```

Everything else still deploys by copy. `claude-skills/README.md` is updated to say a skill may declare
dependencies and must name its install command.

### 4.2 Highlight

The renderer draws a 3px outline around each highlighted slot's bounding box, as an overlay measured in the browser
after layout, so it takes no space and moves nothing. The colour is the `--walkthrough-highlight` custom property
from the tokens file, with a fixed default; views never draw their own highlight.

* `highlight` is part of `step.yaml` and so part of the input hash.
* An entry that does not name a bound `VIEW.SLOT` is an assembly error.
* Highlighting a `null` slot is allowed: "this area is deliberately empty" can be the point of a step.

### 4.3 Reporting a view's missing or bad frontmatter

An assembly error naming the view and the specific problem; the skill never guesses from the wireframe. The
problems are: a missing `VIEW.md` or `wireframe.html`, no frontmatter, a missing `slots` or `states` key, an empty
`states`, a `data-slot` in the wireframe that is not declared (or the reverse), and a root `data-view` that doesn't
match the directory name. Declared slots must match the wireframe's `data-slot` attributes exactly, so a stale
declaration cannot satisfy "every slot is bound". `check` reports this once per view, not once per step using it.

### 4.4 Other points

* **Invalid image** means not a PNG, or no hash in its metadata. It never means the pixels look wrong.
* **Viewport:** the screenshot is exactly the viewport size, not the full page.
* **Fonts:** the tokens stylesheet must not depend on a system font, or renders drift between machines.

## 5 Algorithm

### 5.1 Assembly

From the step's `root`, recursively fill each slot of each placed view with the wireframe of the view bound to
`VIEW.SLOT`, inside its `<div data-slot>`. A view's `data-state` is its entry in `states:`, else its first
declared state. Rejected, with an error naming the step and the offender:

* an unknown view, slot, state or viewport;
* a slot of a placed view left unbound (`null` is the deliberate empty binding);
* a view placed twice;
* a cycle;
* a `highlight` entry that is not a bound `VIEW.SLOT` (§4.2);
* any frontmatter problem in §4.3.

The assembled document is the tokens stylesheet plus the nested fragments. It is held in memory and never written.

### 5.2 Uses

A step uses a view if the view is its `root` or a value in its `slots`. `uses NAME` and `render --view NAME` both
use this; neither needs a browser to find the steps.

### 5.3 Input hash and staleness

SHA-256 over, in a fixed order and each length-prefixed: the `step.yaml`, the wireframe of each view the step
places (sorted by name), the tokens stylesheet, the viewport as `WIDTHxHEIGHT`, and the skill's major version.
Only wireframes of placed views count, so editing an unused view never stales a step. The hash is written to a PNG
text chunk when rendering. A step is stale when the hash in its `step.png` differs from the one recomputed now;
missing when there is no `step.png`; invalid per §4.4.

### 5.4 Link graph

Parse each `STEP.md` for links to sibling step directories. Reported by `check`: a link to a step that doesn't
exist; a step unreachable from step `01` of its use case; a step with no onward link that lacks `**End:**`.

## 6 Output

`render` writes only `step.png` files. `uses` prints step paths, one per line. `check` prints one problem per line
and exits non-zero if there are any. Nothing writes a `STEP.md` or a copy of any wireframe.

## 7 Parked

* Per-step sample content in a view (data binding).
* Interaction: images only, no clickable prototype.
