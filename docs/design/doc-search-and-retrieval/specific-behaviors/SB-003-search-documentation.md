---
reconciliation:
  checked_at: "2026-08-21T16:23:50.981Z"
  uc_technical_interpretation_checksums: {"UC-005": "a0d5c8a5635b52ea44c19eb60deae83a486f6326f72fa67b307b8de776c67bd3"}
  function_checksums: {"IC-002 §2": "0ca06de09bb98cc800304091c69fa374dbe5ee6df14e28a85f14abc63c982d3c", "IC-002 §1": "f09dff9f4896fa1c18f1743c87455d6192cf3c6ac976bcef8c362d4ee7ef0d68", "IC-007 §1": "d4f8779a71003ea0238a9f1a0cc6f122af5d42cda1e592aade19584101662c4a", "IC-005 §5": "92ed670b0aebff5c22712deb5f15252ae355dbfa0da16486e3144226e27dc72f", "IC-007 §2": "2b1260d0849b47e78156792cdf91302248d75ee4f4eade367beba87a3aafa512", "IC-007 §3": "fc81d4a98885ae842775f82c7273037457a64a1306bef494ca9832f831280588", "IC-007 §4": "f2d33a1b597fa960f2e32972fcebfc038e697426102d15cd4de516077c4094a4"}
  behaviors:
    "1":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-007 §1"  # reduce_query("install") -> ["install"]
            children:
              - address: "IC-006 §1"  # reduce_words("install") -> ["install"]
          - address: "IC-005 §5"  # load_word_index(scope, ["install"]) -> 3 matching nodes (1 root + 2 sections)
          - address: "IC-007 §2"  # score_nodes(matching_index, ["install"]) -> 3 scores
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "1.1":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"
          - address: "IC-007 §1"
            children:
              - address: "IC-006 §1"
          - address: "IC-005 §5"
          - address: "IC-007 §2"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "1.2":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"
          - address: "IC-007 §1"
            children:
              - address: "IC-006 §1"
          - address: "IC-005 §5"
          - address: "IC-007 §2"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "2":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"
          - address: "IC-007 §1"
            children:
              - address: "IC-006 §1"
          - address: "IC-005 §5"
          - address: "IC-007 §2"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T16:22:35.000Z"
    "2.1":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("@nonexistent-project") -> registry found, slug absent, raises unknown_scope_slug
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "3":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"
          - address: "IC-007 §1"
            children:
              - address: "IC-006 §1"
          - address: "IC-005 §5"
          - address: "IC-007 §2"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "4":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("docs/example/") -> Scope{roots: ["docs/example/"]}
          - address: "IC-007 §1"  # reduce_query("install") -> ["install"]
            children:
              - address: "IC-006 §1"  # reduce_words("install") -> ["install"]
          - address: "IC-005 §5"  # load_word_index(scope, ["install"]) -> 3 matching nodes
          - address: "IC-007 §2"  # score_nodes(matching_index, ["install"]) -> 3 scores
          - address: "IC-007 §3"  # select_top_n(scores) -> all 3, none dropped (well under the default 20)
          - address: "IC-007 §4"  # preview_content(top_results) -> 3 previews
            children:
              - address: "IC-005 §6"  # read_section_index(guide.md) -> two id-keyed entries (titles "Getting Started", "Appendix"), one call covering both guide.md matches
              - address: "IC-001 §2"  # is_reserved_section("Getting Started") -> false
              - address: "IC-001 §2"  # is_reserved_section("Appendix") -> true, so guide.md's whole-doc preview stops at its start_line
              - address: "IC-005 §6"  # read_section_index(other.md) -> one id-keyed entry (title "Setup") -> its own bounds, no is_reserved_section needed for a section-level match
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T16:25:12.000Z"
    "4.1":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"
          - address: "IC-007 §1"
            children:
              - address: "IC-006 §1"
          - address: "IC-005 §5"
          - address: "IC-007 §2"
          - address: "IC-007 §3"
          - address: "IC-007 §4"
            children:
              - address: "IC-005 §6"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
              - address: "IC-005 §6"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "4.2":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"
          - address: "IC-007 §1"
            children:
              - address: "IC-006 §1"
          - address: "IC-005 §5"
          - address: "IC-007 §2"
          - address: "IC-007 §3"
          - address: "IC-007 §4"
            children:
              - address: "IC-005 §6"
              - address: "IC-001 §2"
              - address: "IC-001 §2"
              - address: "IC-005 §6"
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "5":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §2"  # resolve_chained_scope(["@agent-plugins", "@docs"]) -> combined Scope, 2 roots
            children:
              - address: "IC-002 §1"  # resolve_scope_single("@agent-plugins")
              - address: "IC-002 §1"  # resolve_scope_single("@docs")
          - address: "IC-007 §1"  # reduce_query("install") -> ["install"]
            children:
              - address: "IC-006 §1"  # reduce_words("install") -> ["install"]
          - address: "IC-005 §5"  # load_word_index(scope, ["install"]) -> 4 matching nodes across both roots
          - address: "IC-007 §2"  # score_nodes(matching_index, ["install"]) -> 4 scores
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
    "6":
      call_tree:
        address: "IC-000 §3"
        children:
          - address: "IC-002 §1"  # resolve_scope_single("@agent-plugins") -> no .weaver-docs.yaml found, raises weaver_docs_yaml_not_found
      reviewed:
        reviewed_by: "architect"
        reviewed_at: "2026-08-21T14:25:17.000Z"
