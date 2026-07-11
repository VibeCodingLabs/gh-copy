---
url: https://docs.orgo.ai/guides/cli
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

The Orgo CLI gives you complete control over your cloud computers from the
terminal: launch and manage workspaces and computers, open an interactive
shell, run multi-turn AI agent sessions, and pipe machine-readable output
into any other tool.

## [​](#install) Install

macOS / Linux

npm

```
curl -fsSL https://orgo.ai/install.sh | bash
```

Requires Node 20 or later. The install script will install Node for you
if it’s missing — no `sudo` needed.

## [​](#sign-in) Sign in

```
orgo login
```

Opens your browser, completes a device-code flow, and saves a credential
under `~/.orgo/credentials.json` (mode `0600`). To use a separate
identity in dev, set `ORGO_PROFILE=dev`.

## [​](#commands) Commands

```
orgo                          Show account, workspace, and recent computers
orgo login / logout / whoami  Account management
orgo workspaces (ws)          List, create, switch workspaces
orgo computers  (c)           List, create, start, stop, restart, delete computers
orgo ssh <name>               Interactive shell on a computer
orgo agent                    Multi-turn AI agent TUI (resumable sessions)
orgo run "<prompt>"           One-shot agent run
orgo resume [id]              Resume a prior agent session
orgo sessions                 List saved agent sessions
orgo api-keys                 Manage API keys
orgo billing                  Credits, top-ups, billing portal
```

Every command accepts `--json` for machine-readable output and `--help`
for details. Pipe-friendly by default: TTY detection switches to plain
text + JSON when stdout isn’t a terminal.

## [​](#create-a-computer) Create a computer

```
orgo computers create
```

Interactive by default — prompts for workspace, name, RAM, and CPU with
input validation. For scripts and CI, pass everything as flags:

```
orgo computers create \
  --workspace my-workspace \
  --name agent-1 \
  --ram 4 \
  --cpu 1
```

Valid values: RAM ∈  GB, CPU ∈  cores.

## [​](#ssh) SSH

```
orgo ssh computer-name
```

Opens an interactive terminal session over WebSocket. Lands you in
`/root/Desktop` by default (override with `--cwd`). Standard SSH
disconnect sequences:

| Sequence | Action |
| --- | --- |
| `~.` (at start of line) | OpenSSH-style disconnect |
| `Ctrl+C` `Ctrl+C` (within 800ms) | Discoverable disconnect |
| `Ctrl+D` or `exit` | Standard shell exit |
| Single `Ctrl+C` | Forwarded to remote (interrupts process) |

## [​](#agent-tui) Agent TUI

```
orgo agent
```

Multi-turn agent session with full conversation history, tool-call
visibility, and persistent sessions. Inside the TUI:

| Slash command | Action |
| --- | --- |
| `/help` | List slash commands |
| `/computer` | Switch the agent to a different computer (picker) |
| `/model` | Switch model — Opus 4.7 default |
| `/sessions` | List saved sessions |
| `/resume` | Resume a prior session (picker) |
| `/compact` | Summarize older turns to shrink context |
| `/usage` | Token usage for this session |
| `/screenshot` | Save the live screenshot and open it |
| `/save <name>` | Set the session title |

Sessions auto-persist to `~/.orgo/sessions/` after every turn — Ctrl+C
loses nothing.

### [​](#resume-a-session) Resume a session

```
orgo resume            # interactive picker
orgo resume <id>       # direct
orgo sessions          # list saved sessions
```

## [​](#one-shot-run) One-shot run

For scripts and CI:

```
orgo run "open chrome and search for hermes" --computer agent-1
```

Streams text, tool calls, and tool results to stdout. Add `--json` to
get a single structured object at the end:

```
{
  "text": "Chrome is open on the Google homepage…",
  "tool_calls":   [{ "id": "toolu_…", "name": "computer", "input": { … } }],
  "tool_results": [{ "tool_use_id": "toolu_…", "display": "[screenshot]" }],
  "usage": { "prompt_tokens": 1420, "completion_tokens": 312, "total_tokens": 1732 },
  "computer": { "id": "…", "name": "agent-1" }
}
```

## [​](#api-keys) API keys

```
orgo api-keys list
orgo api-keys create --name ci --workspace my-workspace
orgo api-keys delete <id>
```

Keys can be scoped to a single workspace — useful for CI tokens that
should only see one project’s resources.

## [​](#environment) Environment

| Variable | Purpose |
| --- | --- |
| `ORGO_API_KEY` | Use this key directly (skips `~/.orgo/credentials.json`) |
| `ORGO_API_BASE_URL` | Point at a different API host |
| `ORGO_PROFILE` | Credential profile (default: `default`) |
| `ORGO_JSON=1` | Force JSON output everywhere |
| `ORGO_NO_COLOR=1` | Disable ANSI colors (also respects `NO_COLOR`) |

## [​](#shell-completion) Shell completion

The CLI ships with bash, zsh, and fish completion scripts. To enable for
your current shell:

```
orgo completion --install
```

This adds a one-line source to your shell config. Completion is dynamic
— it queries your live workspaces and computers, so `orgo ssh <Tab>`
shows your actual machines.

## [​](#license) License

MIT.

[Previous](/quickstart)[SkillDrop-in Claude Code skill that gives Claude access to Orgo cloud computers.

Next](/guides/skill)

⌘I