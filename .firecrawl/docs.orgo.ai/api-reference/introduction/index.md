---
url: https://docs.orgo.ai/api-reference/introduction
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

The Orgo API lets you provision virtual computers and control them programmatically. Build AI agent fleets, automation workflows, or browser testing at scale.

## [​](#base-url) Base URL

```
https://www.orgo.ai/api
```

## [​](#authentication) Authentication

All requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer sk_live_...
```

Get your API key at [orgo.ai/start](https://www.orgo.ai/start).

## [​](#quick-start) Quick start

### [​](#1-create-a-workspace) 1. Create a workspace

Workspaces organize your computers.

```
curl -X POST https://www.orgo.ai/api/workspaces \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-workspace"}'
```

### [​](#2-create-a-computer) 2. Create a computer

```
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "agent-1",
    "os": "linux",
    "ram": 4,
    "cpu": 1
  }'
```

### [​](#3-control-the-computer) 3. Control the computer

```
# Take a screenshot
curl https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/screenshot \
  -H "Authorization: Bearer $ORGO_API_KEY"

# Click at coordinates
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/click \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x": 100, "y": 200}'

# Type text
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/type \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!"}'

# Run bash command
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la"}'
```

## [​](#resource-hierarchy) Resource hierarchy

```
User
└── Workspaces
    └── Computers
```

Workspaces group related computers together. Use them to separate environments (production, staging) or projects.

## [​](#computer-specs) Computer specs

| Parameter | Options | Default |
| --- | --- | --- |
| `os` | `linux` | `linux` |
| `cpu` | 1, 2, 4, 8, 16 cores | 1 |
| `ram` | 4, 8, 16, 32, 64 GB | 4 |
| `disk_size_gb` | up to plan limit | 8 |
| `resolution` | `WIDTHxHEIGHTxDEPTH` (e.g., `1024x768x24`, `1920x1080x24`) | `1280x720x24` |

Maximum CPU/RAM/disk per computer is capped by your plan. See <https://orgo.ai/pricing>.

### [​](#recommended-configurations) Recommended configurations

| RAM | CPU | Best for |
| --- | --- | --- |
| 4 GB | 1 core | Standard workflows (default) |
| 8 GB | 2 cores | Heavier automation |
| 16 GB | 4 cores | Development |
| 32 GB | 8 cores | Large-scale processing |

## [​](#available-actions) Available actions

### [​](#mouse) Mouse

* Click (left, right, double)
* Drag
* Scroll

### [​](#keyboard) Keyboard

* Type text
* Press keys (Enter, Tab, ctrl+c, etc.)

### [​](#execution) Execution

* Bash commands
* Python code

### [​](#real-time-websocket) Real-time (WebSocket)

* [Terminal](/api-reference/computers/terminal) - interactive PTY shell
* [Audio](/api-reference/computers/audio) - live PCM audio stream from the VM’s virtual speaker
* [Events](/api-reference/computers/events) - subscribe to window, clipboard, file, process, and idle events

### [​](#lifecycle) Lifecycle

* Start, stop, restart
* Auto-stop (optional, opt-in per computer)
* Clone (copy a computer with full disk state)
* Resize (live CPU/RAM/disk hot-resize)
* Move (transfer between workspaces)

### [​](#other) Other

* Screenshots
* Wait/delays
* RTMP streaming

## [​](#templates) Templates

[Templates](/guides/templates/introduction) are reproducible computers defined in a single `orgo.ai/v1` file — hardware, installed apps, long-running services, secrets, and lifecycle hooks. Orgo builds the file once into a golden snapshot, and every launch restores from it in seconds.

* **Launch a curated template** — pass a `system/…` ref as `template_ref` to [Create computer](/api-reference/computers/create). Works on any paid plan.
* **Author your own** — [validate](/api-reference/templates/validate), [publish](/api-reference/templates/publish), and [build](/api-reference/templates/build) over HTTP (Scale plan). Start at the [Templates API](/api-reference/templates/schema).

## [​](#resource-ids) Resource IDs

Every Orgo resource is identified by a UUID. Pass the UUID in the URL
path wherever you see `{id}` - e.g., `/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/click`.
Workspace and computer UUIDs are returned in the `id` field of every
create / get / list response.

## [​](#error-responses) Error responses

All errors return a JSON object with an `error` field:

```
{
  "error": "Invalid API key"
}
```

| Status | Meaning |
| --- | --- |
| `200` | Success |
| `207` | Partial success (resize only - some dimensions applied, others rejected) |
| `400` | Invalid request - bad JSON, missing required field, out-of-range value |
| `401` | Missing or invalid API key |
| `403` | Authenticated, but not allowed - plan limit exceeded or no access to the resource |
| `404` | Resource not found, or you don’t have access to it |
| `405` | Method not allowed - check the verb for the endpoint |
| `409` | Conflict - resource is in a state that blocks this operation (e.g. stopping a stopped computer) |
| `422` | Validation failed - all dimensions of a resize were rejected |
| `429` | Rate limited - back off and retry |
| `500` | Unexpected server error |

## [​](#rate-limits) Rate limits

API requests are rate limited per API key. If you hit `429`, back off with
exponential retry (start at 1s, double each retry, max 60s). Email
[spencer@orgo.ai](mailto:spencer@orgo.ai) if you need higher limits.

## [​](#next-steps) Next steps

## Create Workspace

Organize computers

## Create Computer

Provision a VM

## Templates

Reproducible computers

## Authentication

API key setup

## Use Any Model

Claude, GPT, Gemini, and more

[AuthenticationAPI key setup, scopes, and rotation

Next](/api-reference/authentication)

⌘I