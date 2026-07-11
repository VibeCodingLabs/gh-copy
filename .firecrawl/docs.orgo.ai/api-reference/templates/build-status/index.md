---
url: https://docs.orgo.ai/api-reference/templates/build-status
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

/

build

Try it

Get build status

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version}/build \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "ref": "<string>",
  "digest": "<string>",
  "golden_dir": "<string>",
  "build_time_ms": 123,
  "reused": true,
  "error": "<string>"
}
```

Returns the current build state of a version. Poll this after [Build template](/api-reference/templates/build) until `status` is `ready`, or stream [build logs](/api-reference/templates/build-events) for live output.

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

Version (semver).

## [​](#response) Response

[​](#param-status)

status

string

One of:

* `not_built` — no golden snapshot yet. Call [Build template](/api-reference/templates/build).
* `building` — a build is in progress.
* `ready` — built and launchable.
* `failed` — the last build failed. See `error`.

[​](#param-ref)

ref

string

Template ref.

[​](#param-digest)

digest

string

Content-addressed digest.

[​](#param-build-time-ms)

build\_time\_ms

integer

Build duration in milliseconds. Present when `ready`.

[​](#param-reused)

reused

boolean

Whether an existing golden was reused.

[​](#param-error)

error

string

Failure reason. Present when `status` is `failed`.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/templates/default/claude-code/1.0.0/build \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "ref": "default/claude-code@1.0.0",
  "digest": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "status": "ready",
  "build_time_ms": 118420,
  "reused": false
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

Build status

[​](#response-ref)

ref

string

[​](#response-digest)

digest

string

[​](#response-status)

status

enum<string>

Available options:

`ready`,

`building`,

`failed`,

`not_built`

[​](#response-golden-dir)

golden\_dir

string

[​](#response-build-time-ms)

build\_time\_ms

integer

Build duration in milliseconds. Present when ready.

[​](#response-reused)

reused

boolean

Whether an existing golden with the same digest was reused.

[​](#response-error)

error

string

Failure reason. Present when status is failed.

[Previous](/api-reference/templates/build)[Stream build logsFollow a template build live over Server-Sent Events.

Next](/api-reference/templates/build-events)

⌘I

Get build status

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version}/build \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "ref": "<string>",
  "digest": "<string>",
  "golden_dir": "<string>",
  "build_time_ms": 123,
  "reused": true,
  "error": "<string>"
}
```