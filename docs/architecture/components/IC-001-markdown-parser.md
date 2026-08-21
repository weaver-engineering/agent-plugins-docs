# IC-001 — MarkdownParser

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.1) first decided this interface

## Purpose

Parses a markdown document's headings and pseudo-numbered figures into every field either UC-002's or UC-003's
own operation could want, in one call — one shared walk rather than two independently-maintained ones (§3.1).

## 1 `parse_markdown_structure`

Parses one document's headings and figures.

`parse_markdown_structure(document: path) -> ParsedStructure`

Per the documentation standard's own §3/§4 rules: `## Context` is excluded from `headings` entirely; `# Appendix`
and `# Rationale` headings are included (HLD §3.1 addendum) like any other heading — a reader can still be
pointed at and shown one via `.sections.yaml` (UC-006). Telling them apart from an ordinary body heading is
`is_reserved_section`'s own job (§2 below), not a field on `Heading` itself. A figure is a fenced code block
carrying a pseudo-number; `pseudo_numbers` and `references` include same-document `§M.N` tokens and markdown-link
anchors; `start_end_lines` gives each node's line range.

```yaml
calls: []
called_from:
  - "IC-000 §1"
  - "IC-000 §2"
```

## 2 `is_reserved_section`

Checks whether a title is one of the two reserved, fixed section names the documentation standard defines
(documentation-standards.md §3) — `"Appendix"` or `"Rationale"` — added while deriving `SB-004` (HLD §3.1
addendum), replacing an earlier, in-memory-only `Heading.kind` field that couldn't survive past a fresh parse to
where later consumers (extraction, reading `.sections.yaml` back) needed the same distinction. A single shared
predicate, not reimplemented per caller — the same reasoning `WordReducer` (HLD §3.10) already established for
`reduce_words`. Case-insensitive (§3.9's later addendum, matching `resolve_target_range`'s own title resolution
for the same reason — a document titled `# APPENDIX` still needs to be recognized as reserved, or the two checks
would quietly disagree about what counts as one).

`is_reserved_section(title: string) -> bool`

```yaml
calls: []
called_from:
  - "IC-001 §3"
  - "IC-007 §4"
  - "IC-008 §2"
```

## 3 `mark_protected_headings`

Maps each `Heading.id` (§4.1) that falls inside a *protected zone* — a heading `is_reserved_section` matches,
and everything nested under it — to *which* reserved name opened that zone. Added this session (HLD §3.1's
second correction): `is_reserved_section` alone only ever answers for one heading in isolation, but the reason
to exclude Appendix/Rationale from word-extraction applies to their whole subtree, not just the heading that
opens it. Walks headings in document order, tracking the depth a zone opened at; every subsequent heading
strictly deeper stays marked with the same zone name, until one appears at that depth or shallower closes it.
Every marked heading still gets a normal `.sections.yaml` entry elsewhere, now including which zone it's in
(HLD §3.9's later addendum) — this only governs word-extraction/numbering directly, though the zone name it
records also lets extraction resolve a `§rationale.1.2`-style qualified reference (the follow-on `SB-004 §1.4.5`
surfaced). The walk itself doesn't care how many `# Appendix`/`# Rationale` headings a document has or where —
that's incidental to a simple depth-tracking algorithm, not a claim that more than the conventional
one-of-each-at-the-end shape is supported: multiple same-titled ones would still collide in `.sections.yaml`'s
own title-keyed... rather, `id`-keyed (§3.9's own general fix) scheme, at the *title* level specifically — the
distributed-addressing idea dropped while deriving `SB-004`.

`mark_protected_headings(headings: [Heading]) -> {[id: string]: "appendix" | "rationale"}`

```yaml
calls:
  - "IC-001 §2"
called_from:
  - "IC-003 §1"
  - "IC-004 §3"
  - "IC-005 §1"
```

# Rationale

Two other shapes were considered and discarded when `parse_markdown_structure` (§1) was decided — see the HLD's
own `# Rationale` (§3.1): two separate single-purpose parsers (discarded — duplicates the same walk), and a
shared low-level AST walk with separate per-caller shaping (discarded — no third caller yet to justify the extra
indirection). One component, broad output, each caller reading only the fields it needs, keeps the actual parse
in exactly one place. `is_reserved_section` (§2) and `mark_protected_headings` (§3) followed the same reasoning
once further cases of the same duplication risk showed up (HLD §3.1's two later corrections): rather than every
consumer independently deciding what "Appendix"/"Rationale" means, or independently re-deriving the same
zone-tracking walk, the one component that already owns title-based structural classification (`## Context`'s
own exclusion) owns both.
