# WVR-171 — MCP Server/Tool Scoping in Claude Code, and How Agents Get Human Input

Free-form, `notes/` — not a spec, not indexed, not reviewed for correctness. Research findings for
[WVR-171](https://linear.app/weaver-engineering/issue/WVR-171/restrict-agents-to-subset-of-all-available-mcp-servers-in-claude-code)
(a pure-research ticket — see its own description for why), feeding
[WVR-94](https://linear.app/weaver-engineering/issue/WVR-94/document-cross-platform-capability-parity-mechanics)'s
canonical agent/MCP-server/tool availability matrix (Claude Code / Codex / OpenCode) and
[WVR-173](https://linear.app/weaver-engineering/issue/WVR-173/redesign-agentplugins-design-skills-around-prose-as-source-regenerable)'s
redesign of the design-assistant-family skills. Covers Claude Code only — Codex is
[WVR-172](https://linear.app/weaver-engineering/issue/WVR-172/reastrict-agent-to-subset-of-all-available-mcp-servers-in-codex)'s
job, OpenCode's mechanism was already solved separately (see WVR-171's own Context).

Verified against Claude Code's own docs (`code.claude.com/docs/en/{sub-agents,mcp,settings,settings-reference,
permissions,cli-reference,hooks}`) and the MCP protocol spec, current as of 2026-08-25, plus one empirical test
run in this session. Citations are inline; anything not directly confirmed is flagged as an inference.

## 1. Two structural levels, not one

Everything below sits at one of two genuinely different levels — the matrix needs to represent both, not
collapse them onto one axis.

* **Session-scoped**: decided once, at the startup of one top-level Claude Code *process*, and fixed for that
  process's whole lifetime. MCP servers connect once at startup from the merged settings hierarchy (managed →
  CLI flags → project-local → shared-project → user). **There is no hot-reload**: changing `.mcp.json` or any
  MCP-related setting has no effect until the process is killed and relaunched (confirmed via Claude Code's own
  GitHub issue tracker — this is a known, currently-unclosed gap, not a doc omission).
  A new session is created by: running `claude` in a terminal, opening a new conversation in the desktop/web
  app, a headless/`-p`/SDK run, a cloud session, or a Remote-Control-connected runtime. **`/clear` does not
  create a new session** in this sense — it resets conversation history within the same running process, so
  already-connected MCP servers stay connected exactly as they were.
* **Sub-agent-scoped**: decided per `Agent`-tool delegation, nested *inside* one session's process. A subagent
  is not a new process or a new session — it's a delegated call that runs in the same process, in its own
  isolated context window (a non-fork subagent doesn't see the parent's conversation history at all), with its
  own tool/MCP scope set by its own frontmatter. It returns a summary to "the main conversation" (the docs' own
  term for the parent) and can itself spawn further subagents up to a depth limit (default 3 below the main
  conversation, then the `Agent` tool itself is withheld except for forks).

Subagent *definitions* are resolved at the same "once at startup" granularity as MCP servers — confirmed
empirically this session: writing a new `~/.claude/agents/*.md` file mid-session did not make it available to
the `Agent` tool; only agents already loaded at session start were listed.

### Relation to `/list-agents`

`/list-agents` lists sessions in the first sense above — independent top-level processes (or Remote-Control-
reached runtimes), each having independently resolved its own settings and connected its own MCP servers at its
own startup, based on whatever directory/settings it's rooted in. They are peers, reachable via inter-session
messaging (`ListAgents`/`SendMessage`), not subagents — none are spawned via the `Agent` tool from inside
another session, and none share a process or context with the session that lists them. If a session spawns an
`Agent`-tool subagent (or a fork), `/list-agents` shows it too, but under a distinct "in-process subagents you
spawned" category — nested one level inside that session's own process, not a peer of it.

**`/remote-control` is narrower than "coordinate multiple runtimes"**: it's device-handoff for *one* already-
running local session (phone/web access to a terminal that stays open) — one remote connection per instance.
The actual cross-runtime coordination mechanism is the general inter-session messaging system
(`ListAgents`/`SendMessage`); Remote Control is just one *kind* of reachable row in that system (the row where
the runtime is reached via phone/web instead of a local terminal you're sitting at).

## 2. Mechanisms that scope MCP server/tool availability

Four independent, layerable mechanisms. None are mutually exclusive.

### 2.1 Session/project-wide server approval (coarse, whole-server)

* `enabledMcpjsonServers` / `disabledMcpjsonServers` / `enableAllProjectMcpServers` (any settings file:
  managed/user/project/local) — approve or reject specific servers declared in a project's `.mcp.json`. This is
  an *approval* gate (trust), not really a scoping tool: a rejected server never connects (zero context cost),
  but there's no per-agent granularity — all-or-nothing for the whole session.
* `disabledMcpServers` — blocks a named MCP server in every scope, full stop.
* None of these are session-only/ad-hoc; they live in a settings file (though `--mcp-config` /
  `--strict-mcp-config` / `--setting-sources` CLI flags, or the SDK's `settingSources` option, can override
  per-invocation).

### 2.2 Settings-level permission rules (`permissions.allow/deny/ask`)

* Pattern syntax: `mcp__<server>` (whole server), `mcp__<server>__*` or `mcp__<server>__<tool>` (specific),
  `mcp__*` (deny-only, every MCP tool everywhere).
* **Key finding, confirmed by the docs**: a `deny` rule matching an MCP tool **removes that tool from Claude's
  context entirely** — "a tool matched by a bare-name glob deny rule is removed from Claude's context, the same
  as a bare tool name." This is a real context-cost lever, not just a runtime gate.
* `allow` rules only pre-approve calls to tools already connected — they don't add visibility. `ask` rules gate
  with a prompt but don't remove anything from context.
* Session/project-wide (settings file), applies to the main thread and, by inheritance, every subagent that
  doesn't override it (§2.3).

### 2.3 Subagent `tools:` / `disallowedTools:` frontmatter — per-subagent, fine-grained

* If a subagent's `tools:` field is **omitted**, it inherits every tool available in the main conversation, MCP
  included. **This is the actual mechanism behind the context-bloat problem that started this investigation**:
  any subagent that doesn't explicitly restrict `tools:` pays for every connected server's tool schemas.
* If `tools:` is **specified**, it's an allowlist — anything not named is unavailable, MCP included.
  `disallowedTools:` is the denylist equivalent. Both accept the same `mcp__` pattern syntax as §2.2, plus
  `mcp__*` in `disallowedTools` only. If both are set, `disallowedTools` is applied first, then `tools` is
  resolved against what's left.
* **design-assistant is already correctly scoped, by accident**: its `tools:` frontmatter
  (`Read, Edit, Write, Bash, Grep, Glob, TaskCreate, TaskUpdate, AskUserQuestion`) names no `mcp__` pattern at
  all, so it already has zero MCP tool exposure today. (Its `AskUserQuestion` entry is a separate, unrelated
  problem — see §3.)

### 2.4 Subagent `mcpServers:` frontmatter — the direct fix for the origin problem

* A subagent can declare an MCP server **inline**, scoped exclusively to itself: connected only when that
  subagent starts, disconnected when it finishes, **invisible to the main conversation and every other
  subagent**.
* Straight from the docs: *"To keep an MCP server out of the main conversation entirely and avoid its tool
  descriptions consuming context there, define it inline here rather than in `.mcp.json`. The subagent gets the
  tools; the parent conversation doesn't."* — this is exactly the Linear-MCP-context-cost scenario that started
  the whole investigation.
* A subagent can instead reference an already-configured server by name (a string, not inline) to reuse/share
  it with the parent session — that's the "inherit" path, and is what costs context when left unrestricted.

### Real gaps for the matrix to note

* There's no way to give the **main interactive session itself** a narrower MCP set than whatever's configured
  at session scope — sub-session-level scoping only exists for subagents (§2.3/§2.4).
* A subagent's *inherited* (string-reference) MCP tools still cost context in that subagent's own window even
  though they don't touch the parent — only an inline `mcpServers:` declaration (§2.4) truly keeps a server out
  of a *given* context window.
* Restarting with a different `--mcp-config`/`--strict-mcp-config` and then `--resume`-ing the same session id
  to keep conversation history *should* work, since each piece is independently documented to behave that way —
  but I could not find the combination explicitly confirmed together in one place. Treat as a likely-true
  inference, not a confirmed fact, until checked empirically.

## 3. How an agent gets human input mid-task — and why it matters here

This is wider than MCP-server visibility, but it surfaced directly out of this investigation and generalizes
beyond design-assistant, so it's recorded here rather than split into a separate note.

### 3.1 `AskUserQuestion` is unconditionally stripped from every subagent

Confirmed **empirically**, not just from docs: invoking design-assistant (which lists `AskUserQuestion` in its
own `tools:` frontmatter) and asking it to call that tool produced:

```
Error: No such tool available: AskUserQuestion. AskUserQuestion is not available inside subagents.
Complete the task with the tools provided and return findings to the orchestrator.
```

This matches the docs exactly: *"The first filter removes these tools, even when listed in the `tools` field:
`AskUserQuestion`."* It is not a permission refusal — the tool is simply absent from a subagent's tool set,
regardless of frontmatter.

**Concrete fallout**: design-assistant's own instructions describe deferring to the architect "using
`AskUserQuestion` or by reporting back and waiting" (WVR-119). Since design-assistant normally runs as a
subagent, the `AskUserQuestion` half of that instruction is dead — only "report back and stop" actually works.
Nobody caught this without running it. Not filing a follow-up ticket for this specifically: design-assistant is
already getting redesigned (WVR-173), so this is input to that redesign, not a standalone fix.

### 3.2 The only other channel: permission prompts

Foreground subagents pass permission prompts straight through to the user and block waiting for a response.
Background subagents (the default) surface them in the main session, named, and the user approves/denies
per-call. But: a follow-up message sent to a subagent via `SendMessage` explicitly does **not** count as
approval and cannot change its settings (v2.1.198+). This channel is a narrow yes/no gate, not dialogue.

### 3.3 MCP elicitation — the real mechanism for a structured "conversation"

Elicitation is an MCP **protocol** capability (not Claude-Code-specific): a server can pause mid-tool-call and
send `elicitation/create` to ask the human a question through the client, then resume once answered.

* **Shape**: `requestedSchema` is a flat object of primitive fields only (string/number/boolean/enum) — no
  nesting, no arrays. Response is one of three actions: `accept` (with data), `decline`, or `cancel`. One
  request/response round-trip per call — not open-ended chat. Nothing stops a server sending a *second*
  `elicitation/create` after the first resolves, so a server can chain one-shot questions to approximate a
  back-and-forth, but each round is independently structured; there's no adaptive mid-answer exchange.
* **Spec-mandated guardrails**: servers must not request sensitive information via elicitation; clients should
  show which server is asking, allow decline/cancel, and validate against the schema.
* **Claude Code's implementation**: two presentation modes — form mode (dialog with the server's fields) or URL
  mode (opens a browser for an OAuth-style flow, confirmed back in the CLI). No configuration needed; dialogs
  appear automatically. An `Elicitation` hook (matched by MCP server name) can auto-respond
  (accept/decline/cancel) without showing a dialog at all — useful for headless/automated runs; a companion
  `ElicitationResult` hook fires after the human answers, before the response reaches the server (an audit
  point). A call blocked on an open elicitation dialog is never backgrounded — Claude Code treats it as
  blocked-on-you, not slow.
* **Relation to subagents — inferred, not directly confirmed**: elicitation is server-driven, not
  model-tool-choice-driven, so nothing in the docs suggests it's stripped inside a subagent the way
  `AskUserQuestion` is. Indirect support: `dontAsk` permission mode explicitly denies MCP tools marked
  `requiresUserInteraction` — implying that in every *other* mode (including inside a subagent), such a call
  does reach the human. I found no explicit statement either way distinguishing subagent-originated elicitation
  from main-conversation elicitation. Worth a direct empirical check before this is relied on anywhere load-
  bearing.

### 3.4 The architectural pattern this implies for AgentPlugins

A subagent cannot itself hold a real conversation with the human — it has no memory across invocations
(non-fork) and no direct question-asking tool. But a **stateful MCP server** can: the server owns the state
that stitches together what looks like a multi-step conversation, across one or more elicitation round-trips,
and the subagent's own tool call is just the trigger — it ends, the elicitation happens (potentially outside
that tool call's own lifetime), and resumes with an answer in hand.

This is the pattern to design the human-judgement points around wherever a subagent (design-assistant or any
future AgentPlugins subagent) needs real, structured input from the architect mid-workflow: model the judgement
point as a call into a state-owning MCP server that uses elicitation, not as an in-subagent `AskUserQuestion`
call or an assumption that the subagent can just "ask and wait" in place. This generalizes beyond
design-assistant to any AgentPlugins capability with a human-judgement step — relevant input for WVR-173's
redesign, and for whatever WVR-94's matrix says about how each of the three platforms lets an agent get human
input, not only about MCP server/tool visibility.

## 4. What the SDK adds beyond the CLI/desktop runtime

* The Agent SDK's `query()` takes an `mcpServers` option at session-construction time — explicit, programmatic
  control, not settings-file resolution.
* `setMcpServers()` adds/removes servers **dynamically mid-session** — something the CLI/desktop runtime
  flatly cannot do (§1: no hot-reload, confirmed via Claude Code's own issue tracker).
* Within the CLI/desktop runtime itself, a running session cannot spin up a second, independently-MCP-
  configured top-level session from inside itself — the only sub-scoping tool available *inside* one process is
  the subagent mechanism (§2.3/§2.4). Getting a genuinely different top-level MCP set means starting an entirely
  separate process/session (§1) — which the current session can't do to itself, only a human (or another
  coordinating session) can.
* Trade-off: the SDK's extra control comes with owning the host application yourself — the CLI's elicitation
  dialog and `Elicitation`/`ElicitationResult` hooks are convenience the SDK doesn't give you for free.

## Open items, not resolved here

* `--resume` + `--mcp-config`/`--strict-mcp-config` combined behavior (§2, "real gaps") — inference, not
  confirmed.
* Whether MCP elicitation from a subagent-originated tool call is handled identically to a main-conversation one
  (§3.3) — inference from adjacent `dontAsk`-mode behavior, not a direct statement.
* Codex's equivalent mechanisms — [WVR-172](https://linear.app/weaver-engineering/issue/WVR-172/reastrict-agent-to-subset-of-all-available-mcp-servers-in-codex).
* OpenCode's mechanism — already solved (see WVR-171's Context for how), not re-derived here.
