# Registered — many-documents

What the registry must be able to hand back after registering `/repo/docs/widgets/`, whatever form it holds it in.
Nothing here says how any of it is stored: these are the facts a search or a fetch over this scope is then
determined by, not a picture of a storage layout.

`words` says whether the node's own text contributed to what a search can match. `lines` is the node's span in
its source document, first line to last.

## 1 `/repo/docs/widgets/doc-a.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Widget Overview` | document | 1-17 | yes |
| `Context` | context | 3-5 | no |
| `§1 What A Widget Is` | section | 6-13 | yes |
| `§1.1 Keys` | section | 10-13 | yes |
| `§2 What The Store Is For` | section | 14-17 | yes |

No figures. No outstanding TODO markers.

## 2 `/repo/docs/widgets/doc-b.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Widget Store Reference` | document | 1-103 | yes |
| `Context` | context | 3-5 | no |
| `§1 Overview` | section | 6-10 | yes |
| `§2 Configuration` | section | 11-51 | yes |
| `§2.1 Basic Options` | section | 15-25 | yes |
| `§2.1.a Minimal Configuration` | figure | 19-24 | no |
| `§2.2 Advanced Options` | section | 26-35 | yes |
| `§2.2.a` | figure | 30-32 | no |
| `§2.3 Defaults` | section | 36-51 | yes |
| `§2.3.a` | figure | 40-48 | no |
| `§3 Usage` | section | 52-72 | yes |
| `§3.1 Common Patterns` | section | 56-72 | yes |
| `§3.1.a Put With Retry` | figure | 60-71 | no |
| `Appendix` | region | 73-86 | no |
| `§Appendix.1 Sample Configuration` | section | 75-78 | no |
| `§Appendix.2 Sample Session` | section | 79-82 | no |
| `§Appendix.3 Glossary` | section | 83-86 | no |
| `Rationale` | region | 87-103 | no |
| `§Rationale.1 Why Configuration Has Two Tiers` | section | 89-100 | no |
| `§Rationale.1.1 The Basic Tier` | section | 93-96 | no |
| `§Rationale.1.2 The Advanced Tier` | section | 97-100 | no |
| `§Rationale.2 Why The Timeout Default Is Still Open` | section | 101-103 | no |

Four figures, one per notation form and the combination the invariant table names as its own rule:

* `§2.1.a` — a `*fig.* 2.1.a` caption line before the fence. Its node spans the caption through the closing
  fence: the caption is what carries the pseudo-number, so it is part of the figure it names, not a line of
  prose sitting above it.
* `§2.2.a` — a bare numeric info string, `` ```2.2.a ``, and no caption. Its node is the fence alone; there is
  nothing else to include.
* `§2.3.a` — a `fig: 2.3.a` key inside a `---`-delimited block within a `` ```mermaid `` fence, and no caption.
  The fence's own info string stays exactly `mermaid`; the frontmatter is content of the figure, not a second
  node.
* `§3.1.a` — carries two markers that disagree: a `*fig.* 3.1.a` caption and a `fig: 3.1.b` frontmatter key
  inside the fence. Registered once, as `3.1.a` — the caption, because it is given first in the document,
  before the fence the frontmatter sits inside of. `3.1.b` is not a second figure and is not registered
  anywhere; it is simply the marker that lost.

Outstanding TODO markers:

| Text | Section | Line | Ref |
|---|---|---|---|
| document the eviction policy properly (WVR-000) | `§2.2 Advanced Options` | 34 | WVR-000 |
| confirm the default timeout is still thirty seconds | `§2.3 Defaults` | 50 | — |

## 3 `/repo/docs/widgets/notes.txt`

Not registered. It is not a markdown document, so it is not a document, and the registry holds nothing about
it — not an entry saying it was skipped, and not an error.
