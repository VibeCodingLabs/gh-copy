---
url: https://docs.orgo.ai/api-reference/computers/delete
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

DELETE

/

computers

/

{id}

Try it

Delete computer

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/computers/{id} \
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

Permanently deletes a computer and all its data.

This action cannot be undone. All files and state will be lost.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID.

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
curl -X DELETE https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002 \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "success": true
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

Computer deleted

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/computers/resize)[Get VNC passwordGet the VNC password used to connect to the computer.

Next](/api-reference/computers/vnc-password)

⌘I

Delete computer

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/computers/{id} \
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