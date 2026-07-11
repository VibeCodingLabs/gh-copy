---
url: https://docs.orgo.ai/guides/migrate
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Orgo gives an AI agent a full Linux cloud computer to operate — desktop, browser, shell, files, and a built-in HTTP control API. This guide moves [Hermes Agent](https://hermes-agent.nousresearch.com/) or [OpenClaw](https://openclaw.ai) from DigitalOcean, Fly.io, or Hetzner onto an Orgo cloud computer with memory, skills, sessions, and configuration preserved.

## [​](#comparison-chart) Comparison Chart

|  | VPS | Orgo |
| --- | --- | --- |
| You manage | OS, firewall, VNC, browser, fonts, TLS, monitoring, backups | Nothing |
| Time to a desktop | 1–3 hours | One API call |
| Boot time | 30 s – 2 min | < 500 ms |
| Click / type / screenshot | Build it yourself | Built in |
| Run shell | `ssh user@host` | `computer.bash(...)` |
| Run Python | Set up Jupyter | `computer.exec(...)` |
| File transfer | `scp` / `rsync` | `/files/upload` |
| HTTP API + TLS | Floating IP + DNS + certs | `www.orgo.ai/api/desktops/{instance_id}/proxy/<path>` (your API key), automatic TLS |
| Live-resize | Usually a reboot | `PATCH /resize` |
| Snapshot / clone | Manual | `POST /clone` |
| Uptime | You patch and restart | Continuous by default |

Orgo is purpose-built for agents that operate a desktop, browser, or any app without a programmatic API. Pure headless backend scripts are equally well served by a VPS.

## [​](#pick-your-agent) Pick your agent

## Hermes Agent

Nous Research. Self-improving agent with persistent skills + memory.

## OpenClaw

Open-source personal AI assistant with messaging-platform gateways.

## [​](#five-steps) Five steps

1. **Snapshot** the agent’s state directory on the source.
2. **Provision** an Orgo computer.
3. **Transfer** the tarball.
4. **Install** the agent with its upstream installer.
5. **Restore + start**, then verify.

Same recipe for both agents. Only step 3 varies by source platform.

## [​](#state-lives-in-one-directory) State lives in one directory

| Agent | Directory | Contents |
| --- | --- | --- |
| Hermes | `~/.hermes/` | `.env`, `config.yaml`, `SOUL.md`, `sessions/`, `memories/`, `skills/`, `cron/`, `hooks/`, `pairing/`, `whatsapp/`, `logs/`, `image_cache/`, `audio_cache/` |
| OpenClaw | `~/.openclaw/` | `openclaw.json`, `workspace/` (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `skills/<name>/SKILL.md`) |

Snapshot that single directory and you preserve identity, memory, skills, and API keys.

## [​](#run-the-migration) Run the migration

Set `ORGO_API_KEY` from [orgo.ai/start](https://orgo.ai/start), then pick the tab for the agent you’re moving.

* Hermes Agent
* OpenClaw

![Hermes Agent](https://mintcdn.com/orgo/wJayerraXQVuhJ4i/images/hermes-agent.png?fit=max&auto=format&n=wJayerraXQVuhJ4i&q=85&s=5f67a5ca72b50b724fc9659beac69a2f)

1

Snapshot on the source

```
# Sanity check there's room for the tarball
df -h ~

systemctl --user stop hermes-gateway 2>/dev/null || true
pkill -f 'hermes gateway' 2>/dev/null || true
tar czf /tmp/hermes-state.tgz -C "$HOME" .hermes
ls -lh /tmp/hermes-state.tgz
```

Tarball is typically 5 MB to a few hundred MB depending on session and media-cache size.

2

Create the Orgo computer

REST

CLI

```
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id":"WORKSPACE_ID","name":"hermes-prod","ram":8,"cpu":4,"disk_size_gb":32}'
# → save the returned id as $COMPUTER_ID
```

3

Transfer the tarball in

Pick the source platform tab in [Transfer the tarball](#transfer-the-tarball). End state: `/root/Desktop/hermes-state.tgz` exists on the Orgo computer.

4

Install Hermes

Run any shell command in the VM via `POST /computers/{id}/bash`. For interactive work, `orgo ssh hermes-prod` opens a live terminal.

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"}'
```

Pulls Python 3.11, Node.js, `uv`, ripgrep, ffmpeg. Registers `hermes` on `$PATH`. Creates an empty `~/.hermes/` skeleton, which the next step replaces.

5

Restore and start

```
# Restore over the fresh skeleton
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"set -e; rm -rf ~/.hermes/sessions ~/.hermes/memories ~/.hermes/skills ~/.hermes/whatsapp ~/.hermes/cron ~/.hermes/hooks ~/.hermes/pairing ~/.hermes/image_cache ~/.hermes/audio_cache; tar xzf /root/Desktop/hermes-state.tgz -C \"$HOME\"; chmod 600 ~/.hermes/.env"}'

# Install + start the gateway
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"hermes gateway install && systemctl --user start hermes-gateway"}'
```

6

Verify

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"hermes doctor && ls ~/.hermes/sessions/ | head && systemctl --user status hermes-gateway --no-pager"}'
```

![OpenClaw](https://mintcdn.com/orgo/wJayerraXQVuhJ4i/images/openclaw.png?fit=max&auto=format&n=wJayerraXQVuhJ4i&q=85&s=712ed5b65ecab9a04ed2d125b236f03f)

1

Snapshot on the source

```
# Sanity check there's room for the tarball
df -h ~

# Linux source
systemctl --user stop openclaw 2>/dev/null || true
# macOS source
launchctl unload ~/Library/LaunchAgents/ai.openclaw.plist 2>/dev/null || true

tar czf /tmp/openclaw-state.tgz -C "$HOME" .openclaw
ls -lh /tmp/openclaw-state.tgz
```

2

Create the Orgo computer

REST

CLI

```
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id":"WORKSPACE_ID","name":"openclaw-prod","ram":8,"cpu":4,"disk_size_gb":32}'
# → save the returned id as $COMPUTER_ID
```

3

Transfer the tarball in

Pick the source platform tab in [Transfer the tarball](#transfer-the-tarball). End state: `/root/Desktop/openclaw-state.tgz` exists on the Orgo computer.

4

Install OpenClaw

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"curl -fsSL https://openclaw.ai/install.sh | bash"}'
```

Pulls Node 24 if missing and installs the `openclaw` CLI globally.

5

Restore and install the daemon

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"set -e; rm -rf ~/.openclaw; mkdir -p ~/.openclaw; tar xzf /root/Desktop/openclaw-state.tgz -C \"$HOME\"; openclaw onboard --install-daemon; openclaw gateway status"}'
```

6

Verify

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"openclaw doctor && ls ~/.openclaw/workspace/skills/ | head && cat ~/.openclaw/openclaw.json"}'
```

Dashboard inside the VM: `http://127.0.0.1:18789/`.

## [​](#transfer-the-tarball) Transfer the tarball

`/files/upload` works from anywhere. Use the source-specific tab when the source is behind NAT or you’d rather skip the round-trip.

* DigitalOcean
* Fly.io
* Hetzner
* Any other VPS

Standard SSH:

```
scp root@droplet.example.com:/tmp/hermes-state.tgz .
curl -X POST https://www.orgo.ai/api/files/upload \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -F "file=@hermes-state.tgz" \
  -F "workspaceId=$WORKSPACE_ID" \
  -F "desktopId=$COMPUTER_ID"
```

For a consistent point-in-time copy under live traffic, take a [DigitalOcean snapshot](https://docs.digitalocean.com/products/snapshots/) first.

Machines have no public SSH. Use `flyctl ssh sftp` over Fly’s wireguard mesh:

```
flyctl ssh console -a YOUR_APP -C "tar czf /tmp/hermes-state.tgz -C /root .hermes"
flyctl ssh sftp get -a YOUR_APP /tmp/hermes-state.tgz ./hermes-state.tgz
curl -X POST https://www.orgo.ai/api/files/upload \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -F "file=@hermes-state.tgz" \
  -F "workspaceId=$WORKSPACE_ID" \
  -F "desktopId=$COMPUTER_ID"
```

Reference: [Fly SSH and SFTP](https://fly.io/docs/flyctl/ssh-sftp/). For Fly Volumes, [snapshot first](https://fly.io/docs/volumes/snapshots/).

Standard SSH:

```
scp root@your-hetzner-ip:/tmp/hermes-state.tgz .
curl -X POST https://www.orgo.ai/api/files/upload \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -F "file=@hermes-state.tgz" \
  -F "workspaceId=$WORKSPACE_ID" \
  -F "desktopId=$COMPUTER_ID"
```

For consistency, take a [Hetzner snapshot](https://docs.hetzner.com/cloud/servers/getting-started/back-up-snapshot/) first.

If you have SSH, you have a path: `tar` the state dir → `scp` to your laptop → `curl` to `/files/upload`. If the source can reach the public internet, skip the laptop step and `curl` directly from the source.

## [​](#what-carries-over) What carries over

| Item | In the tarball | Notes |
| --- | --- | --- |
| LLM API keys | ✓ | `~/.hermes/.env` or `~/.openclaw/openclaw.json`. Re-chmod to 0600. |
| Learned skills | ✓ | `~/.hermes/skills/`, `~/.openclaw/workspace/skills/` |
| Long-term memory | ✓ | `~/.hermes/memories/`, OpenClaw `workspace/` |
| Chat sessions | ✓ | `~/.hermes/sessions/` |
| Slack / Discord / Telegram bot tokens | ✓ | In `.env`, re-read on gateway start |
| Hermes hooks + per-user cron | ✓ | `~/.hermes/hooks/`, `~/.hermes/cron/` |
| WhatsApp / iMessage / Signal pairings | ✗ | Device-bound. Re-scan QR. |
| Systemd unit files | ✗ | Re-run `hermes gateway install` or `openclaw onboard --install-daemon`. |
| `journald` logs | ✗ | App logs in `~/.hermes/logs/` do carry. |
| System `crontab -e` entries | ✗ | Only `~/.hermes/cron/` carries. |
| Hand-installed OS packages | ✗ | Re-install. Installer covers the defaults. |
| Floating IPs / custom DNS | ✗ | Reach the desktop’s API via `www.orgo.ai/api/desktops/{instance_id}/proxy/<path>` (your API key). |

## [​](#gotchas) Gotchas

**Don’t run two gateways on the same bot token.** Stop the source gateway first, verify on Orgo, then delete the source. Two live gateways race for incoming messages.

**`hermes setup` rewrites `.env`.** Run the restore step *after* install. Don’t re-run the wizard or it overwrites the API keys you brought over.

* **sqlite needs disk headroom.** `fsync` returns `EIO` (Errno 5) on a full disk. Size the computer with at least 2× the source state-dir as free disk.
* **Device-bound pairings re-pair.** WhatsApp Web, iMessage, Signal. Re-scan the QR on Orgo.
* **Inbound webhooks don’t hit the VM directly anymore.** There’s no public per-VM hostname; reach the desktop’s API through the authenticated proxy (`https://www.orgo.ai/api/desktops/{instance_id}/proxy/<path>`, with your Orgo API key), or run gateways in outbound/socket mode.

## [​](#rollback) Rollback

Keep the source machine powered on with its gateway stopped until you’re satisfied. To revert:

```
systemctl --user start hermes-gateway   # Hermes
systemctl --user start openclaw         # OpenClaw
```

Delete the source after a few hours of clean operation on Orgo.

## [​](#smoke-test) Smoke test

`hermes doctor` only confirms the binary is wired. To prove memory restored correctly, ask the agent something only it would know:

* Hermes
* OpenClaw

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"hermes chat \"What did we last discuss in our previous session?\""}'
```

The reply should reference real context from the source machine. Generic answers (“I don’t have memory of past chats”) mean `~/.hermes/sessions/` or `~/.hermes/memories/` didn’t restore — re-check the `tar xzf` step and that you didn’t extract before the install step ran.

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"openclaw send self \"What was our last topic?\""}'
```

If the reply has no continuity, inspect `~/.openclaw/workspace/` to confirm sessions and skill files copied across.

## [​](#troubleshooting) Troubleshooting

Gateway won't start after restore

```
# Hermes
journalctl --user -u hermes-gateway -n 80 --no-pager

# OpenClaw
journalctl --user -u openclaw -n 80 --no-pager
```

Most common cause: `.env` lost its 0600 mode during transfer, or `hermes setup` ran a second time and overwrote it. Restore from the tarball, then `chmod 600 ~/.hermes/.env`.

sqlite returns 'database is locked' or fsync EIO

```
df -h /                       # disk full?
lsof | grep '\.hermes/.*\.db' # another process holding it open?
```

If disk is at 100%, the in-VM gateway can’t write checkpoints. Bump `disk_size_gb` with a live resize:

```
curl -X PATCH https://www.orgo.ai/api/computers/$COMPUTER_ID/resize \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"disk_size_gb": 64}'
```

Bot is unresponsive in Slack / Discord / Telegram

Two gateways online with the same bot token race for incoming messages. Stop the source:

```
systemctl --user stop hermes-gateway   # or: openclaw
```

Wait 30 s, then re-test from the messaging client. If still silent, check the gateway logs on Orgo for `unauthorized`-shaped errors — the bot token may have been rotated between snapshot and restore.

WhatsApp QR won't load

The pairing in `~/.hermes/whatsapp/` is bound to the old device’s hardware fingerprint. Wipe it and re-pair:

```
rm -rf ~/.hermes/whatsapp
hermes whatsapp     # or: openclaw whatsapp
```

Upload landed but I can't find the file in the VM

`POST /files/upload` drops files at `/root/Desktop/<filename>` inside the VM. Verify:

```
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command":"ls -lh /root/Desktop/"}'
```

If the file isn’t there, the upload didn’t return 200 — check the curl response body, often a `workspaceId` / `desktopId` mismatch.

## [​](#full-script) Full script

One bash file that runs the whole Hermes migration with `curl` + `jq`. Set `ORGO_API_KEY`, `WORKSPACE_ID`, and `SOURCE_TARBALL`.

```
#!/usr/bin/env bash
set -e

: "${ORGO_API_KEY:?Missing ORGO_API_KEY}"
: "${WORKSPACE_ID:?Missing WORKSPACE_ID}"
SOURCE_TARBALL="${SOURCE_TARBALL:-$HOME/Downloads/hermes-state.tgz}"

API="https://www.orgo.ai/api"
AUTH="Authorization: Bearer $ORGO_API_KEY"
JSON="Content-Type: application/json"

# 1. Create computer
RESP=$(curl -sS -X POST "$API/computers" -H "$AUTH" -H "$JSON" \
  -d "{\"workspace_id\":\"$WORKSPACE_ID\",\"name\":\"hermes-prod\",\"ram\":8,\"cpu\":4,\"disk_size_gb\":32}")
COMPUTER_ID=$(echo "$RESP" | jq -r .id)
HOSTNAME=$(echo "$RESP"  | jq -r .hostname)
echo "Created $COMPUTER_ID at https://$HOSTNAME"

# 2. Upload tarball (lands at /root/Desktop/<filename>)
curl -sS -X POST "$API/files/upload" -H "$AUTH" \
  -F "file=@$SOURCE_TARBALL" \
  -F "workspaceId=$WORKSPACE_ID" \
  -F "desktopId=$COMPUTER_ID" > /dev/null

# Helper: run a bash command inside the VM
run() {
  curl -sS -X POST "$API/computers/$COMPUTER_ID/bash" -H "$AUTH" -H "$JSON" \
    -d "$(jq -n --arg c "$1" '{command:$c}')"
  echo
}

# 3. Install Hermes
run "curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"

# 4. Restore state on top of the fresh skeleton
run 'set -e
rm -rf ~/.hermes/sessions ~/.hermes/memories ~/.hermes/skills \
       ~/.hermes/whatsapp ~/.hermes/cron ~/.hermes/hooks \
       ~/.hermes/pairing ~/.hermes/image_cache ~/.hermes/audio_cache
tar xzf /root/Desktop/hermes-state.tgz -C "$HOME"
chmod 600 ~/.hermes/.env'

# 5. Install + start the gateway
run "hermes gateway install"
run "systemctl --user start hermes-gateway"

# 6. Verify
run "hermes doctor"

echo
echo "Done. https://$HOSTNAME"
```

Swap the install URL + state-dir paths to migrate OpenClaw with the same script.

## [​](#reference) Reference

## Hermes Agent docs

Full Nous Research documentation

## Hermes Agent GitHub

Source + release notes

## OpenClaw site

Project home

## OpenClaw GitHub

Source + `AGENTS.md` spec

## DigitalOcean snapshots

Source-platform snapshots

## Fly.io SSH & SFTP

`flyctl ssh sftp` reference

## Hetzner snapshots

Source-platform snapshots

## Orgo SDK quickstart

`computer.bash`, `.exec`, `.files`

Need a migration outside this shape? [spencer@orgo.ai](mailto:spencer@orgo.ai) or [Discord](https://discord.gg/tbYGpvnnJD).

[Previous](/guides/hermes)[Instance TypesCompute configurations for Orgo cloud computers

Next](/guides/instance-types)

⌘I