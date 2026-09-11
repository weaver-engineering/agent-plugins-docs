# build-manifest

## Context
* [Workflow](../WORKFLOW.md) §4.4 - where this check is registered
* [Boundary Model](../../datamodel/boundary-model.md) §3.3 - the manifest, its closed enumeration, and why it sits at the design target

## Purpose

Is every build setting stated, inherited or exempted? A design target is something that gets **built**, so it
has to say what it is built as — and a finite list of named settings gets an answer per item, where an open
question about "the build setup" gets whatever the architect already had in mind.

## Registration

| | |
|---|---|
| Stage | maturity — `M2` |
| Model check | yes |
| Requires | [boundary-identity](boundary-identity.md) — a manifest belongs to an identified design target |

## What It Inspects

Every `SettingKind` in the closed enumeration, for every design target in scope:

| Dimension | Settings |
|---|---|
| `language` | `language`, `language-version` |
| `build-system` | `build-tool`, `package-manager` |
| `topology` | `architecture-pattern`, `directory-layout`, `module-structure`, `repository-path` |
| `dependency-constraints` | `approved-dependencies`, `banned-dependencies`, `style-and-lint-rules` |
| `test-stack` | `test-runner`, `assertion-library`, `mocking-tooling` |
| `distribution` | `artifact-form`, `registry`, `coordinates` |

Each must be **stated**, **inherited** (carrying `inheritedFrom`), or **exempted** with a reason. There is no
fourth state.

## Findings

| Kind | Raised when | Resolution routes |
|---|---|---|
| `unassessed-manifest-setting` | a setting is none of the three | [state-the-fact](../resolutions/state-the-fact.md) · [exempt](../resolutions/exempt.md) |

Blocks `M2` — signatures and the dictionary are expressed against a type system, and dependency constraints
bound what a function may call, so both become answerable exactly when the catalog does.

## Settings

None.

## Notes For P6

Exemption is a real answer and often the right one: a Library has no container build stages, a single-package
repository has no module structure worth stating. It is an answer, recorded, rather than a blank.

Nothing stops the manifest being settled well before `M2` — often it is known before `M0`, because the architect
starts from an existing stack. Declaring it then is not premature; it removes a later unit of work, and this
check simply stops being the thing that discovers it is missing.

Every design target has one, Library and Service alike. `distribution` is the access vector — how a consumer
gets at this — which for a Library is the whole consumption story.
