# Registered — unchanged-documents

What the registry must be able to hand back after registering `/repo/docs/widgets/`, where `doc-a.md` and
`doc-b.md` are exactly as they were at their last registration and `doc-c.md` is new.

This holds all three in full — the same complete structure it would hold if every one of them were new. What
is unchanged here is what the *report* chooses to say, never what the registry actually computes and keeps.

## 1 `/repo/docs/widgets/doc-a.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Widget Overview` | document | 1-13 | yes |
| `Context` | context | 3-5 | no |
| `§1 What A Widget Is` | section | 6-9 | yes |
| `§2 What The Store Is For` | section | 10-13 | yes |

No figures. No outstanding TODO markers.

## 2 `/repo/docs/widgets/doc-b.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Retry Policy` | document | 1-12 | yes |
| `Context` | context | 3-5 | no |
| `§1 When To Retry` | section | 6-9 | yes |
| `§2 How Many Times` | section | 10-12 | yes |

No figures. No outstanding TODO markers.

## 3 `/repo/docs/widgets/doc-c.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Eviction Policy` | document | 1-9 | yes |
| `Context` | context | 3-5 | no |
| `§1 When A Widget Is Evicted` | section | 6-9 | yes |

No figures. No outstanding TODO markers.

Nothing here distinguishes `doc-a.md` and `doc-b.md` from `doc-c.md`: all three carry the same fields, in the
same shape, whether or not their content matches what the registry already held. Being unchanged is a fact
about the *report*, never a different kind of registration.
