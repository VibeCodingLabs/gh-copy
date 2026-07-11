---
url: https://docs.orgo.ai/api-reference/computers/stop
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

stop

Try it

Stop computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/stop \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true,
  "status": "stopping"
}
```

Stops a running computer. The computer’s disk is preserved — files, installed software, and configuration are all kept — and a stopped computer incurs no compute charges.

Stopping saves the computer’s disk and releases its host. When you [start](/api-reference/computers/start) it again it boots on a freshly chosen host and receives a **new IP address**. Running processes and other in-memory state from before the stop are **not** restored — the computer cold-boots from its saved disk. Only the disk is preserved.

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

`true` if stop was initiated.

Idempotent - stopping an already-stopped computer returns success without side effects.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/stop \
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
* `409` - Computer is not running (e.g. still starting, or already stopped/terminating)

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

Computer stopping

[​](#response-success)

success

boolean

Example:

`true`

[​](#response-status)

status

string

Example:

`"stopping"`

[Previous](/api-reference/computers/start)[Restart computerReboot a running computer.

Next](/api-reference/computers/restart)

⌘I

Stop computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/stop \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true,
  "status": "stopping"
}
```