---
url: https://docs.orgo.ai/api-reference/computers/start
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

start

Try it

Start computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/start \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true,
  "status": "starting"
}
```

Starts a stopped computer. Its disk is restored — files, installed software, and configuration — and the computer boots on a freshly chosen host.

A started computer receives a **new IP address** and boots fresh: running processes and other in-memory state from before the stop are not restored, only the disk. Starting can take longer than a normal request while the saved disk is fetched and the computer cold-boots.

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

`true` if start was initiated.

Idempotent - starting an already-running computer returns success without side effects.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/start \
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
* `409` - Computer is not stopped (e.g. already running, or still being created)

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

Computer starting

[​](#response-success)

success

boolean

Example:

`true`

[​](#response-status)

status

string

Example:

`"starting"`

[Previous](/api-reference/computers/vnc-password)[Stop computerShut down a running computer.

Next](/api-reference/computers/stop)

⌘I

Start computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/start \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true,
  "status": "starting"
}
```