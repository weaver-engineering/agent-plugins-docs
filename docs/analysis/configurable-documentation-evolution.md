# Configurable Documentation Evolution

What the process behind the design assistant actually is, and why it is configurable rather than fixed. The five
issues that built it — the functional-boundary spine
([WVR-181](https://linear.app/weaver-engineering/issue/WVR-181)), the service metamodel
([WVR-182](https://linear.app/weaver-engineering/issue/WVR-182)), the frontmatter schema and parse contract
([WVR-183](https://linear.app/weaver-engineering/issue/WVR-183)), the design layout standard
([WVR-184](https://linear.app/weaver-engineering/issue/WVR-184)) and the workflow itself
([WVR-185](https://linear.app/weaver-engineering/issue/WVR-185)) — assumed throughout that it would be
configurable, and none of them argued the point. This is the argument.

## Context
* [Agent Plugins index](../agent-plugins.md) - root index for this repo
* [evolve-a-design-to-maturity](use-cases/evolve-a-design-to-maturity/USE-CASE.md) - the use case this process
  serves, written for its first configuration
* [find-and-read-documentation](use-cases/find-and-read-documentation/USE-CASE.md) - the registry §3.3 says the
  enterprise case takes with it, and the open question about where it lives
* [Architecture Definition Document](../architecture/architecture-definition-document.md) - what AgentPlugins
  itself delivers: canonical sub-agents, skills and tools, published per platform
* [Data Model §1.2](../design/design-assistant/datamodel/DATA-MODEL.md) - what no configuration can change, and
  the document evolution loop
* [Design A Specifiable Boundary](../design/design-assistant/workflow/WORKFLOW.md) - the default configuration,
  and the check interface §3.1 argues is a product surface
* [Glossary](../glossary.md) - Check Set, Finding, Resolution, Maturity Level, Next Unit Of Work

## 1 What The Process Is

It is a **documentation evolution process**: a loop that assesses a body of documentation against a set of
checks, reports what it finds along with the resolutions available for each finding, and applies the one its
user chooses — then assesses again, against what the documentation now says.

The design assistant's check set is **one configuration** of that process, not the process itself. It supplies
checks about boundaries, operations, condition spaces and behaviors, and resolutions that write those things
down. A different configuration supplies different checks and different resolutions, and the loop is unchanged.

This is visible in the primary use case rather than merely asserted about it. Nothing in
[evolve-a-design-to-maturity](use-cases/evolve-a-design-to-maturity/USE-CASE.md)'s scenario names design
content: its steps are findings, resolutions, checks, levels and addresses throughout. It is written for the
first configuration, and it would serve any of them — which is the clearest evidence available that the loop
and the design assistant are two things.

### 1.1 AgentPlugins Is Its Genesis, Not Its Identity

**AgentPlugins is not this process.** AgentPlugins is canonically defined plugins — sub-agents, skills and
tools — authored once and delivered as a product offering per platform: Claude Code, Codex, OpenCode, and
others as they matter ([Architecture Definition Document](../architecture/architecture-definition-document.md)
§1–§3).

Within that, the **design assistant is one sub-agent**, and its tool is a configured check set and the next
unit of work detector that runs it. That is the whole of the relationship: a plugin catalogue contains a
sub-agent, and that sub-agent has a tool.

The process that tool generalises to is **a product in its own right**, and everything below is about that
product rather than about AgentPlugins. AgentPlugins is where it started — the design assistant is the reason
the loop was built at all, and the first configuration is the one that sub-agent needs. Genesis is not
identity: a plugin catalogue that also happened to produce a documentation evolution product is two products,
and describing AgentPlugins as the second would misstate both.

## 2 Why It Is Configurable

### 2.1 Falsifiability Requires The Check Set To Be Named

The claim the product exists to make is that a body of documentation is complete, consistent, and sufficient
for what happens next. That claim is only decidable relative to what was actually checked: two designs both at
`M4` under different check sets are not asserting the same thing
([Data Model](../design/design-assistant/datamodel/DATA-MODEL.md) §3).

So the check set has to be **named as part of the claim** for the claim to be falsifiable at all. The
alternative is an absolute-sounding assertion whose real content nobody can recover. And once the set must be
stated, it is data — a design that does not say what it is checked against cannot be assessed, which is a
failure rather than a default. Configurability is not a feature added on top of the process; it is what follows
from making the process's own claim checkable.

### 2.2 An Opinion Has To Be Legible To Be Disagreed With

The default check set is an opinion: this is what we currently think "complete enough to build from" means.
Holding an opinion is correct — a mechanism with no default is a mechanism nobody can use — and so is expecting
others to disagree with it.

Built into the model, the opinion is unreachable: disagreeing means forking the schema, and the disagreement
shows up as a divergent product rather than as a stated difference. Held as configuration, a project reads
exactly what it is being assessed against and changes that, and two projects' differing standards remain
comparable because both are written down in the same terms.

### 2.3 The Thing Being Evolved Need Not Be A Design

No element type belongs to the process. Boundary, operation, condition space, behavior — all of them are one
configuration's content ([Data Model](../design/design-assistant/datamodel/DATA-MODEL.md) §1.2), and a process
configured for something else would have none of them. What remains under every configuration is the loop, the
finding, the resolution, the maturity gate and the addressing.

The configurations in prospect are not hypothetical variants of design:

| Configuration | Evolves |
|---|---|
| **Evolve Analysis** | use cases and user personas — the corpus this very document belongs to |
| **Evolve System Architecture** | how a product's services connect, and what crosses between them |
| **Evolve Product Offering** | how a service is actually delivered for consumption |
| **Evolve Statement Of Work** | what has been committed to, for whom, by when |
| **Evolve Product** | the product definition itself: what it is, who it serves, what it claims |
| **Evolve Chaos Engineering** | what failure modes have been hypothesised, injected and survived |
| **Evolve Observability** | what is instrumented, what is inferable from it, and what is not |

Each is the same loop against a different corpus with different checks. Several of them assess documents this
process would itself produce, which is what makes the set coherent rather than a list of adjacent ideas: an
organisation that adopts one has a reason to adopt the next.

### 2.4 Fifty-Five Checks Cannot Ship At Once

A process defined as a numbered sequence of phases has to be built roughly in full before it is useful, because
the sequence is the product. A process defined as a configuration is useful at check one: the first serving is
a configuration plus a single check, and each further check is bottomed out as it is reached rather than
specified in advance.

Configurability is therefore a delivery mechanism and not only an extension mechanism. It is what makes this
product incrementally shippable, and it is why the design assistant can dog-food itself before it is finished.

## 3 What Follows From It

### 3.1 The Check Is A Product Surface

If a consumer supplies its own checks, then the check interface is not an internal detail — it is where the
product is extended, and therefore where it is bought into. What a check declares, and what it returns, is
consumed by people who did not write this product.

Two consequences worth stating now, while the interface is still cheap to get right:

* **A check need not be ours.** A third party writes a check, registers it in a configuration, and the process
  runs it. This is the shape a marketplace for checks would take, and it is reachable from where the design
  already is rather than requiring a different architecture to get to.
* **A check need not use an LLM, or ours.** A check is a question asked of a corpus; nothing about it requires
  a model. Some checks are pure computation, some want a model, and a consumer that brings its own model — its
  own key, its own vendor, its own locally hosted weights — is running the same process.

### 3.2 An Organisation's Claims Become Self-Falsifying

Today a document outside a design's scope is an address and a checksum, referenced and never parsed
([Data Model](../design/design-assistant/datamodel/DATA-MODEL.md) §5.4), and a design target's traces stop at
the targets it contains, taking each at its declared behavior. What keeps that honest inside one design is the
mock consistency check: a fixture standing in for a design target must agree with what that target's own design
produces.

Recorded across an organisation, that check reaches across teams. If a related design's claims are available
and its maturity mechanically assertable, then one team's *use* of another team's boundary stops being an
assumption documented in prose and becomes something the process asserts: the boundary is at the level its kind
requires, and what we mocked of it is what it actually says it does. Designs spanning repositories, teams and
storage solutions become self-falsifying — the contradiction surfaces as a finding rather than as an incident.

This is the enterprise case, and the storage question follows from it rather than defining it: claims spanning
an organisation are not files in one directory, and where they live is a real decision
([find-and-read-documentation](use-cases/find-and-read-documentation/USE-CASE.md) §7) rather than an
implementation detail of this product.

### 3.3 The Enterprise Case Takes Retrieval With It

The process reaches its corpus through indexation and retrieval — register what exists, find what is relevant,
fetch it with enough context to use it. That is the same capability doc search provides, and locally it is
literally the same thing: the tool the agent uses to read the corpus it is evolving is the local index and
retrieval, shared with the doc search tool.

So §3.2's storage question is not one decision. An organisation's claims held in a shared store are only worth
holding there if they can be reached: the enterprise variant needs an **enterprise variant of doc search** over
the same corpus, and choosing where claims live without choosing how they are retrieved settles half a problem.
The two move together.

## 4 What This Does Not Settle

* **Which configurations get written, and in what order.** §2.3 names those in prospect; nothing here commits
  to any of them, and each would need its own analysis before it is more than a name.
* **What a marketplace actually is** — distribution, trust, versioning, what a check is allowed to do when it
  runs. §3.1 argues only that the check interface is a product surface, which is a constraint on how carefully
  it is designed rather than a plan.
* **When the evolution product separates from AgentPlugins, and what that costs.** §1.1 says the two are
  different products; it does not say they get different repositories, different docs, or different release
  cycles, and today they have none of those. The trigger for separating is a second consumer that is not a
  plugin, and nothing here decides what happens at that point.
* **Whether the design assistant's own configuration is the right default.** It is this product's opinion,
  which §2.2 says should be legible and replaceable — not that it is correct.

# Rationale

**Why this is stated in analysis rather than left in the design's rationale.** `WORKFLOW.md` and `DATA-MODEL.md`
each already argue parts of this, and both argue them from inside the design — as justification for why the
workflow is data rather than procedure. That leaves the reasoning available only to a reader who has already
accepted the design, and it leaves the product's own shape undocumented: that the design assistant is one
configuration is a fact about *what is being built*, not about how the workflow is structured. A reader should
be able to answer "why is this configurable" without reading a design document, which is what makes it an
analysis question.

**Why the legs are stated as four arguments rather than one.** They are independently sufficient and they fail
independently. Falsifiability (§2.1) would require a named check set even if there were only ever one
configuration. Deliverability (§2.4) would matter even if the opinion were uncontested. The multiple-corpus
argument (§2.3) is the most exciting and the least load-bearing: it is the only one that depends on something
not yet built. Presenting them as a single case would let the whole thing look speculative, when three quarters
of it holds for the product exactly as it stands today.
