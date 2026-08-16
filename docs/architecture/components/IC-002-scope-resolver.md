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

Accepts `@{slug}` (`-docs` suffix optional), `@docs` (`weaver-engineering/docs`), `@all` (every
weaver-engineering docs repo), or a filesystem path, optionally narrowed by `/{path}`. Defaults to cwd if
omitted.

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
