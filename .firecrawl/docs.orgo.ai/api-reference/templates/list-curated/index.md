---
url: https://docs.orgo.ai/api-reference/templates/list-curated
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

templates

/

global

Try it

List curated templates

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/global \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "templates": [
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

Lists the curated templates Orgo builds and keeps up to date — ready-to-launch environments like Claude Code, OpenClaw, and Hermes. These are available to **every account on any plan**: you don’t need a Scale plan to launch them, only to publish your own.
To launch one, pass its `ref` as `template_ref` to [Create computer](/api-reference/computers/create).

## [​](#response) Response

[​](#param-templates)

templates

array

Array of curated template list items, each with `ref`, `digest`, `published`, and the full `template` document.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/templates/global \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "templates": [
    {
      "ref": "system/claude-code@1.0.0",
      "digest": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
      "published": "2026-06-08T17:00:00Z"
    },
    {
      "ref": "system/openclaw@1.0.0",
      "digest": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3",
      "published": "2026-06-08T17:00:00Z"
    },
    {
      "ref": "system/hermes-agent@1.0.0",
      "digest": "c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4",
      "published": "2026-06-08T17:00:00Z"
    }
  ]
}
```

To list every version of a single curated template, call `GET /templates/global/{namespace}/{name}` — e.g. `https://www.orgo.ai/api/templates/global/system/claude-code`.

## Launch a curated template

Go from a curated `ref` to a running computer in one API call.

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Response

200

application/json

Curated templates

[​](#response-templates)

templates

object[]

Show child attributes

[Previous](/api-reference/templates/build-events)[Test-run a templateBoot a short-lived preview computer from a template ref.

Next](/api-reference/templates/test-run)

⌘I

List curated templates

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/global \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "templates": [
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