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

Per the documentation standard's own §3/§4 rules: eligible headings exclude `## Context`/`# Appendix`/
`# Rationale`; a figure is a fenced code block carrying a pseudo-number; `pseudo_numbers` and `references`
include same-document `§M.N` tokens and markdown-link anchors; `start_end_lines` gives each node's line range.

```yaml
calls: []
called_from:
  - "IC-000 §1"
  - "IC-000 §2"
```

# Rationale

Two other shapes were considered and discarded when this interface was decided — see the HLD's own `# Rationale`
(§3.1): two separate single-purpose parsers (discarded — duplicates the same walk), and a shared low-level AST
walk with separate per-caller shaping (discarded — no third caller yet to justify the extra indirection). One
component, broad output, each caller reading only the fields it needs, keeps the actual parse in exactly one
place.
