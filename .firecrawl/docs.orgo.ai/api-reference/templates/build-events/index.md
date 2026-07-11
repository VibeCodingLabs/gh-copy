---
url: https://docs.orgo.ai/api-reference/templates/build-events
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

/

events

Try it

Stream build logs

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version}/build/events \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "ts": "2023-11-07T05:31:56Z",
  "source": "<string>",
  "line": "<string>"
}
```

Streams the build log as [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events). Use it to render a live, Docker-style build console. The stream stays open for the duration of the build and closes when it reaches `ready` or `failed`.
Each `data:` frame is a JSON object:

[​](#param-ts)

ts

string

Event timestamp (ISO 8601).

[​](#param-level)

level

string

`info`, `success`, `warn`, or `error`.

[​](#param-phase)

phase

string

Build phase: `publish`, `compile`, `boot`, `install`, `snapshot`, `record`, `archive`, or `ready`. A cancelled or timed-out build ends on `cancel` or `timeout`.

[​](#param-source)

source

string

Origin of the line, e.g. `apt`, `pip`, `npm`, or `builder`. Optional.

[​](#param-line)

line

string

A single line of build output.

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

## [​](#example) Example

cURL

Python

JavaScript

```
curl -N https://www.orgo.ai/api/templates/default/claude-code/1.0.0/build/events \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#stream) Stream

```
data: {"ts":"2026-06-08T17:00:01Z","level":"info","phase":"boot","line":"booting build VM"}

data: {"ts":"2026-06-08T17:00:14Z","level":"info","phase":"install","source":"npm","line":"npm install -g @anthropic-ai/claude-code"}

data: {"ts":"2026-06-08T17:01:50Z","level":"info","phase":"archive","source":"builder","line":"uploading golden snapshot"}

data: {"ts":"2026-06-08T17:01:58Z","level":"success","phase":"ready","line":"golden snapshot ready in 118.4s"}
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

text/event-stream

SSE stream of BuildEvent frames

One frame of the build-events SSE stream.

[​](#response-ts)

ts

string<date-time>

[​](#response-level)

level

enum<string>

Available options:

`info`,

`success`,

`warn`,

`error`

[​](#response-phase)

phase

enum<string>

Available options:

`publish`,

`compile`,

`boot`,

`install`,

`snapshot`,

`record`,

`archive`,

`ready`,

`cancel`,

`timeout`

[​](#response-source)

source

string

Origin of the line, e.g. apt, pip, npm, builder.

[​](#response-line)

line

string

A single line of build output.

[Previous](/api-reference/templates/build-status)[List curated templatesBrowse the templates Orgo publishes and maintains.

Next](/api-reference/templates/list-curated)

⌘I

Stream build logs

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/templates/{namespace}/{name}/{version}/build/events \
  --header 'Authorization: Bearer <token>'
```

200

401

```
{
  "ts": "2023-11-07T05:31:56Z",
  "source": "<string>",
  "line": "<string>"
}
```