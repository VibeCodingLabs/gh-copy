---
url: https://docs.orgo.ai/api-reference/templates/publish
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

templates

Try it

Publish template

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/templates \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/yaml' \
  --data '"<string>"'
```

201

400

401

403

409

422

```
{
  "ref": "default/claude-code@1.0.0",
  "digest": "<string>",
  "published": "2023-11-07T05:31:56Z",
  "auto_build": "<string>"
}
```

Publishes a template to your registry. The request body is a complete [`orgo.ai/v1`](/guides/templates/schema) document, sent as YAML (`Content-Type: application/yaml`) or JSON (`Content-Type: application/json`).

Publishing templates requires a **Scale** plan. Every account can still launch [curated templates](/api-reference/templates/list-curated) and any template you’ve published.

**Refs are immutable.** Once `namespace/name@version` is published, re-publishing the same ref with different content returns `409`. Bump `template.version` to ship a change, or pass `?force=true` to overwrite the version in place while iterating.

## [​](#query-parameters) Query parameters

[​](#param-auto-build)

auto\_build

boolean

Build the [golden snapshot](/guides/templates/introduction#golden-snapshots) immediately after publishing. Equivalent to calling [Build template](/api-reference/templates/build) yourself.

[​](#param-force)

force

boolean

Overwrite an existing version in place (delete + republish). Useful for fast iteration on a single version number.

## [​](#request-body) Request body

The raw template document. Validate it first with [Validate template](/api-reference/templates/validate) to catch errors without writing anything.

## [​](#response) Response

[​](#param-ref)

ref

string

The published ref, `namespace/name@version`.

[​](#param-digest)

digest

string

Content-addressed SHA-256 digest of the canonical template.

[​](#param-published)

published

string

ISO 8601 publish timestamp.

[​](#param-auto-build-1)

auto\_build

string

Present only when `?auto_build=true`. The status of the build that was kicked off, e.g. `"building"`.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST "https://www.orgo.ai/api/templates?auto_build=true" \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/yaml" \
  --data-binary @claude-code.yaml
```

### [​](#response-2) Response

```
{
  "ref": "default/claude-code@1.0.0",
  "digest": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "published": "2026-06-08T17:00:00Z",
  "auto_build": "building"
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Empty body, or unparseable YAML / JSON. |
| `401` | Missing or invalid API key. |
| `403` | Publishing requires a Scale plan or higher. |
| `409` | A different template is already published at this `namespace/name@version`. Bump the version or use `?force=true`. |
| `422` | The template failed validation. The `errors` array lists each problem with its `field`, `code`, and `message`. |

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Query Parameters

[​](#parameter-auto-build)

auto\_build

boolean

Build the golden snapshot immediately after publishing.

[​](#parameter-force)

force

boolean

Overwrite an existing version in place (delete + republish). Useful while iterating on one version number.

#### Body

application/yamlapplication/jsonapplication/yamlapplication/json

The orgo.ai/v1 template document as YAML.

#### Response

201

application/json

Published

[​](#response-ref)

ref

string

Example:

`"default/claude-code@1.0.0"`

[​](#response-digest)

digest

string

[​](#response-published)

published

string<date-time>

[​](#response-auto-build)

auto\_build

string

Present only with ?auto\_build=true. The kicked-off build's status, e.g. "building".

[Previous](/api-reference/templates/list)[Validate templateCheck a template document for errors without publishing it.

Next](/api-reference/templates/validate)

⌘I

Publish template

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/templates \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/yaml' \
  --data '"<string>"'
```

201

400

401

403

409

422

```
{
  "ref": "default/claude-code@1.0.0",
  "digest": "<string>",
  "published": "2023-11-07T05:31:56Z",
  "auto_build": "<string>"
}
```