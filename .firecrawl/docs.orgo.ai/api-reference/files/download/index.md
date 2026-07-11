---
url: https://docs.orgo.ai/api-reference/files/download
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

GET

/

files

/

download

Try it

Download file

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/files/download \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "url": "<string>"
}
```

Returns a signed download URL for a file.

## [​](#query-parameters) Query parameters

[​](#param-id)

id

string

required

File ID.

## [​](#response) Response

[​](#param-url)

url

string

Signed download URL (expires in 1 hour).

## [​](#example) Example

cURL

Python

JavaScript

```
curl "https://www.orgo.ai/api/files/download?id=f47ac10b-58cc-4372-a567-0e02b2c3d479" \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

### [​](#response-2) Response

```
{
  "url": "https://storage.example.com/files/..."
}
```

The returned URL is pre-signed and can be used directly in a browser or with any HTTP client. URLs expire after 1 hour.

#### Authorizations

[​](#authorization-authorization)

Authorization

string

header

required

API key authentication. Get your key at orgo.ai/workspaces

#### Query Parameters

[​](#parameter-id)

id

string

required

File ID

#### Response

200

application/json

Download URL

[​](#response-url)

url

string

Signed download URL (expires in 1 hour)

[Previous](/api-reference/files/list)[Delete filePermanently delete an uploaded file.

Next](/api-reference/files/delete)

⌘I

Download file

cURL

```
curl --request GET \
  --url https://www.orgo.ai/api/files/download \
  --header 'Authorization: Bearer <token>'
```

200

401

404

```
{
  "url": "<string>"
}
```