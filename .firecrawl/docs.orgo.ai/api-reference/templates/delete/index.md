---
url: https://docs.orgo.ai/api-reference/templates/delete
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

DELETE

/

templates

/

{namespace}

/

{name}

/

{version}

Try it

Delete template version

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "deleted": true
}
```

Deletes a single published version you own. To replace a version in place instead of deleting it, re-publish with [`?force=true`](/api-reference/templates/publish).

Deleting a version that desktops were launched from does not affect those running computers — they already restored from the golden snapshot. It only removes the version from your registry so it can no longer be launched or built. Curated templates cannot be deleted.

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

[​](#param-version)

version

string

required

Version (semver) to delete.

## [​](#response) Response

[​](#param-deleted)

deleted

boolean

`true` when the version was removed.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X DELETE https://www.orgo.ai/api/templates/default/claude-code/1.0.0 \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{ "deleted": true }
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

Deleted

[​](#response-deleted)

deleted

boolean

Example:

`true`

[Previous](/api-reference/templates/get)[Build templateBake a template version into a golden snapshot.

Next](/api-reference/templates/build)

⌘I

Delete template version

cURL

```
curl --request DELETE \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version} \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "deleted": true
}
```