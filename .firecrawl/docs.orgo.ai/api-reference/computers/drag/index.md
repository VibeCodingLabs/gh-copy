---
url: https://docs.orgo.ai/api-reference/computers/drag
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

drag

Try it

Drag mouse

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/drag \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "start_x": 100,
  "start_y": 100,
  "end_x": 300,
  "end_y": 200,
  "duration": 0.5
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

Performs a mouse drag from start to end coordinates.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-start-x)

start\_x

integer

required

Starting X coordinate.

[​](#param-start-y)

start\_y

integer

required

Starting Y coordinate.

[​](#param-end-x)

end\_x

integer

required

Ending X coordinate.

[​](#param-end-y)

end\_y

integer

required

Ending Y coordinate.

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if the drag was performed.

[​](#param-action)

action

string

Always `drag`.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/drag \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "start_x": 100,
    "start_y": 100,
    "end_x": 300,
    "end_y": 200
  }'
```

### [​](#response-2) Response

```
{
  "success": true,
  "action": "drag",
  "details": { "start_x": 100, "start_y": 100, "end_x": 300, "end_y": 200 }
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Missing required coordinate, or computer instance not available. |
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

[​](#body-start-x)

start\_x

integer

required

Start X coordinate

[​](#body-start-y)

start\_y

integer

required

Start Y coordinate

[​](#body-end-x)

end\_x

integer

required

End X coordinate

[​](#body-end-y)

end\_y

integer

required

End Y coordinate

[​](#body-button)

button

enum<string>

default:left

Mouse button

Available options:

`left`,

`right`

[​](#body-duration)

duration

number

default:0.5

Drag duration in seconds

#### Response

200

application/json

Drag performed

[​](#response-success)

success

boolean

Example:

`true`

[Previous](/api-reference/computers/click)[Type textType a string on the computer keyboard, one character at a time.

Next](/api-reference/computers/type)

⌘I

Drag mouse

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/drag \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "start_x": 100,
  "start_y": 100,
  "end_x": 300,
  "end_y": 200,
  "duration": 0.5
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