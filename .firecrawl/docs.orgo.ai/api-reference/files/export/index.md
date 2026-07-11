---
url: https://docs.orgo.ai/api-reference/files/export
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

files

/

export

Try it

Export file

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/files/export \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "desktopId": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "path": "Desktop/results.txt"
}
'
```

200

400

401

404

```
{
  "success": true,
  "file": {
    "id": "<string>",
    "filename": "<string>",
    "size_bytes": 123,
    "content_type": "<string>",
    "created_at": "2023-11-07T05:31:56Z"
  },
  "url": "<string>"
}
```

Exports a file from a computer’s filesystem and returns a download URL.

The computer must be running to export files.

## [​](#request) Request

[​](#param-desktop-id)

desktopId

string

required

Computer ID to export from.

[​](#param-path)

path

string

required

Path to the file on the computer.

### [​](#path-formats) Path formats

| Format | Example |
| --- | --- |
| Relative to home | `Desktop/results.txt` |
| Absolute path | `/home/user/Desktop/results.txt` |
| With tilde | `~/Desktop/results.txt` |

## [​](#response) Response

[​](#param-success)

success

boolean

`true` if export succeeded.

[​](#param-file)

file

object

The exported file object.

[​](#param-url)

url

string

Signed download URL (expires in 1 hour).

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/files/export \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "desktopId": "a3bb189e-8bf9-3888-9912-ace4e6543002",
    "path": "Desktop/results.txt"
  }'
```

### [​](#response-2) Response

```
{
  "success": true,
  "file": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "filename": "results.txt",
    "size_bytes": 1024,
    "content_type": "text/plain",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "url": "https://storage.example.com/files/..."
}
```

Files can only be exported from within `/home/user`. Paths outside this directory return a 403 error.

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Body

application/json

[​](#body-desktop-id)

desktopId

string

required

Computer ID

[​](#body-path)

path

string

required

Path to file on computer (e.g., Desktop/results.txt)

#### Response

200

application/json

File exported

[​](#response-success)

success

boolean

[​](#response-file)

file

object

Show child attributes

[​](#response-url)

url

string

Signed download URL (expires in 1 hour)

[Previous](/api-reference/files/upload)[List filesList uploaded files in a workspace.

Next](/api-reference/files/list)

⌘I

Export file

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/files/export \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "desktopId": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "path": "Desktop/results.txt"
}
'
```

200

400

401

404

```
{
  "success": true,
  "file": {
    "id": "<string>",
    "filename": "<string>",
    "size_bytes": 123,
    "content_type": "<string>",
    "created_at": "2023-11-07T05:31:56Z"
  },
  "url": "<string>"
}
```