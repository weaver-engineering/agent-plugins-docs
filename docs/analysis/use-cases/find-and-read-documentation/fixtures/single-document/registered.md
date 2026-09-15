# Registered — single-document

What the registry must be able to hand back after registering `/repo/docs/retry-policy.md`, whatever form it holds
it in. Nothing here says how any of it is stored.

`words` says whether the node's own text contributed to what a search can match. `lines` is the node's span in
its source document, first line to last.

## 1 `/repo/docs/retry-policy.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Retry Policy` | document | 1-21 | yes |
| `Context` | context | 3-5 | no |
| `§1 When To Retry` | section | 6-10 | yes |
| `§2 How Many Times` | section | 11-18 | yes |
| `§2.1 Backoff` | section | 15-18 | yes |
| `§3 What To Report` | section | 19-21 | yes |

No figures. No outstanding TODO markers.

Registering a path that names one document registers one document. There is no directory here to walk, and
nothing about the registration of this document differs from the registration of the same document sitting in
a directory of others — which is why @`1.1` establishes the single-path case and leaves every content rule to
@`1.3.1`.
