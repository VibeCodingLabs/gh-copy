---
url: https://docs.orgo.ai/guides/openclaw
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

![OpenClaw](https://mintcdn.com/orgo/wJayerraXQVuhJ4i/images/openclaw.png?fit=max&auto=format&n=wJayerraXQVuhJ4i&q=85&s=712ed5b65ecab9a04ed2d125b236f03f)

[OpenClaw](https://openclaw.ai) is an open-source AI agent that runs on a desktop and controls applications, automates tasks, and connects to messaging platforms through a gateway. This guide installs OpenClaw inside an Orgo cloud computer.

## [​](#why-run-openclaw-on-an-orgo-computer) Why run OpenClaw on an Orgo computer

|  | Local laptop | Orgo cloud computer |
| --- | --- | --- |
| Uptime | Off when the laptop sleeps | Continuous |
| Reachable from other devices | Same network only | Anywhere |
| Persistent state | Tied to one machine | Survives restarts |
| Setup per device | Reinstall each time | One install, one config |
| Isolation | Full access to your personal files, accounts, and credentials | Isolated VM. Only the files and credentials you put on it. |

The agent and its skills live on the cloud computer. Other devices connect to it.

### [​](#isolation) Isolation

OpenClaw is designed to take actions on a computer: install skills, run shell commands, control applications, hit APIs with your credentials. On a personal laptop that means the agent has the same access you do, including your home directory, browser sessions, SSH keys, and `~/.aws/credentials`. On an Orgo computer the blast radius is the VM. The agent has access to whatever you install or paste into that VM and nothing else. Delete the computer and the state is gone.

## [​](#install) Install

1

Create the computer

Open [orgo.ai/workspaces](https://orgo.ai/workspaces) and create a computer with at least **8 GB RAM** and **4 CPU cores**.

2

Open a terminal on the computer

Open the computer in the dashboard and launch **Terminal** from the taskbar.

3

Run the installer

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

The installer detects the OS, installs Node 24 if missing, installs the `openclaw` CLI, and starts the onboarding wizard. The wizard configures a model provider, API key, and gateway port (default `18789`).

4

Install the background daemon

```
openclaw onboard --install-daemon
```

On Linux this registers a `systemd --user` service that auto-starts the gateway on every boot.

5

Verify

```
openclaw --version
openclaw doctor
openclaw gateway status
```

Open `http://127.0.0.1:18789/` in the computer’s browser for the OpenClaw dashboard.

## [​](#install-via-the-orgo-sdk) Install via the Orgo SDK

Drive the install from your laptop. Every `computer.bash(...)` call runs on the cloud computer.

```
from orgo import Computer

computer = Computer(workspace="openclaw", ram=8, cpu=4)

computer.bash("curl -fsSL https://openclaw.ai/install.sh | bash")
computer.bash("openclaw onboard --install-daemon")

print(computer.bash("openclaw gateway status"))
```

State lives in `~/.openclaw/` on disk, so the daemon survives `computer.stop()` and `computer.start()` cycles.

## [​](#gateway) Gateway

The gateway accepts messages from Slack, Discord, Telegram, iMessage, and other platforms. Set it up once on the computer:

```
openclaw gateway setup
```

A computer has no public inbound hostname — run gateways in outbound/socket mode (e.g. Slack Socket Mode, Telegram long-polling). To deliver HTTP webhooks, reach the desktop’s API through the authenticated proxy `https://www.orgo.ai/api/desktops/{instance_id}/proxy/<path>` (requires your Orgo API key).

## [​](#installing-skills) Installing skills

OpenClaw skills are distributed through [ClawHub](https://clawhub.ai):

```
npm install -g clawhub
clawhub search browser
clawhub install browser-automation
```

Skills install into `~/.openclaw/skills/` and persist across restarts.

## [​](#sizing) Sizing

| Workload | RAM | CPU |
| --- | --- | --- |
| Single user, lightweight skills | 8 GB | 4 cores |
| Multiple platforms, browser skills | 16 GB | 4 to 8 cores |
| Multi-agent or long-running flows | 32 GB+ | 8 cores |

## [​](#tips) Tips

* Config and skills live in `~/.openclaw/`.
* View logs with `journalctl --user -u openclaw -f`.

[Previous](/guides/models)[Hermes AgentRun Nous Research Hermes Agent on an Orgo cloud computer

Next](/guides/hermes)

⌘I