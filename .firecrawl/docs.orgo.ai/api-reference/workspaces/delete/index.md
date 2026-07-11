---
url: https://docs.orgo.ai/api-reference/workspaces/delete
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

DELETE

/

workspaces

/

{id}

Try it

Delete workspace

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/workspaces/{id} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true
}
```

Deletes a workspace and all its computers.

This action cannot be undone. All computers in the workspace will be permanently deleted.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Workspace ID.

## [​](#response) Response

Returns a success confirmation.

[​](#param-success)

success

boolean

`true` if deletion was successful.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X DELETE https://www.orgo.ai/api/workspaces/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "success": true
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

Workspace deleted

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/workspaces/get)[Create computerProvision a new virtual computer in a workspace.

Next](/api-reference/computers/create)

⌘I

Delete workspace

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/workspaces/{id} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true
}
```