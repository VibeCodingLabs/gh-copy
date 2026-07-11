---
url: https://docs.orgo.ai/api-reference/authentication
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

All API requests require a Bearer token in the `Authorization` header.

```
Authorization: Bearer sk_live_your_api_key_here
```

## [​](#get-your-api-key) Get your API key

1. Sign in at [orgo.ai/start](https://www.orgo.ai/start).
2. Open a workspace and click **Settings**.
3. In the **API keys** section, click **New key**.
4. Pick a scope (see below) and a name, then click **Create key**.
5. Copy the plaintext value. It is shown once.

## [​](#key-scopes) Key scopes

Every API key has one of two scopes:

| Scope | Can access | Use for |
| --- | --- | --- |
| **Account-wide** | Any workspace you own. | Your laptop, dashboards, scripts that span multiple workspaces. |
| **Workspace-scoped** | One specific workspace and its computers. 403 on every other workspace. | CI, third-party integrations, scripts that should not be able to touch anything else. |

Workspace-scoped keys cannot:

* Create new workspaces.
* List, read, modify, or delete any workspace other than the one they are scoped to.
* Run computer-use agents (`/v1/chat/completions`) against computers in other workspaces.
* Move a computer to a different workspace.

When a scoped key is used outside its workspace, the API returns:

```
{
  "error": "This API key is scoped to workspace <key-workspace>. It cannot access workspace <target>. Use an account-wide key, or create a key scoped to the target workspace.",
  "code": "workspace_scope_mismatch",
  "key_workspace_id": "<key-workspace>",
  "target_workspace_id": "<target>"
}
```

## [​](#rotating-a-key) Rotating a key

Generate a new key, update your client to use it, then delete the old one. Both keys work while you migrate.
API key list, creation, and deletion all live in the dashboard’s workspace settings. There is no API to manage keys programmatically yet.

Store API keys securely. Never commit them to version control or share them publicly. Rotate immediately if a key is exposed.

## [​](#examples) Examples

cURL

Python

JavaScript

```
curl https://www.orgo.ai/api/workspaces \
  -H "Authorization: Bearer sk_live_abc123..."
```

## [​](#environment-variables) Environment variables

```
export ORGO_API_KEY=sk_live_abc123...
```

.env

```
ORGO_API_KEY=sk_live_abc123...
```

## [​](#error-responses) Error responses

| Status | Body | Meaning |
| --- | --- | --- |
| `401` | `{ "error": "Invalid API key..." }` | The Bearer token is not a known Orgo key. Check for typos; generate a new one if needed. |
| `401` | `{ "error": "Missing API key..." }` | No `Authorization` header on the request. |
| `403` | `{ "code": "workspace_scope_mismatch", ... }` | A workspace-scoped key tried to act on a different workspace. |
| `403` | `{ "error": "Access denied" }` | The key’s account does not own or belong to the target workspace. |

See [Troubleshooting](/guides/troubleshooting) for the full error reference and recovery steps.

## [​](#security-tips) Security tips

* Use environment variables. Never hardcode keys.
* Add `.env` to `.gitignore`.
* Create a separate workspace-scoped key per integration. If one leaks, only that workspace is exposed.
* Rotate keys when team members leave.

## [​](#need-help) Need help?

Email [spencer@orgo.ai](mailto:spencer@orgo.ai). Always include the `request_id` from the error response when reporting a problem.

[Previous](/api-reference/introduction)[Create chat completionOpenAI-compatible endpoint that lets an AI model drive a computer

Next](/api-reference/chat/completions)

⌘I