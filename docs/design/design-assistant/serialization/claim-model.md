# Claim Model

## Context
* [Serialization](SERIALIZATION.md) - what frontmatter is for, and the scope and file classes it operates over
* [Anchoring](anchoring.md) - how `_anchors` addresses prose, and how references differ from anchors
* [Parse Contract](parse-contract.md) - how claims fold into entities, and what happens when two compete
* [Data Model](../datamodel/DATA-MODEL.md) - the entities and attributes a claim's body is written in
* [Decision Model](../datamodel/decision-model.md) - `Sourcing`, carried by every authored claim
* [Reconciliation Model](../datamodel/reconciliation-model.md) - `Provenance`, carried by every derived claim

## 1 The Claim

A **claim** asserts that something in this document establishes some part of one model entity.

```yaml
_claims:
  - _target: bnd/order-service/op/create-order
    _anchors:
      "§2.1": "sha256:8f3a…"
    _sourcing: {kind: elicited, basis: "§2.1"}
    name: Create Order
    purpose: §2.1
    signature:
      parameters:
        - {name: order, type: type/order}
```

`_target` is a model address ([Data Model](../datamodel/DATA-MODEL.md) §5.1). Everything else divides in two:

* keys beginning `_` are **serialization's own**, defined in this document;
* every other key is an **attribute of the targeted entity**, spelled exactly as the data model spells it, at
  whatever depth the data model puts it.

The body is not a description of the entity in some serialization dialect. It is a fragment of the entity
itself. A claim contributing an operation's SLIs contains an `slis:` key holding SLIs; a claim contributing its
whole definition contains every attribute. There is no translation layer, and therefore nothing that can drift
out of step with the data model as it changes.

The `_` prefix is reserved. No model attribute may be named with a leading underscore, which is what keeps
serialization's keys and the model's keys from ever colliding.

## 2 Grounding

Every claim must be **grounded**: it must say what would have to be re-examined to establish it again. There
are exactly two grounds, and they correspond to the model's own split between authored and derived facts
([Reconciliation Model](../datamodel/reconciliation-model.md) §2).

| Claim | Carries | Re-derivable from |
|---|---|---|
| Authored | `_anchors`, `_sourcing` | the prose at its anchors |
| Derived | `_provenance` | re-running the derivation against the design |

`_anchors` maps each anchor to a digest of the prose it resolves to ([Anchoring](anchoring.md) §3).
`_sourcing` is the model's `Sourcing` ([Decision Model](../datamodel/decision-model.md) §5): how the fact
entered the model and who may change it. `_provenance` is the model's `Provenance`
([Reconciliation Model](../datamodel/reconciliation-model.md) §2): every source address with a checksum of its
content at the time, plus when and by what.

**A claim with neither grounding is invalid.** It asserts a fact that nothing establishes and that nothing can
re-establish — it cannot be checked, cannot be invalidated, and cannot be re-judged. This is the rule that makes
"the whole frontmatter is re-derivable" true without exception: authored claims re-derive from prose, derived
claims re-derive from the design, and there is no third kind that re-derives from nothing.

An authored claim in a prose document must anchor within that document
([Anchoring](anchoring.md) §1). A derived claim has no prose to anchor to, which is the entire reason
frontmatter-only documents exist ([Serialization](SERIALIZATION.md) §4).

## 3 Fragments

A claim may carry a whole entity or any part of one, to any depth. The entity is the merge of every claim
naming it, wherever those claims live ([Parse Contract](parse-contract.md) §2).

**A claim's extent is the extent of one act of attribution, not of one model element.** Claims are split where
different prose establishes different parts, and not otherwise:

* one section establishing an entire operation is **one** claim;
* a section establishing its purpose and a later section establishing its SLIs are **two** claims, each
  anchored to its own section;
* two sections that jointly establish one attribute are **one** claim with two anchors.

The shape of a document's frontmatter is therefore dictated by how that document is organised — which is
correct for something whose job is to index prose, and is what keeps the frontmatter proportionate to the
document rather than to the model.

## 4 Prose Pointers

Where an attribute's type is prose — `Prose`, `Description`, a `basis` — the claim may hold an anchor in place
of a copy of the text:

```yaml
purpose: §2.1
```

The value is then the prose at that anchor. Nothing is duplicated, and re-derivation is trivial because the
value *is* the source.

**A prose pointer must resolve within the claim's own anchors** — either an anchor itself, or a section nested
inside one ([Anchoring](anchoring.md) §2). A claim may not point at prose it has not anchored, because the
anchor digests are what detect that the prose moved; a pointer outside them would be a value with no
invalidation path.

## 5 Document References

