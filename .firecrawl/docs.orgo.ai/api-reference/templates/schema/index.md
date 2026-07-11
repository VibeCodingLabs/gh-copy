---
url: https://docs.orgo.ai/api-reference/templates/schema
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

template-schema

Try it

Get template schema

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/template-schema
```

200

```
{}
```

Returns the complete `orgo.ai/v1` template schema as [JSON Schema](https://json-schema.org/) (Draft 2020-12) — every field, its type, accepted values, and a description. This is the canonical machine-readable contract for templates, consumed by editors, the CLI, and AI agents.

This endpoint is **public**. It requires no API key, sets permissive CORS headers, and is cacheable, so any tool can fetch it directly.

## [​](#response) Response

A JSON Schema document. The top-level `properties` describe each template field; `$defs` holds the reusable sub-objects (`hardware`, `app`, `service`, `trigger`, and so on). For a guided walkthrough, see the [schema reference](/guides/templates/schema).

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/template-schema
```

### [​](#response-excerpt) Response (excerpt)

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://orgo.ai/schemas/template/orgo.ai-v1.json",
  "title": "Orgo Template (orgo.ai/v1)",
  "type": "object",
  "required": ["api_version", "template"],
  "properties": {
    "api_version": { "type": "string", "enum": ["orgo.ai/v1"] },
    "template": { "$ref": "#/$defs/metadata" },
    "hardware": { "$ref": "#/$defs/hardware" }
  }
}
```

Point your editor’s YAML language server at this URL for inline autocomplete and validation:

```
# yaml-language-server: $schema=https://www.orgo.ai/api/template-schema
api_version: orgo.ai/v1
```

#### Response

200 - application/schema+json

The orgo.ai/v1 JSON Schema document.

The response is of type `object`.

[Previous](/api-reference/files/delete)[List templatesList the templates you have published.

Next](/api-reference/templates/list)

⌘I

Get template schema

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/template-schema
```

200

```
{}
```