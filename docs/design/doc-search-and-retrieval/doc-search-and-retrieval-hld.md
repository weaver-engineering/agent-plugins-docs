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

* [Feature doc-search-and-retrieval](doc-search-and-retrieval-feature.md) — explicitly excludes: why these four
  capabilities exist and what each does (already-written analysis, linked below, immutable once its Technical
  Interpretation is derived — not re-opened by this design); the capability catalog entry itself
  (`docs/architecture/capability-catalog.md`, already present, not duplicated here); and the mechanics of
  achieving parity between Claude Code and OpenCode for any given capability
  (`docs/design/cross-platform-capability-parity.md`, WVR-94, a separate placeholder document this design does
  not resolve)
  - Design Task: WVR-95
    + [UC-002](../../analysis/use-cases/UC-002-auto-number-document-sections.md)
    + [UC-003](../../analysis/use-cases/UC-003-index-a-path.md)
    + [UC-005](../../analysis/use-cases/UC-005-search-documentation.md)
    + [UC-006](../../analysis/use-cases/UC-006-extract-document-content.md)

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

**Extended while deriving `SB-002`'s specific behaviors (Design Feature Instructions §5.1):** `# Appendix` and
`# Rationale` headings must be locatable — `.sections.yaml` needs their existence and line range so a reader can
still be pointed at and shown one on request (UC-006) — but excluded from `.words.yaml`, to keep the word index
focused on meaningful content. `parse_markdown_structure` now includes Appendix/Rationale headings in its own
`headings` output (previously excluded entirely, alongside Context). `# Context` stays excluded from `headings`
entirely, unlike Appendix/Rationale — nothing needs to locate or extract it the way UC-006 needs to for the
other two.

One alternative was considered and discarded: giving `PathIndexer` its own separate, narrower Appendix/
Rationale heading detector, leaving `parse_markdown_structure` untouched. Discarded because it reintroduces
exactly the duplicate-walk concern this Key Decision's original two-separate-parsers candidate was rejected
over — a second, independent detector that has to change in lockstep with the first every time the documentation
standard's own heading rules do, for no interface benefit over extending the one shared parse.

