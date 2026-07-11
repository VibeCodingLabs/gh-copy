---
url: https://docs.orgo.ai/guides/templates/schema
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

A template is a single `orgo.ai/v1` document, written in YAML or JSON. This page is the field-by-field reference. The canonical machine-readable contract is the [JSON Schema](/api-reference/templates/schema) at `GET /api/template-schema` — point your editor at it for autocomplete and inline validation.

```
# yaml-language-server: $schema=https://www.orgo.ai/api/template-schema
```

## [​](#two-forms) Two forms

Templates accept a **canonical** form and a shorter **sugar** form. Both normalize to the same document and the same `digest`.

Canonical

Sugar

```
api_version: orgo.ai/v1
template:
  name: my-workstation
  version: 1.0.0
hardware:
  cpu: 2
  ram_gb: 4
  resolution: 1280x800x24
env:
  NODE_ENV: production
files:
  - to: /opt/welcome.txt
    inline: "hello"
hooks:
  on_first_boot: |
    echo "ready"
```

### [​](#sugar-→-canonical) Sugar → canonical

| Sugar | Canonical |
| --- | --- |
| `name: foo@1.0.0` | `template: { name: foo, version: 1.0.0 }` |
| `cpu: 2` | `hardware: { cpu: 2 }` |
| `ram: 4gb` | `hardware: { ram_gb: 4 }` |
| `display: 1280x800` | `hardware: { resolution: 1280x800x24 }` |
| `wallpaper: "https://…"` | downloads the image and sets it as the desktop background on every boot |
| `files: { /path: "text" }` | `files: [{ to: /path, inline: "text" }]` |
| `on_first_boot: |` | `hooks: { on_first_boot: … }` |

