---
url: https://docs.orgo.ai/api-reference/computers/exec
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

exec

Try it

Execute Python

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/exec \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "code": "import os\nprint(os.getcwd())",
  "timeout": 10
}
'
```

200

401

404

```
{
  "output": "/home/user\n",
  "success": true
}
```

Executes Python code on the computer in a short-lived interpreter and returns its output.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-code)

code

string

required

Python code to execute.

[​](#param-timeout)

timeout

integer

default:"10"

Timeout in seconds (1-300).

## [​](#response) Response

[​](#param-output)

output

string

Captured stdout from the interpreter.

[​](#param-success)

success

boolean

`true` if the code ran without raising an uncaught exception.

[​](#param-error)

error

string

Error message, if execution failed.

[​](#param-error-type)

error\_type

string

Python exception class (e.g., `SyntaxError`, `NameError`).

[​](#param-timeout-1)

timeout

boolean

`true` if execution was killed by the timeout.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/exec \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import os\nprint(os.getcwd())",
    "timeout": 10
  }'
```

### [​](#successful-response) Successful response

```
{
  "output": "/home/user\n",
  "success": true,
  "action": "exec",
  "timeout": false
}
```

### [​](#error-response) Error response

```
{
  "output": "",
  "success": false,
  "action": "exec",
  "error": "name 'undefined_var' is not defined",
  "error_type": "NameError"
}
```

For shell commands, use [Execute bash](/api-reference/computers/bash) instead.

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Missing or non-string `code`, or computer instance not available. |
| `401` | Missing or invalid API key. |
| `403` | You do not have access to this computer. |
| `404` | Computer not found. |
| `500` | Upstream desktop agent failure. |

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

#### Body

application/json

[​](#body-code)

code

string

required

Python code to execute

[​](#body-timeout)

timeout

integer

default:10

Timeout in seconds

Required range: `1 <= x <= 300`

#### Response

200

application/json

Code executed

[​](#response-output)

output

string

Code output

[​](#response-success)

success

boolean

Whether execution succeeded

[​](#response-error)

error

string

Error message if failed

[​](#response-error-type)

error\_type

string

Error type if failed

[​](#response-timeout)

timeout

boolean

Whether execution timed out

[Previous](/api-reference/computers/bash)[Terminal WebSocketInteractive PTY shell over WebSocket - real-time bidirectional terminal I/O.

Next](/api-reference/computers/terminal)

⌘I

Execute Python

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/exec \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "code": "import os\nprint(os.getcwd())",
  "timeout": 10
}
'
```

200

401

404

```
{
  "output": "/home/user\n",
  "success": true
}
```