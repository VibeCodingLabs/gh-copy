---
url: https://docs.orgo.ai/api-reference/computers/bash
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

POST

/

computers

/

{id}

/

bash

Try it

Execute bash

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/bash \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "command": "ls -la /home/user"
}
'
```

200

401

404

```
{
  "output": "total 32\ndrwxr-xr-x 4 user user 4096 Jan 15 10:30 .\ndrwxr-xr-x 3 root root 4096 Jan 15 10:00 ..\n-rw-r--r-- 1 user user  220 Jan 15 10:00 .bashrc\ndrwxr-xr-x 2 user user 4096 Jan 15 10:30 Desktop\n",
  "success": true
}
```

Executes a bash command on the computer and returns the combined stdout/stderr output.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID (UUID).

## [​](#body-parameters) Body parameters

[​](#param-command)

command

string

required

Bash command to execute.

[​](#param-timeout)

timeout

integer

default:"200"

Maximum execution time in seconds before the command is killed.

## [​](#response) Response

[​](#param-output)

output

string

Combined stdout and stderr.

[​](#param-exit-code)

exit\_code

integer

Process exit code.

[​](#param-command-1)

command

string

Echo of the command that was executed.

[​](#param-success)

success

boolean

`true` if the command ran (regardless of exit code). Check `exit_code` to determine if the command itself succeeded.

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la /home/user"}'
```

### [​](#response-2) Response

```
{
  "success": true,
  "action": "bash",
  "command": "ls -la /home/user",
  "output": "total 32\ndrwxr-xr-x 4 user user 4096 Jan 15 10:30 .\ndrwxr-xr-x 3 root root 4096 Jan 15 10:00 ..\n-rw-r--r-- 1 user user  220 Jan 15 10:00 .bashrc\ndrwxr-xr-x 2 user user 4096 Jan 15 10:30 Desktop\n",
  "exit_code": 0
}
```

For Python code execution, use [Execute Python](/api-reference/computers/exec) instead.

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| `400` | Computer instance not available. |
| `401` | Missing or invalid API key. |
| `403` | You do not have access to this computer. |
| `404` | Computer not found. |
| `500` | Upstream desktop agent failure (process spawn error, timeout killed). |

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

[​](#body-command)

command

string

required

Bash command to execute

#### Response

200

application/json

Command executed

[​](#response-output)

output

string

Command output

[​](#response-success)

success

boolean

Whether command succeeded

[Previous](/api-reference/computers/wait)[Execute PythonRun a Python snippet on the computer and capture its stdout.

Next](/api-reference/computers/exec)

⌘I

Execute bash

cURL

```
curl --request POST \
  --url https://www.orgo.ai/api/computers/{id}/bash \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "command": "ls -la /home/user"
}
'
```

200

401

404

```
{
  "output": "total 32\ndrwxr-xr-x 4 user user 4096 Jan 15 10:30 .\ndrwxr-xr-x 3 root root 4096 Jan 15 10:00 ..\n-rw-r--r-- 1 user user  220 Jan 15 10:00 .bashrc\ndrwxr-xr-x 2 user user 4096 Jan 15 10:30 Desktop\n",
  "success": true
}
```