## [​](#top-level-fields) Top-level fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `api_version` | string | yes | Must be `orgo.ai/v1`. |
| `template` | object | yes | [Identity](#metadata): name, version, description. |
| `hardware` | object | no | [VM resource shape](#hardware). |
| `secrets` | array | no | [Vault secrets](/guides/templates/secrets) the template needs. |
| `vars` | map | no | [Variables](#vars-and-interpolation) for `${var.X}` interpolation. |
| `env` | map | no | [Environment variables](#env), literal or secret-backed. |
| `build` | object | no | [Build-time install steps](#build). |
| `files` | array | no | [Files](#files) written into the VM. |
| `apps` | array | no | [Apps, services, and health checks](#apps). |
| `triggers` | array | no | [Reactive automation](/guides/templates/triggers). |
| `terminal` | array | no | [Pre-staged tmux sessions](#terminal). |
| `hooks` | object | no | [Lifecycle shell hooks](#hooks). |
| `telemetry` | object | no | [Metrics and logs](#telemetry). |
| `egress_policy` | object | no | [Per-VM network rules](#egress-policy). |
| `streaming` | array | no | [Outbound RTMP streams](#streaming). |

## [​](#template) template

Identity and provenance. `name` and `version` are required.

```
template:
  name: claude-code          # lowercase kebab-case, 1-64 chars
  version: 1.0.0             # semver, immutable once published
  description: Claude Code CLI, ready in the terminal.
  publisher: orgo            # optional handle (kebab-case)
  license: MIT               # optional SPDX id (informational)
  homepage: https://…        # optional
  source: https://github.com/…  # optional
```

## [​](#hardware) hardware

The VM’s resource shape. Every field is optional; sensible defaults apply.

| Field | Values | Notes |
| --- | --- | --- |
| `os` | `linux` | Linux only. |
| `cpu` | `1`, `2`, `4`, `8`, `16` | vCPU count. Capped by your plan. |
| `ram_gb` | `4`, `8`, `16`, `32`, `64` | RAM in GB. Capped by your plan. |
| `disk_gb` | integer ≥ 1 | Disk in GB. |
| `gpu` | `none`, `t4`, `l4`, `a10`, `l40s`, `a100-40`, `a100-80`, `h100` | GPU model. |
| `gpu_count` | integer ≥ 0 | Number of GPUs. |
| `resolution` | `WIDTHxHEIGHTxDEPTH` | e.g. `1280x720x24`. |
| `auto_stop_minutes` | `0`–`1440` | Idle minutes before auto-stop. `0` disables. |
| `region` | `auto-us`, `iad`, `sjc`, `lax` | Placement region. |
| `audio` | boolean | Enable the audio device. Defaults to `false`. |
| `bandwidth_mbps` | integer ≥ 0 | Network bandwidth cap (Mbps). |

Hardware in a [Create computer](/api-reference/computers/create) request overrides these defaults at launch.

## [​](#vars-and-interpolation) vars and interpolation

`vars` are compile-time strings, interpolated across the document before build.

```
vars:
  region: sjc2
  tag: v7

env:
  REGION: "${var.region}"

files:
  - to: /opt/config
    inline: "region=${var.region} tag=${var.tag}"
```

* `${var.X}` resolves from `vars`.
* `${env.X}` resolves from a literal `env` value (not secret-backed ones).
* `$${var.X}` escapes to a literal `${var.X}`.
* An unknown reference is a validation error with the exact field path.

## [​](#env) env

Environment variables written to the VM. Keys must be `UPPER_SNAKE_CASE`. Each value is a literal string, or a `{secret: <name>}` reference resolved from the launching user’s vault at create time.

```
secrets:
  - name: anthropic_api_key

env:
  NODE_ENV: production
  ANTHROPIC_API_KEY:
    secret: anthropic_api_key
```

See [Secrets](/guides/templates/secrets) for the full secret-injection model.


## [​](#build) build

Package and command steps run once when baking the golden snapshot, before app installs. This is where dependencies get pre-installed so launches are instant.

```
build:
  apt: [ffmpeg, ripgrep]
  pip: [requests, httpx]
  npm: [pnpm]
  run:                      # up to 64 shell commands, in order
    - curl -fsSL https://example.com/install.sh | bash
```

## [​](#files) files

Files materialized into the VM. Each entry sets exactly one of `from` or `inline`.

```
files:
  - to: /opt/hello.txt
    inline: "hello world"

  - to: /usr/share/backgrounds/bg.png
    from: https://example.com/bg.png   # http, https, git, s3, file, or secret://

  - to: /opt/run.sh
    mode: "0755"                        # octal permissions
    inline: |
      #!/bin/bash
      echo hi

  - to: /root/.config/app.json
    from: secret://app_config           # pulled from the vault
    when: runtime                        # build (default) or runtime
```

| Field | Description |
| --- | --- |
| `to` | Absolute destination path (or `~/…`). No `..`, no reserved system paths. |
| `from` | Source URI: `file`, `git`, `http`, `https`, `s3`, or `secret://<name>`. |
| `inline` | Inline file content. |
| `mode` | Octal permissions, e.g. `"0644"`. |
| `owner` / `group` | Ownership, resolved against the VM’s `/etc/passwd`. |
| `when` | `build` (baked into the snapshot) or `runtime` (re-applied each boot). |

`to` must be an absolute path with no `..`. Reserved system paths are rejected: `/proc`, `/sys`, `/boot`, `/dev`, `/tmp`, `/run`, plus the Orgo runtime (`/etc/orgo`, `/var/orgo`, `/orgo`, `/etc/supervisor`, and Orgo’s own binaries under `/opt` and `/usr/local/sbin`). Your apps can still write under `/opt` and elsewhere — only Orgo’s own runtime files are off-limits.

## [​](#apps) apps

An app bundles an install step with the long-running services, health checks, and ports it needs. Services are managed by supervisord, so they start at boot and respawn on crash.

```
apps:
  - name: my-app
    title: "My Application"
    install: |
      npm install -g my-app
    services:
      - name: my-app-server
        run: "my-app serve --port 8000"
        cwd: /opt/my-app
        user: root            # default: orgo (unprivileged)
        restart: always       # always | on-failure | no
        env:
          PORT: "8000"
    health:
      type: http              # http | tcp | command | process
      url: http://127.0.0.1:8000/health
      every: 15s
      timeout: 3s
      retries: 3
      on_fail: restart_service:my-app-server
    ports:
      - { internal: 8000, public: true }
    autostart:
      - { run: "firefox http://localhost:8000", delay: 3 }
```

### [​](#services) services

| Field | Description |
| --- | --- |
| `name` | Unique service name (kebab-case). **Required.** |
| `run` | The long-lived command. **Required.** |
| `cwd` / `user` / `env` | Working directory, run-as user, and extra environment variables for this service. |
| `restart` | `always` (default), `on-failure`, or `no`. |
| `stop_signal` / `log` | Stop signal (e.g. `TERM`) and log file path. |

### [​](#health) health

A polled liveness check. After `retries` consecutive failures, `on_fail` runs — this is the per-app **watchdog**.

| `type` | Checks |
| --- | --- |
| `http` | `url` returns 2xx/3xx |
| `tcp` | `port` accepts a connection |
| `command` | `command` exits `0` |
| `process` | `process` name is running |

`on_fail` is one of `restart_service:<name>`, `restart_vm`, `alert`, or `none`.

### [​](#ports) ports

| Field | Description |
| --- | --- |
| `internal` | In-VM port (1–65535). `5900`, `5999`, `6080`, `8080` are reserved. **Required.** |
| `external` | Externally mapped port (`0` = none). |
| `protocol` | `tcp`, `udp`, `http`, or `ws`. |
| `public` | Expose publicly. When `true`, the host port is returned in the computer’s `template_ports`. |

## [​](#terminal) terminal

Pre-staged tmux sessions, created detached at first boot. Orgo’s browser terminal attaches to them by name.

```
terminal:
  - name: logs
    title: "Service Logs"
    cwd: /opt/my-app
    run: "tail -F /var/log/orgo/my-app.log"
```

Sessions are **not** auto-restarted. For a process that must respawn, use an [app service](#apps) instead.

## [​](#hooks) hooks

Shell that runs at lifecycle points. Each runs with `set -e`; the default timeout is 10 minutes.

| Hook | When |
| --- | --- |
| `on_first_boot` | Once, on the VM’s first boot. |
| `on_every_boot` | Every boot, including restores. |
| `on_pre_snapshot` | Before a golden snapshot is captured. |
| `on_resume` | After restoring from a snapshot. |
| `on_shutdown` | On graceful shutdown. |

```
hooks:
  on_first_boot: |
    echo "ready" > /var/lib/orgo/stamp
  on_resume: |
    echo "restored at $(date)"
```

`on_resume` is the right place to do per-VM work that depends on launch-time state (like a freshly injected secret), because it runs on every restore — see [Secrets](/guides/templates/secrets).

## [​](#telemetry) telemetry

```
telemetry:
  metrics: true               # flag the VM as scrape-ready
  logs: [my-app-server]       # service log paths/names to ship
  otel_endpoint: https://otel.example.com   # push OTLP metrics + logs
```

## [​](#egress_policy) egress\_policy

Per-VM network filtering, enforced on the host.

```
egress_policy:
  mode: allow                 # allow = only these reachable; block = everything except these
  rules:
    - "*.github.com"
    - "api.anthropic.com"
    - "10.0.0.0/8"
```

Rules are domain patterns, exact domains, IPs, or CIDRs. The VNC and desktop API paths are always reachable.


## [​](#streaming) streaming

Outbound RTMP(S) streams of the desktop.

```
streaming:
  - name: live
    url: rtmps://ingest.example.com/app
    key:
      secret: stream_key       # literal string or a vault secret
    autostart: true
```

`streaming` is parsed and validated today; the runtime streamer is rolling out. Track status in the [JSON Schema](/api-reference/templates/schema).

## [​](#next-steps) Next steps

## Secrets

The full secret-injection model.

## Triggers

Sources, actions, and dedup.

## Examples

Annotated real templates.

## Publish API

Ship a template over HTTP.

[Previous](/guides/templates/quickstart)[SecretsLet templates require API keys without ever storing them.

Next](/guides/templates/secrets)

⌘I