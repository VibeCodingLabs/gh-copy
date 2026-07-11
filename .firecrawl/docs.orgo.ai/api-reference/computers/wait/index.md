---
url: https://docs.orgo.ai/api-reference/computers/wait
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

wait

Try it

Wait

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/wait \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "seconds": 2
}'
```

200

401

404

```
{
  "success": true
}
```

Pauses execution on the computer for the specified duration. The request blocks until the wait completes.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-seconds)

seconds

number

required

How long to pause, in seconds (0-60).

[​](#param-duration)

duration

number

deprecated

Deprecated alias for `seconds`. Accepted on input for backwards compatibility.

## [​](#response) Response

[​](#param-success)

success

boolean

`true` when the wait completes.

[​](#param-action)

action

string

Always `wait`.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/wait \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seconds": 2.0}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "action": "wait"
}
```

Use waits sparingly - prefer polling for the condition you actually care about (window focus, file change) over fixed delays.

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Invalid or out-of-range `seconds` value, or computer instance not available. |
| `401` | Missing or invalid API key. |
| `403` | You do not have access to this computer. |
| `404` | Computer not found. |
| `500` | Upstream desktop agent failure. |

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

[​](#body-seconds)

seconds

number

required

How long to pause, in seconds

Required range: `0 <= x <= 60`

[​](#body-duration)

duration

number

deprecated

Deprecated alias for `seconds`. Accepted on input for backwards compatibility.

Required range: `0 <= x <= 60`

#### Response

200

application/json

Wait completed

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/computers/scroll)[Execute bashRun a bash command on the computer and get its output.

Next](/api-reference/computers/bash)

⌘I

Wait

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/wait \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "seconds": 2
}'
```

200

401

404

```
{
  "success": true
}
```