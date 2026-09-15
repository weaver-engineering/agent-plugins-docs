# Registered — nested-directory, with `--recurse`

What the registry must be able to hand back after registering `/repo/docs/handbook/` with `--recurse`. The corpus is
identical to the one behind
[`nested-directory.registered-shallow`](registered-shallow.md); only the invocation differs.

## 1 `/repo/docs/handbook/index.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Handbook` | document | 1-12 | yes |
| `Context` | context | 3-5 | no |
| `§1 How This Handbook Is Arranged` | section | 6-9 | yes |
| `§2 Where To Start` | section | 10-12 | yes |

## 2 `/repo/docs/handbook/onboarding/setup.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Setup` | document | 1-12 | yes |
| `Context` | context | 3-5 | no |
| `§1 Accounts` | section | 6-9 | yes |
| `§2 Machine` | section | 10-12 | yes |

## 3 `/repo/docs/handbook/onboarding/tooling/editors.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Editors` | document | 1-9 | yes |
| `Context` | context | 3-5 | no |
| `§1 Which Editor` | section | 6-9 | yes |

No figures and no outstanding TODO markers in any of the three.

Each document's registration is identical in kind: nothing about a node's type, position or words depends on
how deep the document sat, and `editors.md` two levels down is registered exactly as `index.md` at the top is.
Depth decides which documents are in scope, and nothing else about them.
