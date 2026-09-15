# Registered — nested-directory, without `--recurse`

What the registry must be able to hand back after registering `/repo/docs/handbook/` with no `--recurse` flag.

## 1 `/repo/docs/handbook/index.md`

| Node | Type | Lines | Words |
|---|---|---|---|
| *(document root)* `Handbook` | document | 1-12 | yes |
| `Context` | context | 3-5 | no |
| `§1 How This Handbook Is Arranged` | section | 6-9 | yes |
| `§2 Where To Start` | section | 10-12 | yes |

No figures. No outstanding TODO markers.

## 2 `/repo/docs/handbook/onboarding/setup.md`

Nothing. The subdirectory was not descended into.

## 3 `/repo/docs/handbook/onboarding/tooling/editors.md`

Nothing, for the same reason, two levels down.

Neither document is registered, neither is reported, and neither is an error. A caller who wanted them asks
for them with `--recurse`; a caller who did not has been given exactly the scope they named.
