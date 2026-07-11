---
url: https://docs.orgo.ai/quickstart
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

This guide uses the **raw HTTP API**. It’s the same surface every Orgo SDK wraps. Drop `curl`, `requests`, or `fetch` against `https://www.orgo.ai/api` and you’re done. No SDK required.

Prefer a helper library? Skip to [Use the SDK](#use-the-sdk) after you’ve
seen the raw calls. The SDK is a thin wrapper around the exact same
endpoints.

## [​](#1-get-your-api-key) 1. Get your API key

Create an account at [orgo.ai/start](https://www.orgo.ai/start), then copy
your key from [orgo.ai/workspaces](https://www.orgo.ai/workspaces).

```
export ORGO_API_KEY=sk_live_...
```

Every request takes this as a bearer token:

```
Authorization: Bearer $ORGO_API_KEY
```

## [​](#2-create-a-workspace) 2. Create a workspace

Workspaces group related computers.

cURL

Python

TypeScript

```
curl -X POST https://www.orgo.ai/api/workspaces \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "quickstart"}'
```

Response:

```
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "quickstart",
  "status": "active",
  "created_at": "2026-04-22T10:00:00Z"
}
```

Save the `id`. You’ll pass it as `workspace_id` when creating a computer.

## [​](#3-create-a-computer) 3. Create a computer

cURL

Python

TypeScript

```
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "agent-1",
    "ram": 4,
    "cpu": 1
  }'
```

Response (abridged):

```
{
  "id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
  "name": "agent-1",
  "status": "running",
  "ram": 4,
  "cpu": 1,
  "resolution": "1280x720x24",
  "url": "https://orgo.ai/workspaces/550e8400-e29b-41d4-a716-446655440000/computers/a3bb189e-8bf9-3888-9912-ace4e6543002"
}
```

The computer boots in under 500ms and is ready to accept commands immediately.

## [​](#4-take-a-screenshot) 4. Take a screenshot

cURL

Python

TypeScript

```
curl https://www.orgo.ai/api/computers/$COMPUTER_ID/screenshot \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

## [​](#5-click-type-and-run-shell-commands) 5. Click, type, and run shell commands

cURL

Python

TypeScript

```
# Click at (100, 200)
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/click \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x": 100, "y": 200}'

# Type text
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/type \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!"}'

# Press Enter
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/key \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key": "Enter"}'

# Run a shell command
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/bash \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la"}'
```

Full list of actions: [Mouse](/api-reference/computers/click) · [Keyboard](/api-reference/computers/type) · [Scroll](/api-reference/computers/scroll) · [Bash](/api-reference/computers/bash) · [Python exec](/api-reference/computers/exec) · [Wait](/api-reference/computers/wait) · [Drag](/api-reference/computers/drag).

## [​](#6-let-an-ai-drive-it) 6. Let an AI drive it

Orgo exposes an OpenAI-compatible endpoint at `/api/v1/chat/completions`.
Point any OpenAI SDK at `https://www.orgo.ai/api/v1`, pass
`computer_id`, and the model will screenshot, click, and type on its own
until your instruction is done.

cURL

Python

TypeScript

```
curl https://www.orgo.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "computer_id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
    "messages": [
      {"role": "user", "content": "Open Chrome and search for AI news"}
    ]
  }'
```

Stream the agent’s progress token-by-token with `"stream": true`. See [Create chat completion](/api-reference/chat/completions) for the full spec, including thread continuation, custom Anthropic key, and error handling.

## [​](#7-lifecycle) 7. Lifecycle

```
# Stop  (auto-stop also does this after idle timeout)
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/stop \
  -H "Authorization: Bearer $ORGO_API_KEY"

# Start a stopped computer
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/start \
  -H "Authorization: Bearer $ORGO_API_KEY"

# Restart (reboot)
curl -X POST https://www.orgo.ai/api/computers/$COMPUTER_ID/restart \
  -H "Authorization: Bearer $ORGO_API_KEY"

# Delete permanently
curl -X DELETE https://www.orgo.ai/api/computers/$COMPUTER_ID \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

Auto-stop is disabled by default. Configure it per-computer with `auto_stop_minutes`. See [Auto-stop](/guides/auto-stop).


---

## [​](#use-the-sdk) Use the SDK

If you’d rather not wire HTTP calls by hand, the official SDKs wrap this
exact surface. They give you typed helpers, connection pooling for VNC,
and one-line `computer.prompt("do X")` for the AI agent loop.

Python

TypeScript

```
pip install orgo
```

Python

TypeScript

```
from orgo import Computer

computer = Computer(workspace="quickstart")

# Each of these is a direct wrapper over a single HTTP call.
computer.left_click(100, 200)
computer.type("Hello, world!")
computer.key("Enter")
output = computer.bash("ls -la")

# One-liner for the AI agent loop
computer.prompt("Open Chrome and search for AI news")

computer.destroy()
```

Both SDKs read `ORGO_API_KEY` from the environment and default to the
same base URL you’d call directly.


---

## [​](#next-steps) Next steps

## API Reference

Every endpoint, every field.

## Use any model

Claude, GPT, Gemini, Hermes. Any OpenAI-compatible model.

## Embed computers

Drop a live VM into your own app via VNC.

[Previous](/introduction)[CLIDrive Orgo cloud computers from your terminal.

Next](/guides/cli)

⌘I