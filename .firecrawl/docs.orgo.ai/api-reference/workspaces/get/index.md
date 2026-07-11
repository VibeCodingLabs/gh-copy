---
url: https://docs.orgo.ai/api-reference/workspaces/get
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

workspaces

/

{id}

Try it

Get workspace

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/workspaces/{id} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "production",
  "user_id": "<string>",
  "status": "active",
  "icon_url": "<string>",
  "created_at": "2023-11-07T05:31:56Z",
  "updated_at": "2023-11-07T05:31:56Z",
  "desktops": [
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
  ]
}
```

Returns a workspace by ID, including its computers (`desktops`).

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Workspace ID.

## [​](#response) Response

[​](#param-id-1)

id

string

Workspace identifier.

[​](#param-name)

name

string

Workspace name.

[​](#param-user-id)

user\_id

string

Owner user ID.

[​](#param-status)

status

string

Workspace status.

[​](#param-icon-url)

icon\_url

string

Icon URL, if set.

[​](#param-created-at)

created\_at

string

ISO 8601 timestamp.

[​](#param-updated-at)

updated\_at

string

ISO 8601 timestamp.

[​](#param-desktops)

desktops

array

Computers in this workspace.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/workspaces/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "production",
  "user_id": "4d96f9a0-7727-4b63-889a-32544c206d7c",
  "status": "active",
  "icon_url": null,
  "created_at": "2026-04-07T10:30:00Z",
  "updated_at": "2026-04-07T10:30:00Z",
  "desktops": [
    {
      "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
      "name": "agent-1",
      "os": "linux",
      "ram": 4,
      "cpu": 1,
      "status": "running"
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "name": "agent-2",
      "os": "linux",
      "ram": 8,
      "cpu": 2,
      "status": "stopped"
    }
  ]
}
```

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

Workspace ID

#### Response

200

application/json

Workspace details

[​](#response-id)

id

string

Unique workspace identifier

Example:

`"550e8400-e29b-41d4-a716-446655440000"`

[​](#response-name)

name

string

Workspace name

Example:

`"production"`

[​](#response-user-id)

user\_id

string

Owner user ID

[​](#response-status)

status

enum<string>

Available options:

`active`,

`inactive`

Example:

`"active"`

[​](#response-icon-url-one-of-0)

icon\_url

string | null

Optional icon URL

[​](#response-created-at)

created\_at

string<date-time>

[​](#response-updated-at)

updated\_at

string<date-time>

[​](#response-desktops)

desktops

object[]

Show child attributes

[Previous](/api-reference/workspaces/list)[Delete workspaceDelete a workspace and all its computers.

Next](/api-reference/workspaces/delete)

⌘I

Get workspace

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/workspaces/{id} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "production",
  "user_id": "<string>",
  "status": "active",
  "icon_url": "<string>",
  "created_at": "2023-11-07T05:31:56Z",
  "updated_at": "2023-11-07T05:31:56Z",
  "desktops": [
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
  ]
}
```