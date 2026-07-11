---
url: https://docs.orgo.ai/api-reference/templates/validate
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

templates

/

validate

Try it

Validate template

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/templates/validate \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/yaml' \
  --data '"<string>"'
```

200

401

422

```
{
  "ok": true,
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
  },
  "errors": [
    {
      "field": "hardware.cpu",
      "code": "invalid_enum",
      "message": "<string>",
      "hint": "<string>"
    }
  ]
}
```

Validates a template against the `orgo.ai/v1` schema and returns either the normalized document or a structured list of errors. This endpoint has **no side effects** — nothing is written, so it is cheap enough to call on every keystroke in an editor.

## [​](#request-body) Request body

The raw template document, as YAML (`Content-Type: application/yaml`) or JSON.

## [​](#response) Response

[​](#param-ok)

ok

boolean

`true` if the template is valid.

[​](#param-template)

template

object

The normalized template (sugar expanded into canonical form). Present when `ok` is `true`.

[​](#param-errors)

errors

array

Present when `ok` is `false`. Each entry pinpoints one problem.

Show error

[​](#param-field)

field

string

Dotted path to the offending field, e.g. `hardware.cpu`.

[​](#param-code)

code

string

Machine-readable code, e.g. `invalid_enum`, `required`, `unknown_ref`.

[​](#param-message)

message

string

Human-readable explanation.

[​](#param-hint)

hint

string

Optional suggestion for fixing it.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/templates/validate \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/yaml" \
  --data-binary @claude-code.yaml
```

### [​](#response-—-valid) Response — valid

```
{
  "ok": true,
  "template": {
    "api_version": "orgo.ai/v1",
    "template": { "name": "claude-code", "version": "1.0.0" }
  }
}
```

### [​](#response-—-invalid) Response — invalid

```
{
  "ok": false,
  "errors": [
    {
      "field": "hardware.cpu",
      "code": "invalid_enum",
      "message": "cpu must be one of 1, 2, 4, 8, 16"
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

#### Body

application/yamlapplication/jsonapplication/yamlapplication/json

The body is of type `string`.

#### Response

200

application/json

Validation result

[​](#response-ok)

ok

boolean

[​](#response-template)

template

object

An orgo.ai/v1 template document. Only `api_version` and `template` are required. See the full JSON Schema at GET /template-schema, or the schema guide at <https://docs.orgo.ai/guides/templates/schema>.

Show child attributes

[​](#response-errors)

errors

object[]

Show child attributes

[Previous](/api-reference/templates/publish)[List template versionsList every published version of one template.

Next](/api-reference/templates/list-versions)

⌘I

Validate template

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/templates/validate \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/yaml' \
  --data '"<string>"'
```

200

401

422

```
{
  "ok": true,
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
  },
  "errors": [
    {
      "field": "hardware.cpu",
      "code": "invalid_enum",
      "message": "<string>",
      "hint": "<string>"
    }
  ]
}
```