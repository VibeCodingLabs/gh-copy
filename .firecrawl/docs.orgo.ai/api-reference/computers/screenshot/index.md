---
url: https://docs.orgo.ai/api-reference/computers/screenshot
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

computers

/

{id}

/

screenshot

Try it

Take screenshot

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id}/screenshot \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."
}
```

Captures a screenshot of the computer’s display, uploads it to storage, and returns a URL you can fetch.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if the screenshot was captured and stored.

[​](#param-image)

image

string

Public URL of the uploaded PNG.

[​](#param-metadata)

metadata

object

Information about the stored screenshot.

Show metadata fields

[​](#param-id-1)

id

string

Screenshot record ID.

[​](#param-timestamp)

timestamp

string

ISO 8601 creation timestamp.

[​](#param-size)

size

integer

File size in bytes.

[​](#param-storage-path)

storage\_path

string

Internal storage path.

## [​](#example) Example

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/screenshot \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "success": true,
  "image": "https://storage.orgo.ai/screenshots/4d96f9a0/2026-04-20/abc123.png",
  "metadata": {
    "id": "9f2b7c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
    "timestamp": "2026-04-20T12:00:00Z",
    "size": 187342,
    "storage_path": "screenshots/4d96f9a0/2026-04-20/abc123.png"
  }
}
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Computer instance not available. |
| `401` | Missing or invalid API key. |
| `403` | You do not have access to this computer. |
| `404` | Computer not found. |
| `500` | Capture or upload failed. |

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Path Parameters

[​](#parameter-id)

id

string

required

Computer ID

#### Response

200

application/json

Screenshot captured

[​](#response-image)

image

string

Base64-encoded PNG or URL to the image

[Previous](/api-reference/computers/restart)[Click mousePerform a left, right, or double click at given screen coordinates.

Next](/api-reference/computers/click)

⌘I

Take screenshot

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/computers/{id}/screenshot \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."
}
```