A claim may **reference a document** it does not parse: a fixture, a use case, a document supporting the design.
A reference is an address and a checksum of the referenced content, recorded as provenance
([Data Model](../datamodel/DATA-MODEL.md) §5.4).

References are not anchors, and the distinction is load-bearing
([Anchoring](anchoring.md) §5). An anchor is resolved to a span, digested, and re-anchored mechanically when
the document is restructured. A reference is recorded and checksummed and never resolved, never parsed, never
rewritten. That is what lets a design depend on a use case without owning it: a change to the referenced
content moves its checksum, invalidating the claim and requiring re-judgement, without the referenced document
ever being read into the model.

A reference is how an out-of-scope file participates in the design ([Serialization](SERIALIZATION.md) §3). The
design points at the fixture; whatever the design needs to know about it is stated in the claim doing the
pointing.

## 6 Naming Another Element

A ref-valued attribute — `calls: [fn/validate-order]`, `type: type/order` — names an element of the **model**,
not a document, and behaves nothing like §5's document reference. It is not checksummed, because the model is
not a document; and it is rewritten mechanically when the element it names is re-addressed
([Write Contract](write-contract.md) §4), which a document reference never is.

**Naming an address asserts that it exists.** That is true of `_target` and of every ref-valued attribute
alike: an address is in the model exactly when some claim names it. There is no separate act of bringing an
element into existence for a reference to then point at, so **a reference cannot dangle** — and there is no
finding for one, because the condition it would report cannot arise.

What an element named only by references has is existence and nothing else. Everything else about it comes from
claims targeting it, and until some claim does, it is simply incomplete — which the maturity checkpoints
already report as work to do ([Data Model](../datamodel/DATA-MODEL.md) §5.2), in the same way as any other
element that has been identified and not yet filled in. A design's floor is an element with an identity and
nothing more, and arriving at one by being named is not a different state from arriving at one any other way.

An address therefore leaves the model only when the **last claim naming it** goes — by the claim being removed,
or by the document carrying it being deleted ([Parse Contract](parse-contract.md) §6.1). While the prose
authoring a claim stands, the claim stands, and so does every name it asserts.

# Rationale

**Why the claim body is the model's own attributes rather than attribute/value pairs.** An earlier form gave
each claim a single `attribute` and `value`, with target, anchors, digest and sourcing repeated around every
one. It is correct and unusable: the data model is large, so a document establishing one entity produces dozens
of near-identical blocks, and the frontmatter swamps the prose it is supposed to index. Carrying model
fragments instead makes the repeated part appear once per act of attribution rather than once per attribute,
and removes the dialect that would otherwise have to be kept in step with the data model.

**Why grounding is required rather than encouraged.** An ungrounded claim is indistinguishable from a fact
somebody typed into the frontmatter by hand — which is exactly the thing this scheme refuses to trust
([Assessment And Trust](assessment-and-trust.md) §3). Requiring grounding at the schema level means the
question "what would I have to look at to check this" always has an answer, and means invalidation is total:
there is no category of fact that quietly never goes stale.

**Why prose pointers are restricted to the claim's own anchors.** The alternative is a value pointing at prose
whose digest nothing records, which would go stale silently — the one failure mode this entire mechanism exists
to prevent. Restricting pointers inward makes the anchor set the complete statement of what the claim depends
on, so a claim's freshness is decidable from the claim alone.

**Why references are checksummed but never resolved.** The design assistant must detect that a use case
changed, because that invalidates what relies on it. It must not own use cases, which belong to Analysis and
are edited on their own terms. Recording an address and a checksum gives exactly the first property and none
of the second — and keeps every anchor document-local, so restructuring one document can never require
rewriting another.

**Why naming an element is enough to bring it into existence.** The alternative treats definition and reference
as different acts, which immediately needs a rule for a reference to something never defined — a dangling-ref
finding, and with it a question about what the model holds in the meantime. Making existence follow from being
named removes the category: an element referred to and not yet described is not an error, it is an element with
one attribute, and the checkpoints already know how to report an element that is missing the rest. It also
makes deletion consistent with everything else here, since a name goes when the last claim naming it goes,
exactly as an attribute goes when the last claim stating it goes.

**Why this makes a missed rename loud rather than silent.** Re-addressing must rewrite every claim naming the
moved element ([Write Contract](write-contract.md) §4), and missing one is the obvious way to get it wrong.
Under a dangling-reference model the leftover claim points at nothing, which is detectable only if something
goes looking. Under this one it asserts the old address still exists, so the old element survives with almost
no attributes and surfaces as conspicuously unfinished work. The mistake is the same; what differs is that the
model reports it without being asked.