---
# SB-003 — Search Documentation

## Context
* [UC-005 — Search Documentation](../../../analysis/use-cases/UC-005-search-documentation.md) - the use case this file's behaviors realize
* [IC-000 — Docs Tooling CLI](../../../architecture/components/IC-000-docs-tooling-cli.md) - §3, the bound entry point below
* Specific Behaviors (@docs/workflows/feature-workflow/specific-behaviors.md) - the convention this document follows

**Realizes:** UC-005 steps 1-5

**Bound Pseudocode (UC-005):**

```
FUNCTION IC-000 §3:
  IF scope IS chained:
    resolved_scope <-- [IC-002 §2: resolve_chained_scope - scope]
  ELSE:
    resolved_scope <-- [IC-002 §1: resolve_scope_single - scope]
  reduced_query <-- [IC-007 §1: reduce_query - query]
  matching_index <-- [IC-005 §5: load_word_index - resolved_scope, reduced_query]
  scores <-- [IC-007 §2: score_nodes - matching_index, reduced_query]
  IF mode IS details:
    top_results <-- [IC-007 §3: select_top_n - scores]
    previews <-- [IC-007 §4: preview_content - top_results]
    RETURN top_results, previews
  ELSE:
    RETURN scores
```

(§7.1 Mechanical Reconciliation — computed by hand, same basis as `SB-001`'s own note. Subset relationship:
already established deriving §1-§6 above. Side effects: N/A, no External Dependencies. Exceptions: swept —
`weaver_docs_yaml_not_found`/`unknown_scope_slug` are now declared on both `IC-002 §1` (origin) and `IC-000 §3`
(its own caller, added this pass) — see `IC-000`'s own doc.)

## 1 Happy Path

**Realizes:** happy path

**Given** a scope `docs/example/`, already indexed (UC-003), containing two documents:
* `docs/example/guide.md` — `.words.yaml`: `document: {install: 1, guide: 1}`, `sections: {"Getting Started":
  {install: 1, tool: 1, run: 1}}`
* `docs/example/other.md` — `.words.yaml`: `document: {other: 1}`, `sections: {"Setup": {install: 2,
  configure: 1}}`

**When** `search_documentation(query: "install", scope: "docs/example/", mode: "list")` is invoked (`IC-000 §3`)

**Then** since `scope` isn't chained, `resolve_scope_single` (`IC-002 §1`) resolves it to `{roots:
["docs/example/"], specifier: "docs/example/"}`; `reduce_query` (`IC-007 §1`) reduces `"install"` to `["install"]`
(already a bare significant word, no stemming needed); `load_word_index` (`IC-005 §5`) returns every matching
node — including `guide.md`'s own root, per the §3.9 addendum resolved above:
```yaml
- {document: "docs/example/guide.md", section: null, matched_words: ["install"], total_word_count: 2}
- {document: "docs/example/guide.md", section: "Getting Started", matched_words: ["install"], total_word_count: 3}
- {document: "docs/example/other.md", section: "Setup", matched_words: ["install"], total_word_count: 3}
```
`score_nodes` (`IC-007 §2`), under the default algorithm (match count normalized by the node's own total word
count, MSS step 3), returns:
```yaml
- {document: "docs/example/guide.md", section: null, score: 0.5}
- {document: "docs/example/guide.md", section: "Getting Started", score: 0.333}
- {document: "docs/example/other.md", section: "Setup", score: 0.667}
```
(`guide.md`'s root scores `1/2 = 0.5`; its `"Getting Started"` section scores `1/3 ≈ 0.333`; `other.md`'s
`"Setup"` section scores `2/3 ≈ 0.667`, since `install` occurs twice there — a document-level score genuinely
appears here, `guide.md`'s own root match, alongside its section's, exactly what MSS step 4 asks for and what
was structurally impossible before this behavior's own §3.9 correction); `mode` is `"list"`, so the operation
returns `scores` directly, with no `select_top_n`/`preview_content` call.

### 1.1 No Matches

**Realizes:** happy path — Extension 3a

**Given** — as §1, the same scope and indexed documents

**When** — as §1, but `search_documentation(query: "nonexistent", scope: "docs/example/", mode: "list")` is
invoked (`IC-000 §3`)

**Then** — as §1 up through `reduce_query`, which reduces `"nonexistent"` to `["nonexistent"]`; but
`load_word_index` finds no node anywhere in scope containing it, returning `[]`; `score_nodes` is still called,
with an empty `matching_index`, and returns `[]` — no separate branch needed, an empty result flows through the
same path as any other query; the operation returns `scores: []`, not an error

### 1.2 Partial Multi-Word Match

**Realizes:** happy path

**Given** — as §1, the same scope and indexed documents

**When** — as §1, but `search_documentation(query: "install missing", scope: "docs/example/", mode: "list")` is
invoked (`IC-000 §3`) — a two-word query where only `"install"` appears anywhere in scope, `"missing"` doesn't

**Then** `reduce_query` reduces `"install missing"` to `["install", "missing"]`; `load_word_index` returns the
same three nodes as §1 — each one's `matched_words` is `["install"]` only, since none of them contain
`"missing"`:
```yaml
- {document: "docs/example/guide.md", section: null, matched_words: ["install"], total_word_count: 2}
- {document: "docs/example/guide.md", section: "Getting Started", matched_words: ["install"], total_word_count: 3}
- {document: "docs/example/other.md", section: "Setup", matched_words: ["install"], total_word_count: 3}
```
`score_nodes` combines per-term scores summed (MSS step 3) — `"missing"` contributes `0` to every node, since
it matches nowhere — so the result is numerically identical to §1's:
```yaml
- {document: "docs/example/guide.md", section: null, score: 0.5}
- {document: "docs/example/guide.md", section: "Getting Started", score: 0.333}
- {document: "docs/example/other.md", section: "Setup", score: 0.667}
```
demonstrating MSS step 3's own requirement directly: an unmatched term doesn't zero out or exclude a result that
another term in the same query did match, it's simply additively neutral.

## 2 Scope By Slug

**Realizes:** happy path

**Given** cwd `/workspace/AgentPlugins/agent-plugins-docs/notes/`; a registry two levels up, at
`/workspace/.weaver-docs.yaml`:
```yaml
agent-plugins: AgentPlugins/agent-plugins-docs/docs
docs: docs
```
— and, under the resolved root `/workspace/AgentPlugins/agent-plugins-docs/docs/example/`, the same two indexed
documents as §1 (`guide.md`, `other.md`, identical `.words.yaml` content)

**When** `search_documentation(query: "install", scope: "@agent-plugins", mode: "list")` is invoked (`IC-000 §3`)

**Then** `resolve_scope_single` (`IC-002 §1`) walks up from cwd — `.../agent-plugins-docs/`, then `.../AgentPlugins/`,
neither holding a `.weaver-docs.yaml` — until it finds one at `/workspace/`; reads its mapping; resolves
`"agent-plugins"` to `"AgentPlugins/agent-plugins-docs/docs"`, relative to `/workspace/` (the registry file's own
directory, since the entry isn't absolute), giving `Scope{roots: ["/workspace/AgentPlugins/agent-plugins-docs/docs"],
specifier: "@agent-plugins"}`; everything from here on is identical to §1 — `reduce_query`, `load_word_index`,
`score_nodes` — producing the same three scores (`0.5`, `0.333`, `0.667`) against content now found under the
resolved root instead of a literal `docs/example/`

### 2.1 Slug Not In Registry

**Realizes:** unhappy path — slug absent from registry

**Given** — as §2, the same cwd and `.weaver-docs.yaml` (entries `agent-plugins`, `docs`)

**When** — as §2, but `search_documentation(query: "install", scope: "@nonexistent-project", mode: "list")` is
invoked (`IC-000 §3`)

**Then** `resolve_scope_single` walks up and finds `/workspace/.weaver-docs.yaml`, exactly as in §2 — the
registry lookup itself succeeds — but `"nonexistent-project"` isn't one of its entries; it raises
`unknown_scope_slug`, uncaught, straight out of `search_documentation`. `reduce_query`/`load_word_index`/
`score_nodes` never run.

## 3 Scope By All

**Realizes:** happy path

**Given** — as §2's cwd and `.weaver-docs.yaml` (two entries: `agent-plugins`, `docs`); the same `guide.md`/
`other.md` under the `agent-plugins` root as §1/§2, plus a third document, `/workspace/docs/standards/
install-guide.md`, under the `docs` root, `.words.yaml`: `document: {install: 1}, sections: {}`

**When** `search_documentation(query: "install", scope: "@all", mode: "list")` is invoked (`IC-000 §3`)

**Then** `resolve_scope_single` (`IC-002 §1`) recognizes `@all` *before* attempting any registry lookup — it
never looks up a slug literally named `"all"` — reads `/workspace/.weaver-docs.yaml`, and combines *every*
entry it contains: `Scope{roots: ["/workspace/AgentPlugins/agent-plugins-docs/docs", "/workspace/docs"],
specifier: "@all"}`; `reduce_query` reduces `"install"` to `["install"]`; `load_word_index` searches both roots
and returns matches from each:
```yaml
- {document: ".../agent-plugins-docs/docs/example/guide.md", section: null, matched_words: ["install"], total_word_count: 2}
- {document: ".../agent-plugins-docs/docs/example/guide.md", section: "Getting Started", matched_words: ["install"], total_word_count: 3}
- {document: ".../agent-plugins-docs/docs/example/other.md", section: "Setup", matched_words: ["install"], total_word_count: 3}
- {document: "/workspace/docs/standards/install-guide.md", section: null, matched_words: ["install"], total_word_count: 1}
```
`score_nodes` scores all four together — the first three as in §1 (`0.5`, `0.333`, `0.667`), and
`install-guide.md`'s own root at `1/1 = 1.0`, since `install` is its only word — the operation returns all four
scores, combined from both registry entries into one result set

## 4 Details Mode

**Realizes:** happy path

**Given** — as §1, the same scope and indexed word content, now with each document's own literal source given
too (needed for previews, not exercised by §1 itself) — `guide.md` also carries an Appendix, which contributes
nothing to `.words.yaml` (§3.1 addendum) so it doesn't disturb §1's own scoring:
```
docs/example/guide.md:
  # Install Guide

  ## Context
  * [Other Doc](other.md) - related

  ## 1 Getting Started
  Install the tool and run it.

  # Appendix
  Extra configuration details not covered above.

