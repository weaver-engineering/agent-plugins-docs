# Doc Search & Retrieval — High-Level Design

## Context
* [WVR-95](https://linear.app/weaver-engineering/issue/WVR-95) - the Feature this design realizes
* [UC-002 — Auto-Number Document Sections](../../analysis/use-cases/UC-002-auto-number-document-sections.md) - realized by this design
* [UC-003 — Index A Path](../../analysis/use-cases/UC-003-index-a-path.md) - realized by this design
* [UC-005 — Search Documentation](../../analysis/use-cases/UC-005-search-documentation.md) - realized by this design
* [UC-006 — Extract Document Content](../../analysis/use-cases/UC-006-extract-document-content.md) - realized by this design
* [Architecture Definition Document](../../architecture/architecture-definition-document.md) - §1 names this an MCP server (default for tools, not the bare-delivery exception), §4 names this Feature as the worked exemplar for the analysis/design/catalog document boundary
* Design Directory And HLD (@docs/workflows/feature-workflow/design-directory-and-hld.md) - the convention this document follows

## 1 Scope

This design covers the Doc Search & Retrieval MCP server: the four documentation tools already analysed as
standalone use cases —
[UC-002](../../analysis/use-cases/UC-002-auto-number-document-sections.md) (auto-numbering),
[UC-003](../../analysis/use-cases/UC-003-index-a-path.md) (indexing),
[UC-005](../../analysis/use-cases/UC-005-search-documentation.md) (search), and
[UC-006](../../analysis/use-cases/UC-006-extract-document-content.md) (extraction) — bundled and hosted
together as one MCP server rather than shipped as four bare tools, per the Architecture Definition Document's
§1 default-to-MCP model.

It explicitly excludes: why these four capabilities exist and what each does (already-written analysis, linked
above, immutable once its Technical Interpretation is derived below — not re-opened by this design); the
capability catalog entry itself (`docs/architecture/capability-catalog.md`, already present, not duplicated
here); and the mechanics of achieving parity between Claude Code and OpenCode for any given capability
(`docs/design/cross-platform-capability-parity.md`, WVR-94, a separate placeholder document this design does
not resolve).

## 2 Solution Overview

* `IC-000` — the CLI entry point — four commands, one per use case. Talks to every other component below;
  nothing else does.
* `MarkdownParser` — parses a document's headings/figures into pseudo-numbers, references, and start/end lines
  in one call. Talks to: nothing (pure function over document text).
* `ScopeResolver` — resolves an `@{scope}` specifier, single or chained. Talks to: nothing (pure function over
  a specifier string).
* `AutoNumberer` — computes fresh numbering, maps old→new ids, rewrites headings/references, formats the
  change report. Talks to: `MarkdownParser`'s output (consumes it, doesn't call it directly — `IC-000` sequences
  the two).
* `PathIndexer` — walks a path into independent per-directory units, extracts words/TODOs from each unit's
  documents. Talks to: `MarkdownParser`'s output (same relationship as `AutoNumberer`), and calls `WordReducer`
  directly for the word-extraction step.
* `WordReducer` — the documentation standard's own §4 tokenization/stemming/stopword rules, applied to any
  text. Talks to: nothing (pure function over a text string) — called *by* `PathIndexer` and `Searcher`, calls
  nothing itself.
* `IndexStore` — reads and writes the persisted `.index/` file format: writes `PathIndexer`'s extracted content,
  lists/finds-stale/removes entries, and reads matching sections back out for `Searcher`. Talks to: the
  filesystem directly (§6 — in-process I/O, not an External Dependency).
  * Data at rest (§4): each of `.sections.yaml`/`.words.yaml`/`.todo.yaml` follows the shape already fixed by
    the documentation standard (§4) — this design doesn't redefine that shape, only produces and consumes it.
* `Searcher` — reduces a query via `WordReducer`, scores `IndexStore`'s matching sections, selects the top N,
  previews content. Talks to: `WordReducer` directly, `IndexStore` (`load_word_index`).
* `ContentExtractor` — resolves a document and target range, reads verbatim source text. Talks to: the
  filesystem directly (§6), and `IndexStore`'s persisted `sections.yaml` (to resolve a `§section` reference to a
  line range) — the one place a component outside `IndexStore` reads its data directly rather than through
  `IC-000` sequencing two calls.

