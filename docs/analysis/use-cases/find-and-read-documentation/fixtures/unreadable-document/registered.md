# Registered — unreadable-document

What the registry must be able to hand back after registering `/repo/docs/widgets/`, where `secret.md` could not be
read.

## 1 `/repo/docs/widgets/doc-a.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Widget Overview` | document | 1-13 | yes |
| `Context` | context | 3-5 | no |
| `§1 What A Widget Is` | section | 6-9 | yes |
| `§2 What The Store Is For` | section | 10-13 | yes |

No figures. No outstanding TODO markers.

## 2 `/repo/docs/widgets/secret.md`

Nothing. It is a markdown document and it is in scope, but it could not be opened, so nothing about its
structure or its words is known and nothing is recorded. This is not the same absence as `notes.txt` in
[many-documents](../many-documents/registered.md): that file was never a document to begin with, and this one
is, only unreachable. The difference is exactly why one is silent and this one is named in a warning.
