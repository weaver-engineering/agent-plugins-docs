# Registered Before — unchanged-documents

The registry's state when this run begins: what it already holds for `/repo/docs/widgets/`, from an earlier
registration of the same path.

This says what the registry holds, never how — the same discipline
[stale-registration](../stale-registration/registered-before.md) follows. What matters here is only that
`doc-a.md` and `doc-b.md`'s content, as registered then, is byte-identical to their content now; `doc-c.md`
did not exist under this path at all.

| Path | Holds |
|---|---|
| `/repo/docs/widgets/doc-a.md` | 2 sections, `§1` - `§2`; no figures; no TODOs |
| `/repo/docs/widgets/doc-b.md` | 2 sections, `§1` - `§2`; no figures; no TODOs |

`/repo/docs/widgets/doc-c.md` is not listed: this run is the first time anything is registered at that path.
