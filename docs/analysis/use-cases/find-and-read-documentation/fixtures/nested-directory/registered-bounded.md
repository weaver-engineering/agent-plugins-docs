# Registered — nested-directory, with `--depth 1`

What the registry must be able to hand back after registering `/repo/docs/handbook/` with `--depth 1`. The corpus is
identical to the one behind
[`nested-directory.registered-shallow`](registered-shallow.md) and
[`nested-directory.registered-recursed`](registered-recursed.md); only the invocation differs.

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

Nothing. It sits two levels below the registered path, and the walk stopped after one.

`setup.md`'s registration is identical here to its registration under `--recurse`
([`nested-directory.registered-recursed`](registered-recursed.md)) — nothing about how a document in scope is
registered depends on which flag put it there, only whether it is in scope at all.
