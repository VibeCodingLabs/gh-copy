---
url: https://docs.orgo.ai/api-reference/computers/resize
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

PATCH

/

computers

/

{id}

/

resize

Try it

Resize computer

cURL

```
curl --request PATCH \
  --url https://www.orgo.ai/api/computers/{id}/resize \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "disk_size_gb": 123,
  "bandwidth_limit_mbps": 123
}
'
```

200

401

```
{
  "vcpus": 123,
  "mem_gb": 123,
  "disk_size_gb": 123,
  "bandwidth_limit_mbps": 123
}
```

Live-resizes a running computer’s CPU, RAM, disk, or bandwidth without rebooting. All fields are optional - only include what you want to change.

The computer must be in `running` state. CPU and bandwidth changes apply instantly; RAM and disk grow online. Response surfaces the *applied* values, not the requested ones - if a dimension didn’t land, its previous value is returned.

## [​](#path-parameters) Path parameters

[​](#param-id)

id

string

required

Computer ID.

## [​](#body-parameters) Body parameters

[​](#param-vcpus)

vcpus

integer

New CPU count: `1`, `2`, `4`, `8`, or `16`. Capped by your plan’s per-computer limit.

[​](#param-mem-gb)

mem\_gb

integer

New RAM in GB: `4`, `8`, `16`, or `32`. A live resize tops out at `32` GB (larger sizes are only available when the computer is first created). Also capped by your plan’s per-computer limit.

[​](#param-disk-size-gb)

disk\_size\_gb

integer

New disk size in GB. **Disk can only grow** - shrinking is not supported.

[​](#param-bandwidth-limit-mbps)

bandwidth\_limit\_mbps

integer

New bandwidth cap in Mbps. Capped by your plan limit.

[​](#param-auto-stop-minutes)

auto\_stop\_minutes

integer

Optional: also update the auto-stop setting as part of the same call. `0` disables auto-stop.

## [​](#response) Response

Returns the effective configuration after the resize attempt. Values reflect what the VM actually accepted, not what you asked for.

[​](#param-vcpus-1)

vcpus

integer

Effective CPU count.

[​](#param-mem-gb-1)

mem\_gb

integer

Effective RAM in GB.

[​](#param-disk-size-gb-1)

disk\_size\_gb

integer

Effective disk size in GB.

[​](#param-bandwidth-limit-mbps-1)

bandwidth\_limit\_mbps

integer

Effective bandwidth limit in Mbps.

[​](#param-auto-stop-minutes-1)

auto\_stop\_minutes

integer

Echoes the requested `auto_stop_minutes` if one was supplied.

[​](#param-results)

results

object

Per-dimension result breakdown (`{requested, applied, ok, error}`). Only present if a resize operation ran.

[​](#param-partial)

partial

boolean

`true` if some dimensions failed while others succeeded.

### [​](#status-codes) Status codes

* `200` - All requested dimensions applied successfully
* `207` - Mixed result - some dimensions applied, others failed (check `results`)
* `422` - All requested dimensions failed

## [​](#example) Example

cURL

Python

JavaScript

```
curl -X PATCH https://www.orgo.ai/api/computers/a3bb189e-8bf9-3888-9912-ace4e6543002/resize \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "vcpus": 4,
    "mem_gb": 8,
    "disk_size_gb": 30
  }'
```

### [​](#response-2) Response

```
{
  "vcpus": 4,
  "mem_gb": 8,
  "disk_size_gb": 30,
  "bandwidth_limit_mbps": 1000,
  "results": {
    "vcpus": { "requested": 4, "applied": 4, "ok": true },
    "mem_mb": { "requested": 8192, "applied": 8192, "ok": true },
    "disk_gb": { "requested": 30, "applied": 30, "ok": true }
  },
  "partial": false
}
```

## [​](#errors) Errors

* `400` - Invalid value (e.g. shrinking disk, value not in allowed list), or not a metal VM
* `401` - Invalid or missing API key
* `403` - Value exceeds your plan’s per-computer limit, or no access
* `404` - Computer not found
* `409` - Computer is not running
* `422` - All requested dimensions failed to apply

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

[​](#body-vcpus)

vcpus

enum<integer>

New CPU count. Capped by plan.

Available options:

`1`,

`2`,

`4`,

`8`,

`16`

[​](#body-mem-gb)

mem\_gb

enum<integer>

New RAM in GB. Live resize is capped at 32 GB (the VMM boot-memory ceiling); larger sizes are only available at create time. Also capped by your plan.

Available options:

`4`,

`8`,

`16`,

`32`

[​](#body-disk-size-gb)

disk\_size\_gb

integer

New disk size in GB. Grow only — shrinking not supported.

[​](#body-bandwidth-limit-mbps)

bandwidth\_limit\_mbps

integer

New bandwidth cap in Mbps. Capped by plan.

#### Response

200

application/json

Resize complete

[​](#response-vcpus)

vcpus

integer

[​](#response-mem-gb)

mem\_gb

integer

[​](#response-disk-size-gb)

disk\_size\_gb

integer

[​](#response-bandwidth-limit-mbps)

bandwidth\_limit\_mbps

integer

[Previous](/api-reference/computers/move)[Delete computerPermanently delete a computer.

Next](/api-reference/computers/delete)

⌘I

Resize computer

cURL

```
curl --request PATCH \
  --url https://www.orgo.ai/api/computers/{id}/resize \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "disk_size_gb": 123,
  "bandwidth_limit_mbps": 123
}
'
```

200

401

```
{
  "vcpus": 123,
  "mem_gb": 123,
  "disk_size_gb": 123,
  "bandwidth_limit_mbps": 123
}
```