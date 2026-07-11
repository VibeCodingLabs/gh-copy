---
url: https://docs.orgo.ai/api-reference/computers/create
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

Try it

Create computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "agent-1",
  "os": "linux",
  "ram": 4,
  "cpu": 1
}
'
```

201

400

401

404

```
{
  "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "name": "agent-1",
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "os": "linux",
  "ram": 4,
  "cpu": 1,
  "status": "running",
  "url": "https://orgo.ai/workspaces/a3bb189e-8bf9-3888-9912-ace4e6543002",
  "created_at": "2026-04-07T10:35:00Z",
  "instance_id": "a3881618",
  "hostname": "www.orgo.ai",
  "connection_url": "https://www.orgo.ai/desktops/a3881618",
  "vnc_password": "a06db12a8683df96"
}
```

Creates a new virtual computer in a workspace. The computer starts automatically after creation.

Computers boot in under 500ms and come pre-configured with a desktop environment, browser, and common tools.

## [​](#request) Request

[​](#param-workspace-id)

workspace\_id

string

required

ID of the workspace to create the computer in.

[​](#param-name)

name

string

required

Computer name. Must be unique within the workspace.

[​](#param-os)

os

string

default:"linux"

Operating system. Currently only `linux` is supported.

[​](#param-ram)

ram

integer

default:"4"

RAM in GB: `4`, `8`, `16`, `32`, or `64`. Capped by your plan’s per-computer limit.

[​](#param-cpu)

cpu

integer

default:"1"

CPU cores: `1`, `2`, `4`, `8`, or `16`. Capped by your plan’s per-computer limit.

[​](#param-disk-size-gb)

disk\_size\_gb

integer

default:"8"

Disk size in GB. Defaults to 8 GB. Capped by your plan’s per-computer limit.

[​](#param-resolution)

resolution

string

default:"1280x720x24"

Display resolution in `WIDTHxHEIGHTxDEPTH` format (e.g., `1024x768x24`, `1920x1080x24`).

[​](#param-template-ref)

template\_ref

string

Launch from a [template](/guides/templates/introduction)’s golden snapshot instead of a base image, so the computer boots fully configured. Format `namespace/name@version` — e.g. `system/claude-code@1.0.0` (curated) or `default/my-template@1.0.0` (your own). The hardware fields above override the template’s defaults; the template’s build must be `ready`.

### [​](#common-configurations) Common configurations

| RAM | CPU | Best for |
| --- | --- | --- |
| 4 GB | 1 core | Standard workflows (default) |
| 8 GB | 2 cores | Heavier automation |
| 16 GB | 4 cores | Development, memory-intensive tasks |
| 32 GB | 8 cores | Large-scale processing |
| 64 GB | 16 cores | Enterprise workloads |

Maximum CPU/RAM per computer is capped by your plan. See <https://orgo.ai/pricing>.

## [​](#response) Response

Returns the created computer object.

[​](#param-id)

id

string

Unique computer identifier.

[​](#param-name-1)

name

string

Computer name.

[​](#param-workspace-id-1)

workspace\_id

string

Parent workspace ID.

[​](#param-os-1)

os

string

Operating system.

[​](#param-ram-1)

ram

integer

RAM in GB.

[​](#param-cpu-1)

cpu

integer

CPU cores.

[​](#param-resolution-1)

resolution

string

Display resolution in `WIDTHxHEIGHTxDEPTH` format.

[​](#param-status)

status

string

One of `creating`, `starting`, `running`, `stopping`, `stopped`, `restarting`, `deleting`, `error`.

[​](#param-url)

url

string

URL to view the computer in the dashboard.

[​](#param-created-at)

created\_at

string

ISO 8601 timestamp.

[​](#param-instance-id)

instance\_id

string

Stable identifier for the underlying compute instance. Use this to construct the `hostname` and to reference the VM across restarts.

[​](#param-hostname)

hostname

string

Same-origin host for the computer’s connection endpoints. Always `www.orgo.ai`.

[​](#param-connection-url)

connection\_url

string

Same-origin connection base (`https://www.orgo.ai/desktops/{instance_id}`). Append `/ws/websockify`, `/ws/terminal`, or `/ws/audio` for the WebSocket endpoints; HTTP Desktop API calls go to `https://www.orgo.ai/api/desktops/{instance_id}/proxy/{endpoint}`.

