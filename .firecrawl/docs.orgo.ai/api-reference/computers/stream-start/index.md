---
url: https://docs.orgo.ai/api-reference/computers/stream-start
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

stream

/

start

Try it

Start stream

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/stream/start \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "connection_name": "twitch"
}
'
```

200

401

404

```
{
  "success": true,
  "status": "<string>",
  "pid": 123
}
```

Starts streaming the computer’s display via RTMP.

Before using this endpoint, configure an RTMP connection in your [account settings](https://www.orgo.ai/settings).

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID.

## [​](#request) Request

[​](#param-connection-name)

connection\_name

string

required

Name of the configured RTMP connection.

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if stream started.

[​](#param-status)

status

string

Stream status: `streaming`.

[​](#param-pid)

pid

integer

Stream process ID.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/stream/start \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"connection_name": "twitch"}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "status": "streaming",
  "pid": 12345
}
```

## [​](#use-cases) Use cases

* Live demonstrations of AI agents
* Recording automation workflows
* Debugging and monitoring agent behavior
* Creating content for tutorials

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

[​](#body-connection-name)

connection\_name

string

required

Name of the configured RTMP connection

#### Response

200

application/json

Stream started

[​](#response-success)

success

boolean

[​](#response-status)

status

string

[​](#response-pid)

pid

integer

Stream process ID

[Previous](/api-reference/computers/events)[Get stream statusCheck whether an RTMP stream is currently active.

Next](/api-reference/computers/stream-status)

⌘I

Start stream

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/stream/start \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "connection_name": "twitch"
}
'
```

200

401

404

```
{
  "success": true,
  "status": "<string>",
  "pid": 123
}
```