docs/example/other.md:
  # Other

  ## Context
  * [Other Doc](other.md) - related

  ## 1 Setup
  Install, install, and configure.
```

**When** — as §1, but `search_documentation(query: "install", scope: "docs/example/", mode: "details")` is
invoked (`IC-000 §3`), with `--max-results`/`--preview-lines` both left at their defaults (`20`/`5`, HLD §3.8)

**Then** — as §1 through `score_nodes`, producing the same three scores; `select_top_n` (`IC-007 §3`) sorts them
descending and keeps all three (well within the default cap of `20`, so nothing is dropped); `preview_content`
(`IC-007 §4`) reads each match's own lines: for the `section: null` (document-level) match, that's the first `5`
lines of `guide.md`'s *whole document* — every section in order, excluding its Appendix (HLD §3.9 addendum) —
which at only `5` lines doesn't reach as far as `## 1 Getting Started` yet, let alone the Appendix (§4.1 below
uses a larger `--preview-lines` to actually reach and prove that boundary); for each section-level match, the
first `5` lines of that section specifically, capped by its own content — both sections here are shorter than
`5` lines, so the whole section shows:
```yaml
top_results:
  - {document: "docs/example/other.md", section: "Setup", score: 0.667}
  - {document: "docs/example/guide.md", section: null, score: 0.5}
  - {document: "docs/example/guide.md", section: "Getting Started", score: 0.333}
previews:
  - {document: "docs/example/other.md", section: "Setup", preview_lines: ["## 1 Setup", "Install, install, and configure."]}
  - {document: "docs/example/guide.md", section: null, preview_lines: ["# Install Guide", "", "## Context", "* [Other Doc](other.md) - related", ""]}
  - {document: "docs/example/guide.md", section: "Getting Started", preview_lines: ["## 1 Getting Started", "Install the tool and run it."]}
```
the operation returns `top_results, previews`

