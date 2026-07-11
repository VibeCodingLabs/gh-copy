---
url: https://docs.orgo.ai/guides/troubleshooting
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Every Orgo API error response is JSON with two stable fields plus an optional `request_id` to use when contacting support.

```
{
  "error": "Invalid API key. Check it for typos or generate a new one at https://www.orgo.ai/start.",
  "request_id": "f0c2c4a8-9d8e-4d2f-b8a6-2a9a4c2d4b1f"
}
```

When the error originated on the desktop side of the request, the response also includes the upstream status:

```
{
  "error": "screen is unavailable",
  "request_id": "f0c2c4a8-9d8e-4d2f-b8a6-2a9a4c2d4b1f",
  "upstream_status": 409
}
```

Always include `request_id` when emailing [spencer@orgo.ai](mailto:spencer@orgo.ai) about a failed call. It maps directly to a server-side log line.

## [​](#authentication) Authentication

| Symptom | What it means | Fix |
| --- | --- | --- |
| `401 Invalid API key.` | The Bearer token in your `Authorization` header is not a known Orgo API key. | Generate a new key at [orgo.ai/start](https://www.orgo.ai/start). Check for whitespace or a missing `sk_` prefix. |
| `401 Missing API key.` | No `Authorization` header on the request. | Set `Authorization: Bearer $ORGO_API_KEY`. |
| `401 Your session has expired.` | You called the API from a browser session that timed out. | Sign in again, or switch to an API key for programmatic calls. |
| `403 Access denied` on a computer or workspace | The key belongs to a different account, or you were removed from the workspace. | Confirm the workspace ID, or ask the workspace owner to re-invite you. |
| `403 workspace_scope_mismatch` | The API key is workspace-scoped and the request targets a different workspace. The response includes `key_workspace_id` and `target_workspace_id` so the boundary is explicit. | Use an account-wide key, or create a key scoped to the target workspace. See [Authentication](/api-reference/authentication). |

Orgo API keys come in two flavors: **account-wide** (can access every workspace you own) and **workspace-scoped** (locked to one workspace, 403 anywhere else). Pick the scope at key-creation time in workspace settings.

## [​](#computer-not-responding) Computer not responding

| Symptom | What it means | Fix |
| --- | --- | --- |
| `404 Computer not found` | The ID in the URL doesn’t match a computer your account can see. | Re-fetch the ID from `GET /workspaces/{id}`. |
| `400 Desktop instance not available` | The computer record exists, but it never got a backing VM (still booting or failed). | Wait a few seconds and retry. If it persists, `POST /computers/{id}/restart`. |
| `503 Could not reach the desktop. Try again in a moment.` | The control plane could not connect to the desktop. Usually transient. | Retry with exponential backoff (1s, 2s, 4s). If it keeps failing, restart the computer. |
| `409 Conflict` | The action is blocked by the computer’s current state, e.g. resize while not running. | Read the message; restart or stop the computer if needed. |

## [​](#action-errors-bash-click-type-exec-etc) Action errors (bash, click, type, exec, etc.)

When an action endpoint returns a non-200, the `upstream_status` field tells you whether the failure came from Orgo’s control plane or from the desktop itself.

| `upstream_status` | Meaning |
| --- | --- |
| Not present | The error originated in Orgo’s control plane (auth, lookup, validation). |
| `400` | The desktop rejected the request body (e.g. bash command parse error, click out of bounds). |
| `408`, `504` | The desktop timed out the action. Common with long bash commands; pass a higher `timeout` in the body. |
| `500` | The desktop crashed handling the action. Capture the `request_id` and contact support. |

## [​](#recovering-a-stuck-computer) Recovering a stuck computer

A computer is “stuck” if it returns `200` on `GET /computers/{id}` but action calls fail.

1. `GET https://www.orgo.ai/api/desktops/{instance_id}/proxy/health`. If this returns 200, the desktop is up and the issue is in the control plane. Retry your action.
2. If `/health` fails, `POST /computers/{id}/restart`. State is preserved across restart.
3. If restart fails, capture `request_id`s from a few attempts and email [spencer@orgo.ai](mailto:spencer@orgo.ai). Do not delete the computer; deletion drops the disk.

## [​](#rate-limits) Rate limits

`429 Too Many Requests` means you have exceeded the per-key rate limit. Back off with exponential retry (start at 1s, double each retry, max 60s). If you need higher limits, email [spencer@orgo.ai](mailto:spencer@orgo.ai).

## [​](#reporting-a-bug) Reporting a bug

When something is broken, send:

* The `request_id` from the error response (the most important field).
* The exact request you made (method, URL, body, redacted of secrets).
* The full error response.

Email: [spencer@orgo.ai](mailto:spencer@orgo.ai). Discord: [discord.gg/tbYGpvnnJD](https://discord.gg/tbYGpvnnJD).

[Previous](/guides/embed-vms)[TemplatesReproducible cloud computers, defined in a single file and launched in seconds.

Next](/guides/templates/introduction)

⌘I