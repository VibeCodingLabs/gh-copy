---
url: https://docs.orgo.ai/api-reference/templates/list-versions
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

templates

/

{namespace}

/

{name}

Try it

List template versions

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name} \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "versions": [
    {
      "ref": "default/claude-code@1.0.0",
      "digest": "<string>",
      "published": "2023-11-07T05:31:56Z",
      "template": {
        "api_version": "orgo.ai/v1",
        "template": {
          "name": "claude-code",
          "version": "1.0.0",
          "description": "<string>"
        },
        "hardware": {},
        "secrets": [
          {}
        ],
        "vars": {},
        "env": {},
        "build": {},
        "files": "<array>",
        "apps": "<array>",
        "triggers": "<array>",
        "terminal": "<array>",
        "hooks": {},
        "telemetry": {},
        "egress_policy": {},
        "streaming": "<array>"
      }
    }
  ]
}
```

Lists all published versions of a single template, so you can show a version history or resolve the latest.

## [​](#path-parameters) Path parameters

[​](#param-namespace)

namespace

string

required

Template namespace.

[​](#param-name)

name

string

required

Template name.

## [​](#response) Response

[​](#param-versions)

versions

array

Array of template list items, one per published version. Each has `ref`, `digest`, `published`, and the full `template` document.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/templates/default/claude-code \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "versions": [
    {
      "ref": "default/claude-code@1.0.0",
      "digest": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
      "published": "2026-06-08T17:00:00Z"
    }
  ]
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

[​](#parameter-namespace)

namespace

string

required

Template namespace.

[​](#parameter-name)

name

string

required

Template name.

#### Response

200

application/json

Versions

[​](#response-versions)

versions

object[]

Show child attributes

[Previous](/api-reference/templates/validate)[Get templateFetch a single template version and its full document.

Next](/api-reference/templates/get)

⌘I

List template versions

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name} \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "versions": [
    {
      "ref": "default/claude-code@1.0.0",
      "digest": "<string>",
      "published": "2023-11-07T05:31:56Z",
      "template": {
        "api_version": "orgo.ai/v1",
        "template": {
          "name": "claude-code",
          "version": "1.0.0",
          "description": "<string>"
        },
        "hardware": {},
        "secrets": [
          {}
        ],
        "vars": {},
        "env": {},
        "build": {},
        "files": "<array>",
        "apps": "<array>",
        "triggers": "<array>",
        "terminal": "<array>",
        "hooks": {},
        "telemetry": {},
        "egress_policy": {},
        "streaming": "<array>"
      }
    }
  ]
}
```