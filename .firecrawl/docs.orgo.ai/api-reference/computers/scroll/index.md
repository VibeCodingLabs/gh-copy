---
url: https://docs.orgo.ai/api-reference/computers/scroll
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

scroll

Try it

Scroll

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/scroll \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "direction": "down",
  "amount": 3
}
'
```

200

401

404

```
{
  "success": true
}
```

Scrolls the mouse wheel up or down at the cursor’s current position (or at `x`, `y` if provided).

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-direction)

direction

string

default:"down"

Scroll direction: `up` or `down`.

[​](#param-amount)

amount

integer

default:"1"

Number of scroll clicks.

[​](#param-x)

x

integer

Optional X coordinate to move the cursor to before scrolling.

[​](#param-y)

y

integer

Optional Y coordinate to move the cursor to before scrolling.

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if the scroll was performed.

[​](#param-action)

action

string

Always `scroll`.

## [​](#example) Example

cURL

Python

JavaScript

```
# Scroll down 3 clicks
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/scroll \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"direction": "down", "amount": 3}'

# Scroll up 10 clicks
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/scroll \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"direction": "up", "amount": 10}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "action": "scroll",
  "details": { "direction": "down", "amount": 3 }
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Computer instance not available. |
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

[​](#body-direction)

direction

enum<string>

required

Scroll direction

Available options:

`up`,

`down`

[​](#body-amount)

amount

integer

default:3

Scroll amount (clicks)

Required range: `x >= 1`

#### Response

200

application/json

Scroll performed

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/computers/key)[WaitPause execution for up to 60 seconds - useful between actions.

Next](/api-reference/computers/wait)

⌘I

Scroll

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/scroll \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "direction": "down",
  "amount": 3
}
'
```

200

401

404

```
{
  "success": true
}
```