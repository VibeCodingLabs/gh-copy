---
url: https://docs.orgo.ai/api-reference/computers/move
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

PATCH

/

computers

/

{id}

/

move

Try it

Move computer to another workspace

cURL

```
curl --request PATCH \
  --url https://www.orgo.ai/api/computers/{id}/move \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "workspace_id": "<string>",
  "project_id": "<string>"
}
'
```

200

401

403

404

```
{
  "success": true,
  "workspace_id": "<string>",
  "project_id": "<string>"
}
```

Moves a computer to a different workspace within your account. The computer keeps its state, configuration, and ID - only its parent workspace changes. You must own both the source and destination workspaces.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer UUID.

## [​](#body-parameters) Body parameters

[​](#param-project-id)

project\_id

string

required

ID of the destination workspace. Must be owned by the same user. (Workspaces are still referred to as `project_id` on this endpoint for backwards compatibility.)

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if the move succeeded.

[​](#param-project-id-1)

project\_id

string

The destination workspace ID.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X PATCH https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/move \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "550e8400-e29b-41d4-a716-446655440099"}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "project_id": "550e8400-e29b-41d4-a716-446655440099"
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | `project_id` missing, or the computer is already in that workspace. |
| `401` | Missing or invalid API key. |
| `403` | You do not own the source and/or destination workspace. |
| `404` | Computer not found. |
| `500` | Internal error while updating the database. |

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

#### Body

application/json

[​](#body-workspace-id)

workspace\_id

string

required

Destination workspace ID

[​](#body-project-id)

project\_id

string

deprecated

Deprecated alias for `workspace_id`. Accepted on input for backwards compatibility.

#### Response

200

application/json

Computer moved

[​](#response-success)

success

boolean

Example:

`true`

[​](#response-workspace-id)

workspace\_id

string

[​](#response-project-id)

project\_id

string

deprecated

Deprecated alias for `workspace_id`.

[Previous](/api-reference/computers/clone)[Resize computerChange CPU, RAM, disk, or bandwidth on a running computer.

Next](/api-reference/computers/resize)

⌘I

Move computer to another workspace

cURL

```
curl --request PATCH \
  --url https://www.orgo.ai/api/computers/{id}/move \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "workspace_id": "<string>",
  "project_id": "<string>"
}
'
```

200

401

403

404

```
{
  "success": true,
  "workspace_id": "<string>",
  "project_id": "<string>"
}
```