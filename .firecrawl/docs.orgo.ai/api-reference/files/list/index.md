---
url: https://docs.orgo.ai/api-reference/files/list
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

files

Try it

List files

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/files \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "files": [
    {
      "id": "<string>",
      "filename": "<string>",
      "size_bytes": 123,
      "content_type": "<string>",
      "created_at": "2023-11-07T05:31:56Z"
    }
  ]
}
```

Lists all files in a workspace, optionally filtered by computer.

## [​](#query-parameters) Query parameters

[​](#param-project-id)

projectId

string

required

Workspace ID.

[​](#param-desktop-id)

desktopId

string

Optional computer ID to filter files by.

## [​](#response) Response

[​](#param-files)

files

array

Array of file objects.

## [​](#example) Example

cURL

Python

JavaScript

```
# List all files in a workspace
curl "https://www.orgo.ai/api/files?projectId=550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer $ORGO_API_KEY"

# List files for a specific computer
curl "https://www.orgo.ai/api/files?projectId=550e8400-e29b-41d4-a716-446655440000&desktopId=a3bb189e-8bf9-3888-9912-ace4e6543002" \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "files": [
    {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "filename": "document.pdf",
      "size_bytes": 102400,
      "content_type": "application/pdf",
      "source": "upload",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "c3d4e5f6-a7b8-9012-cdef-345678901234",
      "filename": "results.txt",
      "size_bytes": 1024,
      "content_type": "text/plain",
      "source": "export",
      "created_at": "2024-01-15T11:00:00Z"
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

[​](#parameter-project-id)

projectId

string

required

Workspace ID

[​](#parameter-desktop-id)

desktopId

string

Optional computer ID to filter by

#### Response

200

application/json

List of files

[​](#response-files)

files

object[]

Show child attributes

[Previous](/api-reference/files/export)[Download fileGet a signed download URL for a file.

Next](/api-reference/files/download)

⌘I

List files

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/files \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "files": [
    {
      "id": "<string>",
      "filename": "<string>",
      "size_bytes": 123,
      "content_type": "<string>",
      "created_at": "2023-11-07T05:31:56Z"
    }
  ]
}
```