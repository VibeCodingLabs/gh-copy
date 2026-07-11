---
url: https://docs.orgo.ai/api-reference/computers/clone
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

clone

Try it

Clone computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/clone \
  --header 'Authorization: Bearer <token>'
```

201

401

403

404

```
{
  "id": "<string>",
  "name": "agent-1 (clone)",
  "status": "running"
}
```

Creates a copy of an existing computer with the same disk state, name suffixed with `(clone)`. Useful for branching off from a configured base.

Cloning preserves the full disk state - installed software, files, browser sessions, everything. The clone gets a new ID and a fresh network identity.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Source computer ID.

## [​](#response) Response

[​](#param-id-1)

id

string

New computer ID.

[​](#param-name)

name

string

Clone name (e.g., `agent-1 (clone)` or `agent-1 (clone 2)`).

[​](#param-status)

status

string

Clone status - typically `running` immediately after creation.

## [​](#plan-limits) Plan limits

Cloning counts toward your plan’s computer limit. If you’re at your limit, the request returns `403`. Upgrade your plan or delete a computer first.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/clone \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "id": "b4cc290f-9bf9-3888-9912-ace4e6543003",
  "name": "agent-1 (clone)",
  "status": "running"
}
```

## [​](#errors) Errors

* `400` - Source computer has no server address (cannot clone)
* `401` - Invalid or missing API key
* `403` - You don’t have access to this computer, or plan limit reached
* `404` - Source computer not found

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

Source computer ID

#### Response

201

application/json

Clone created

[​](#response-id)

id

string

[​](#response-name)

name

string

Example:

`"agent-1 (clone)"`

[​](#response-status)

status

string

Example:

`"running"`

[Previous](/api-reference/computers/get)[Move computerMove a computer to a different workspace while preserving its state and ID.

Next](/api-reference/computers/move)

⌘I

Clone computer

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/clone \
  --header 'Authorization: Bearer <token>'
```

201

401

403

404

```
{
  "id": "<string>",
  "name": "agent-1 (clone)",
  "status": "running"
}
```