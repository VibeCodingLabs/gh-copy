---
url: https://docs.orgo.ai/api-reference/workspaces/list
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

workspaces

Try it

List workspaces

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/workspaces \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "workspaces": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "production",
      "user_id": "4d96f9a0-7727-4b63-889a-32544c206d7c",
      "status": "active",
      "icon_url": null,
      "created_at": "2026-04-07T10:30:00Z",
      "updated_at": "2026-04-07T10:30:00Z",
      "desktops": []
    }
  ]
}
```

Returns all workspaces owned by or shared with the authenticated user. Each workspace includes its computers (`desktops`).

## [​](#response) Response

[​](#param-workspaces)

workspaces

array

Array of workspace objects, each containing its `desktops`.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/workspaces \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "workspaces": [
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
        }
      ]
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

#### Response

200

application/json

List of workspaces

[​](#response-workspaces)

workspaces

object[]

Show child attributes

[Previous](/api-reference/workspaces/create)[Get workspaceRetrieve a workspace by ID.

Next](/api-reference/workspaces/get)

⌘I

List workspaces

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/workspaces \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "workspaces": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "production",
      "user_id": "4d96f9a0-7727-4b63-889a-32544c206d7c",
      "status": "active",
      "icon_url": null,
      "created_at": "2026-04-07T10:30:00Z",
      "updated_at": "2026-04-07T10:30:00Z",
      "desktops": []
    }
  ]
}
```