### 4.1 Non-Default Result Limits

**Realizes:** happy path

**Given** — as §4, the same scope, documents, and source content (including `guide.md`'s Appendix)

**When** — as §4, but `--max-results: 10` and `--preview-lines: 10` are both given explicitly, in place of the
defaults `20`/`5`

**Then** `select_top_n` keeps all three results (still well under `10`, so no visible difference from §4 there);
`preview_content`, now asked for `10` lines each, proves the flag is genuinely threaded through — and, for
`guide.md`'s document-level match, proves the Appendix-exclusion boundary (HLD §3.9 addendum) takes priority
over the requested line count: `guide.md`'s whole document (excluding its Appendix) is only `8` lines long, so
even though `10` were requested, the preview stops at `8`, never reaching the Appendix's own two lines:
```yaml
top_results:
  - {document: "docs/example/other.md", section: "Setup", score: 0.667}
  - {document: "docs/example/guide.md", section: null, score: 0.5}
  - {document: "docs/example/guide.md", section: "Getting Started", score: 0.333}
previews:
  - {document: "docs/example/other.md", section: "Setup", preview_lines: ["## 1 Setup", "Install, install, and configure."]}
  - {document: "docs/example/guide.md", section: null, preview_lines: ["# Install Guide", "", "## Context", "* [Other Doc](other.md) - related", "", "## 1 Getting Started", "Install the tool and run it.", ""]}
  - {document: "docs/example/guide.md", section: "Getting Started", preview_lines: ["## 1 Getting Started", "Install the tool and run it."]}
```
(the two section-level previews are unchanged from §4 — both sections are shorter than even the default `5`,
so raising the cap to `10` doesn't reach any further content for either of them)

### 4.2 Truncation At The Overridden Limit

**Realizes:** happy path

**Given** — as §4.1, the same scope/documents/source

**When** — as §4.1, but `--max-results: 2` in place of `10` (`--preview-lines` stays `10`) — fewer than the `3`
nodes that actually match

**Then** `score_nodes` still produces all `3` scores, unchanged; `select_top_n` sorts them descending and keeps
only the top `2` — `other.md`'s `"Setup"` (`0.667`) and `guide.md`'s root (`0.5`) — dropping `guide.md`'s
`"Getting Started"` section (`0.333`, the lowest); `preview_content` only ever sees those `2`, so it's never
even asked to preview the dropped one:
```yaml
top_results:
  - {document: "docs/example/other.md", section: "Setup", score: 0.667}
  - {document: "docs/example/guide.md", section: null, score: 0.5}
previews:
  - {document: "docs/example/other.md", section: "Setup", preview_lines: ["## 1 Setup", "Install, install, and configure."]}
  - {document: "docs/example/guide.md", section: null, preview_lines: ["# Install Guide", "", "## Context", "* [Other Doc](other.md) - related", "", "## 1 Getting Started", "Install the tool and run it.", ""]}
```
truncation happens against the `2` actually passed in, not a hardcoded `20`

## 5 Chained Scope

**Realizes:** happy path

**Given** — as §3, the same cwd, `.weaver-docs.yaml` (entries `agent-plugins`, `docs`), and indexed content
under both roots

**When** `search_documentation(query: "install", scope: "@agent-plugins@docs", mode: "list")` is invoked
(`IC-000 §3`)

**Then** since `scope` is chained, `IC-000 §3` calls `resolve_chained_scope` (`IC-002 §2`) instead of
`resolve_scope_single` directly — it calls `resolve_scope_single` (`IC-002 §1`) once for `"@agent-plugins"` and
once for `"@docs"`, each going through the same registry walk as §2, then combines both into one `Scope`:
`{roots: ["/workspace/AgentPlugins/agent-plugins-docs/docs", "/workspace/docs"], specifier: "@agent-plugins@docs"}`
— the same combined roots §3's `@all` reached, arrived at explicitly rather than via the reserved keyword;
everything from here on is identical to §3 — `reduce_query`, `load_word_index`, `score_nodes` — producing the
same four scores across both roots:
```yaml
- {document: ".../agent-plugins-docs/docs/example/guide.md", section: null, score: 0.5}
- {document: ".../agent-plugins-docs/docs/example/guide.md", section: "Getting Started", score: 0.333}
- {document: ".../agent-plugins-docs/docs/example/other.md", section: "Setup", score: 0.667}
- {document: "/workspace/docs/standards/install-guide.md", section: null, score: 1.0}
```

## 6 No Registry Found

**Realizes:** unhappy path — `.weaver-docs.yaml` not found

**Given** cwd `/tmp/scratch/some/deep/path/`, with no `.weaver-docs.yaml` anywhere from there up to filesystem
root

**When** `search_documentation(query: "install", scope: "@agent-plugins", mode: "list")` is invoked (`IC-000 §3`)

**Then** `resolve_scope_single` walks up through every parent directory to filesystem root without ever finding
a `.weaver-docs.yaml`; it raises `weaver_docs_yaml_not_found`, uncaught, straight out of `search_documentation` —
the same `RAISE`-and-propagate pattern `duplicate_identity` (SB-001 §4) already uses. `reduce_query`/
`load_word_index`/`score_nodes` never run.
