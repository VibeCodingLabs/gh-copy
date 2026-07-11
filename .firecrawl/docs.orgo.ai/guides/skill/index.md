---
url: https://docs.orgo.ai/guides/skill
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

The Orgo skill is an [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for Claude Code. It teaches Claude when and how to spin up an Orgo cloud computer — for browser automation, visual testing, sandboxed runs, or any task that needs a real GUI.
Once installed, Claude Code discovers it automatically. No prompting required.

## [​](#install) Install

Personal (all your projects)

Project (this repo only)

```
mkdir -p ~/.claude/skills/computer && \
  curl -fsSL https://orgo.ai/skills/computer/SKILL.md \
    -o ~/.claude/skills/computer/SKILL.md
```

Restart Claude Code if it’s already running. Claude will pick up the skill on next start.

## [​](#try-it) Try it

```
spin up an orgo computer and screenshot the orgo.ai homepage
```

```
open chrome on my orgo computer, sign into github, take a screenshot
```

```
test how my dev server renders at https://localhost:3000 on a real browser
```

Claude reads the skill’s metadata at startup (~100 tokens) and only loads the full body when one of these prompts triggers it. Cost when idle: nothing.

## [​](#what’s-inside) What’s inside

The skill is a single `SKILL.md` file with YAML frontmatter (`name`, `description`, `when_to_use`) followed by procedural instructions Claude uses when the user’s request matches:

* **One-shot agent runs** — `orgo run "<prompt>"` with `--json` output for piping.
* **Interactive agent TUI** — `orgo agent` with persistent, resumable sessions.
* **Direct shell access** — `orgo ssh <name>` with OpenSSH-style disconnect.
* **Provisioning** — `orgo computers create` interactive or flagged.
* **Screenshots** — direct via REST or through the agent.
* **Pricing awareness** — uses existing running computers before provisioning fresh ones.
* **Guardrails** — clear “when NOT to use” so Claude doesn’t spin up a VM for tasks the Read/Edit/Bash tools already handle.

The full source is in [§ SKILL.md](#skillmd) below, or fetch the raw file from [orgo.ai/skills/computer/SKILL.md](https://orgo.ai/skills/computer/SKILL.md).

## [​](#where-it-works) Where it works

| Surface | Status |
| --- | --- |
| **Claude Code** (CLI / IDE) | Drop into `~/.claude/skills/computer/` and it works |
| **claude.ai** | Settings → Features → upload as a `.zip` containing the `computer/` folder |
| **Claude API** | Upload via `/v1/skills` endpoints (workspace-shared) |

## [​](#uninstall) Uninstall

```
rm -rf ~/.claude/skills/computer       # personal install
rm -rf .claude/skills/computer         # project install
```

## [​](#prerequisites) Prerequisites

The skill assumes the user has:

* An Orgo account — sign up at [orgo.ai](https://orgo.ai).
* The `orgo` CLI installed (`curl -fsSL https://orgo.ai/install.sh | bash`).
* Run `orgo login` once.

If any of these aren’t done, Claude will surface the right command when triggered — installation is a one-liner.

## [​](#license) License

The skill source is MIT-licensed. Audit it before installing (the SKILL.md is plain markdown) and treat as you would any package you’d add to your Claude Code setup.


---

## [​](#skill-md) SKILL.md

Byte-for-byte what’s served at [orgo.ai/skills/computer/SKILL.md](https://orgo.ai/skills/computer/SKILL.md) and what Claude Code reads when the skill is triggered.

### [​](#frontmatter) Frontmatter

```
---
name: computer
description: Spin up a real cloud Linux desktop with Chrome and drive it from the terminal — clicks, types, screenshots, bash, multi-step AI agent runs. Backed by Orgo (orgo.ai).
when_to_use: Use when the user wants to automate desktop or browser tasks, run an AI agent on its own VM, take screenshots of a real Chrome page, test a website visually in a real browser, sandbox an installer or untrusted code, or have a computer that stays online across sessions. Trigger phrases include "open chrome", "screenshot the page", "sandbox this", "automate this site", "run an agent on a VM", "test on a real browser".
---
```

| Field | Length | Constraint |
| --- | --- | --- |
| `name` | 8 chars | ≤64 chars, lowercase + digits + hyphens, no `anthropic`/`claude` |
| `description` | 165 chars | ≤1,024 chars per API; truncated at 1,536 chars in the skill listing |
| `when_to_use` | 419 chars | Claude Code extension; matched separately for trigger detection |
| Combined budget | 584 chars | Well under the 1,536-char listing cap |

### [​](#body) Body

Everything below is what Claude actually reads when the skill is triggered. Kept under 5k tokens so the model loads it efficiently.

```
# Computer

This skill gives you a real cloud Linux desktop you can drive from the terminal. Each computer boots in under 500 ms, has Chrome and the standard userland, and stays running until you stop it. Backed by Orgo (https://orgo.ai) — one CLI, one API.

Use this skill any time the user wants something that needs a real GUI: browser automation, visual testing, running an agent on its own desktop, sandboxing untrusted software, or any "open a page and do X" task that doesn't fit a single curl or local script.

## Install once

```bash
curl -fsSL https://orgo.ai/install.sh | bash   # installs Node + the orgo CLI
orgo login                                      # device-code OAuth in the browser
```

If the user already has Node 20+: `npm install -g orgo` instead.

Confirm with `orgo --version`. If `command not found`, add `~/.local/bin` to the user's shell PATH — the installer prints the exact line.

## Common workflows

### One-shot: have the agent drive the computer for you

```bash
orgo run "open chrome and screenshot the orgo.ai homepage" --computer agent-1
```

Streams text + tool calls + tool results to stdout. Add `--json` for a single structured object at the end:

```bash
orgo run "find the pricing for the Team plan on orgo.ai" --computer agent-1 --json
# → {"text": "...", "tool_calls": [...], "tool_results": [...], "usage": {...}}
```

### Interactive agent with persistent history

```bash
orgo agent --computer agent-1
```

Inside the TUI, slash commands: /help, /computer, /model, /sessions, /resume, /compact, /usage, /screenshot. Sessions auto-save to ~/.orgo/sessions/ after every turn — resume later with `orgo resume`.

### Direct shell on the VM

```bash
orgo ssh agent-1
# Lands in /root/Desktop. Disconnect with ~. (at line start) or Ctrl+C Ctrl+C.
```

### Provision a fresh computer

```bash
orgo computers create                             # interactive picker (workspace, name, RAM, CPU)
orgo computers create --name agent-1 --ram 4 --cpu 1
orgo computers list                               # see what's running
```

## When this skill is the right tool

Reach for this skill when the task needs a real GUI or a persistent computer:

- "Open this URL in Chrome and tell me what's on the page" — visual content the Read tool can't see.
- "Sign into X and click through Y" — real session cookies, not headless.
- "Test how this CSS change looks" — screenshot a dev server through a real browser.
- "Run an agent on a long-running task and check back on it later" — sessions outlive your terminal.
- "Try this installer / run this untrusted binary" — sandboxed from the user's machine.

## When NOT to use this skill

Don't spin up a cloud computer for things the user already has tools for:

- Reading local files → Read tool.
- Editing local files → Edit tool.
- One-shot HTTP / API requests → Bash + curl.
- Code you can write and run locally in Node/Python.
- Anything you can answer from training data.

A good check: does the task need vision of a rendered page, persistence across sessions, or isolation from the user's machine? If none of those, skip this skill.

## Plan awareness

Orgo plans are monthly subscriptions with a fixed computer-count limit per tier (Hacker: 5, Team: 20, Scale: 50). Computers are persistent — there's no per-hour metering — but every running or stopped computer counts against the limit until deleted.

What that means in practice:

- Reuse before provisioning. Run `orgo computers list` first.
- Delete throwaways with `orgo computers delete <name>` when the task is done. Stopping doesn't free the slot.
- Agent calls (`orgo run`, `orgo agent`) consume bundled AI credits ($5 Hacker / $25 Team / $100 Scale per month). Long Opus runs are expensive — consider `--model claude-sonnet-4-6` for routine work.

## Notes

- Every command accepts `--help` and `--json`.
- TTY detection switches the CLI to plain text + JSON when stdout isn't a terminal — safe to pipe.
- Credentials live in ~/.orgo/credentials.json (mode 0600). Use ORGO_PROFILE=<name> to switch identities.
- Full docs: https://docs.orgo.ai. CLI reference: https://docs.orgo.ai/guides/cli.
```

[Previous](/guides/cli)[Use Any ModelBuild computer use agents with Claude, GPT, Gemini, or any model

Next](/guides/models)

⌘I