---
url: https://docs.orgo.ai/api-reference/computers/key
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

key

Try it

cURL

enter

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/key \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "key": "Enter"
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

Presses a key or key combination. Pass modifiers joined with `+` (for example `ctrl+shift+t`).

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-key)

key

string

required

Key or key combination to press.

### [​](#common-keys) Common keys

| Key | Description |
| --- | --- |
| `Enter` | Enter/Return key |
| `Tab` | Tab key |
| `Escape` | Escape key |
| `Backspace` | Backspace key |
| `Delete` | Delete key |
| `Up`, `Down`, `Left`, `Right` | Arrow keys |
| `Home`, `End` | Home/End keys |
| `Page_Up`, `Page_Down` | Page navigation |
| `F1`-`F12` | Function keys |

### [​](#common-combinations) Common combinations

| Combination | Description |
| --- | --- |
| `ctrl+c` | Copy |
| `ctrl+v` | Paste |
| `ctrl+a` | Select all |
| `ctrl+s` | Save |
| `alt+Tab` | Switch windows |
| `alt+F4` | Close window |
| `ctrl+shift+t` | Reopen closed tab |

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if the key was pressed.

[​](#param-action)

action

string

Always `key_press`.

## [​](#example) Example

cURL

Python

JavaScript

```
# Press Enter
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/key \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key": "Enter"}'

# Ctrl+C
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/key \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key": "ctrl+c"}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "action": "key_press",
  "details": { "key": "Enter" }
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Missing `key`, or computer instance not available. |
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

[​](#body-key)

key

string

required

Key or key combination (e.g., Enter, Tab, ctrl+c, alt+F4)

Example:

`"Enter"`

#### Response

200

application/json

Key pressed

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/computers/type)[ScrollScroll the mouse wheel up or down.

Next](/api-reference/computers/scroll)

⌘I

cURL

enter

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/key \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "key": "Enter"
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