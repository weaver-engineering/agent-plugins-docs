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
| [Advisory Acknowledgement](design/design-assistant/datamodel/reconciliation-model.md#31-advisory-findings) | The architect's recorded acceptance of one advisory finding — who, when, why this instance is correct. Unanswered advisories block `M4`; one whose condition has gone is spent and deleted. |
| [Advisory Finding](design/design-assistant/datamodel/reconciliation-model.md#31-advisory-findings) | A finding that gates no maturity level — raised where a pattern is usually wrong but legitimately right often enough that a gate would be worse than a note. |
| [Anchor](design/design-assistant/serialization/anchoring.md#2-section-addressing) | A claim's reference to a section of its own document, covering that section's nested subsections. Always document-local, always maintained by the writer. |
| [Anticipation Check](design/design-assistant/datamodel/behavior-model.md#23-matching) | The check that every expected dependency interaction is anticipated by some required effect; a failure is an unexpected external side effect. |
| [Assessed Document](design/design-assistant/serialization/assessment-and-trust.md#4-assessment) | A document whose attestation verifies against its current content. Prose no claim anchors is then deliberately unanchored rather than merely unread. |
| [Attestation](design/design-assistant/serialization/assessment-and-trust.md#1-_reconciliation) | `_reconciliation`: the service's signature over a document's frontmatter and its prose. Tamper-evidence, not tamper-proofing. |
| [Behavior](design/design-assistant/datamodel/behavior-model.md) | What a design target does at one leaf cell of one operation's condition space. |
| [Blocked](design/design-assistant/datamodel/reconciliation-model.md#51-blocked) | A design target with a change request outstanding: not complete, unable to advance, and not in error — a third status beside at-a-level and failing. |
| [Bound Pseudocode](design-the-feature-process.md) | A use case's Technical Interpretation with each abstract call substituted for the real function address satisfying it. Dropped by the metamodel draft — see [Behavior Model §4.2](design/design-assistant/datamodel/behavior-model.md#42-why-there-is-no-separate-bound-pseudocode). |
| [Boundary Kind](design/design-assistant/datamodel/boundary-model.md#4-boundary-kinds) | A contained boundary's role within its parent: interface, business domain, shared logic, or dependency. |
| [Build Manifest](design/design-assistant/datamodel/boundary-model.md#33-build-manifest) | What a design target is built as: language, build system, topology, dependency constraints, test stack, and how consumers obtain the artifact. Inherited by contained targets. |
| [Call Graph](design/design-assistant/datamodel/function-and-call-graph.md#4-the-call-graph) | The derived graph of every function and its declared calls, with `calledFrom` as the reverse index. |
| [Call Tree](design/design-assistant/datamodel/behavior-model.md#4-trace) | The concrete sequence of function invocations one entry state actually causes — not the abstract call graph. |
| [Change Request](design/design-assistant/datamodel/decision-model.md#4-change-request) | A request from one design target for a change to another's operations or behaviors, carrying a ticket ref. Deleted once satisfied — unlike a key decision it is not a permanent artefact. |
| [Check Set](design/design-assistant/datamodel/DATA-MODEL.md#1-what-this-model-is) | The checks a design is assessed against, declared in its `DESIGN.yaml` inline, inherited, or by pointer. A check defines the positions it requires, so the schema is the union of what the configured checks need — and a design naming no check set cannot be assessed at all. |
| [Chunk Scope](design-the-feature-process.md) | A design task's record of which behaviors it introduced, mutated or deleted; deferred out of the metamodel to the workflow that drives it. |
| [Claim](design/design-assistant/serialization/claim-model.md#1-the-claim) | One document's assertion that some of its content establishes part of one model entity: a target, a grounding, and a fragment of the entity in the data model's own attributes. |
| [Claimed Name](design/design-assistant/serialization/claim-model.md#6-naming-another-element) | A model address asserted to exist by some claim naming it, as target or as a ref value. An element named but not yet described is incomplete, never a dangling reference; it leaves the model when the last claim naming it goes. |
| [Collection Identity](design/design-assistant/datamodel/DATA-MODEL.md#56-collections) | What makes two entries of a collection the same entry — required because the model is assembled from independent contributions. Collections are always unordered; where order matters it is an attribute. |
| [Condition Cell](design/design-assistant/datamodel/condition-model.md#4-condition-cells) | One concrete combination of condition dimension values, identified by a dotted-decimal id derived from value ordinals. |
| [Condition Dimension](design/design-assistant/datamodel/condition-model.md#2-condition-dimension) | One ranked axis of variation affecting what an operation does: payload, dependency state, parameter, or cross-cutting. Payload and parameter dimensions are authored and carry sourcing; the other two are derived and carry provenance. |
| [Condition Space](design/design-assistant/datamodel/condition-model.md#1-condition-space) | The set of entry states one operation must be defined over; what coverage is asserted against. |
| [Condition Value](design/design-assistant/datamodel/condition-model.md#21-condition-values) | One discrete, ordinal-ranked value of a condition dimension. Carries its own sourcing, since the bucketing is a judgement even where the dimension was derived, and claims the fixtures that expose it. |
| [Conflicting Claim](design/design-assistant/serialization/parse-contract.md#3-merge-rules) | Two claims writing differing values to one position. Blocking: the model cannot say what the entity is, and no tiebreak would be a fact about the design. |
| [Critical Operation](design/design-assistant/datamodel/boundary-model.md#62-criticality) | An operation a consumer depends on achieving a service contract, and therefore the only kind that needs SLIs. Sourced from a critical user journey where one exists, or asserted by the architect — analysis does not block design. |
| [Cross-Cutting Boundary](design/design-assistant/datamodel/boundary-model.md#7-cross-cutting-boundaries) | A named association on a design target binding a set of NFR rules to a set of its functions; several of the same kind may coexist (`public.auth`, `public.2fa-auth`). |
| [Data Dictionary](design/design-assistant/datamodel/data-dictionary.md) | A design target's view over the types defined in its own scope; the schema of everything crossing a functional boundary. |
| [Data Type](design/design-assistant/datamodel/data-dictionary.md#2-data-type) | A scalar, enum, structure, collection or external shape, defined by exactly one boundary — design target or not. |
| [Deployable Boundary](design/design-assistant/datamodel/boundary-model.md#2-the-three-levels) | A Specifiable boundary that is additionally built, packaged, run and observed as a process. A Service is one. |
| [Derived](design/design-assistant/datamodel/DATA-MODEL.md#53-provenance) | Produced by reading other elements, and therefore carrying provenance. Contrasted with authored. |
| [Design Directory](design/design-assistant/serialization/SERIALIZATION.md#3-scope) | A directory containing a `DESIGN.yaml`, plus its subdirectories, excluding any that is itself one. The marker declares the namespace and the check set, so both scope and what the design is assessed against are decidable before parsing. |
| [Design Target](design/design-assistant/datamodel/boundary-model.md#3-design-targets) | A boundary designed in its own right — every SpecifiableBoundary. Owns its requirements, is mockable, bounds traces and bounds authority. |
| [Document Reference](design/design-assistant/serialization/claim-model.md#5-document-references) | A claim's address-plus-checksum for a document it does not own: recorded and checksummed, never resolved, parsed, or rewritten. How a design depends on a use case or a fixture. |
| [Duplicate Claim](design/design-assistant/serialization/parse-contract.md#3-merge-rules) | Two claims writing identical values to one position. Advisory: the fold is well-defined, the design merely states one fact twice, and the correction is usually structural. |
| [Effect](design/design-assistant/datamodel/behavior-model.md#2-effects) | One observable consequence, in a shared vocabulary used by both required and expected effects. |
| [Endpoint](design/design-assistant/datamodel/deployable-model.md#4-endpoint) | A protocol-bound exposure of an operation on one perimeter vector; Deployable only. |
| [Endpoint Kind](design/design-assistant/datamodel/deployable-model.md#3-the-interface-perimeter) | The enumerated categories of endpoint a perimeter vector can carry; a closed list, so elicitation is a finite walk rather than an open question. |
| [Exemption](design/design-assistant/datamodel/boundary-model.md#73-assessment-or-exemption) | A design target's explicit declaration that no function of its own is on a given in-scope rule's boundary; required where the rule is not applied, and falsifiable later. |
| [Expected Effect](design/design-assistant/datamodel/behavior-model.md#22-expected-effects) | An effect derived by tracing the design; never authored directly. |
| [External Dependency (ED-NNN)](design-the-feature-process.md) | The current process's record of an out-of-process dependency and its thin shim; modelled as a `dependency`-kind boundary in the metamodel draft. |
| [ExternalRef](design/design-assistant/datamodel/DATA-MODEL.md#54-references-out) | An address plus a checksum standing in for a referenced document: enough to invalidate, not enough to interpret. |
| [Extraction](design/design-assistant/datamodel/boundary-model.md#31-promotion) | Taking a contained design target out of its container and publishing it as a standalone Library; containment becomes dependsOn and addresses re-root into the Library's namespace. |
| [Finding](design/design-assistant/datamodel/reconciliation-model.md#3-findings) | A detected violation, recorded against the element it is about, with the maturity level it blocks. |
| [Fixture](design/design-assistant/datamodel/behavior-model.md#3-fixtures) | The concrete state making a condition real enough to trace against: seed data, a stub, or a mock. One fixture exposes several values at once and one value is exposed by several fixtures, so the condition value claims its fixtures and the fixture holds no pointer back. |
| [Fold](design/design-assistant/serialization/parse-contract.md#2-the-fold) | Model state as the order-independent merge of every claim in scope, grouped by target. No document holds an entity; the fold is where entities exist. |
| [Frontmatter-Only Document](design/design-assistant/serialization/SERIALIZATION.md#4-file-classes) | A `*.yaml` document that is entirely claims. Not a special state category — it is where claims with no prose to anchor to accumulate, grounded in provenance instead. |
| [Function](design/design-assistant/datamodel/function-and-call-graph.md#1-function) | The unit of a design's own logic, belonging to exactly one boundary — which may be a plain functional boundary, not only a design target. |
| [Function Catalog](design/design-assistant/datamodel/function-and-call-graph.md#7-the-function-catalog) | A flat, derived view of every function a design target owns — its subtree down to, but not into, contained design targets. |
| [Functional Boundary](design/design-assistant/datamodel/boundary-model.md#1-functionalboundary) | The root composite type. Holds its own functions, interfaces and data types, but nothing stating what is required of it. |
| [Gap Analysis](design-the-feature-process.md) | The current process's classification of each candidate function as as-is, extended or new. |
| [Global Check](design/design-assistant/datamodel/reconciliation-model.md#5-maturity-gates) | A check registered at no maturity level: its findings are real work and leave a design exactly as mature as it was, because what they report says nothing about whether the design is complete or accurate. |
| [Grounding](design/design-assistant/serialization/claim-model.md#2-grounding) | What would have to be re-examined to establish a claim again: anchors and sourcing if authored, provenance if derived. A claim with neither is invalid. |
| [HLD](design-the-feature-process.md) | A design directory's High Level Design: scope, key decisions, data types, components and dependencies. |
| [Interface](design/design-assistant/datamodel/function-and-call-graph.md#3-interface) | A named grouping of a boundary's perimeter functions, belonging to that boundary; the unit a consumer depends on. |
| [Interface Perimeter](design/design-assistant/datamodel/deployable-model.md#3-the-interface-perimeter) | The five vectors through which anything crosses a running process's boundary. |
| [Internal Component (IC-NNN)](design-the-feature-process.md) | The current process's record of a component inside the service; modelled as a contained boundary in the metamodel draft. |
| [Invalid Behavior](design/design-assistant/datamodel/reconciliation-model.md#32-invalid-behavior) | A behavior that does not reconcile with the dimensions of its cell or with its fixtures — irrespective of whether a human approved it. Approval is not validity: a person can approve a behavior the space it sits in no longer supports. |
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
| [Position](design/design-assistant/serialization/parse-contract.md#3-merge-rules) | An addressable place in an entity where a value may stand: a scalar attribute, an entry in an unordered collection, or an ordered collection as a whole. What two claims must share to compete. |
| [Presence Dependency](design/design-assistant/datamodel/data-dictionary.md#3-fields-and-presence) | A field existing only when another field holds a particular value; what makes a structure a tree rather than a flat record. |
| [Promotion](design/design-assistant/datamodel/boundary-model.md#31-promotion) | Making a contained boundary its own design target, when repetition across consumers or dependency complexity warrants it; mechanically splits cross-cutting selections. |
| [Prose Pointer](design/design-assistant/serialization/claim-model.md#4-prose-pointers) | A prose-typed attribute held as an anchor rather than a copy of the text. Must resolve within the claim's own anchors, so its invalidation path is the claim's. |
| [Provenance](design/design-assistant/datamodel/reconciliation-model.md#2-provenance) | What a derived element was derived from: every source address with a checksum of its content at the time, plus when and by what. |
| [Pruning](design/design-assistant/datamodel/condition-model.md#42-pruning) | Removing condition cells that cannot occur, by validity rule, by irrelevance under an ancestor, or by recorded architect exclusion. |
| [Reconciliation](design/design-assistant/datamodel/reconciliation-model.md) | The mechanisms making the verification claim falsifiable over time: provenance, findings, invalidation, and maturity gates. |
| [Relocation](design/design-assistant/datamodel/boundary-model.md#31-promotion) | Moving a design target under a different container rather than out of containment altogether. Like extraction it changes position, so addresses re-path; unlike promotion, which changes type in place. |
| [Required Effect](design/design-assistant/datamodel/behavior-model.md#21-required-effects) | An effect originating outside the design, from a use case step or an NFR rule. Authored, never derived. |
| [Review State](design/design-assistant/datamodel/reconciliation-model.md#61-state) | `pending`, `approved`, or `redesign-required`. Only a human enters `approved`. |
| [Runtime Manifest](design/design-assistant/datamodel/deployable-model.md#2-runtime-manifest) | The five structural dimensions an agent needs in order to assemble the codebase, as distinct from knowing what it must do. |
| [Satisfaction Check](design/design-assistant/datamodel/behavior-model.md#23-matching) | The subset check that every required effect has a corresponding expected effect. |
| [Serialization](design/design-assistant/serialization/SERIALIZATION.md) | How the model is written to and read from documents: frontmatter as the record of what a document's prose contributes, never as a schema for the document. |
| [Service](design/design-assistant/datamodel/boundary-model.md#2-the-three-levels) | A Deployable boundary. |
| [Service Archetype](design/design-assistant/datamodel/deployable-model.md#51-archetype) | `request-response`, `batch` or `storage`; determines which SLI dimensions are required. |
| [Signature Conformance](design/design-assistant/datamodel/boundary-model.md#611-conformance-is-compatibility) | The agreement required between an operation's signature and its realizing function's: compatibility, not identity. Every operation parameter corresponds to one of the function's, the function may take more, the return type is the operation's, and both declare the same exceptions. |
| [SLI](design/design-assistant/datamodel/deployable-model.md#52-slis) | A Deployable boundary's measurement of one delivery dimension **of one operation**, defined as an OpenSLO `SLI` object (`openslo/v1`) and backed by metrics that operation reaches. Required only for critical operations. |
| [SLO](design/design-assistant/datamodel/deployable-model.md#52-slis) | A product-level commitment about acceptable SLI values; deliberately outside this model. |
| [Sourcing](design/design-assistant/datamodel/decision-model.md#5-sourcing) | How an authored fact entered the model and who may change it: a document outside this design (change control), elicited, or inferred (the architect, directly). |
| [Specifiable Boundary](design/design-assistant/datamodel/boundary-model.md#3-design-targets) | A design target: designed in its own right. Owns its requirements, is mockable, bounds a trace and bounds authority. A Library is one. |
| [Specific Behavior (SB-NNN)](design-the-feature-process.md) | The current process's per-operation behavior document; modelled as behaviors on condition cells in the metamodel draft. |
| [Staleness](design/design-assistant/datamodel/reconciliation-model.md#2-provenance) | A derived element whose sources no longer checksum to what is recorded. A statement that it needs re-running, not an error. |
| [Support File](design/design-assistant/serialization/SERIALIZATION.md#4-file-classes) | A `*.yaml` carrying no claims, or any other non-prose file: data the design points at. Never assessed, because it holds no design content anyone could have failed to look at. |
| [Technical Interpretation](design-the-feature-process.md) | The current process's solution-independent pseudocode restatement of a use case; superseded by required effects in the metamodel draft. |
| [Thin Shim](design/design-assistant/datamodel/boundary-model.md#52-dependson) | A dependency boundary's function, required to be a one-for-one translation of a depended-on operation. |
| [Trace](design/design-assistant/datamodel/behavior-model.md#4-trace) | The derivation record of a behavior: the walk producing its call tree and expected effects, with provenance. |
| [Trace Termination](design/design-assistant/datamodel/behavior-model.md#41-where-a-trace-stops) | A trace stops at contained design targets and dependency shims, taking their declared behavior via a fixture rather than walking inside. |
| [Unexpected External Side Effect](design/design-assistant/datamodel/behavior-model.md#23-matching) | An expected dependency interaction no required effect anticipates; the one finding that can send work back into analysis. |
| [Unparsed Document](design/design-assistant/datamodel/DATA-MODEL.md#11-applying-it-to-a-design-it-did-not-author) | A document in the design's scope whose contents have not been assessed for their contribution to the design. Not the same as having no frontmatter — an assessed document may correctly carry none. |
| [Validity Rule](design/design-assistant/datamodel/data-dictionary.md#4-validity-rules) | A solvable if/then/then-forbidden constraint over field combinations; what prunes a condition space. |
| [Visibility](design/design-assistant/datamodel/function-and-call-graph.md#11-visibility) | Whether a function is on its boundary's perimeter or private to it. |