**Corrected while deriving `SB-004`'s specific behaviors (Design Feature Instructions §5.1):** the first version
of this addendum tagged each `Heading` with a `kind: "body" | "appendix" | "rationale"` field so a consumer could
tell Appendix/Rationale apart from ordinary body headings. That field only ever existed on the *in-memory*
`ParsedStructure` a fresh `parse_markdown_structure` call produces — fine for `extract_words`/`compute_numbering`/
`rewrite_headings`, which always run against a fresh parse, but useless to `resolve_target_range` (`IC-008 §2`),
which runs later against the *persisted* `.sections.yaml` (documentation-standards.md §4, a shared cross-project
standard whose own documented shape has no room for a `kind` field, and isn't something this design process
edits directly). `Heading.kind` (§4.1) is removed; a new function, `is_reserved_section(title: string) -> bool`
(`IC-001 §2`), replaces it — a single shared predicate checking a title against the two reserved, fixed names
`"Appendix"`/`"Rationale"` (documentation-standards.md §3 — always exactly those titles, never arbitrary),
called directly by every consumer that needs the distinction: `extract_words`, `compute_numbering` (against a
heading's own title in `ParsedStructure` — `rewrite_headings` needs no separate call, since it only ever numbers
what `compute_numbering`'s own `Numbering` map already includes), `preview_content` (`IC-007 §4`), and
`resolve_target_range` (against a title key in `sections.yaml`, read via `IC-005 §6`) — deliberately *not*
`find_closest_section`, whose own job is typo-correction for a failed `§section` reference, where Appendix/
Rationale are still legitimate candidates (`IC-008`'s own `# Rationale`). One rule, one place it lives, checked
by title wherever a heading actually occurs — not a `kind` computed once and unable to survive
past the process that computed it. The alternative — keeping `kind` for the in-memory consumers and giving
`resolve_target_range` its own separate title check — was discarded: it's the exact shape of duplication
`WordReducer` (§3.10) already exists to prevent, just for a different pair of functions.

**Corrected again, same session:** `# Appendix`/`# Rationale` are *protected headings*, not just individually
excluded ones — the reason to exclude them from word-extraction in the first place (guiding an agent to the
document's own distilled truth, not its justification) applies just as much to whatever's nested *underneath*
one, and a document may reasonably give its own Appendix real substructure (`## 1 Config Reference`, etc.). A
per-heading `is_reserved_section` check alone doesn't cover this: `parse_markdown_structure` walks every
heading regardless of nesting, so a subsection inside an Appendix would otherwise be word-extracted normally,
polluting search with exactly the supporting material the exclusion exists to keep out — while still correctly
appearing in `.sections.yaml`, since being locatable and extractable is the whole benefit worth keeping (an
agent that's read "the truth" can still be pointed at its own supporting detail on request). `extract_words` and
`compute_numbering` now track *protected zones*, not single headings: a heading matching `is_reserved_section`
opens a zone at its own depth; every subsequent heading deeper than that stays inside the zone (skipped, same as
the opening heading itself) until one appears at that depth or shallower, which closes it. A new shared
function, `mark_protected_headings(headings: [Heading]) -> {[id: string]: "appendix" | "rationale"}` (`IC-001
§3`), maps every `Heading.id` (§4.1) that falls inside a zone to *which* reserved name opened it — computed
once, called by both consumers, rather than each independently re-deriving the same depth-tracking walk (the
zone name itself, not just a flat membership list, is what `write_index_files` needs to populate `SectionIndex`'s
own `zone` field — §3.9's later addendum — `extract_words`/`compute_numbering` only ever check membership,
ignoring which zone). `preview_content`/`resolve_target_range` don't need it — their own "whole document ends
before the first protected heading" boundary only ever cares about *where the first zone starts*, which
`is_reserved_section` alone already finds correctly walking headings in order.

Scoping note, not a capability claim: the walk itself doesn't care how many `# Appendix`/`# Rationale` headings
exist or where — it would exclude words correctly under any of them, wherever they sit. That's an incidental
property of a simple depth-tracking algorithm, not a design decision to support more than the conventional
shape (documentation-standards.md §3's own framing is singular — "Optional `# Appendix`," "Optional
`# Rationale`," each at most one, typically last). Multiple same-titled Appendix/Rationale headings scattered
through a document — the distributed-addressing idea dropped while deriving `SB-004` — would still collide in
`.sections.yaml`'s own title-keyed scheme the moment a second one existed; nothing here fixes that. The zone
mechanism only ever needs to correctly exclude *whichever* Appendix/Rationale headings a document actually has —
it isn't what makes having more than one of either a supported shape.

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

**Extended while deriving `SB-003`'s specific behaviors (Design Feature Instructions §5.1):** how `@{slug}`
(and `@docs`, which is just the reserved slug `docs`) actually resolves to a concrete filesystem root was never
decided — assuming every docs repo lives under a fixed `weaver-engineering/` workspace layout was considered
and rejected by the architect directly: there's no guarantee every docs repo sits under a directory literally
named `weaver-engineering`. Resolved instead via an explicit registry file, `.weaver-docs.yaml`: starting from
cwd, `resolve_scope_single` walks upward through parent directories until it finds one (the same discovery
pattern `.git`/`.nvmrc` already use in this ecosystem), then reads it as a YAML mapping of slug to docs root:
```yaml
agent-plugins: AgentPlugins/agent-plugins-docs/docs
docs: docs
```
Each path is relative to `.weaver-docs.yaml`'s own directory unless it's already absolute — both forms are
supported, so a registry entry can point anywhere on disk, not only within the tree the registry file itself
lives in. `@all` is a reserved specifier, recognized *before* any registry lookup — it enumerates every entry in
the registry directly, never attempting to look up a slug literally named `"all"`, and combines them the same
way `resolve_chained_scope` combines several `resolve_scope_single` calls. (A project actually registered under
the slug `all` would be permanently unreachable via `@{slug}` — the registry format doesn't itself prevent that
collision; worth the architect's own awareness, not resolved here.) Not designed here: how `.weaver-docs.yaml`
itself gets created or kept up to date as projects are added — that's a workspace-setup concern outside this
Feature's own scope;
`resolve_scope_single` only needs to be able to find and read one, not maintain it. Failure to find a
`.weaver-docs.yaml` anywhere up the tree, or a slug absent from the one that's found, is a real failure mode
this decision surfaces but doesn't resolve — left to `SB-003`'s own unhappy-path derivation.

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

**Refined while deriving `SB-004`'s specific behaviors (Design Feature Instructions §5.1):** clamping only
covers a range with *some* genuine overlap with valid content — `start` itself inside bounds, `end` running
past them. Two further cases have no valid overlap at all, and clamping them would produce nonsense rather than
a partial answer, so both fail instead, raising `invalid_range`: `start` after `end` (a malformed range,
regardless of bounds), and `start` itself already past the target's own real end. For a `§section[{start}-{end}]`
reference, "the target's own real end" is that section's own `end_line`. For a bare `[{start}-{end}]` (no
`§section` — the whole document), it's the same whole-document boundary `resolve_target_range`'s own §3.9
addendum already established — the point before any `# Appendix`/`# Rationale`, not the file's physical last
line — so a `start` that only exists because of Appendix/Rationale content still fails, the same as one past the
literal end of file.

**`find_closest_section`'s real mechanism, settled the same session:** an initial framing treated `section_not_found`'s
own recovery as fuzzy title matching (`§Apendix` → `§Appendix`) — wrong. It's a *numeric-hierarchy* walk, and
only ever applies to a `§section` reference that's a valid pseudo-number: strip the reference's own last
dot-separated segment (`"1.2.3"` → `"1.2"`) and check whether *that* number exists; repeat if it still doesn't,
one segment shorter each time. The first existing ancestor found is the returned pointer — not a guess based on
how similar any title looks, an exact number that's simply less specific than what was asked for. A
title-shaped reference that matches nothing has no hierarchy to walk at all — it stays a plain
`section_not_found`, no pointer, no fallback. If the walk exhausts every segment and even the top-level number
doesn't exist either, there's no ancestor left to point to at all — at that point `extract_content` doesn't fail:
it falls all the way back to the whole document (the same range §1's own whole-document extraction computes,
Appendix/Rationale excluded per §3.9's own addendum) and returns that content directly, a success, not a
failure-plus-pointer. `IC-000 §4`'s own bound pseudocode is revised accordingly: `find_closest_section` (`IC-008
§3`) returns either a `Heading` (an existing ancestor found) or nothing at all (exhausted) — the former still
returns `failure, closest`; the latter calls `resolve_target_range` again with `reference.section` cleared and
returns that content as success instead.

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

**Corrected while deriving `SB-003 §1`'s specific behavior (Design Feature Instructions §5.2):** UC-005 MSS
step 4 requires "a document-level score alongside each section's," and documentation-standards.md §4 already
treats the document root as its own node with its own scoped word count, on equal footing with a section — but
`load_word_index` (`IC-005 §5`) only ever searched sections, and its own return type, `MatchingSection` (§4.34),
typed `section` as a non-nullable `string`, with no shape for a document-root match at all, even though
`score_nodes`'s own output type, `ScoredNode` (§4.36), already had `section: string|null` with `null` meaning
exactly a document-level score — a score nothing upstream could ever actually produce. `load_word_index` now
also checks a document's own root `WordCounts` (the `document` key of `WordIndex`, §4.16) for a match,
alongside its sections; `MatchingSection.section` (§4.34) is now `string|null` to match, `null` meaning the same
thing it already means on `ScoredNode`. Without this, a document whose only content is root-level prose (no
headings at all — the shape `SB-002 §1.3` derives) would have been entirely invisible to search.

**Corrected while deriving `SB-003 §4`'s specific behavior (Design Feature Instructions §5.2):** what "a
document's/section's own content" means for `preview_content` (`IC-007 §4`) was never actually specified beyond
"first `--preview-lines` lines," and the architect corrected an initial, wrong assumption (that a document-level
match's preview was scoped to just its own root/preamble text, mirroring how word-extraction scopes the
document root). The real rule: a **document**-level preview is the first N lines of the *whole document* —
spanning every section and subsection in document order — **excluding** any `# Appendix`/`# Rationale` content
(§3.1's own later correction: computed via `is_reserved_section`, `IC-001 §2`, checked against each section
title `IC-005 §6` returns, not a `kind` field — the whole-document range runs from line 1 up to, but not
including, the first heading `is_reserved_section` matches, or end of file if there is none). A **section**-level
preview is the first N lines of that section specifically, including any subsections it contains — a section's
own `start_line`/`end_line` (§4.1) already spans through its subsections by construction, so no separate
handling is needed there — capped by the section's own content length, never spilling into a sibling section.
This is also why `# Appendix`/`# Rationale` can never appear as a search result at all: they carry no word
counts (§3.1 addendum) to ever match a query in the first place — the only way to see one is
`extract_content`'s (UC-006) explicit `§Appendix`/`§Rationale` reference, direct and deliberate, not a side
effect of search. `preview_content` now also calls `IC-005 §6`/`IC-001 §2` itself (§5's own `calls:` list below,
updated) to determine the boundary — it wasn't declared to call anything before this correction, because the
need for it wasn't yet known.

**Corrected the same way for `resolve_target_range` (`IC-008 §2`, UC-006):** a whole-document reference (no
`§section` given) resolves to the document's content excluding `# Appendix`/`# Rationale`, the same boundary
`preview_content` now uses, via the same `is_reserved_section` (`IC-001 §2`) call — retrieving either of those
two sections is only possible by naming it explicitly (`§Appendix`/`§Rationale`), the ordinary
`section_not_found` path (§3 of this document) if it doesn't exist. Recorded here even though `SB-004` (UC-006)
hasn't been fully derived yet, so this doesn't need rediscovering later.

**A general fix, surfaced but not limited to Appendix/Rationale, while deriving `SB-004`:** `.sections.yaml` keyed
by title (documentation-standards.md §4) collides the moment any two headings anywhere in a document share a
title — an entirely ordinary, expected document shape (a repeated subsection name like "Overview" or "Examples"
under two different parents), not an edge case. `read_section_index`'s own `SectionIndex` (§4.33) is re-keyed by
each heading's own stable `id` (`Heading.id`, §4.1 — already unique by construction) instead; `title` moves from
being the key to being a field within each entry, alongside the `number`/`type`/`start_line`/`end_line` it
already carries. This is a correction to `.sections.yaml`'s own documented shape
(`weaver-engineering/docs`'/documentation-standards.md's, not something this design process edits directly —
flagged for that repo's own follow-up) — legitimate for this design to define, since this Feature's own
`IndexStore` is the first real tool ever writing that file for real, per documentation-standards.md's own
Rationale ("existing hand-written `.index/` files... will get corrected... once the indexing tool itself exists
and does a real pass").

Resolving a `§{section}` reference (`resolve_target_range`, `IC-008 §2`) now tries two things instead of one
direct key lookup: if the reference matches a valid pseudo-number pattern (documentation-standards.md §3's own
regex), resolve against whichever entry's `number` field equals it — inherently unique, since `compute_numbering`
never assigns the same number twice. Otherwise, treat it as a title and match against entries' `title` fields —
case-insensitively (elicited while deriving `SB-004 §1.4.1`: `§aPpeNdix` resolves the same as `§Appendix`),
consistent with `is_reserved_section`'s own case-insensitive check (§3.1's own later addendum) so the two never
quietly disagree about what a given heading actually is: exactly one match resolves normally; zero matches is
the existing `section_not_found` path (§3 above); *more than one* match is new — raises `ambiguous_section`,
mirroring Extension 2b's own shape (wildcard matches more than one document → fail, return the candidate list)
at the section level instead of the document level, so a caller can retry using one candidate's own `number` to
disambiguate. A section without a `number` (Appendix/Rationale, or any hidden-`0` heading) that also collides on
title has no fallback address to retry with — a real but narrow gap this doesn't fully close, left as a known
limitation rather than solved by inventing a synthetic identifier no caller would ever type.

**A third resolution path, found while deriving `SB-004 §1.4.5`'s own follow-on:** a `§{section}` reference can
also be zone-qualified — `§rationale.1.2` / `§appendix.1.2` (case-insensitive on the zone name, matching
`is_reserved_section`'s own case-insensitivity) — addressing a number *within* that specific protected zone
rather than globally. Necessary because Appendix/Rationale subsections keep whatever numbers their author typed
(`mark_protected_headings` only ever stops them being auto-*renumbered*, HLD §3.1's second addendum) with no
coordination against the main body's own numbering — `"1"` inside a Rationale and `"1"` in the body are
independent numbering scopes that can legitimately collide. Resolution: split on the first `.`, check the first
segment against `is_reserved_section`; if it matches, resolve the remainder as a number *scoped to entries whose
own `zone` field equals it* (§4.33) — otherwise fall through to the existing two paths (plain number, then
title) unchanged. A bare, unqualified number (`§1.2`) still only ever resolves against `zone: null` (ordinary
body) entries — it was never ambiguous with anything inside a protected zone to begin with, since those simply
aren't candidates for an unqualified lookup.

### 3.10 `WordReducer` As Its Own Component

`extract_words` (`PathIndexer`) and `reduce_query` (`Searcher`) both need the documentation standard's own §4
tokenization/stemming/stopword rules — the index has to be built and queried against the identical reduction,
or matching breaks. The original §5 draft asserted this in prose ("same reduction the index itself was built
with") without anything actually enforcing it: two independent implementations that happen to claim equivalence
aren't mechanically guaranteed to stay equivalent as either one changes. Extracted into its own component,
`WordReducer`, with one function (`reduce_words`) both `extract_words` and `reduce_query` call directly — the
rule now lives in exactly one place, and staying consistent is structural, not a maintained-by-hand invariant.

**Extended while deriving `SB-002 §1.1`'s specific behavior (Design Feature Instructions §5.2):** `reduce_words`
recognizes a TODO-marker pattern (any of the six recognized spellings — `//`/`#` prefix × `TODO`/`TO-DO`/
`TO_DO`, case-insensitive) *wherever it occurs in the input text*, not only where the line-start rule
(documentation-standards.md §4) would also make it a genuine `extract_todos` marker, and canonicalizes every
occurrence to the single literal token `"//todo"` — one occurrence, one token, regardless of which of the six
spellings was actually used. This is deliberate, not an artifact of the ordinary tokenization rule (`/` merely
staying inside a token, §3.1's original reasoning for `"//todo"` surviving as a token at all, undersold what was
actually wanted): it's what lets a query for any one spelling (`reduce_query` calling the same `reduce_words`)
match every TODO occurrence in scope regardless of which spelling the author happened to use, a single canonical
search term for "there's outstanding work here" — the same reasoning documentation-standards.md's own stopword
list already applies (a root form blocking all its inflections) turned around: here, distinct *surface forms*
of the same marker concept collapse to one indexed term instead of one root blocking several forms. The rest of
a marker line — the description text after the marker — stays excluded from word-extraction as before; only the
marker pattern itself contributes the canonical token.

## 4 Data Types

Retroactively populated from the Key Decisions (§3.1 onward) that decided each interface — per
`weaver-engineering/docs` PR #19's addition to Design Feature Instructions §4.1/§4.2, a new data shape is
normally recorded here in the same step as the Key Decision that introduces it; this Feature's own §3 predates
that requirement, so this section fills in after the fact, concrete enough for §5's specific behaviors to
instantiate with literal example values. `path`, `string`, `bool`, `int`, `float`, and literal string-enum
types (e.g. `"list" | "details"`) are primitives, not defined here.

Every structured value gets its own named entry — one field per line, and a nested object gets factored into
its own `§4.N` rather than inlined anonymously (`weaver-engineering/docs` PR #20's addition to HLD-TEMPLATE.md
§4) — even where that means a small, single-use shape exists mainly so a signature elsewhere has a real name to
cite.

### 4.1 `Heading` (§3.1)

One element of `ParsedStructure.headings` (§4.6).

```
Heading = {
  id: string,
  title: string,
  depth: int,
  pseudo_number: string|null,
  start_line: int,
  end_line: int
}
```

`id` is the parser's own stable per-node identifier — concretely, `string(start_line)` (settled while answering
a question raised against `documentation-standards.md`'s own retrofit of this Feature's `SectionIndex`
correction, §3.9): a heading's own `start_line` is already unique within one document (two headings can't share
a line) and already computed as part of parsing, so it needs no separate scheme of its own. Not yet the
renumbered `§M` id UC-002 computes (§4.18). `find_closest_section` (`IC-008 §3`) returns one `Heading` directly
when it finds an ancestor, `null` when it doesn't (§3.7's later correction) — not a new type either way. Whether
a given heading is `# Appendix`/`# Rationale` isn't a field here — `is_reserved_section`
(`IC-001 §2`, §3.1's own later correction) checks a heading's own `title` directly, since that's the one piece
of information guaranteed to survive from a fresh parse all the way to the persisted `.sections.yaml` a later
read has to work from. `# Appendix`/`# Rationale` get an `id` the exact same way any other heading does — no
special-casing needed, since `id` was never derived from numbering or depth-in-the-body-sequence to begin with.

### 4.2 `Figure` (§3.1)

One element of `ParsedStructure.figures` (§4.6) — a fenced code block carrying a pseudo-number.

```
Figure = {
  id: string,
  pseudo_number: string,
  start_line: int,
  end_line: int
}
```

### 4.3 `PseudoNumberEntry` (§3.1)

One element of `ParsedStructure.pseudo_numbers` (§4.6) — every typed pseudo-number found, headings and figures
alike, kept as its own flat list because it's what `IC-003 §2` (`build_id_map`) actually iterates, without
needing to know headings and figures apart.

```
PseudoNumberEntry = {
  value: string,
  owner_id: string
}
```

### 4.4 `ReferenceToken` (§3.1)

One element of `ParsedStructure.references` (§4.6) — a same-document `§M.N` token or markdown-link anchor found
anywhere in the document body, before renumbering resolves whether it survives.

```
ReferenceToken = {
  token: string,
  kind: "section" | "anchor",
  start_line: int
}
```

### 4.5 `LineRange` (§3.1)

One value of `ParsedStructure.start_end_lines` (§4.6) — every node's own line range.

```
LineRange = {
  start_line: int,
  end_line: int
}
```

### 4.6 `ParsedStructure` (§3.1)

Returned by `parse_markdown_structure` (`IC-001 §1`). One parse serves both UC-002 and UC-003, so every field
either caller needs is present, whether or not a given caller reads it.

```
ParsedStructure = {
  headings: [Heading],
  figures: [Figure],
  pseudo_numbers: [PseudoNumberEntry],
  references: [ReferenceToken],
  start_end_lines: { [node_id: string]: LineRange }
}
```

### 4.7 `Scope` (§3.3)

Returned by `resolve_scope_single`/`resolve_chained_scope` (`IC-002 §1`/`§2`) — a resolved, concrete filesystem
target: the parsed form of a `@{slug}`/`@docs`/`@all`/path specifier, or several combined.

```
Scope = {
  roots: [path],
  specifier: string
}
```

`roots` is one or more resolved filesystem roots this scope covers; `specifier` is the original specifier(s),
kept for reporting/error messages.

### 4.8 `Unit` (§3.9)

One independent per-directory group `resolve_index_units` (`IC-004 §1`) produces; `resolve_documents_in_unit`
(`IC-004 §2`) reads its own immediate `.md` files.

```
Unit = {
  directory: path
}
```

### 4.9 `Units` (§3.9)

`resolve_index_units`'s (`IC-004 §1`) own return value.

```
Units = [Unit]
```

### 4.10 `Documents` (§3.9)

`resolve_documents_in_unit`'s (`IC-004 §2`) own return value — one unit's own immediate `.md` documents, never
another unit's.

```
Documents = [path]
```

### 4.11 `Entry` (§3.9)

One existing `.index/` entry `remove_index_entries` (`IC-005 §4`) operates on.

```
Entry = {
  document_path: path,
  index_files: [path]
}
```

`index_files` is whichever of `.sections.yaml`/`.words.yaml`/`.todo.yaml` this entry actually owns (a file is
omitted entirely when it has no content to hold, UC-003 Extension 5a).

### 4.12 `Entries` (§3.9)

`list_index_entries`'s and `find_stale_entries`'s (`IC-005 §2`/`§3`) own return value.

```
Entries = [Entry]
```

### 4.13 `TodoEntry` (§3.9)

One element of `Todos` (§4.14) — a single `//TODO`-style marker.

```
TodoEntry = {
  text: string,
  section: string,
  line: int,
  ref: string|null
}
```

### 4.14 `Todos` (§3.9)

`extract_todos`'s (`IC-004 §4`) own output.

```
Todos = [TodoEntry]
```

### 4.15 `WordCounts` (§3.9, §3.10)

A word→count map — one document's or one section's own significant-word tally, per the documentation
standard's own `.words.yaml` shape (documentation-standards.md §4).

```
WordCounts = { [word: string]: int }
```

### 4.16 `WordIndex` (§3.9, §3.10)

`extract_words`'s (`IC-004 §3`) own output: `WordReducer.reduce_words` (`IC-006 §1`) called once per node (the
document itself, plus each section/figure) and recorded against that node — not the same shape as `Words`
(§4.17), which is one call's own flat token list. This is the correction this retrofit makes to
`write_index_files`'s own `words` parameter, previously mistyped as `Words`.

```
WordIndex = {
  document: WordCounts,
  sections: { [section_name: string]: WordCounts }
}
```

### 4.17 `Words` (§3.10)

`reduce_words`'s (`IC-006 §1`) own output for one call — shared by `extract_words` (building `WordIndex`
entries, one call per node) and `reduce_query` (reducing a query string) so both are mechanically the same
reduction (§3.10), not two independently-asserted-equivalent implementations.

```
Words = [string]
```

Case-folded, stemmed, stopword-free tokens (documentation-standards.md §4).

### 4.18 `Numbering` (§3.9)

`compute_numbering`'s (`IC-003 §1`) fresh position-based numbering.

```
Numbering = { [node_id: string]: string }
```

Maps a `ParsedStructure` node id (§4.1) to its new `§M` id, or `"0"` for a hidden first section.

### 4.19 `IdMapEntry` (§3.9)

One value of `IdMap` (§4.20).

```
IdMapEntry = {
  new_id: string,
  node_id: string
}
```

### 4.20 `IdMap` (§3.9)

`build_id_map`'s (`IC-003 §2`) old→new id map, keyed by pseudo-number and title (UC-002 MSS step 3).

```
IdMap = { [(old_pseudo_number, title)]: IdMapEntry }
```

### 4.21 `SurvivingReference` (§3.9)

One element of `SurvivingReferences` (§4.22).

```
SurvivingReference = {
  token: string,
  start_line: int,
  old_id: string,
  new_id: string
}
```

### 4.22 `SurvivingReferences` (§3.9)

`find_surviving_references`'s (`IC-003 §3`) own output: which `ParsedStructure.references` (§4.6) entries have
an entry in `IdMap` (§4.20), evaluated against the original document (UC-002 MSS step 4).

```
SurvivingReferences = [SurvivingReference]
```

### 4.23 `RenumberedEntry` (§3.9)

One element of `NumberingReport.renumbered` (§4.26).

```
RenumberedEntry = {
  old: string,
  new: string,
  title: string
}
```

### 4.24 `RewrittenReference` (§3.9)

One element of `NumberingReport.references_rewritten` (§4.26).

```
RewrittenReference = {
  old: string,
  new: string,
  line: int
}
```

### 4.25 `RemovedReference` (§3.9)

One element of `NumberingReport.references_removed` (§4.26).

```
RemovedReference = {
  old: string,
  line: int
}
```

### 4.26 `NumberingReport` (§3.9)

`format_report`'s (`IC-003 §6`) own output, decided while deriving `SB-001` (see §3.9's addendum) — a
structured diff, one entry per change; `human_readable` and `machine_consumable` mode (§3.5) render the same
data differently, not two different shapes.

```
NumberingReport = {
  renumbered: [RenumberedEntry],
  references_rewritten: [RewrittenReference],
  references_removed: [RemovedReference]
}
```

### 4.27 `IndexedDocument` (§3.9)

One element of `IndexReport.indexed` (§4.29).

```
IndexedDocument = {
  document: path,
  sections_written: bool,
  words_written: bool,
  todos_written: bool
}
```

### 4.28 `RemovedDocument` (§3.9)

One element of `IndexReport.removed` (§4.29) — one stale `.index/` entry removed.

```
RemovedDocument = {
  document: path
}
```

### 4.29 `IndexReport` (§3.9)

`index_path`'s (`IC-000 §2`) own return value. Unlike `NumberingReport`, no dedicated formatting function
exists for it — UC-003 has no human/machine-mode distinction to decide between (§3.6 only decides the
`--recursive`/`--depth` flags), so `IC-000 §2` accumulates it directly across the per-`Unit` loop rather than
calling a `format_report`-equivalent.

```
IndexReport = {
  indexed: [IndexedDocument],
  removed: [RemovedDocument]
}
```

### 4.30 `Reference` (§3.7, §3.9)

The parsed form of an `extract_content`/`resolve_document`/`resolve_target_range` argument
(`{slug}[/§M.N][/L1-L2]`), before it's resolved against any actual document.

```
Reference = {
  slug_or_path: string,
  section: string|null,
  line_range: [int, int]|null
}
```

### 4.31 `TargetRange` (§3.7, §3.9)

`resolve_target_range`'s (`IC-008 §2`) own output: the concrete line range `read_source_text` reads, already
clamped to the document's actual bounds (§3.7).

```
TargetRange = {
  start_line: int,
  end_line: int
}
```

### 4.32 `DocumentMatches` (§3.9)

`resolve_document`'s (`IC-008 §1`) own output — cardinality covers UC-006 Extensions 2a (empty) and 2b
(multiple) as its two non-single-match outcomes.

```
DocumentMatches = [path]
```

### 4.33 `SectionIndex` (§3.9)

`read_section_index`'s (`IC-005 §6`) own output — one document's own `.sections.yaml` content, read directly
(added while binding `ContentExtractor`, §4.3 addendum below §3.9). Keyed by each heading/figure's own stable
`id` (§3.9's later general-fix addendum), not by title — two entries can share a title without colliding, since
`title` is now a field, not the key. `zone` records which protected zone (§3.1's second addendum) the entry
falls inside, if any — `null` for ordinary body content — added while deriving `SB-004 §1.4.5`'s own follow-on:
Appendix/Rationale's own numbering is never coordinated with the main body's (`mark_protected_headings` skips
numbering it, §3.1), so a subsection inside either can legitimately share a bare number with an unrelated body
section (both a `## 1 Config Reference` inside `# Rationale` and a `## 1 Getting Started` in the body can be
`"1"`) — `zone` is what lets `§rationale.1.2`/`§appendix.1.2` resolve *within* the right one instead of
colliding globally.

```
SectionIndex = { [id: string]: { title: string, number: string|null, type: "section" | "code-block", start_line: int, end_line: int, zone: "appendix" | "rationale" | null } }
```

### 4.33.1 `SectionCandidate` (§3.9)

One element of `SectionCandidates` (§4.33.2) — enough for a caller to retry a disambiguated reference.

```
SectionCandidate = {
  title: string,
  number: string|null
}
```

### 4.33.2 `SectionCandidates` (§3.9)

`resolve_target_range`'s (`IC-008 §2`) own output on an `ambiguous_section` failure — every entry sharing the
referenced title, so the caller can retry with one candidate's own `number` (where it has one).

```
SectionCandidates = [SectionCandidate]
```

### 4.34 `MatchingSection` (§3.8, §3.9)

One element of `MatchingIndex` (§4.35).

```
MatchingSection = {
  document: path,
  section: string|null,
  matched_words: Words,
  total_word_count: int
}
```

`section: null` means the match is against the document's own root `WordCounts` (`WordIndex.document`, §4.16),
not any of its sections — the same meaning `ScoredNode.section` (§4.36) already gives `null` (§3.9 addendum).

### 4.35 `MatchingIndex` (§3.8, §3.9)

`load_word_index`'s (`IC-005 §5`) own output: `.words.yaml` content under a resolved scope, filtered to the
reduced query — only sections that actually contain a matching word, not the whole scoped tree.

```
MatchingIndex = [MatchingSection]
```

### 4.36 `ScoredNode` (§3.8, §3.9)

One element of `Scores` (§4.37).

```
ScoredNode = {
  document: path,
  section: string|null,
  score: float
}
```

`section: null` means a document-level score, not a section-level one.

### 4.37 `Scores` (§3.8, §3.9)

`score_nodes`'s (`IC-007 §2`) own output.

```
Scores = [ScoredNode]
```

### 4.38 `TopResults` (§3.8)

`select_top_n`'s (`IC-007 §3`) own output: `Scores` (§4.37), truncated to `--max-results` (§3.8, default `20`).

```
TopResults = Scores
```

### 4.39 `PreviewedResult` (§3.8, §3.9)

One element of `Previews` (§4.40).

```
PreviewedResult = {
  document: path,
  section: string|null,
  preview_lines: [string]
}
```

### 4.40 `Previews` (§3.8, §3.9)

`preview_content`'s (`IC-007 §4`) own output: `--preview-lines` (§3.8, default `5`) lines per result, for
details mode.

```
Previews = [PreviewedResult]
```

*(Three things flagged for architect review rather than silently treated as decided: `ParsedStructure.pseudo_numbers`
(§4.3) as a field distinct from each heading/figure's own `pseudo_number` is inferred from `IC-003 §2`'s own
iteration need, not stated explicitly anywhere; `IndexReport`'s accumulator shape (§4.29) is inferred from
`IC-000 §2`'s bound pseudocode returning `report` without ever constructing it, a gap in the recorded bound
pseudocode this fills rather than resolves formally; and `WordIndex` (§4.16) is a genuine correction, not a
formatting fix — `write_index_files`'s `words` parameter and `extract_words`'s own return were both typed
`Words` before this retrofit, which doesn't hold up: `Words` is one `reduce_words` call's flat token list,
while what actually gets persisted to `.words.yaml` is per-node, with counts.)*

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
  * `is_reserved_section` — **new** — added while deriving `SB-004` (§3.1 addendum): a shared predicate checking
    a title against the two reserved section names, `"Appendix"`/`"Rationale"`, called by anything needing a
    single heading's own status — `Searcher` (`preview_content`), and `ContentExtractor` (`resolve_target_range`
    only — `find_closest_section` deliberately doesn't call it; see its own note below). Used by UC-005, UC-006.
  * `mark_protected_headings` — **new** — added the same session (§3.1's second addendum): returns every heading
    id inside a *protected zone* — a reserved heading and everything nested under it — via `is_reserved_section`
    plus a depth-tracking walk, since word-extraction/numbering need the whole subtree excluded, not just the
    reserved heading itself. Called by `PathIndexer` (`extract_words`) and `AutoNumberer` (`compute_numbering`
    only — `rewrite_headings` needs no separate call). Used by UC-002, UC-003.
* [`ScopeResolver`](../../architecture/components/IC-002-scope-resolver.md) — new
  * `resolve_scope_single` — **new** — decided (§3.3) as a split interface. Used by UC-005, UC-006.
  * `resolve_chained_scope` — **new** — calls `resolve_scope_single` once per specifier and combines results.
    Used by UC-005 only — UC-006 has no path to it at all (§3.3). Supersedes the single `resolve_scope`
    candidate Gap Analysis originally surfaced.
* [`AutoNumberer`](../../architecture/components/IC-003-auto-numberer.md) — new
  * `compute_numbering` — **new** — fresh numbering by document position and heading depth; skips every heading
    `MarkdownParser` (`mark_protected_headings`) marks — `# Appendix`/`# Rationale` and their own nested
    subsections alike. Used by UC-002.
  * `build_id_map` — **new** — old→new id map keyed by pseudo-number and title; raises `duplicate_identity`
    (Extension 3b). Used by UC-002.
  * `find_surviving_references` — **new** — same-document references whose old id survives into the map,
    evaluated against the original document (MSS step 4). Used by UC-002.
  * `rewrite_headings` — **new** — applies computed numbering to headings/figures; only ever asked to number
    what `compute_numbering` already skipped Appendix/Rationale for. Used by UC-002.
  * `rewrite_references` — **new** — rewrites the surviving reference set. Used by UC-002.
  * `format_report` — **new** — human-readable or machine-consumable per `invoked_by`/`--json` (§3.5). Used by
    UC-002. Not (yet) shared with the other three use cases' own output — each currently formats its own
    result independently; revisit if a common report shape emerges once all four are actually built.
* [`PathIndexer`](../../architecture/components/IC-004-path-indexer.md) — new
  * `resolve_index_units` — **new** — resolves `path`/`recursive`/`depth` to independent per-directory units
    (§5's own note below on why this isn't one flat document list). Used by UC-003.
  * `resolve_documents_in_unit` — **new** — one unit's own immediate `.md` documents. Used by UC-003.
  * `extract_words` — **new** — significant words per node: calls `WordReducer.reduce_words` per node's own
    text, then records the result against that node (documentation standard §4 rules); skips every heading
    `MarkdownParser` (`mark_protected_headings`) marks — `# Appendix`/`# Rationale` and their own nested
    subsections alike. Used by UC-003.
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
  * `preview_content` — **new** — first `--preview-lines` lines per result in details mode (§3.8); for a
    document-level result, the whole document excluding `# Appendix`/`# Rationale` — calls `IndexStore`
    (`read_section_index`) and `MarkdownParser` (`is_reserved_section`) to find that boundary (§3.9 addendum).
    Used by UC-005.
* [`ContentExtractor`](../../architecture/components/IC-008-content-extractor.md) — new
  * `resolve_document` — **new** — exact path or `**{slug}` wildcard match; cardinality covers Extensions
    2a/2b. Used by UC-006.
  * `resolve_target_range` — **new** — whole document, `§section`, line range, or both; a whole-document
    reference excludes `# Appendix`/`# Rationale` (§3.9 addendum) — either is still reachable by naming it
    explicitly; raises `section_not_found` (Extension 3a); calls `IndexStore` (`read_section_index`) and
    `MarkdownParser` (`is_reserved_section`). Used by UC-006.
  * `find_closest_section` — **new** — nearest matching section on a `section_not_found` failure; also calls
    `IndexStore` (`read_section_index`) — deliberately *doesn't* call `is_reserved_section`, unlike
    `resolve_target_range` above: this is typo-correction for a failed reference, where Appendix/Rationale are
    still legitimate candidates, not a default to exclude them from. Used by UC-006.
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
