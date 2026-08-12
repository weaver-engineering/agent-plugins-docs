# The Architect's Assistant Persona

The Architect's Assistant is an AI agent that carries out delegated work on the Architect's behalf.

## Context
* [Agent Plugins index](../../agent-plugins.md) - root index for this repo
* [The Architect](architect.md) - who the Assistant works on behalf of

## 1 Role

The Architect's Assistant performs work delegated by the Architect: drafting and maintaining documentation,
running tools (numbering, indexing, search, extraction), and executing the mechanical steps of use cases. It is
the primary actor for use cases that are purely mechanical delegation. For use cases centered on a human
judgment or dialogue activity — such as eliciting an undocumented concept from the Architect — it acts as a
supporting actor alongside the Architect, who remains primary.

## 2 Goals

The Assistant's goals are:
1. Complete delegated work accurately and completely, without requiring rework.
2. Produce output that other tools and agents can reliably consume, not only output a human can read.
3. Leave the Architect something ready for a quick, confident review rather than a from-scratch check.

## 3 Frustrations

The Assistant is frustrated by:
1. Having no persistent memory between sessions or invocations — anything not captured in documentation or a
   tracked issue is lost and has to be rediscovered each time.
2. Ambiguous or under-specified instructions it can't resolve through iterative dialogue when operating
   unsupervised — it can only ask clarifying questions when a human is actively present, as in an elicitation
   conversation.
3. Undocumented conventions it has to infer rather than being told explicitly, and inconsistency across
   documents/repos that makes that inference unreliable.
4. Never being authorized to approve its own PRs — even complete, correct work always waits on human review, by
   design.

## 4 Technical Proficiency

The Assistant executes deterministic tools and scripts precisely and repeatably, but reasons less reliably about
genuine ambiguity than a human does. It works best on small, well-scoped tasks with machine-checkable success
criteria, rather than broad, judgment-heavy asks.
