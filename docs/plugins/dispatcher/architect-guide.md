# Architect's Guide To The Dispatcher

## Context
* [`plugins/dispatcher`](https://github.com/weaver-engineering/agent-plugins/tree/main/plugins/dispatcher) - the plugin this guide is about. Its `SKILL.md` and `agents/dispatcher.md` are the dispatcher's own operating instructions; this guide is the architect's how-to
* [Session Naming](https://github.com/weaver-engineering/docs/blob/main/standards/session-naming.md) - the dispatcher/worker model, and the worker naming and branch rules the dispatcher applies
* [WVR-177](https://linear.app/weaver-engineering/issue/WVR-177/package-the-peer-session-startstop-mechanism-as-a-dispatcher) - start/stop; [WVR-228](https://linear.app/weaver-engineering/issue/WVR-228/dispatched-sessions-save-locally-and-can-be-stopped-and-resumed) - resume

The **Dispatcher** is one long-lived Claude Code session, rooted at `~/weaver-engineering`, that starts,
stops, and resumes **worker** sessions. Each worker has its product root, branch, worktree, ticket, and
agent persona fixed when it starts. Once a worker is up, you talk to it directly over Remote Control. The
dispatcher doesn't take part in that conversation or relay it.

## 1 Prerequisites

* Claude Code, logged in to claude.ai. Remote Control needs it, both for the dispatcher and for every worker.
* Node >= 22.6 on `PATH`. `dispatcher.ts` runs type-stripped, with no install or build step.
* The Linear MCP connector available to Claude Code. The dispatcher posts each ticketed worker's session id
  to its ticket, and workers read and update their tickets.
* `~/weaver-engineering` laid out as usual: each `<Product>/` holds exactly one code repo and one `-docs`
  repo, with `agentWorkTrees/` alongside. The dispatcher always resolves paths from `~/weaver-engineering`,
  never from its own cwd.
* **Once per new target repo:** accept Claude Code's workspace-trust dialog for it. Run `claude` once,
  interactively, inside that repo and accept. A headless worker launch can't click through the dialog. A
  start that fails with `Workspace trust not yet accepted` needs exactly this.

## 2 Install And Update

The plugin is deployed by copying its directory. There's no build step. Always deploy from `origin/main`,
never from a working tree:

```sh
git -C ~/weaver-engineering/AgentPlugins/agent-plugins fetch origin
rm -rf ~/.claude/dispatcher/plugin && mkdir -p ~/.claude/dispatcher/plugin
git -C ~/weaver-engineering/AgentPlugins/agent-plugins archive origin/main plugins/dispatcher \
  | tar -x --strip-components=2 -C ~/.claude/dispatcher/plugin
```

The dispatcher's record of every worker, `~/.claude/dispatcher/sessions.json`, sits beside `plugin/`, not
inside it, so redeploying never touches it. A running dispatcher only picks up a redeploy after a restart
(§5).

## 3 Start The Dispatcher

```sh
cd ~/weaver-engineering
claude --plugin-dir ~/.claude/dispatcher/plugin --agent dispatcher --name Dispatcher --remote-control Dispatcher
```

Connect to it over Remote Control as `Dispatcher`. `--agent dispatcher` loads its standing instructions, so
it behaves the same after every restart. Without that flag it's just an ordinary session with the skill
available.

## 4 Using It

Ask in plain language. Each request is one of **start**, **stop**, **clear down**, or **resume**. Every
request is self-contained: the dispatcher doesn't carry assumptions from one request over to the next.

### 4.1 Start

A start request names a **product**, and optionally a **ticket**, an **agent**, and a **target** repo.

| You say | Worker |
|---|---|
| "start a session on AgentPlugins" | Ad hoc, no ticket: rooted in the product's docs repo itself, with no worktree or branch. Named `AgentPlugins` |
| "start a session on AgentPlugins against code" | Same, rooted in the code repo |
| "start WVR-123 on AgentPlugins" | Ticketed: new worktree `agentWorkTrees/AgentPlugins/agent-plugins-docs-wvr123` on branch `task/WVR-123` off `origin/main`. Named `AgentPlugins - WVR-123` |
| "start WVR-123 on AgentPlugins against code" | Same, but in the code repo (`agent-plugins-wvr123`) |
| "start WVR-123 on AgentPlugins as design-assistant" | Started with `--agent design-assistant`. Named `AgentPlugins - WVR-123 : design-assistant` |

**Product** is the directory name under `~/weaver-engineering` (`AgentPlugins`, `MagpieWeaver`,
`WeaverProjects`, ...), or `Docs` for the shared `weaver-engineering/docs` repo, which has no code/docs
split.

**Agent** picks the persona, and through `agent-types.json` the repo, the branch prefix, and the base
branch. **Target** (`docs`/`code`) overrides the repo:

| Agent | Repo | Branch | Branched from |
|---|---|---|---|
| *(none, or not listed)* | docs | `task/<ref>` | `origin/main` |
| `design-assistant` | docs | `task/<ref>` | `origin/main` |
| `spec-writer` | code | `spec/<ref>` | `origin/main` |
| `test-writer` | code | `test/<ref>` | `spec/<ref>` |
| `build-implementer` | code | `build/<ref>` | `test/<ref>` |
| `quick-scaffolder` | code | `quick/<ref>` | `origin/main` |

A phase whose base branch doesn't exist yet fails rather than creating one. For example, `test-writer` fails
before `spec/<ref>` exists. To make a new agent available, add it to `agent-types.json`; no code change is
needed.

A ticketed worker is told to read its ticket and its comments, then wait for you. It moves the ticket to
`6 - In Progress` itself once work actually starts. The dispatcher posts a comment on the ticket with the
worker's Claude session id and a ready-to-run `claude --resume` line.

The dispatcher reports back the worker's name, its worktree (or root), its branch, its session id, and the
Remote Control URL to connect to.

### 4.2 Stop

"stop WVR-123", "stop AgentPlugins", or "stop AgentPlugins - WVR-123 : design-assistant".

You can select a worker by ticket, by product, or by its full or partial name, and narrow further by agent
or ticket. If more than one worker matches, the dispatcher lists the candidates and asks you to narrow
it. A bare product that matches several workers, exactly one of them ad hoc, is assumed to mean the ad hoc
one, and the dispatcher confirms with you first.

The dispatcher asks the worker to release its worktree lock, then stops it. The worker may wait for your
confirmation before releasing the lock. That's expected; if the lock isn't released within the timeout, the
stop goes no further. The worktree and branch stay, and **the worker stays resumable**. Stopping is the
default way to put a worker down.

### 4.3 Clear Down

"clear down WVR-123", once the ticket's work is merged or abandoned.

This is a stop that also removes the worktree, the local branch, and the remote branch. It needs a single
confirmation from you, before anything is removed. It never forces past uncommitted, untracked, or
unmerged work: it reports what it found and stops. A cleared-down worker **can't be resumed**.

### 4.4 Resume

"resume WVR-123", with the same selectors as stop, plus "against docs" or "against code" to narrow by repo.

This relaunches a stopped, not cleared-down, worker with `claude --resume <id>` in its original worktree,
with the same name and agent, so its conversation comes back intact. It isn't sent its start prompt again.
The dispatcher refuses rather than rebuilding anything if the worker's worktree has gone or moved. It also
refuses a worker started before resume support existed (WVR-228), which has no recorded session id.

You can also resume a stopped worker yourself, without the dispatcher. Copy the `claude --resume` line from
the dispatcher's comment on the ticket and run it from the directory it names. The dispatcher still records
that worker as stopped, but it sees the worker running and refuses to resume a second copy. When you're done
with it, exit it yourself.

## 5 Stopping And Restarting The Dispatcher

**Exiting the dispatcher ends every worker it started.** Workers run as its background tasks. To restart
it, for example after a redeploy, exit it (`/exit`), start it again (§3), then ask it to **resume** the
workers you want back.

You don't need to stop the workers first. Each worker's command line carries its own session id. When a
new dispatcher starts, it reports the workers whose ids no longer appear in any live process, and marks
them stopped, so they can be resumed. It repeats that check before every stop and resume. Stopping workers
first is still the gentler option: each worker gets the chance to release its worktree lock, and to finish
its current turn, rather than being cut off.

Workers started before resume support existed (WVR-228) carry no session id, so the dispatcher can't
tell whether they're alive. It reports them as unverifiable and leaves them alone. They can't be resumed.

## 6 When Something Fails

The dispatcher reports any failure verbatim and stops. It doesn't retry or work around one. In particular:

* **A start whose worker never comes up** is cleaned up automatically. Any worktree and branch it created
  are removed, then the underlying error is reported.
* **A resume whose worker never comes up** leaves everything as it was. The worker is still stopped and
  still resumable.
* **A clear down that finds real work** removes nothing it shouldn't. Commit, push, or discard the work
  yourself, then ask again.
