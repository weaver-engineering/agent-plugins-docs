# IC-002 — ScopeResolver

**Kind:** internal service

## Context
* [Doc Search & Retrieval — High-Level Design](../../design/doc-search-and-retrieval/doc-search-and-retrieval-hld.md) - the design directory whose Key Decisions (§3.3) first decided this interface

## Purpose

Resolves an `@{scope}` specifier — a single project, `@docs`, `@all`, or a filesystem path — to a concrete
scope. Split into two functions (§3.3) so that a caller with no legitimate need to chain multiple specifiers
has no function available that would let it.

## 1 `resolve_scope_single`

Resolves exactly one scope specifier.

`resolve_scope_single(specifier: string) -> Scope`

Accepts `@{slug}` (`-docs` suffix optional), `@docs` (the reserved slug `docs`), `@all` (every registered docs
repo), or a filesystem path, optionally narrowed by `/{path}`. Defaults to cwd if omitted.

`@{slug}`/`@docs`/`@all` resolve via `.weaver-docs.yaml` (HLD §3.3 addendum): starting from cwd, walk upward
through parent directories until one is found, then read it as a YAML mapping of slug to docs root — each path
relative to the registry file's own directory unless already absolute. `@all` is recognized *before* any
registry lookup and combines every entry in the registry directly — it never looks up a slug literally named
`"all"`. Raises `weaver_docs_yaml_not_found` if no `.weaver-docs.yaml` is found anywhere up the tree from cwd
(`SB-003 §6`), or `unknown_scope_slug` if one is found but doesn't list the requested slug (`SB-003 §2.1`) — both
uncaught here, propagating to this function's own caller.

```yaml
calls: []
called_from:
  - "IC-000 §3"
  - "IC-000 §4"
  - "IC-002 §2"
```

## 2 `resolve_chained_scope`

Resolves several chained specifiers and combines the results.

`resolve_chained_scope(specifiers: string[]) -> Scope`

Calls `resolve_scope_single` once per specifier in `@{slug}@{slug}` form and combines the results. UC-006 has
no path to this function at all — its own scope exclusion is structural, not caller discipline (§3.3).

```yaml
calls:
  - "IC-002 §1"
called_from:
  - "IC-000 §3"
```

# Rationale

The discarded alternative — one `resolve_scope` handling both single and chained cases internally — is recorded
in the HLD's own `# Rationale` (§3.3): it would have relied on the caller simply never passing more than one
specifier to respect UC-006's own exclusion, rather than the interface itself preventing it.
