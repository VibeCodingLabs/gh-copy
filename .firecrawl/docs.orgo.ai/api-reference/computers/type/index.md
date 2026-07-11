---
url: https://docs.orgo.ai/api-reference/computers/type
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

type

Try it

Type text

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/type \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "text": "Hello, world!"
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

Types text on the computer keyboard. Each character is sent as an individual keystroke, so unicode characters and printable symbols are supported.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-text)

text

string

required

Text to type. Supports unicode characters.

[​](#param-delay-ms)

delay\_ms

integer

default:"12"

Delay between keystrokes in milliseconds. Lower values type faster; higher values can help with flaky inputs.

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if text was typed.

[​](#param-action)

action

string

Always `type`.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/type \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!"}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "action": "type",
  "details": { "text_length": 13 }
}
```

Use [Press key](/api-reference/computers/key) for special keys like Enter, Tab, or keyboard shortcuts.

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Missing `text`, or computer instance not available. |
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

[​](#body-text)

text

string

required

Text to type

#### Response

200

application/json

Text typed

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/computers/drag)[Press keyPress a single key or a key combination like ctrl+c.

Next](/api-reference/computers/key)

⌘I

Type text

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/type \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "text": "Hello, world!"
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