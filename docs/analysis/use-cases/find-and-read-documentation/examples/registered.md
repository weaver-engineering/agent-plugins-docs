# Registered — the example corpus

What the registry holds after `corpus/` is registered, whatever form it holds it in. Nothing here says
how any of it is stored.

`words` says whether the node's own text contributed to what a search can match. `lines` is the node's
span in its source document, first line to last. A node with `words: no` stays addressable and can still
be reported; it is simply never matched.

**Derived, not typed.** `python3 derive.py --check` recomputes every figure below from `corpus/`.

## 1 `a-document-with-contexts.md`

| Node | Type | Reference | Lines | Words | Indexed |
|---|---|---|---|---|---|
| *(document root)* `A Document With Contexts` | document | `a-document-with-contexts` | 1-49 | 119 | yes |
| &nbsp;&nbsp;`Context` | context | — | 3-7 | — | no |
| &nbsp;&nbsp;`1 Scope` | section | `a-document-with-contexts§1` | 8-11 | 10 | yes |
| &nbsp;&nbsp;`2 This Is A Top Section Without Context` | section | `a-document-with-contexts§2` | 12-42 | 96 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;`2.1 This Is A Nested Section Without Context` | section | `a-document-with-contexts§2.1` | 16-19 | 13 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;`2.2 This Is A Nested Section With Context` | section | `a-document-with-contexts§2.2` | 20-42 | 72 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Context` | context | — | 22-25 | — | no |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Overview` | section | `a-document-with-contexts§2.2.0` | 26-28 | 11 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`2.2.1 This Is A Sub Section Of A Section With Context` | section | `a-document-with-contexts§2.2.1` | 29-42 | 52 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`2.2.1.1 Sub Blah Blah` | section | `a-document-with-contexts§2.2.1.1` | 37-39 | 13 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`2.2.1.2 Sub Blah Blah 2` | section | `a-document-with-contexts§2.2.1.2` | 40-42 | 14 | yes |
| &nbsp;&nbsp;`3 This Is A Top Level Section With Context` | section | `a-document-with-contexts§3` | 43-49 | 9 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;`Context` | context | — | 45-49 | — | no |

No outstanding TODO markers.

## 2 `policies/eviction-policy.md`

| Node | Type | Reference | Lines | Words | Indexed |
|---|---|---|---|---|---|
| *(document root)* `Cache Eviction Policy` | document | `policies/eviction-policy` | 1-30 | 161 | yes |
| &nbsp;&nbsp;`Context` | context | — | 3-6 | — | no |
| &nbsp;&nbsp;`1 Scope` | section | `policies/eviction-policy§1` | 7-11 | 33 | yes |
| &nbsp;&nbsp;`2 When An Entry Is Evicted` | section | `policies/eviction-policy§2` | 12-26 | 99 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;`2.1 Pressure Eviction` | section | `policies/eviction-policy§2.1` | 17-21 | 37 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;`2.2 Age Eviction` | section | `policies/eviction-policy§2.2` | 22-26 | 28 | yes |
| &nbsp;&nbsp;`3 What Is Never Evicted` | section | `policies/eviction-policy§3` | 27-30 | 26 | yes |

No outstanding TODO markers.

## 3 `policies/retention-policy.md`

| Node | Type | Reference | Lines | Words | Indexed |
|---|---|---|---|---|---|
| *(document root)* `Data Retention Policy` | document | `policies/retention-policy` | 1-21 | 78 | yes |
| &nbsp;&nbsp;`Context` | context | — | 3-5 | — | no |
| &nbsp;&nbsp;`1 Data Classes` | section | `policies/retention-policy§1` | 6-9 | 24 | yes |
| &nbsp;&nbsp;`2 Retention By Class` | section | `policies/retention-policy§2` | 10-17 | 18 | yes |
| &nbsp;&nbsp;`3 Expiry` | section | `policies/retention-policy§3` | 18-21 | 33 | yes |

No outstanding TODO markers.

## 4 `procedures/cache-tuning.md`

| Node | Type | Reference | Lines | Words | Indexed |
|---|---|---|---|---|---|
| *(document root)* `Cache Tuning` | document | `procedures/cache-tuning` | 1-33 | 99 | yes |
| &nbsp;&nbsp;`Context` | context | — | 3-5 | — | no |
| &nbsp;&nbsp;`1 What To Measure` | section | `procedures/cache-tuning§1` | 6-10 | 32 | yes |
| &nbsp;&nbsp;`2 Sizing` | section | `procedures/cache-tuning§2` | 11-16 | 41 | yes |
| &nbsp;&nbsp;`3 When Tuning Will Not Help` | section | `procedures/cache-tuning§3` | 17-20 | 24 | yes |
| &nbsp;&nbsp;`Rationale` | rationale | — | 21-29 | — | no |
| &nbsp;&nbsp;`Appendix A: Worked Sizing Example` | appendix | — | 30-33 | — | no |

Outstanding TODO at line 15: TODO: name the eviction rate that counts as "near zero" once we have a month of production figures.

## 5 `procedures/eviction-procedures.md`

| Node | Type | Reference | Lines | Words | Indexed |
|---|---|---|---|---|---|
| *(document root)* `Eviction Procedures` | document | `procedures/eviction-procedures` | 1-28 | 139 | yes |
| &nbsp;&nbsp;`Context` | context | — | 3-5 | — | no |
| &nbsp;&nbsp;`1 Before You Start` | section | `procedures/eviction-procedures§1` | 6-10 | 30 | yes |
| &nbsp;&nbsp;`2 Policies In Force` | section | `procedures/eviction-procedures§2` | 11-24 | 77 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;`2.1 Cache Eviction` | section | `procedures/eviction-procedures§2.1` | 15-19 | 29 | yes |
| &nbsp;&nbsp;&nbsp;&nbsp;`2.2 Bulk Eviction` | section | `procedures/eviction-procedures§2.2` | 20-24 | 33 | yes |
| &nbsp;&nbsp;`3 After Eviction` | section | `procedures/eviction-procedures§3` | 25-28 | 30 | yes |

No outstanding TODO markers.

## 6 Totals

5 documents, 39 nodes, of which 30 can answer a search and 9 are structure only.

`corpus/notes.txt` is not a markdown document. It is not registered, it is not reported, and no
answer mentions it — silently, because a file that is not a document is not a failure.
