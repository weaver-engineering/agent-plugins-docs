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

*(Not yet populated — depends on Solution Shape (Design Feature Instructions §2.3 / §4), which decides which of
§5's new candidates actually earn a standing Internal Component document versus staying Chunk-private, per
Design Directory And HLD §4.3. Gap Analysis (§3, below) is done; this section fills in once Ideation has run.)*

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

## 4 Data Types

*(Not yet populated — depends on the Internal Component interfaces §3/§5 decide.)*

## 5 Internal Components

Gap Analysis (Design Feature Instructions §3) result: `docs/architecture/components/` has no existing entries
for this project (confirmed directly, not assumed), so every candidate function the four Technical
Interpretations collectively name classifies **new** — there is nothing existing to compare any of them
against. Grouped below by which component each function actually belongs to (Design Directory And HLD §5
template, per `weaver-engineering/docs` PR #17), not by which use case happened to surface it first — a
component two use cases both rely on appears once, both functions nested beneath it. Which of these components
actually earn a standing `IC-NNN` document versus staying Chunk-private (Design Directory And HLD §4.3) is
still Solution Shape's decision (§2.3/§4), not made here.

* `MarkdownParser` — new — defined in this design
  * `parse_markdown_structure` — **new** — decided (§3.1) as one shared component satisfying both UC-002's and
    UC-003's parsing needs, superseding the separately-named `parse_document`/`parse_structure` candidates Gap
    Analysis originally surfaced. Used by UC-002, UC-003.
* `ScopeResolver` — new — defined in this design
  * `resolve_scope_single` — **new** — decided (§3.3) as a split interface. Used by UC-005, UC-006.
  * `resolve_chained_scope` — **new** — calls `resolve_scope_single` once per specifier and combines results.
    Used by UC-005 only — UC-006 has no path to it at all (§3.3). Supersedes the single `resolve_scope`
    candidate Gap Analysis originally surfaced.
* `AutoNumberer` — new — defined in this design
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
* `PathIndexer` — new — defined in this design
  * `resolve_index_units` — **new** — resolves `path`/`recursive`/`depth` to independent per-directory units
    (§5's own note below on why this isn't one flat document list). Used by UC-003.
  * `resolve_documents_in_unit` — **new** — one unit's own immediate `.md` documents. Used by UC-003.
  * `extract_words` — **new** — significant words per node, documentation standard §4 rules. Used by UC-003.
  * `extract_todos` — **new** — `//TODO`-style markers with text/section/line/ref. Used by UC-003.
* `IndexStore` — new — defined in this design
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
* `Searcher` — new — defined in this design
  * `reduce_query` — **new** — same tokenization/stemming/stopword reduction the index itself was built with.
    Used by UC-005.
  * `score_nodes` — **new** — document- and section-level relevance scores together (§3.8, §7's own open
    question about algorithm selection). Used by UC-005.
  * `select_top_n` — **new** — top `--max-results` results (§3.8). Used by UC-005.
  * `preview_content` — **new** — first `--preview-lines` lines per result in details mode (§3.8). Used by
    UC-005.
* `ContentExtractor` — new — defined in this design
  * `resolve_document` — **new** — exact path or `**{slug}` wildcard match; cardinality covers Extensions
    2a/2b. Used by UC-006.
  * `resolve_target_range` — **new** — whole document, `§section`, line range, or both; raises
    `section_not_found` (Extension 3a). Used by UC-006.
  * `find_closest_section` — **new** — nearest matching section on a `section_not_found` failure. Used by
    UC-006.
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
done, and every individual gap from Phase 3 Ideation (§3.1-§3.8) is resolved — including every use case's own
§7 Open Design Question (Design Directory And HLD §2.1's own requirement). Per Design Feature Instructions §1,
the next unit of work is §4.2's Merge Pass (checking whether any of §5's still-separately-listed new candidates
actually turned out to want the same function once visible side by side), followed by deciding which of them
earn a standing `IC-NNN` document (Design Directory And HLD §4.3) versus staying Chunk-private — populating §2's
Solution Overview is what that produces.)*

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
