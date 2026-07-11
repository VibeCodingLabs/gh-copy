---
url: https://docs.orgo.ai/api-reference/chat/threads
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Threads are the durable conversation context behind multi-turn agent runs. Each thread is scoped to a single computer and stores the full message history so the AI can build on what it has already done. Pass a thread’s ID into [Create chat completion](/api-reference/chat/completions) to continue a session.

Threads are created implicitly. Every call to `POST /v1/chat/completions` with a `computer_id` either continues an existing thread (when `thread_id` is passed) or creates a new one and returns its ID. Use these endpoints to list, inspect, rename, archive, or delete threads - you rarely need to create them by hand.

## [​](#endpoints) Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/chat/threads?desktopId={id}` | List threads for a computer. |
| `POST` | `/api/chat/threads` | Create an empty thread. |
| `GET` | `/api/chat/threads/{id}` | Get a thread with full message history. |
| `PATCH` | `/api/chat/threads/{id}` | Update title, replace messages, archive, or unarchive. |
| `DELETE` | `/api/chat/threads/{id}` | Delete a thread. |
| `POST` | `/api/chat/threads/{id}/title` | Auto-generate a title with Claude Haiku. |

**Base URL:** `https://www.orgo.ai`
**Auth:** `Authorization: Bearer sk_live_...` on every request.


---

## [​](#list-threads) List threads

```
GET /api/chat/threads?desktopId={desktop_uuid}
```

Returns every thread the authenticated user owns for the given computer, including full message history.

### [​](#query-parameters) Query parameters

