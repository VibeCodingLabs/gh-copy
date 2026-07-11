---
url: https://docs.orgo.ai/api-reference/workspaces/create
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

workspaces

Try it

Create workspace

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/workspaces \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "name": "my-workspace",
  "icon_url": "<string>",
  "status": "active"
}
'
```

201

400

401

```
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "my-workspace",
  "user_id": "4d96f9a0-7727-4b63-889a-32544c206d7c",
  "status": "active",
  "icon_url": null,
  "created_at": "2026-04-07T10:30:00Z"
}
```

Creates a new workspace to organize your computers.

Workspaces are containers for computers. Use them to separate different projects, environments, or teams.

## [​](#request) Request

[​](#param-name)

name

string

required

Workspace name. Must be unique within your account.

[​](#param-icon-url)

icon\_url

string

Optional URL of an icon for the workspace.

[​](#param-status)

status

string

default:"active"

Workspace status: `active` or `inactive`.

## [​](#response) Response

[​](#param-id)

id

string

Unique workspace identifier.

[​](#param-name-1)

name

string

Workspace name.

[​](#param-user-id)

user\_id

string

Owner user ID.

[​](#param-status-1)

status

string

Workspace status.

[​](#param-icon-url-1)

icon\_url

string

Icon URL, if set.

[​](#param-created-at)

created\_at

string

ISO 8601 timestamp.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/workspaces \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "production"}'
```

### [​](#response-2) Response

```
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "production",
  "user_id": "4d96f9a0-7727-4b63-889a-32544c206d7c",
  "status": "active",
  "icon_url": null,
  "created_at": "2026-04-07T10:30:00Z"
}
```

## [​](#errors) Errors

* `400` - Name is empty, or a workspace with this name already exists

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Body

application/json

[​](#body-name)

name

string

required

Workspace name. Must be unique within your account.

Minimum string length: `1`

Example:

`"my-workspace"`

[​](#body-icon-url)

icon\_url

string

Optional icon URL

[​](#body-status)

status

enum<string>

default:active

Available options:

`active`,

`inactive`

#### Response

201

application/json

Workspace created

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

[Previous](/api-reference/chat/threads)[List workspacesList all workspaces accessible to the API key.

Next](/api-reference/workspaces/list)

⌘I

Create workspace

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/workspaces \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "name": "my-workspace",
  "icon_url": "<string>",
  "status": "active"
}
'
```

201

400

401

```
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "my-workspace",
  "user_id": "4d96f9a0-7727-4b63-889a-32544c206d7c",
  "status": "active",
  "icon_url": null,
  "created_at": "2026-04-07T10:30:00Z"
}
```