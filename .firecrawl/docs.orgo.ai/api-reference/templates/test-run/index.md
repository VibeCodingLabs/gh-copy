---
url: https://docs.orgo.ai/api-reference/templates/test-run
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

templates

/

run

Try it

Test-run a template

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/templates/run \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "ref": "default/my-template@1.0.0"
}
'
```

200

401

```
{
  "id": "<string>",
  "desktop_id": "<string>",
  "status": "<string>",
  "vnc_password": "<string>",
  "public_host": "<string>",
  "resolution": "<string>"
}
```

Boots a **short-lived, auto-reaped** computer from a template `ref` — the same in-editor “Run” that the dashboard uses to test a template before sharing it. The preview is reclaimed automatically after a period of inactivity.

Test-runs require a **Scale** plan. For a **persistent** computer, use [Create computer](/api-reference/computers/create) with `template_ref` instead — that’s the durable path and it counts toward your plan’s computer quota.

## [​](#request-body) Request body

[​](#param-ref)

ref

string

required

Template ref to boot, in `namespace/name@version` form. Your own (`default/…`) or a curated (`system/…`) ref. The template’s build must be `ready`.

## [​](#response) Response

Returns a short-lived computer you connect to exactly like any other. The key fields:

[​](#param-desktop-id)

desktop\_id

string

The preview’s identifier. Build its connection URLs the same way as any computer (`https://www.orgo.ai/desktops/{desktop_id}/…`), and pass it back to stop the run.

[​](#param-id)

id

string

The underlying VM id.

[​](#param-status)

status

string

Current status.

[​](#param-vnc-password)

vnc\_password

string

VNC / WebSocket token for the preview.

See [Create computer](/api-reference/computers/create) for the full connection model.

## [​](#example) Example

Start

Stop

```
curl -X POST https://www.orgo.ai/api/templates/run \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ref": "default/my-template@1.0.0"}'
```

## [​](#stop-a-test-run) Stop a test-run

`DELETE /templates/run?id={desktop_id}` stops the preview and reclaims the VM. Previews are also reaped automatically, so a missed stop won’t leak a computer.

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `401` | Missing or invalid API key. |
| `403` | Test-runs require a Scale plan or higher. |
| `409` | The template’s build isn’t `ready`. [Build it](/api-reference/templates/build) first. |
| `429` | Run-VM rate limit or concurrency cap reached. Back off and retry. |

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Body

application/json

[​](#body-ref)

ref

string

required

Example:

`"default/my-template@1.0.0"`

#### Response

200

application/json

Preview computer booted

A short-lived preview computer booted from a template ref. Connect to it like any computer; it is auto-reaped.

[​](#response-id)

id

string

Underlying VM id.

[​](#response-desktop-id)

desktop\_id

string

Ephemeral desktop id. Use it for same-origin connection URLs and to stop the run via DELETE /templates/run?id=.

[​](#response-status)

status

string

[​](#response-vnc-password)

vnc\_password

string

[​](#response-public-host)

public\_host

string

[​](#response-resolution)

resolution

string

[Previous

List curated templatesBrowse the templates Orgo publishes and maintains.](/api-reference/templates/list-curated)

⌘I

Test-run a template

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/templates/run \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "ref": "default/my-template@1.0.0"
}
'
```

200

401

```
{
  "id": "<string>",
  "desktop_id": "<string>",
  "status": "<string>",
  "vnc_password": "<string>",
  "public_host": "<string>",
  "resolution": "<string>"
}
```