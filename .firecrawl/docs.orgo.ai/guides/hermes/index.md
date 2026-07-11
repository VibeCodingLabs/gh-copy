---
url: https://docs.orgo.ai/guides/hermes
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

![Hermes Agent](https://mintcdn.com/orgo/wJayerraXQVuhJ4i/images/hermes-agent.png?fit=max&auto=format&n=wJayerraXQVuhJ4i&q=85&s=5f67a5ca72b50b724fc9659beac69a2f)
[Hermes Agent](https://hermes-agent.nousresearch.com/) is Nous Research’s self-improving AI agent. It builds skills from experience, refines them during use, and maintains a persistent model of the user across sessions. This guide installs Hermes inside an Orgo cloud computer.

## [​](#why-run-hermes-on-an-orgo-computer) Why run Hermes on an Orgo computer

|  | Local laptop | Orgo cloud computer |
| --- | --- | --- |
| Uptime | Off when the laptop sleeps | Continuous |
| Reachable from other devices | Same network only | Anywhere |
| Persistent state and learned skills | Tied to one machine | Lives in `~/.hermes/` on the computer |
| Setup per device | Reinstall each time | One install, one config |
| Isolation | Full access to your personal files, accounts, and credentials | Isolated VM. Only the files and credentials you put on it. |

The agent, its tools, gateway, and learned skills live on the cloud computer. Other devices connect to it.

### [​](#isolation) Isolation

Hermes is designed to take actions on a computer: install packages, edit files, run shell commands, hit APIs with your credentials. On a personal laptop that means the agent has the same access you do, including your home directory, browser sessions, SSH keys, and `~/.aws/credentials`. On an Orgo computer the blast radius is the VM. The agent has access to whatever you install or paste into that VM and nothing else. Delete the computer and the state is gone.

## [​](#install) Install

1

Create the computer

Open [orgo.ai/workspaces](https://orgo.ai/workspaces) and create a computer with at least **8 GB RAM** and **4 CPU cores**. The installer pulls Python, Node.js, ripgrep, and ffmpeg.

2

Open a terminal on the computer

Open the computer in the dashboard and launch **Terminal** from the taskbar.

3

Run the installer

```
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

The installer handles everything in one shot:

* Installs Python 3.11+, Node.js 22, ripgrep, ffmpeg, and `uv` if missing.
* Clones the repo and sets up a virtual environment.
* Registers the global `hermes` command on `$PATH`.
* Walks through picking an LLM provider and pasting an API key.

Reload the shell to pick up the new command:

```
source ~/.bashrc
```

4

Run the setup wizard

```
hermes setup
```

For Nous Portal accounts:

```
hermes setup --portal
```

5

Start chatting

```
hermes
```

Quit with `Ctrl+D`. Hermes persists everything it learns to `~/.hermes/`.

## [​](#install-via-the-orgo-sdk) Install via the Orgo SDK

```
from orgo import Computer

computer = Computer(workspace="hermes", ram=8, cpu=4)

computer.bash(
    "curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
)

print(computer.bash("source ~/.bashrc && hermes --version"))
```

Configure model and tools by SSHing in and running `hermes setup`, or by templating `~/.hermes/config.toml` ahead of time.

## [​](#messaging-gateways) Messaging gateways

Hermes can accept messages from Slack, Discord, Telegram, email, and more:

```
hermes gateway setup
```

A computer has no public inbound hostname — run gateways in outbound/socket mode (e.g. Slack Socket Mode, Telegram long-polling). To deliver HTTP webhooks, reach the desktop’s API through the authenticated proxy `https://www.orgo.ai/api/desktops/{instance_id}/proxy/<path>` (requires your Orgo API key).

## [​](#cli-commands) CLI commands

| Command | What it does |
| --- | --- |
| `hermes` | Start an interactive chat session. |
| `hermes setup` | Re-run the full guided setup. |
| `hermes model` | Switch LLM provider or model. |
| `hermes tools` | Enable or disable tools. |
| `hermes gateway setup` | Wire up Slack, Discord, and other platforms. |
| `hermes config set <key> <value>` | Update a single config value. |
| `hermes update` | Pull the latest Hermes release. |
| `hermes doctor` | Diagnose install or config issues. |

Full reference: [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs).

## [​](#sizing) Sizing

| Workload | RAM | CPU |
| --- | --- | --- |
| Single user, terminal chat | 8 GB | 4 cores |
| Skills, browser tools, gateway | 16 GB | 4 to 8 cores |
| Long-running flows with many tools | 32 GB+ | 8 cores |

## [​](#tips) Tips

* Identity and learned skills live in `~/.hermes/`.
* For multi-tenant setups, run one Hermes computer per user.

[Previous](/guides/openclaw)[Migrate from a VPSMove Hermes Agent or OpenClaw from DigitalOcean, Fly.io, or Hetzner onto an Orgo cloud computer with memory, skills, and sessions intact.

Next](/guides/migrate)

⌘I