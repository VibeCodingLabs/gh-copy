---
url: https://docs.orgo.ai/api-reference/computers/stream-status
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

computers

/

{id}

/

stream

/

status

Try it

Get stream status

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id}/stream/status \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "status": "streaming",
  "start_time": "2024-01-15T10:30:00Z",
  "pid": 12345
}
```

Returns the current streaming status.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID.

## [​](#response) Response

[​](#param-status)

status

string

Stream status: `idle`, `streaming`, or `terminated`.

[​](#param-start-time)

start\_time

string

ISO 8601 timestamp when stream started (only if streaming).

[​](#param-pid)

pid

integer

Stream process ID (only if streaming).

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/stream/status \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#when-streaming) When streaming

```
{
  "status": "streaming",
  "start_time": "2024-01-20T10:30:00Z",
  "pid": 12345
}
```

### [​](#when-idle) When idle

```
{
  "status": "idle"
}
```

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

Stream status

[​](#response-status)

status

enum<string>

Available options:

`idle`,

`streaming`,

`terminated`

[​](#response-start-time)

start\_time

string<date-time>

[​](#response-pid)

pid

integer

[Previous](/api-reference/computers/stream-start)[Stop streamEnd an active RTMP stream.

Next](/api-reference/computers/stream-stop)

⌘I

Get stream status

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id}/stream/status \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "status": "streaming",
  "start_time": "2024-01-15T10:30:00Z",
  "pid": 12345
}
```