[​](#param-desktop-id)

desktopId

string

required

UUID of the computer (the `id` field from [Create computer](/api-reference/computers/create)). Threads are scoped per-computer; to list across computers, call this endpoint once per computer.

### [​](#response) Response

[​](#param-threads)

threads

array

Array of thread objects, most recent first.

Show thread

[​](#param-id)

id

string

Thread UUID.

[​](#param-remote-id)

remoteId

string

Same as `id`. Kept for compatibility with assistant-ui clients.

[​](#param-status)

status

string

`active` or `archived`.

[​](#param-title)

title

string

Human-readable title. Omitted if no title has been generated yet.

[​](#param-messages)

messages

array

Full message history - `[{ role, content }, ...]`. May be empty for brand-new threads.

[​](#param-updated-at)

updated\_at

string

ISO 8601 timestamp of the last modification.

### [​](#example) Example

Python

TypeScript

cURL

```
import requests

r = requests.get(
    "https://www.orgo.ai/api/chat/threads",
    params={"desktopId": "a3bb189e-8bf9-3888-9912-ace4e6543002"},
    headers={"Authorization": "Bearer sk_live_a3bb189e8bf93888"},
)
for t in r.json()["threads"]:
    print(t["id"], t.get("title", "(untitled)"))
```

```
{
  "threads": [
    {
      "id": "thr_01HX8W3Z6PN2Q1MRT7YV9K4BFA",
      "remoteId": "thr_01HX8W3Z6PN2Q1MRT7YV9K4BFA",
      "status": "active",
      "title": "GitHub search",
      "messages": [
        { "role": "user", "content": "Open github.com" },
        { "role": "assistant", "content": "Done - GitHub is open." }
      ],
      "updated_at": "2026-04-20T14:22:05.123Z"
    }
  ]
}
```

---

## [​](#create-thread) Create thread

```
POST /api/chat/threads
```

Creates an empty thread bound to a computer. Only needed when you want a thread ID before making the first completion - otherwise, omit this call and let `POST /v1/chat/completions` create one for you.

### [​](#request) Request

[​](#param-desktop-id-1)

desktopId

string

required

UUID of the computer to attach the thread to.

[​](#param-local-id)

localId

string

Optional client-side identifier. Echoed back as `externalId` in the response so clients can reconcile local and remote threads.

### [​](#response-2) Response

Returns `201 Created`.

[​](#param-remote-id-1)

remoteId

string

The new thread’s UUID. Use this as `thread_id` in subsequent chat completions.

[​](#param-external-id)

externalId

string

Mirror of `localId` from the request. Omitted if not supplied.

### [​](#example-2) Example

Python

TypeScript

cURL

```
import requests

r = requests.post(
    "https://www.orgo.ai/api/chat/threads",
    headers={"Authorization": "Bearer sk_live_a3bb189e8bf93888"},
    json={"desktopId": "a3bb189e-8bf9-3888-9912-ace4e6543002"},
)
thread_id = r.json()["remoteId"]
```

---

## [​](#get-thread) Get thread

```
GET /api/chat/threads/{id}
```

Fetches a single thread with its full message history. 403 if the thread belongs to another user; 404 if it does not exist.

### [​](#response-3) Response

[​](#param-remote-id-2)

remoteId

string

Thread UUID.

[​](#param-status-1)

status

string

`active` or `archived`.

[​](#param-title-1)

title

string

Title if set, otherwise omitted.

[​](#param-messages-1)

messages

array

Full message history in chronological order.

---

## [​](#update-thread) Update thread

```
PATCH /api/chat/threads/{id}
```

Updates title, replaces messages, or toggles archive state. Archive takes precedence over other fields when both are present.

### [​](#request-2) Request

[​](#param-title-2)

title

string

New human-readable title.

[​](#param-messages-2)

messages

array

Replaces the entire stored message history with this array. Use with care - this is a full overwrite, not an append.

[​](#param-archive)

archive

boolean

Set to `true` to archive. Archived threads are hidden from default list views but remain fetchable by ID.

[​](#param-unarchive)

unarchive

boolean

Set to `true` to restore an archived thread.

### [​](#response-4) Response

[​](#param-remote-id-3)

remoteId

string

Thread UUID.

[​](#param-status-2)

status

string

Updated status (`active` or `archived`).

[​](#param-title-3)

title

string

Updated title if set.

### [​](#example-3) Example

```
curl -X PATCH https://www.orgo.ai/api/chat/threads/thr_01HX8W3Z6PN2Q1MRT7YV9K4BFA \
  -H "Authorization: Bearer sk_live_a3bb189e8bf93888" \
  -H "Content-Type: application/json" \
  -d '{"title": "GitHub research session"}'
```

---

## [​](#delete-thread) Delete thread

```
DELETE /api/chat/threads/{id}
```

Permanently deletes the thread and its message history. Prefer `PATCH` with `archive: true` if you might need the conversation back.

### [​](#response-5) Response

```
{ "success": true }
```

---

## [​](#generate-title) Generate title

```
POST /api/chat/threads/{id}/title
```

Generates a short (3–6 word) title from the first few messages using Claude Haiku and saves it to the thread. Returns an assistant-ui-compatible text stream rather than JSON.

### [​](#request-3) Request

[​](#param-messages-3)

messages

array

required

The messages to summarize. Only the first three are considered. Each message is `{ role, content }` where `content` may be a string or an array of `{ type: "text", text }` blocks.

### [​](#response-6) Response

`text/plain` stream in the assistant-ui format:

```
0:"GitHub search session"
```

The generated title is also persisted to the thread, so a subsequent `GET` will include it in the `title` field.


---

## [​](#using-threads-with-completions) Using threads with completions

Threads compose with [chat completions](/api-reference/chat/completions) - you almost never manage them directly in production code:

```
# First turn - server creates the thread, returns its ID
first = client.chat.completions.create(
    model="claude-sonnet-4.6",
    messages=[{"role": "user", "content": "Open Chrome and go to github.com"}],
    extra_body={"computer_id": computer_id},
)
thread_id = first.orgo["thread_id"]

# Later turn - agent picks up where it left off
client.chat.completions.create(
    model="claude-sonnet-4.6",
    messages=[{"role": "user", "content": "Search for 'orgo'"}],
    extra_body={"computer_id": computer_id, "thread_id": thread_id},
)
```

## [​](#errors) Errors

| Status | Meaning |
| --- | --- |
| 400 | `desktopId` or `messages` missing from the request body. |
| 401 | Missing or invalid `Authorization` header. |
| 403 | The thread exists but belongs to a different user. |
| 404 | Thread does not exist. |
| 500 | Unexpected server error. Retry with backoff. |

Error responses are JSON with a single `error` field:

```
{ "error": "desktopId is required" }
```

[Previous](/api-reference/chat/completions)[Create workspaceCreate a new workspace to organize computers.

Next](/api-reference/workspaces/create)

⌘I