Not a restatement of the specific behaviors (Design Directory And HLD's own Rationale on why not) — this is the
map a reader orients from before going anywhere else in this document; §5 carries each component's own function
list and per-function notes, §7 carries the behaviors themselves once derived.

## 3 Key Decisions

### 3.1 `parse_markdown_structure` Interface

UC-002's and UC-003's parsing needs are met by a single shared component, `parse_markdown_structure(document)`,
returning every field either caller could want in one call — headings, figures, pseudo-numbers, references, and
start/end lines. UC-002 (`auto_number_document`) reads `pseudo_numbers` and `references`; UC-003
(`index_path`)'s `parse_structure` step reads `start_end_lines`. Neither caller narrows the interface to only
its own fields.

### 3.2 Delivery Surface: CLI Now, MCP Later

This Feature ships as a command-line tool now, not an MCP tool — the ADD's own MCP-hosting default (§1) is
about how this capability is eventually *published*, not something this design phase builds today. Every
operation's core logic (each `IC-000` function below) is written as a plain, directly-testable function; the
CLI is a thin argument-parsing wrapper around it, the same relationship an MCP tool wrapper would have if one
gets built later. Nothing about this design commits to CLI-specific concerns (argv parsing, exit codes) leaking
into the core functions themselves. This resolves the "MCP vs CLI" half of UC-002/003/005/006's own §7 Open
Design Questions; each use case's *specific* flag/format questions are still open, and get their own subsection
here as each is decided.

### 3.3 `resolve_scope` Interface

Split into two functions rather than one. `resolve_scope_single(specifier)` resolves exactly one scope
(`@{slug}`, `@docs`, `@all`, or a filesystem path) and is what both UC-005 and UC-006 call. `resolve_chained_scope(specifiers)`
— UC-005 only — calls `resolve_scope_single` once per specifier and combines the results; UC-006 has no path to
it at all, so its own scope exclusion (no `@{slug}@{slug}` chaining) is enforced by which function exists for
it to call, not left to caller discipline.

### 3.4 Filesystem Is Not An External Dependency

Confirmed as reasoned in §6: every file-touching function (`read_source_text`, `write_index_files`,
`parse_markdown_structure`, `list_index_entries`, `remove_index_entries`) is an ordinary Internal Component
doing in-process I/O against files this project itself manages — not a formal External Dependency. No `ED-NNN`
document exists or is needed for the filesystem.

### 3.5 UC-002 Report Format And Exit Codes

Bare invocation prints a human-readable report; `--json` switches to structured output. This is how
`auto_number_document`'s `invoked_by` parameter (Technical Interpretation) actually gets set in practice: the
Assistant's own tooling always passes `--json` when it shells out, a human typing the command directly doesn't
— resolving Extension 8a without the binary needing to know who's calling it. Exit code `0` means the run
completed, whether or not changes were made; non-zero only on a real error (`duplicate_identity`, Extension 3b).

### 3.6 UC-003 Recurse/Depth Flags

`--recursive` opts into walking the full tree (default: the given directory's immediate `.md` files only, per
the use case's own default). `--recursive --depth N` caps how many levels deep. `--depth` without `--recursive`
is a usage error — depth only means something once recursion is on.

### 3.7 UC-006 Out-Of-Bounds Line Range

Clamped, not an error: a requested range is silently capped to whatever actually exists (`[40-200]` on a
50-line document returns lines 40-50). Consistent with the use case's own existing pattern of degrading
gracefully on a partial match (Extension 2a's empty wildcard result) rather than failing — distinct from
Extension 3a's `§section`-not-found case, which *does* fail, because a missing section is a wrong reference
entirely, not a partially-satisfiable range.

### 3.8 UC-005 Algorithm Selection And Details-Mode Defaults

Three independent flags, not one bundled together: `--calc <name>` selects the scoring algorithm (default
unspecified — whichever `score_nodes` treats as its own baseline). `--max-results <N>` caps the ranked list
(default `20`). `--preview-lines <X>` caps each result's preview length in details mode (default `5`). None of
the three implies or constrains another — selecting an algorithm doesn't change how many results or preview
lines come back, and vice versa.

This resolves the last Open Design Question in scope — every use case's `## 7 Open Design Questions` (§2.1's
own requirement) is now either resolved (§3.1-§3.8) or, where genuinely out of this Feature's scope (UC-005's
cross-repo score comparability, Extension 3b), explicitly left alone rather than silently ignored.

### 3.9 `IC-000`, `AutoNumberer`, `PathIndexer`, `IndexStore`, `Searcher`, `ContentExtractor` Interfaces

Unlike `MarkdownParser` (§3.1) and `ScopeResolver` (§3.3), none of these six components had a genuinely
competing shape to weigh — each one's functions, and the grouping itself, follow directly from its owning use
case's own Technical Interpretation (already immutable, already reviewed) plus the review-driven corrections
already recorded (UC-003's per-unit restructuring, UC-005's query-narrowing). `IC-000`'s own shape is fixed by
Design Directory And HLD §4.4 (one function per operation, per use case) — not a design choice this Feature
makes. No separate multi-candidate ideation was run for any of the six; each function/component's own one-line
note in §5 *is* its justification, not a placeholder pending a fuller writeup. The one real judgement call among
this group — `IndexStore` vs. `PathIndexer` as two components rather than one — already has its own Rationale
entry, immediately below.

`format_report`'s (`IC-003 §6`) own `report` shape was the one piece this group left genuinely undecided —
UC-002 §7 deferred it explicitly. Elicited directly from the architect while deriving `SB-001`'s specific
behaviors (Design Feature Instructions §5): a structured diff, one entry per change, the same data in both
`human_readable` and `machine_consumable` mode (§3.5) — the two differ only in rendering. See §4.6.

### 3.10 `WordReducer` As Its Own Component

`extract_words` (`PathIndexer`) and `reduce_query` (`Searcher`) both need the documentation standard's own §4
tokenization/stemming/stopword rules — the index has to be built and queried against the identical reduction,
or matching breaks. The original §5 draft asserted this in prose ("same reduction the index itself was built
with") without anything actually enforcing it: two independent implementations that happen to claim equivalence
aren't mechanically guaranteed to stay equivalent as either one changes. Extracted into its own component,
`WordReducer`, with one function (`reduce_words`) both `extract_words` and `reduce_query` call directly — the
rule now lives in exactly one place, and staying consistent is structural, not a maintained-by-hand invariant.

## 4 Data Types

Retroactively populated from the Key Decisions (§3.1 onward) that decided each interface — per
`weaver-engineering/docs` PR #19's addition to Design Feature Instructions §4.1/§4.2, a new data shape is
normally recorded here in the same step as the Key Decision that introduces it; this Feature's own §3 predates
that requirement, so this section fills in after the fact, concrete enough for §5's specific behaviors to
instantiate with literal example values. `path`, `string`, `bool`, `int`, `float`, and literal string-enum
types (e.g. `"list" | "details"`) are primitives, not defined here.

### 4.1 `ParsedStructure` (§3.1)

Returned by `parse_markdown_structure` (`IC-001 §1`). One parse serves both UC-002 and UC-003, so every field
either caller needs is present, whether or not a given caller reads it.

```
ParsedStructure = {
  headings: [{ id: string, title: string, depth: int, pseudo_number: string|null, start_line: int, end_line: int }],
  figures: [{ id: string, pseudo_number: string, start_line: int, end_line: int }],
  pseudo_numbers: [{ value: string, owner_id: string }],
  references: [{ token: string, kind: "section" | "anchor", start_line: int }],
  start_end_lines: { [node_id: string]: { start_line: int, end_line: int } }
}
```

`id`/`owner_id`/`node_id` are the parser's own stable per-node identifiers (document position + depth) — not
yet the renumbered `§M` ids UC-002 computes (§4.5). `pseudo_numbers` duplicates each heading/figure's own
`pseudo_number` as a flat list keyed by node id; kept as its own field because it's what `IC-003 §2` (`build_id_map`)
actually iterates, without needing to know headings and figures apart.

### 4.2 `Scope` (§3.3)

Returned by `resolve_scope_single`/`resolve_chained_scope` (`IC-002 §1`/`§2`) — a resolved, concrete filesystem
target: the parsed form of a `@{slug}`/`@docs`/`@all`/path specifier, or several combined.

```
Scope = {
  roots: [path],      # one or more resolved filesystem roots this scope covers
  specifier: string    # the original specifier(s), for reporting/error messages
}
```

### 4.3 `Unit`, `Entry` (§3.9)

`Unit` — one independent per-directory group `resolve_index_units` (`IC-004 §1`) produces; `resolve_documents_in_unit`
(`IC-004 §2`) reads its own immediate `.md` files.

```
Unit = { directory: path }
```

`Entry` — one existing `.index/` entry `list_index_entries`/`find_stale_entries`/`remove_index_entries`
(`IC-005 §2`-`§4`) operate on.

```
Entry = { document_path: path, index_files: [path] }   # the .sections.yaml/.words.yaml/.todo.yaml this entry owns
```

### 4.4 `Words`, `Todos` (§3.9, §3.10)

`Words` — `reduce_words`'s (`IC-006 §1`) own output, shared by `extract_words` (building the index) and
`reduce_query` (querying it) so both are mechanically the same reduction (§3.10).

```
Words = [string]   # case-folded, stemmed, stopword-free tokens
```

`Todos` — `extract_todos`'s (`IC-004 §4`) own output.

```
Todos = [{ text: string, section: string, line: int, ref: string|null }]
```

### 4.5 `Numbering`, `IdMap`, `SurvivingReferences` (§3.9)

`Numbering` — `compute_numbering`'s (`IC-003 §1`) fresh position-based numbering.

```
Numbering = { [node_id: string]: string }   # ParsedStructure node id -> new §M id, or "0" for a hidden first section
```

`IdMap` — `build_id_map`'s (`IC-003 §2`) old→new id map, keyed by pseudo-number and title (UC-002 MSS step 3).

```
IdMap = { [(old_pseudo_number, title)]: { new_id: string, node_id: string } }
```

`SurvivingReferences` — `find_surviving_references`'s (`IC-003 §3`) own output: which `ParsedStructure.references`
entries have an entry in `IdMap`, evaluated against the original document (UC-002 MSS step 4).

```
SurvivingReferences = [{ token: string, start_line: int, old_id: string, new_id: string }]
```

### 4.6 `NumberingReport` (§3.9)

`format_report`'s (`IC-003 §6`) own output, decided while deriving `SB-001` (see §3.9's addendum) — a
structured diff, one entry per change; `human_readable` and `machine_consumable` mode (§3.5) render the same
data differently, not two different shapes.

```
NumberingReport = {
  renumbered: [{ old: string, new: string, title: string }],
  references_rewritten: [{ old: string, new: string, line: int }],
  references_removed: [{ old: string, line: int }]
}
```

### 4.7 `IndexReport` (§3.9)

`index_path`'s (`IC-000 §2`) own return value. Unlike `NumberingReport`, no dedicated formatting function
exists for it — UC-003 has no human/machine-mode distinction to decide between (§3.6 only decides the
`--recursive`/`--depth` flags), so `IC-000 §2` accumulates it directly across the per-`Unit` loop rather than
calling a `format_report`-equivalent.

```
IndexReport = {
  indexed: [{ document: path, sections_written: bool, words_written: bool, todos_written: bool }],
  removed: [{ document: path }]   # stale .index/ entries removed
}
```

### 4.8 `Reference`, `TargetRange` (§3.7, §3.9)

`Reference` — the parsed form of an `extract_content`/`resolve_document`/`resolve_target_range` argument
(`{slug}[/§M.N][/L1-L2]`), before it's resolved against any actual document.

```
Reference = { slug_or_path: string, section: string|null, line_range: [int, int]|null }
```

`TargetRange` — `resolve_target_range`'s (`IC-008 §2`) own output: the concrete line range `read_source_text`
reads, already clamped to the document's actual bounds (§3.7).

```
TargetRange = { start_line: int, end_line: int }
```

`find_closest_section`'s (`IC-008 §3`) own `closest_section` reuses one entry from `ParsedStructure.headings`
(§4.1) directly — not a new type.

### 4.9 `MatchingIndex`, `Scores`, `TopResults`, `Previews` (§3.8, §3.9)

`MatchingIndex` — `load_word_index`'s (`IC-005 §5`) own output: `.words.yaml` content under a resolved scope,
filtered to the reduced query.

```
MatchingIndex = [{ document: path, section: string, matched_words: Words, total_word_count: int }]
```

`Scores` — `score_nodes`'s (`IC-007 §2`) own output.

```
Scores = [{ document: path, section: string|null, score: float }]   # section null = document-level score
```

`TopResults` — `select_top_n`'s (`IC-007 §3`) own output: `Scores`, truncated to `--max-results` (§3.8, default `20`).

```
TopResults = Scores   # same shape, just truncated
```

`Previews` — `preview_content`'s (`IC-007 §4`) own output: `--preview-lines` (§3.8, default `5`) lines per result.

```
Previews = [{ document: path, section: string|null, preview_lines: [string] }]
```

*(Two assumptions flagged for architect review rather than silently treated as decided: `ParsedStructure.pseudo_numbers`
as a field distinct from each heading/figure's own `pseudo_number` (§4.1) is inferred from `IC-003 §2`'s own
iteration need, not stated explicitly anywhere; `IndexReport`'s accumulator shape (§4.7) is inferred from
`IC-000 §2`'s bound pseudocode returning `report` without ever constructing it — a gap in the recorded bound
pseudocode this fills rather than resolves formally.)*

## 5 Internal Components

Gap Analysis (Design Feature Instructions §3) confirmed `docs/architecture/components/` had no existing entries
for this project, so every function classified **new**. Grouped by which component each function actually
belongs to (Design Directory And HLD §5 template), not by which use case happened to surface it first. Every
component below now has its own standing `IC-NNN` document, created and numbered per `weaver-engineering/docs`
PR #18's own addition to §4.2 (the Merge Pass) — including `IC-000` itself, since this is the project's first
Feature.

* [`IC-000` — Docs Tooling CLI](../../architecture/components/IC-000-docs-tooling-cli.md) — the system's own
  entry point (Design Directory And HLD §4.4): the CLI's four top-level commands, one per use case in scope.
  Each is the one operation its own use case performs (§7) and the root of that operation's own call tree.
  * `auto_number_document` — **new** — CLI entry for UC-002. Calls `MarkdownParser`, `AutoNumberer`.
  * `index_path` — **new** — CLI entry for UC-003. Calls `MarkdownParser`, `PathIndexer`, `IndexStore`.
  * `search_documentation` — **new** — CLI entry for UC-005. Calls `ScopeResolver`, `Searcher`, `IndexStore`
    (`load_word_index`).
  * `extract_content` — **new** — CLI entry for UC-006. Calls `ScopeResolver`, `ContentExtractor`.
* [`MarkdownParser`](../../architecture/components/IC-001-markdown-parser.md) — new
  * `parse_markdown_structure` — **new** — decided (§3.1) as one shared component satisfying both UC-002's and
    UC-003's parsing needs, superseding the separately-named `parse_document`/`parse_structure` candidates Gap
    Analysis originally surfaced. Used by UC-002, UC-003.
* [`ScopeResolver`](../../architecture/components/IC-002-scope-resolver.md) — new
  * `resolve_scope_single` — **new** — decided (§3.3) as a split interface. Used by UC-005, UC-006.
  * `resolve_chained_scope` — **new** — calls `resolve_scope_single` once per specifier and combines results.
    Used by UC-005 only — UC-006 has no path to it at all (§3.3). Supersedes the single `resolve_scope`
    candidate Gap Analysis originally surfaced.
* [`AutoNumberer`](../../architecture/components/IC-003-auto-numberer.md) — new
  * `compute_numbering` — **new** — fresh numbering by document position and heading depth. Used by UC-002.
  * `build_id_map` — **new** — old→new id map keyed by pseudo-number and title; raises `duplicate_identity`
    (Extension 3b). Used by UC-002.
  * `find_surviving_references` — **new** — same-document references whose old id survives into the map,
    evaluated against the original document (MSS step 4). Used by UC-002.
  * `rewrite_headings` — **new** — applies computed numbering to headings/figures. Used by UC-002.
  * `rewrite_references` — **new** — rewrites the surviving reference set. Used by UC-002.
  * `format_report` — **new** — human-readable or machine-consumable per `invoked_by`/`--json` (§3.5). Used by
    UC-002. Not (yet) shared with the other three use cases' own output — each currently formats its own
    result independently; revisit if a common report shape emerges once all four are actually built.
* [`PathIndexer`](../../architecture/components/IC-004-path-indexer.md) — new
  * `resolve_index_units` — **new** — resolves `path`/`recursive`/`depth` to independent per-directory units
    (§5's own note below on why this isn't one flat document list). Used by UC-003.
  * `resolve_documents_in_unit` — **new** — one unit's own immediate `.md` documents. Used by UC-003.
  * `extract_words` — **new** — significant words per node: calls `WordReducer.reduce_words` per node's own
    text, then records the result against that node (documentation standard §4 rules). Used by UC-003.
  * `extract_todos` — **new** — `//TODO`-style markers with text/section/line/ref. Used by UC-003.
* [`IndexStore`](../../architecture/components/IC-005-index-store.md) — new
  * `write_index_files` — **new** — persists `sections`/`words`/`todo` `.index/` files for one document; omits
    a file with no content to hold (Extension 5a). Used by UC-003.
  * `list_index_entries` — **new** — existing `.index/` entries for one unit. Used by UC-003.
  * `find_stale_entries` — **new** — entries in a unit with no corresponding current document. Used by UC-003.
  * `remove_index_entries` — **new** — deletes stale entries. Used by UC-003.
  * `load_word_index` — **new** — reads `.words.yaml` content under a resolved scope, filtered to a reduced
    query (§3.8's precursor decision in UC-005's own Technical Interpretation): returns only matching sections
    plus each one's total word count, not the whole scoped tree. Used by UC-005. Read side of the same `.index/`
    file format `PathIndexer`'s functions write — grouped here with the other file-level operations rather than
    with `PathIndexer`, since it's about the persisted format, not about walking/extracting from source `.md`.
  * `read_section_index` — **new** — added while binding `ContentExtractor` (§4.3): reads one document's own
    section boundaries directly, which neither `load_word_index` (scoped to a query match) nor any
    `PathIndexer` function exposes. Used by UC-006.
* [`WordReducer`](../../architecture/components/IC-006-word-reducer.md) — new
  * `reduce_words` — **new** — the documentation standard's own §4 tokenization/stemming/stopword rules,
    applied to any given text: case-fold, strip punctuation except the characters that stay inside a token,
    reduce plurals/possessives to their root, drop stopwords. Used by `PathIndexer` (`extract_words`, reducing a
    node's full text) and `Searcher` (`reduce_query`, reducing a query string) — the one place both actually
    call the same implementation, rather than each independently claiming to apply "the same rules."
* [`Searcher`](../../architecture/components/IC-007-searcher.md) — new
  * `reduce_query` — **new** — calls `WordReducer.reduce_words` on the query string, so it's mechanically the
    same reduction the index itself was built with, not just an equivalent one reimplemented independently.
    Used by UC-005.
  * `score_nodes` — **new** — document- and section-level relevance scores together (§3.8, §7's own open
    question about algorithm selection). Used by UC-005.
  * `select_top_n` — **new** — top `--max-results` results (§3.8). Used by UC-005.
  * `preview_content` — **new** — first `--preview-lines` lines per result in details mode (§3.8). Used by
    UC-005.
* [`ContentExtractor`](../../architecture/components/IC-008-content-extractor.md) — new
  * `resolve_document` — **new** — exact path or `**{slug}` wildcard match; cardinality covers Extensions
    2a/2b. Used by UC-006.
  * `resolve_target_range` — **new** — whole document, `§section`, line range, or both; raises
    `section_not_found` (Extension 3a); calls `IndexStore` (`read_section_index`). Used by UC-006.
  * `find_closest_section` — **new** — nearest matching section on a `section_not_found` failure; also calls
    `IndexStore` (`read_section_index`). Used by UC-006.
  * `read_source_text` — **new** — reads verbatim source text at a resolved range, clamped to actual bounds
    (§3.7), never reconstructed from index data. Used by UC-006.

## 6 External Dependencies

None identified — confirmed as Key Decision §3.4. Every component in §5 that touches the filesystem
(`ContentExtractor`, `IndexStore`, `MarkdownParser`) does so against files this same project owns and manages,
in-process — not a separate real system whose behavior can only be observed by calling it (Design Directory And
HLD §3's own bar: "a network boundary, real time, real randomness, another team's own data"). A unit test can
exercise these against a temp directory without needing anything external.

## 7 Specific Behaviors

* [SB-001 — Auto-Number A Document](specific-behaviors/SB-001-auto-number-document.md) - realizes [UC-002](../../analysis/use-cases/UC-002-auto-number-document-sections.md) (stub — behaviors not yet derived)
* [SB-002 — Index A Path](specific-behaviors/SB-002-index-a-path.md) - realizes [UC-003](../../analysis/use-cases/UC-003-index-a-path.md) (stub — behaviors not yet derived)
* [SB-003 — Search Documentation](specific-behaviors/SB-003-search-documentation.md) - realizes [UC-005](../../analysis/use-cases/UC-005-search-documentation.md) (stub — behaviors not yet derived)
* [SB-004 — Extract Document Content](specific-behaviors/SB-004-extract-document-content.md) - realizes [UC-006](../../analysis/use-cases/UC-006-extract-document-content.md) (stub — behaviors not yet derived)

*(All four use cases in scope now have a Technical Interpretation and an identified operation, Gap Analysis is
done, every individual gap from Phase 3 Ideation (§3.1-§3.10) is resolved — including every use case's own §7
Open Design Question (Design Directory And HLD §2.1's own requirement) — and the Merge Pass (§4.2) has run:
reading all ten Key Decisions together found no two describing functions that should have been the same one
(the one real candidate, `IndexStore` vs. `PathIndexer`, was already resolved as a deliberate split at Ideation
time, in §3.9's own Rationale entry — not something the Merge Pass is re-litigating; `WordReducer`, §3.10, was
the opposite finding — two independent implementations that should have been one — caught by review rather than
by the Merge Pass itself, since it wasn't yet a second Key Decision to compare against anything when first
drafted). §4.2's remaining half is also done: every Internal Component or External Dependency named in §5/§6
now has its own standing `IC-NNN` document under `docs/architecture/components/` — unconditional per Design
Feature Instructions §4.2 (`weaver-engineering/docs` PR #18), not a test any of them had to qualify for —
`IC-000` included, since this was the project's first Feature and `IC-000` is the one component every project
needs from its own first Feature onward (§4.2). §4.3 is done too: each `SB-NNN`'s own Bound Pseudocode block is
recorded, citing real addresses. Per Design Feature Instructions §1, the next unit of work is §5 — deriving each `SB-NNN`'s
actual specific behaviors, one `SB-NNN` at a time — which includes its own named human-judgement point (a quick
sanity check per freshly-derived behavior, presented to the architect, never self-approved).)*

## 8 Technology Stack

*(Not yet populated — inherits from the workspace's own established convention for this kind of tool
(`agent-plugins/packages/<name>`: pnpm workspace package, TypeScript ESM, `tsc`, Vitest — per
`weaver-engineering docs-standards-adopted` precedent) unless Key Decisions (§3) find a reason to diverge; not
asserted as decided until §3 actually says so.)*

# Rationale

**§3.1 `parse_markdown_structure` interface.** Two other candidates were considered and discarded:

* *Two separate, single-purpose parsers* (`parse_document` for UC-002, `parse_structure` for UC-003, each
  independently walking the document). Discarded: both need the exact same underlying walk — find headings,
  detect figures, per the documentation standard's own rules — so this duplicates that walk in two places that
  would have to change in lockstep every time the standard's own heading/figure rules do, for no interface
  benefit over a single call.
* *Shared low-level AST walk, separate per-caller shaping* (`parse_markdown_ast` plus two thin callers reshaping
  its output). Discarded in favor of the simpler one-call option: with only two callers today, and both wanting
  a strict subset of the same fields rather than needing genuinely different *shapes* of the same data, the
  extra component this candidate adds doesn't earn its keep yet — reconsider if a third caller's needs ever
  diverge enough that reshaping actually matters.

The chosen option (one component, broad output, each caller reads only the fields it needs) keeps the actual
parse in exactly one place while still giving each caller a direct, un-reshaped answer.

**§3.2 CLI now, MCP later.** Two MCP-schema options were proposed (MCP tool only; MCP tool plus a thin CLI
wrapper) — both discarded by the architect's own correction: designing the MCP surface at all is premature
here. The ADD's MCP-hosting default (§1) governs how this Feature is eventually *published*, not what this
design phase has to build. Building a CLI now, with core logic kept separate from CLI-specific concerns so an
MCP wrapper is addable later without rework, delivers a real, usable tool today without committing to schema
decisions (tool naming, param typing conventions) this Feature doesn't actually need yet.

**§3.3 `resolve_scope` split.** The alternative — one `resolve_scope(specifiers)` handling both single and
chained cases internally — was discarded: UC-006 draws its own scope boundary explicitly ("not the chained
multi-project form... since extraction already knows where it's going"), and a single function accepting a list
either way relies on caller discipline to respect that boundary rather than the interface itself preventing it.
Splitting into `resolve_scope_single`/`resolve_chained_scope` makes UC-006's own exclusion structural: it has no
function to call that would even let it chain.

**§3.5 UC-002 report format.** The alternative — auto-detecting human vs. machine output via whether stdout is
a TTY — was discarded: it works for a human running the command interactively, but the Assistant's own
constraint (Technical Proficiency, its persona) is that it needs machine-consumable output *reliably*, not
dependent on however its own process happens to invoke this tool (which may or may not attach a TTY depending
on the caller's own plumbing). An explicit `--json` flag is unambiguous regardless of invocation context.

**§3.6 UC-003 recurse flags.** The alternative — a single `--depth N` flag where `0` means non-recursive — was
discarded in favor of the two-flag form: it overloads one flag with two jobs (turning recursion on, and how far)
and needs a sentinel value for "unlimited," whereas `--recursive`/`--depth` keeps "recurse at all" and "how far"
as two separate, independently-omittable questions — closer to the use case's own framing of recursion as a
distinct opt-in, not a magnitude.

**§3.7 UC-006 out-of-bounds range.** The alternative — failing with the actual bounds reported, mirroring
Extension 3a's `§section`-not-found handling — was discarded: 3a fails because a *named section that doesn't
exist* is a wrong reference (nothing at that address), whereas an out-of-bounds line range names a real
document/section that *does* exist, just asks for more of it than there is — closer to Extension 2a's empty
wildcard match (a valid request, an incomplete answer) than to 3a's bad reference.

**§3.8 UC-005 defaults.** No alternative candidates were proposed for `--max-results`/`--preview-lines` as
separate flags — the architect corrected an initial framing that bundled them with `--calc` as if related, on
the basis that algorithm choice and result-volume are genuinely independent questions. `20`/`5` are the
architect's own stated defaults, not derived from any stated NFR.

**§5 component grouping.** An earlier version of this section listed functions in one flat bullet per use
case — corrected after the architect flagged it, and after `weaver-engineering/docs` PR #17 fixed the HLD
template itself to require nesting by component. The one genuinely non-obvious call is `IndexStore` versus
`PathIndexer`: `load_word_index` (UC-005, reads `.words.yaml`) could have been grouped with `PathIndexer`
(UC-003's own walking/extraction functions) since both are "the indexing domain." Split instead along a
different seam — persisted-file operations (`write_index_files`, `list_index_entries`, `find_stale_entries`,
`remove_index_entries`, `load_word_index`) versus source-walking/extraction operations
(`resolve_index_units`, `resolve_documents_in_unit`, `extract_words`, `extract_todos`) — because the former
group is defined by the `.index/` file format itself (what UC-003 writes is exactly what UC-005 reads), while
the latter is defined by walking real `.md` source, a different concern `IndexStore` has no reason to know
about. This is a judgement call, not a mechanical one, since Chunking (which would observe actual cross-Chunk
calls) hasn't happened yet — flagged here rather than left implicit, per Design Directory And HLD §4.3, and
open to revision once Chunking either confirms or contradicts it.
