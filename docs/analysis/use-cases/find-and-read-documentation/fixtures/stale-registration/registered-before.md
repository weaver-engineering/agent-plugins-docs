# Registered Before — stale-registration

The registry's state when this run begins: what it already holds for `/repo/docs/widgets/`, from an earlier
registration of the same path.

This says what the registry holds, never how. Its storage form is §7's first open question and nothing here
answers it — the fact being stated is only that a registration for `doc-b.md` exists and can still be handed
back, which is true of any form the registry might take.

| Path | Holds |
|---|---|
| `/repo/docs/widgets/doc-a.md` | 3 sections, `§1` - `§2`; no figures; no TODOs |
| `/repo/docs/widgets/doc-b.md` | 7 sections, `§1` - `§3`; `Appendix` 3 sections; `Rationale` 4 sections; 4 figures; 2 TODOs |

`/repo/docs/widgets/doc-b.md` has since been deleted from the corpus. The registry does not know that yet: until
this run, a search over this scope would still return sections of a document that is no longer there, and a
fetch against one of those references would find nothing behind it.
