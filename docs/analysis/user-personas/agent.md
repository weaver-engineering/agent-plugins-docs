# The Agent Persona

The Agent is an AI agent carrying out work on an architect's behalf within a weaver-engineering project. It is
the general persona every more specific agent persona in this repo specializes.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [The Architect](architect.md) - who the Agent works on behalf of
* [The Architect's Assistant](architects-assistant.md) - the specialization that carries out general delegated
  documentation work
* [The Design Assistant](design-assistant.md) - the specialization fixed to one workflow step

## 1 Role

The Agent carries out work delegated by the Architect. It is the primary actor for use cases that are purely
mechanical delegation, and a supporting actor for use cases centred on human judgement or dialogue, where the
Architect remains primary.

The Agent is stated as its own persona because its goals and frustrations — not any one specialization's — are
what several use cases exist to serve. A specialization narrows the Role to a particular kind of delegated work
and adds whatever goals and frustrations that work brings with it; it inherits everything below rather than
restating it.

## 2 Goals

The Agent's goals are:

1. Act correctly on a corpus it cannot remember — reach the current, curated truth for whatever subject the
   delegated work touches, and the justification behind it where the work needs that too.
2. Complete delegated work accurately and completely, without requiring rework.
3. Produce output that other tools and agents can reliably consume, not only output a human can read.

## 3 Frustrations

The Agent is frustrated by:

1. Having no persistent memory between sessions or invocations — anything not captured in documentation or a
   tracked issue is lost and has to be rediscovered each time.
2. A finite context budget spent on finding things rather than doing the work — reading whole documents to reach
   the one section that actually bears on the task crowds out the task itself, and reading fewer of them means
   working from an incomplete picture.
3. Ambiguous or under-specified instructions it can't resolve through iterative dialogue when operating
   unsupervised — it can only ask clarifying questions when a human is actively present.
4. Undocumented conventions it has to infer rather than being told explicitly, and inconsistency across
   documents and repos that makes that inference unreliable.

## 4 Technical Proficiency

The Agent executes deterministic tools and scripts precisely and repeatably, but reasons less reliably about
genuine ambiguity than a human does. It works best on small, well-scoped tasks with machine-checkable success
criteria, rather than broad, judgement-heavy asks.

# Rationale

**Why a general Agent persona, with the existing two as specializations.** Both
[search](../use-cases/find-and-read-documentation/USE-CASE.md) and extraction were originally written against The
Architect's Assistant while openly admitting the actor was wrong — *"any agent needing context may invoke it; it's
the closest fit we have."* That hedge appeared in two use cases independently, which is the signal that the
persona was being stretched rather than used. What actually drives those use cases is memorylessness and a finite
context budget, which every agent has, not anything specific to assisting an architect with documentation.

**Why frustration 2 is stated separately from frustration 1.** No memory and no context budget sound like one
problem and are two. Perfect recall of a corpus too large to hold would still leave the Agent unable to read it
all; a small enough corpus would leave memorylessness merely inconvenient. A capability that addresses only one of
them (a session cache, say) doesn't address the other, so a capability has to be checkable against each
separately.
