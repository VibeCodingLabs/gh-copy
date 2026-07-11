---
url: https://docs.orgo.ai/api-reference/files/delete
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

DELETE

/

files

/

delete

Try it

Delete file

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/files/delete \
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

Permanently deletes a file from storage.

This action cannot be undone.

## [​](#query-parameters) Query parameters

[​](#param-id)

id

string

required

File ID.

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if deletion was successful.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X DELETE "https://www.orgo.ai/api/files/delete?id=f47ac10b-58cc-4372-a567-0e02b2c3d479" \
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

#### Query Parameters

[​](#parameter-id)

id

string

required

File ID

#### Response

200

application/json

File deleted

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/files/download)[Get template schemaFetch the canonical orgo.ai/v1 template JSON Schema.

Next](/api-reference/templates/schema)

⌘I

Delete file

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/files/delete \
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