---
url: https://docs.orgo.ai/api-reference/computers/stream-stop
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

stream

/

stop

Try it

Stop stream

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/stream/stop \
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

Stops an active RTMP stream.

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

`true` if stream was stopped.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/stream/stop \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "success": true
}
```

Always stop streams when done to free resources.

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

Stream stopped

[​](#response-success)

success

boolean

[Previous](/api-reference/computers/stream-status)[Upload fileUpload a file and sync it to running computers.

Next](/api-reference/files/upload)

⌘I

Stop stream

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/stream/stop \
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