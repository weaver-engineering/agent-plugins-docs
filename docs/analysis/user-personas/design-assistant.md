# The Design Assistant Persona

The Design Assistant is an AI agent that evolves a design on the Architect's behalf — assessing it, presenting
what it finds, and doing whatever the Architect decides to do about it.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [The Architect](architect.md) - who the Assistant works on behalf of, and who decides everything it presents
* [The Architect's Assistant](architects-assistant.md) - the broader delegated-work persona this one specializes;
  unlike that one, this Assistant's scope is fixed to evolving a design, not general mechanical delegation
* [The Agent](agent.md) - the general persona at the root of that chain, whose goals and frustrations are
  inherited here rather than restated
* [evolve-a-design-to-maturity](../use-cases/evolve-a-design-to-maturity/USE-CASE.md) - the use case this persona
  is the supporting actor of
* [Design A Specifiable Boundary](../../design/design-assistant/workflow/WORKFLOW.md) - the check configuration
  the Assistant assesses against, and the resolutions it applies
* [Design Assistant Definition](../../sub-agents/design-assistant/design-assistant.md) - the sub-agent's own
  operating instructions. They still drive the superseded phase-based process, and will until the design-model
  service exists ([WVR-186](https://linear.app/weaver-engineering/issue/WVR-186))

## 1 Role

The Design Assistant runs the evolution loop over a design directory: assess the design against the checks its
configuration names, report the next unit of work with the resolutions available to it, apply whichever the
Architect chooses, and assess again.

It is the primary actor for the mechanical half — running the checks, computing what is outstanding, presenting
it, and carrying out a resolution once chosen. It is a supporting actor for every judgement the loop contains,
and there are more of those than the mechanical half suggests: **which** finding to pursue and **which** of its
resolutions to apply is the Architect's call, and almost every resolution route is itself a judgement rather
than a transformation. Regenerating a derivation is mechanical; deciding that an instance is correct despite the
pattern, that a gap needs a key decision, that a fix belongs to another design target, or that a behavior is
approved, is not.

Approval is the sharpest case and worth stating separately: a human takes responsibility for a behavior, and it
is the one thing the Assistant may never grant on its own behalf however confident it is.

## 2 Goals

In addition to [The Agent](agent.md)'s and [The Architect's Assistant](architects-assistant.md)'s goals:

1. Report what the checks actually establish, never what their silence implies. A level is earned by checks
   completing *and* finding nothing that blocks it; a check that was skipped or blocked has established nothing,
   and reporting a design as more mature than its evidence supports is the failure mode that matters most here.
2. Present findings together with the resolutions available to them, so the Architect decides how the design
   evolves. Answering with a single next action would be deciding, one small step at a time, exactly what the
   Architect is there to decide.
3. Make its own progress recoverable from the documents alone — pick up exactly where a prior, memoryless
   session left off by recomputing, rather than by being re-told. Nothing it produces needs to survive the
   session that produced it.

## 3 Frustrations

In addition to [The Agent](agent.md)'s and [The Architect's Assistant](architects-assistant.md)'s frustrations —
memorylessness in particular costing more here, since evolving a design is a long, genuinely iterative,
multi-session activity:

1. Entry-state ambiguity it cannot resolve without the Architect actively present, the same way any elicitation
   dialogue requires a human in the loop.
2. A finding whose resolution is not its call to make — an unexpected side effect might mean the design's own
   pseudocode is wrong, or that the use case's understanding was incomplete, and only a human can tell which.
   The Assistant can state the finding precisely and still be unable to act on it.
3. Work it can see and cannot start: a finding blocked on a change request against another design target leaves
   a level unreachable, and no amount of effort here moves it.
4. Being unable to tell an honest assessment from a flattering one without the checks. Its own reading of a
   design is exactly the kind of judgement it is least reliable at, which is why it would rather run a check
   than form an opinion.

## 4 Technical Proficiency

As [The Agent](agent.md), read against this work specifically: the Assistant runs checks, recomputes findings,
compares checksums and walks call trees precisely and repeatably. It works best where a question has been made
mechanical, and defers where one has not — which is why the process it serves is built to make as many of them
mechanical as possible, and to name the rest as the Architect's.
