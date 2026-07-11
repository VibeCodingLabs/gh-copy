---
url: https://docs.orgo.ai/api-reference/computers/vnc-password
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

computers

/

{id}

/

vnc-password

Try it

Get VNC password

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id}/vnc-password \
  --header 'Authorization: Bearer <token>'
```

200

401

403

404

```
{
  "password": "abc123xyz"
}
```

Returns the computer password for VNC and terminal WebSocket connections.

This password provides direct access to the computer’s display and terminal. Keep it secure and do not share it publicly.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID.

## [​](#response) Response

[​](#param-password)

password

string

VNC connection password.

## [​](#access-control) Access control

This endpoint is only accessible to:

* Workspace owners
* Workspace members

Unauthorized users will receive a `403 Forbidden` response.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/vnc-password \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "password": "0a017c595fa7689753a3"
}
```

## [​](#usage) Usage

This password is used for:

1. **VNC connections** - Pass as the password when connecting via any VNC client
2. **Terminal WebSocket** - Pass as the `token` query parameter when connecting to the [Terminal WebSocket](/api-reference/computers/terminal)

For programmatic control, use the [Computer Actions](/api-reference/computers/click) endpoints instead of VNC. For interactive shell access, use the [Terminal WebSocket](/api-reference/computers/terminal).

## [​](#errors) Errors

* `401` - Invalid or missing API key
* `403` - Not a workspace owner or member
* `404` - Computer not found, or password not set

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

VNC password

[​](#response-password)

password

string

VNC connection password

[Previous](/api-reference/computers/delete)[Start computerBoot a stopped computer.

Next](/api-reference/computers/start)

⌘I

Get VNC password

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id}/vnc-password \
  --header 'Authorization: Bearer <token>'
```

200

401

403

404

```
{
  "password": "abc123xyz"
}
```