---
url: https://docs.orgo.ai/api-reference/templates/get
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

templates

/

{namespace}

/

{name}

/

{version}

Try it

Get template

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
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
```

Returns one template version, including the complete `orgo.ai/v1` document. Curated templates resolve here too — use their `system` namespace, e.g. `system/claude-code/1.0.0`.

## [​](#path-parameters) Path parameters

[​](#param-namespace)

namespace

string

required

Template namespace. Your own templates default to `default`.

[​](#param-name)

name

string

required

Template name.

[​](#param-version)

version

string

required

Version (semver), e.g. `1.0.0`.

## [​](#response) Response

[​](#param-ref)

ref

string

Template ref, `namespace/name@version`.

[​](#param-digest)

digest

string

Content-addressed SHA-256 digest.

[​](#param-published)

published

string

ISO 8601 publish timestamp.

[​](#param-template)

template

object

The full template document. See the [schema reference](/guides/templates/schema).

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/templates/default/claude-code/1.0.0 \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "ref": "default/claude-code@1.0.0",
  "digest": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "published": "2026-06-08T17:00:00Z",
  "template": {
    "api_version": "orgo.ai/v1",
    "template": {
      "name": "claude-code",
      "version": "1.0.0",
      "description": "Claude Code CLI, ready in the terminal."
    },
    "hardware": { "cpu": 2, "ram_gb": 4, "resolution": "1280x720x24" }
  }
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `401` | Missing or invalid API key. |
| `404` | No such template version in this namespace. |

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

[​](#parameter-name)

name

string

required

[​](#parameter-version)

version

string

required

#### Response

200

application/json

Template version

[​](#response-ref)

ref

string

Template ref, `namespace/name@version`.

Example:

`"default/claude-code@1.0.0"`

[​](#response-digest)

digest

string

Content-addressed SHA-256 digest of the canonical template. Two semantically identical templates always share a digest.

[​](#response-published)

published

string<date-time>

[​](#response-template)

template

object

An orgo.ai/v1 template document. Only `api_version` and `template` are required. See the full JSON Schema at GET /template-schema, or the schema guide at <https://docs.orgo.ai/guides/templates/schema>.

Show child attributes

[Previous](/api-reference/templates/list-versions)[Delete template versionDelete one published version from your registry.

Next](/api-reference/templates/delete)

⌘I

Get template

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
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
```