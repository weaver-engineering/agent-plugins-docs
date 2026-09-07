# Glossary

## Context
* [Data Model](design/design-assistant/datamodel/DATA-MODEL.md) - the service metamodel most entries below are drawn from
* [Design The Feature Process](design-the-feature-process.md) - the process the metamodel supports, and the source of the process terms below
* @docs/standards/documentation-standards.md - §2's rule that every new concept gets a row here in the PR that introduces it

One row per concept term used across this repo's docs: the term (linked to the document that defines it) and a
one-line definition. Any new concept introduced into this repo's docs gets a row here in the same PR that
introduces it (Documentation Standards §2) — this file is never left to catch up later. A term's own document is
where detail actually lives and is expected to grow; this table stays a one-line pointer to it, never a second
copy of its content.

Terms owned by the workspace-level Product/Service model — Product, Platform, Feature, Use Case, Product
Offering, Persona — are defined in `weaver-engineering/docs/glossary.md` and are not duplicated here.

Where a term's metamodel treatment differs from the process as currently written, the row states both. The
metamodel is a draft under review; it does not silently retire a term the process still uses.

## 1 Terms

| Term | Definition |
| :--- | :--- |
| [Access Vector](design/design-assistant/datamodel/boundary-model.md#33-build-manifest) | The `distribution` dimension of a build manifest — how a consumer obtains and references the artifact. For a Library it is the whole consumption story. |
| [Address](design/design-assistant/datamodel/DATA-MODEL.md#51-addressing) | An element's identifier: typed path segments nesting through the boundaries that structure it, optionally prefixed with a namespace. Derived, never allocated. |
| [Advisory Acknowledgement](design/design-assistant/datamodel/reconciliation-model.md#31-advisory-findings) | The architect's recorded acceptance of one advisory finding — who, when, why this instance is correct. Unanswered advisories block `M4`. |
| [Advisory Finding](design/design-assistant/datamodel/reconciliation-model.md#31-advisory-findings) | A finding that gates no maturity level — raised where a pattern is usually wrong but legitimately right often enough that a gate would be worse than a note. |
| [Anticipation Check](design/design-assistant/datamodel/behavior-model.md#23-matching) | The check that every expected dependency interaction is anticipated by some required effect; a failure is an unexpected external side effect. |
| [Behavior](design/design-assistant/datamodel/behavior-model.md) | What a design target does at one leaf cell of one operation's condition space. |
| [Blocked](design/design-assistant/datamodel/reconciliation-model.md#51-blocked) | A design target with a change request outstanding: not complete, unable to advance, and not in error — a third status beside at-a-level and failing. |
| [Bound Pseudocode](design-the-feature-process.md) | A use case's Technical Interpretation with each abstract call substituted for the real function address satisfying it. Dropped by the metamodel draft — see [Behavior Model §4.2](design/design-assistant/datamodel/behavior-model.md#42-why-there-is-no-separate-bound-pseudocode). |
| [Boundary Kind](design/design-assistant/datamodel/boundary-model.md#4-boundary-kinds) | A contained boundary's role within its parent: interface, business domain, shared logic, or dependency. |
| [Build Manifest](design/design-assistant/datamodel/boundary-model.md#33-build-manifest) | What a design target is built as: language, build system, topology, dependency constraints, test stack, and how consumers obtain the artifact. Inherited by contained targets. |
| [Call Graph](design/design-assistant/datamodel/function-and-call-graph.md#4-the-call-graph) | The derived graph of every function and its declared calls, with `calledFrom` as the reverse index. |
| [Call Tree](design/design-assistant/datamodel/behavior-model.md#4-trace) | The concrete sequence of function invocations one entry state actually causes — not the abstract call graph. |
| [Change Request](design/design-assistant/datamodel/decision-model.md#4-change-request) | A request from one design target for a change to another's operations or behaviors, carrying a ticket ref. Deleted once satisfied — unlike a key decision it is not a permanent artefact. |
| [Chunk Scope](design-the-feature-process.md) | A design task's record of which behaviors it introduced, mutated or deleted; deferred out of the metamodel to the workflow that drives it. |
| [Condition Cell](design/design-assistant/datamodel/condition-model.md#4-condition-cells) | One concrete combination of condition dimension values, identified by a dotted-decimal id derived from value ordinals. |
| [Condition Dimension](design/design-assistant/datamodel/condition-model.md#2-condition-dimension) | One ranked axis of variation affecting what an operation does: payload, dependency state, parameter, or cross-cutting. |
| [Condition Space](design/design-assistant/datamodel/condition-model.md#1-condition-space) | The set of entry states one operation must be defined over; what coverage is asserted against. |
| [Condition Value](design/design-assistant/datamodel/condition-model.md#21-condition-values) | One discrete, ordinal-ranked value of a condition dimension. |
| [Cross-Cutting Boundary](design/design-assistant/datamodel/boundary-model.md#7-cross-cutting-boundaries) | A named association on a design target binding a set of NFR rules to a set of its functions; several of the same kind may coexist (`public.auth`, `public.2fa-auth`). |
| [Data Dictionary](design/design-assistant/datamodel/data-dictionary.md) | A design target's view over the types defined in its own scope; the schema of everything crossing a functional boundary. |
| [Data Type](design/design-assistant/datamodel/data-dictionary.md#2-data-type) | A scalar, enum, structure, collection or external shape, defined by exactly one boundary — design target or not. |
| [Deployable Boundary](design/design-assistant/datamodel/boundary-model.md#2-the-three-levels) | A Specifiable boundary that is additionally built, packaged, run and observed as a process. A Service is one. |
| [Derived](design/design-assistant/datamodel/DATA-MODEL.md#53-provenance) | Produced by reading other elements, and therefore carrying provenance. Contrasted with authored. |
| [Design Target](design/design-assistant/datamodel/boundary-model.md#3-design-targets) | A boundary designed in its own right — every SpecifiableBoundary. Owns its requirements, is mockable, bounds traces and bounds authority. |
| [Effect](design/design-assistant/datamodel/behavior-model.md#2-effects) | One observable consequence, in a shared vocabulary used by both required and expected effects. |
| [Endpoint](design/design-assistant/datamodel/deployable-model.md#4-endpoint) | A protocol-bound exposure of an operation on one perimeter vector; Deployable only. |
| [Endpoint Kind](design/design-assistant/datamodel/deployable-model.md#3-the-interface-perimeter) | The enumerated categories of endpoint a perimeter vector can carry; a closed list, so elicitation is a finite walk rather than an open question. |
| [Exemption](design/design-assistant/datamodel/boundary-model.md#73-assessment-or-exemption) | A design target's explicit declaration that no function of its own is on a given in-scope rule's boundary; required where the rule is not applied, and falsifiable later. |
| [Expected Effect](design/design-assistant/datamodel/behavior-model.md#22-expected-effects) | An effect derived by tracing the design; never authored directly. |
| [External Dependency (ED-NNN)](design-the-feature-process.md) | The current process's record of an out-of-process dependency and its thin shim; modelled as a `dependency`-kind boundary in the metamodel draft. |
| [ExternalRef](design/design-assistant/datamodel/DATA-MODEL.md#54-references-out) | An address plus a checksum standing in for a referenced document: enough to invalidate, not enough to interpret. |
| [Extraction](design/design-assistant/datamodel/boundary-model.md#31-promotion) | Taking a contained design target out of its container and publishing it as a standalone Library; containment becomes dependsOn and addresses re-root into the Library's namespace. |
| [Finding](design/design-assistant/datamodel/reconciliation-model.md#3-findings) | A detected violation, recorded against the element it is about, with the maturity level it blocks. |
| [Fixture](design/design-assistant/datamodel/behavior-model.md#3-fixtures) | The concrete state realizing a condition value: seed data, a stub, or a mock. |
| [Function](design/design-assistant/datamodel/function-and-call-graph.md#1-function) | The unit of a design's own logic, belonging to exactly one boundary — which may be a plain functional boundary, not only a design target. |
| [Function Catalog](design/design-assistant/datamodel/function-and-call-graph.md#7-the-function-catalog) | A flat, derived view of every function a design target owns — its subtree down to, but not into, contained design targets. |
| [Functional Boundary](design/design-assistant/datamodel/boundary-model.md#1-functionalboundary) | The root composite type. Holds its own functions, interfaces and data types, but nothing stating what is required of it. |
| [Gap Analysis](design-the-feature-process.md) | The current process's classification of each candidate function as as-is, extended or new. |
| [HLD](design-the-feature-process.md) | A design directory's High Level Design: scope, key decisions, data types, components and dependencies. |
| [Interface](design/design-assistant/datamodel/function-and-call-graph.md#3-interface) | A named grouping of a boundary's perimeter functions, belonging to that boundary; the unit a consumer depends on. |
| [Interface Perimeter](design/design-assistant/datamodel/deployable-model.md#3-the-interface-perimeter) | The five vectors through which anything crosses a running process's boundary. |
| [Internal Component (IC-NNN)](design-the-feature-process.md) | The current process's record of a component inside the service; modelled as a contained boundary in the metamodel draft. |
| [Invalidation](design/design-assistant/datamodel/reconciliation-model.md#4-invalidation) | The single rule that a change makes every derived element whose provenance names it stale. |
| [Key Decision](design/design-assistant/datamodel/decision-model.md#3-key-decision) | A recorded choice among candidates that closes an open design question and produces elements. |
| [Library](design/design-assistant/datamodel/boundary-model.md#2-the-three-levels) | A Specifiable boundary that is never deployed as a process. Not a degenerate Service. |
| [Manifest Setting](design/design-assistant/datamodel/boundary-model.md#33-build-manifest) | One named, enumerated fact in a build or runtime manifest; stated, inherited, or exempted with a reason, never blank. |
| [Maturity Level](design/design-assistant/datamodel/DATA-MODEL.md#52-maturity) | `M0`–`M5`: what a boundary has reached, and what each attribute becomes required by. |
| [Metric](design/design-assistant/datamodel/function-and-call-graph.md#6-metrics) | A measurement defined by the emitting function, carrying both `measures` (prose: what quantity) and `unit` (enum: in what units). |
| [Mock Consistency](design/design-assistant/datamodel/behavior-model.md#31-mock-consistency) | The check that a stub or mock standing in for a design target declares only results that target's own design actually produces. |
| [Namespace](design/design-assistant/datamodel/DATA-MODEL.md#511-namespaces) | An `ns/` address prefix naming an independently published design, so a library's own addresses are the same for every consumer. |
| [NFR Rule](design/design-assistant/datamodel/condition-model.md#5-nfr-rules) | A rule carried by a cross-cutting boundary that generates condition dimensions and required effects into an operation's space. |
| [NFR Rule Scope](design/design-assistant/datamodel/boundary-model.md#72-rules-are-inherited-selections-are-not) | The rules a design exists within, resolved by walking out to the owning Product. Rules inherit; which functions they govern never does. |
| [Open Design Question](design/design-assistant/datamodel/decision-model.md#2-open-design-question) | A known gap the design needs an answer to and does not have. |
| [OpenSLO](design/design-assistant/datamodel/deployable-model.md#52-slis) | The open specification an SLI definition must validate against; the model requires the validation and names the revision, and leaves the structure to the standard. |
| [Operation](design/design-assistant/datamodel/boundary-model.md#6-operation) | A point on a design target's perimeter at which it can be invoked from outside. Exists at Specifiable level, unlike an endpoint. |
| [Perimeter Vector](design/design-assistant/datamodel/deployable-model.md#3-the-interface-perimeter) | One of the five closed categories of process boundary crossing. |
| [Presence Dependency](design/design-assistant/datamodel/data-dictionary.md#3-fields-and-presence) | A field existing only when another field holds a particular value; what makes a structure a tree rather than a flat record. |
| [Promotion](design/design-assistant/datamodel/boundary-model.md#31-promotion) | Making a contained boundary its own design target, when repetition across consumers or dependency complexity warrants it; mechanically splits cross-cutting selections. |
| [Provenance](design/design-assistant/datamodel/reconciliation-model.md#2-provenance) | The addresses and checksums a derived element was derived from, plus when and by what. |
| [Provenance](design/design-assistant/datamodel/reconciliation-model.md#2-provenance) | What a derived element was derived from: every source address with a checksum of its content at the time, plus when and by what. |
| [Pruning](design/design-assistant/datamodel/condition-model.md#42-pruning) | Removing condition cells that cannot occur, by validity rule, by irrelevance under an ancestor, or by recorded architect exclusion. |
| [Reconciliation](design/design-assistant/datamodel/reconciliation-model.md) | The mechanisms making the verification claim falsifiable over time: provenance, findings, invalidation, and maturity gates. |
| [Required Effect](design/design-assistant/datamodel/behavior-model.md#21-required-effects) | An effect originating outside the design, from a use case step or an NFR rule. Authored, never derived. |
| [Review State](design/design-assistant/datamodel/reconciliation-model.md#61-state) | `pending`, `approved`, or `redesign-required`. Only a human enters `approved`. |
| [Runtime Manifest](design/design-assistant/datamodel/deployable-model.md#2-runtime-manifest) | The five structural dimensions an agent needs in order to assemble the codebase, as distinct from knowing what it must do. |
| [Satisfaction Check](design/design-assistant/datamodel/behavior-model.md#23-matching) | The subset check that every required effect has a corresponding expected effect. |
| [Service](design/design-assistant/datamodel/boundary-model.md#2-the-three-levels) | A Deployable boundary. |
| [Service Archetype](design/design-assistant/datamodel/deployable-model.md#51-archetype) | `request-response`, `batch` or `storage`; determines which SLI dimensions are required. |
| [SLI](design/design-assistant/datamodel/deployable-model.md#52-slis) | A Deployable boundary's measurement of one delivery dimension, defined as an OpenSLO `SLI` object (`openslo/v1`) and backed by metrics the design's own functions emit. |
| [SLO](design/design-assistant/datamodel/deployable-model.md#52-slis) | A product-level commitment about acceptable SLI values; deliberately outside this model. |
| [Sourcing](design/design-assistant/datamodel/decision-model.md#5-sourcing) | How an authored fact entered the model and who may change it: a document outside this design (change control), elicited, or inferred (the architect, directly). |
| [Specifiable Boundary](design/design-assistant/datamodel/boundary-model.md#3-design-targets) | A design target: designed in its own right. Owns its requirements, is mockable, bounds a trace and bounds authority. A Library is one. |
| [Specific Behavior (SB-NNN)](design-the-feature-process.md) | The current process's per-operation behavior document; modelled as behaviors on condition cells in the metamodel draft. |
| [Staleness](design/design-assistant/datamodel/reconciliation-model.md#2-provenance) | A derived element whose sources no longer checksum to what is recorded. A statement that it needs re-running, not an error. |
| [Technical Interpretation](design-the-feature-process.md) | The current process's solution-independent pseudocode restatement of a use case; superseded by required effects in the metamodel draft. |
| [Thin Shim](design/design-assistant/datamodel/boundary-model.md#52-dependson) | A dependency boundary's function, required to be a one-for-one translation of a depended-on operation. |
| [Trace](design/design-assistant/datamodel/behavior-model.md#4-trace) | The derivation record of a behavior: the walk producing its call tree and expected effects, with provenance. |
| [Trace Termination](design/design-assistant/datamodel/behavior-model.md#41-where-a-trace-stops) | A trace stops at contained design targets and dependency shims, taking their declared behavior via a fixture rather than walking inside. |
| [Unexpected External Side Effect](design/design-assistant/datamodel/behavior-model.md#23-matching) | An expected dependency interaction no required effect anticipates; the one finding that can send work back into analysis. |
| [Unparsed Document](design/design-assistant/datamodel/DATA-MODEL.md#11-applying-it-to-a-design-it-did-not-author) | A document in the design's scope whose contents have not been assessed for their contribution to the design. Not the same as having no frontmatter — an assessed document may correctly carry none. |
| [Validity Rule](design/design-assistant/datamodel/data-dictionary.md#4-validity-rules) | A solvable if/then/then-forbidden constraint over field combinations; what prunes a condition space. |
| [Visibility](design/design-assistant/datamodel/function-and-call-graph.md#11-visibility) | Whether a function is on its boundary's perimeter or private to it. |
