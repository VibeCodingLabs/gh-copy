---
url: https://docs.orgo.ai/api-reference/computers/restart
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

restart

Try it

Restart computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/restart \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true,
  "status": "restarting"
}
```

Restarts a computer. Equivalent to stop + start.

A small number of legacy hosts are still being migrated to the new VMM. On those hosts this endpoint may return `405 Method Not Allowed`. Fall back to calling stop followed by start if you hit this.

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

`true` if restart was initiated.

## [​](#use-cases) Use cases

* Recover from a hung or unresponsive state
* Clear temporary files and caches
* Reset the running environment

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/restart \
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
* `405` - Not supported on legacy hosts (rare; use stop + start)

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

Computer restarting

[​](#response-success)

success

boolean

Example:

`true`

[​](#response-status)

status

string

Example:

`"restarting"`

[Previous](/api-reference/computers/stop)[Take screenshotCapture the current desktop as a PNG and return a signed URL.

Next](/api-reference/computers/screenshot)

⌘I

Restart computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/restart \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "success": true,
  "status": "restarting"
}
```