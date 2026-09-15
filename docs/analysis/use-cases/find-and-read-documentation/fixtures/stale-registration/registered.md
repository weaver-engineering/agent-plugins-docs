# Registered — stale-registration

What the registry must be able to hand back after re-registering `/repo/docs/widgets/`, with `doc-b.md` no longer
under it.

`words` says whether the node's own text contributed to what a search can match. `lines` is the node's span in
its source document, first line to last.

## 1 `/repo/docs/widgets/doc-a.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Widget Overview` | document | 1-16 | yes |
| `Context` | context | 3-5 | no |
| `§1 What A Widget Is` | section | 6-13 | yes |
| `§1.1 Keys` | section | 10-13 | yes |
| `§2 What The Store Is For` | section | 14-16 | yes |

No figures. No outstanding TODO markers.

## 2 `/repo/docs/widgets/doc-b.md`

Nothing. The registry holds no node, no word and no TODO for this path, and a search over this scope can no
longer return one.

What matters is *how* that state was reached. This is not `doc-b.md`'s registration with its entries removed:
it is the registration of what is under the path now, computed from the corpus as it currently stands, in which
`doc-b.md` simply does not appear. The registry was never asked what it used to hold, and no comparison against
it took place. The same result would follow from registering this path for the very first time.