[​](#param-vnc-password)

vnc\_password

string

VNC / Bearer token for the computer’s WebSocket APIs (VNC, terminal, bash, audio, events). **Rotates on every restart** - do not persist across restarts; use a fresh value from the latest `POST /computers` or `GET /computers/{id}`.

**Fast path: 1 API call.** The response above contains everything needed to connect - no follow-up `GET /computers/{id}` or `GET /computers/{id}/vnc-password` is required. Just poll `https://www.orgo.ai/api/desktops/{instance_id}/proxy/health` until it returns 200 (~300 ms with golden snapshots), then connect.

## [​](#example) Example

cURL

Python

JavaScript

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

### [​](#response-2) Response

```
{
  "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "name": "agent-1",
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "os": "linux",
  "ram": 4,
  "cpu": 1,
  "resolution": "1280x720x24",
  "status": "running",
  "url": "https://orgo.ai/workspaces/550e8400-e29b-41d4-a716-446655440000/computers/a3bb189e-8bf9-3888-9912-ace4e6543002",
  "created_at": "2026-04-07T10:35:00Z",
  "instance_id": "a3881618",
  "hostname": "www.orgo.ai",
  "connection_url": "https://www.orgo.ai/desktops/a3881618",
  "vnc_password": "a06db12a8683df96"
}
```

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Body

application/json

[​](#body-workspace-id)

workspace\_id

string

required

ID of the workspace to create the computer in

Example:

`"550e8400-e29b-41d4-a716-446655440000"`

[​](#body-name)

name

string

required

Computer name

Minimum string length: `1`

Example:

`"agent-1"`

[​](#body-os)

os

enum<string>

default:linux

Operating system

Available options:

`linux`

[​](#body-cpu)

cpu

enum<integer>

default:1

CPU cores. Capped by plan.

Available options:

`1`,

`2`,

`4`,

`8`,

`16`

[​](#body-ram)

ram

enum<integer>

default:4

RAM in GB. Capped by plan.

Available options:

`4`,

`8`,

`16`,

`32`,

`64`

[​](#body-disk-size-gb)

disk\_size\_gb

integer

default:8

Disk size in GB. Capped by plan.

[​](#body-resolution)

resolution

string

default:1280x720x24

Display resolution in WIDTHxHEIGHTxDEPTH format

Example:

`"1280x720x24"`

[​](#body-template-ref)

template\_ref

string

Launch from a template's golden snapshot instead of a base image. Format `namespace/name@version`, e.g. `system/claude-code@1.0.0` (curated) or `default/my-template@1.0.0` (your own). The hardware fields above override the template's defaults. The template's build must be `ready`.

Example:

`"system/claude-code@1.0.0"`

#### Response

201

application/json

Computer created

[​](#response-id)

id

string

Unique computer identifier

Example:

`"a3bb189e-8bf9-3888-9912-ace4e6543002"`

[​](#response-name)

name

string

Computer name

Example:

`"agent-1"`

[​](#response-project-name)

project\_name

string

Name of the parent workspace

Example:

`"production"`

[​](#response-os)

os

enum<string>

Operating system

Available options:

`linux`

Example:

`"linux"`

[​](#response-ram)

ram

enum<integer>

RAM in GB

Available options:

`4`,

`8`,

`16`,

`32`,

`64`

Example:

`4`

[​](#response-cpu)

cpu

enum<integer>

CPU cores

Available options:

`1`,

`2`,

`4`,

`8`,

`16`

Example:

`1`

[​](#response-disk-size-gb)

disk\_size\_gb

integer

Disk size in GB

Example:

`8`

[​](#response-status)

status

enum<string>

Current status

Available options:

`creating`,

`starting`,

`running`,

`stopping`,

`stopped`,

`restarting`,

`deleting`,

`error`

Example:

`"running"`

[​](#response-url)

url

string

Dashboard URL for the computer

Example:

`"https://orgo.ai/workspaces/a3bb189e-8bf9-3888-9912-ace4e6543002"`

[​](#response-created-at)

created\_at

string<date-time>

[​](#response-instance-id)

instance\_id

string

Stable identifier for the underlying compute instance. Use this for proxy hostnames and for any client that needs to reference the VM across restarts.

Example:

`"a3881618"`

[​](#response-hostname)

hostname

string

Same-origin host for the computer's connection endpoints (always `www.orgo.ai`).

Example:

`"www.orgo.ai"`

[​](#response-connection-url)

connection\_url

string

Same-origin connection base ([https://www.orgo.ai/desktops/{instance\_id}](https://www.orgo.ai/desktops/%7Binstance_id%7D)). Append /ws/websockify, /ws/terminal, or /ws/audio for WebSocket endpoints; HTTP Desktop API calls go to [https://www.orgo.ai/api/desktops/{instance\_id}/proxy/{endpoint}](https://www.orgo.ai/api/desktops/%7Binstance_id%7D/proxy/%7Bendpoint%7D).

Example:

`"https://www.orgo.ai/desktops/a3881618"`

[​](#response-vnc-password)

vnc\_password

string

VNC / WebSocket Bearer token. Rotates on every restart - do not persist across restarts.

Example:

`"a06db12a8683df96"`

[Previous](/api-reference/workspaces/delete)[Get computerRetrieve a computer by ID.

Next](/api-reference/computers/get)

⌘I

Create computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "agent-1",
  "os": "linux",
  "ram": 4,
  "cpu": 1
}
'
```

201

400

401

404

```
{
  "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "name": "agent-1",
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "os": "linux",
  "ram": 4,
  "cpu": 1,
  "status": "running",
  "url": "https://orgo.ai/workspaces/a3bb189e-8bf9-3888-9912-ace4e6543002",
  "created_at": "2026-04-07T10:35:00Z",
  "instance_id": "a3881618",
  "hostname": "www.orgo.ai",
  "connection_url": "https://www.orgo.ai/desktops/a3881618",
  "vnc_password": "a06db12a8683df96"
}
```