---
url: https://docs.orgo.ai/api-reference/templates/list
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

templates

Try it

List templates

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates \
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

Returns the templates published under your account. Each item carries the template’s `ref`, its content-addressed `digest`, the `published` timestamp, and the full template document.

Looking for the curated templates Orgo ships (Claude Code, OpenClaw, Hermes)? Use [List curated templates](/api-reference/templates/list-curated) instead.

## [​](#query-parameters) Query parameters

[​](#param-namespace)

namespace

string

Filter to a single namespace. Your own templates are published under `default` unless you choose another namespace.

## [​](#response) Response

[​](#param-templates)

templates

array

Array of template list items.

Show item

[​](#param-ref)

ref

string

Template ref, in `namespace/name@version` form.

[​](#param-digest)

digest

string

Content-addressed SHA-256 digest of the canonical template. Two semantically identical templates always share a digest.

[​](#param-published)

published

string

ISO 8601 timestamp of when the version was published.

[​](#param-template)

template

object

The full `orgo.ai/v1` document. See the [schema reference](/guides/templates/schema).

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/templates \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "templates": [
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

#### Query Parameters

[​](#parameter-namespace)

namespace

string

Filter to a single namespace. Your own templates default to `default`.

#### Response

200

application/json

Your templates

[​](#response-templates)

templates

object[]

Show child attributes

[Previous](/api-reference/templates/schema)[Publish templatePublish a template document to your registry.

Next](/api-reference/templates/publish)

⌘I

List templates

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates \
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