---
url: https://docs.orgo.ai/api-reference/computers/click
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

click

Try it

cURL

left-click

curl --request POST \
--url https://www.orgo.ai/api/computers/{id}/click \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '
{
"x": 100,
"y": 200
}
'

200

401

404

```
{
  "success": true
}
```

Performs a mouse click at the specified coordinates.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-x)

x

integer

required

X coordinate (pixels from left edge).

[​](#param-y)

y

integer

required

Y coordinate (pixels from top edge).

[​](#param-button)

button

string

default:"left"

Mouse button: `left` or `right`.

[​](#param-double)

double

boolean

default:"false"

If `true`, performs a double-click. When `double` is set, `button` is ignored.

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if the click was performed.

[​](#param-action)

action

string

Action name: `click` or `double_click`.

## [​](#example) Example

cURL

Python

JavaScript

```
# Left click at (100, 200)
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/click \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x": 100, "y": 200}'

# Right click
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/click \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x": 100, "y": 200, "button": "right"}'

# Double click
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/click \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x": 100, "y": 200, "double": true}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "action": "click",
  "details": { "x": 100, "y": 200, "button": "left", "double": false }
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Computer instance not available (not running). |
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

[​](#body-x)

x

integer

required

X coordinate

Required range: `x >= 0`

[​](#body-y)

y

integer

required

Y coordinate

Required range: `x >= 0`

[​](#body-button)

button

enum<string>

default:left

Mouse button

Available options:

`left`,

`right`

[​](#body-double)

double

boolean

default:false

Double-click

#### Response

200

application/json

Click performed

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/computers/screenshot)[Drag mouseDrag the mouse from one screen coordinate to another.

Next](/api-reference/computers/drag)

⌘I

cURL

left-click

curl --request POST \
--url https://www.orgo.ai/api/computers/{id}/click \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '
{
"x": 100,
"y": 200
}
'

200

401

404

```
{
  "success": true
}
```