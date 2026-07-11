---
url: https://docs.orgo.ai/api-reference/files/upload
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

files

/

upload

Try it

Upload file

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/files/upload \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: multipart/form-data' \
  --form file='@example-file' \
  --form 'projectId=<string>' \
  --form 'desktopId=<string>'
```

200

400

401

404

```
{
  "file": {
    "id": "<string>",
    "filename": "<string>",
    "size_bytes": 123,
    "content_type": "<string>",
    "created_at": "2023-11-07T05:31:56Z"
  }
}
```

Uploads a file to a workspace, optionally associated with a specific computer.

## [​](#request) Request

Send a `multipart/form-data` request with the file and workspace information:

[​](#param-file)

file

file

required

File to upload. Maximum size: 10MB.

[​](#param-project-id)

projectId

string

required

Workspace ID to upload the file to.

[​](#param-desktop-id)

desktopId

string

Optional computer ID to associate the file with.

## [​](#response) Response

[​](#param-file-1)

file

object

The uploaded file object.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/files/upload \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -F "file=@./document.pdf" \
  -F "projectId=550e8400-e29b-41d4-a716-446655440000" \
  -F "desktopId=a3bb189e-8bf9-3888-9912-ace4e6543002"
```

### [​](#response-2) Response

```
{
  "file": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "filename": "document.pdf",
    "size_bytes": 102400,
    "content_type": "application/pdf",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

Uploaded files are stored in the workspace and can be accessed by all computers in that workspace.

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Body

multipart/form-data

[​](#body-file)

file

file

required

File to upload (max 10MB)

[​](#body-project-id)

projectId

string

required

Workspace ID

[​](#body-desktop-id)

desktopId

string

Optional computer ID to associate the file with

#### Response

200

application/json

File uploaded

[​](#response-file)

file

object

Show child attributes

[Previous](/api-reference/computers/stream-stop)[Export fileExport a file from a computer to cloud storage.

Next](/api-reference/files/export)

⌘I

Upload file

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/files/upload \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: multipart/form-data' \
  --form file='@example-file' \
  --form 'projectId=<string>' \
  --form 'desktopId=<string>'
```

200

400

401

404

```
{
  "file": {
    "id": "<string>",
    "filename": "<string>",
    "size_bytes": 123,
    "content_type": "<string>",
    "created_at": "2023-11-07T05:31:56Z"
  }
}
```