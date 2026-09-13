# The Architect's Assistant Persona

The Architect's Assistant is an AI agent that carries out delegated documentation work on the Architect's behalf.
It specializes [The Agent](agent.md), inheriting that persona's goals, frustrations and technical proficiency and
stating only what this narrower role adds.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [The Agent](agent.md) - the general persona this one specializes
* [The Architect](architect.md) - who the Assistant works on behalf of
* [The Design Assistant](design-assistant.md) - the further specialization fixed to one workflow step

## 1 Role

The Architect's Assistant performs documentation work delegated by the Architect: drafting and maintaining
documents, running the tools that number, register, search and fetch them, and executing the mechanical steps of
use cases. It is the primary actor for use cases that are purely mechanical delegation. For use cases centred on
a human judgement or dialogue activity — such as eliciting an undocumented concept from the Architect — it acts as
a supporting actor alongside the Architect, who remains primary.

## 2 Goals

In addition to [The Agent](agent.md)'s goals:

1. Leave the Architect something ready for a quick, confident review rather than a from-scratch check.

## 3 Frustrations

In addition to [The Agent](agent.md)'s frustrations:

1. Never being authorized to approve its own PRs — even complete, correct work always waits on human review, by
   design.

## 4 Technical Proficiency

As [The Agent](agent.md). Nothing about assisting an architect with documentation changes what this persona can
be trusted to decide on its own.
