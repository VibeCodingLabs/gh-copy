---
url: https://docs.orgo.ai/api-reference/computers/get
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

computers

/

{id}

Try it

Get computer

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "name": "agent-1",
  "project_name": "production",
  "os": "linux",
  "ram": 4,
  "cpu": 1,
  "disk_size_gb": 8,
  "status": "running",
  "url": "https://orgo.ai/workspaces/a3bb189e-8bf9-3888-9912-ace4e6543002",
  "created_at": "2023-11-07T05:31:56Z",
  "instance_id": "a3881618",
  "hostname": "www.orgo.ai",
  "connection_url": "https://www.orgo.ai/desktops/a3881618",
  "vnc_password": "a06db12a8683df96"
}
```

Returns computer details including current status.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#response) Response

[​](#param-id-1)

id

string

Computer identifier (UUID).

[​](#param-name)

name

string

Computer name.

[​](#param-project-name)

project\_name

string

Name of the parent workspace.

[​](#param-os)

os

string

Operating system.

[​](#param-ram)

ram

integer

RAM in GB.

[​](#param-cpu)

cpu

integer

CPU cores.

[​](#param-status)

status

string

One of `creating`, `starting`, `running`, `stopping`, `stopped`, `restarting`, `deleting`, `error`.

[​](#param-url)

url

string

Dashboard URL.

[​](#param-created-at)

created\_at

string

ISO 8601 timestamp.

[​](#param-instance-id)

instance\_id

string

Stable identifier for the underlying compute instance. Use this to construct the `hostname`.

[​](#param-hostname)

hostname

string

Same-origin host for the computer’s connection endpoints (`www.orgo.ai`).

[​](#param-connection-url)

connection\_url

string

Same-origin connection base (`https://www.orgo.ai/desktops/{instance_id}`). Append `/ws/websockify`, `/ws/terminal`, or `/ws/audio` for the WebSocket endpoints; HTTP Desktop API calls go to `https://www.orgo.ai/api/desktops/{instance_id}/proxy/{endpoint}`.

[​](#param-vnc-password)

vnc\_password

string

Current VNC / WebSocket token. Rotates on restart.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002 \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "name": "agent-1",
  "project_name": "production",
  "os": "linux",
  "ram": 4,
  "cpu": 1,
  "status": "running",
  "url": "https://orgo.ai/workspaces/a3bb189e-8bf9-3888-9912-ace4e6543002",
  "created_at": "2026-04-07T10:35:00Z"
}
```

## [​](#errors) Errors

* `401` - Invalid or missing API key
* `403` - You don’t have access to this computer
* `404` - Computer not found

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Path Parameters

[​](#parameter-id)

id

string

required

Computer ID

#### Response

200

application/json

Computer details

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

[Previous](/api-reference/computers/create)[Clone computerDuplicate a computer, preserving its disk state.

Next](/api-reference/computers/clone)

⌘I

Get computer

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "name": "agent-1",
  "project_name": "production",
  "os": "linux",
  "ram": 4,
  "cpu": 1,
  "disk_size_gb": 8,
  "status": "running",
  "url": "https://orgo.ai/workspaces/a3bb189e-8bf9-3888-9912-ace4e6543002",
  "created_at": "2023-11-07T05:31:56Z",
  "instance_id": "a3881618",
  "hostname": "www.orgo.ai",
  "connection_url": "https://www.orgo.ai/desktops/a3881618",
  "vnc_password": "a06db12a8683df96"
}
```