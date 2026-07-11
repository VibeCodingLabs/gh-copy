---
url: https://docs.orgo.ai/api-reference/chat/completions
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Send a message to an AI model and have it drive an Orgo computer on your behalf. The model sees the screen, clicks, types, and runs shell commands until your request is satisfied, then returns the final assistant message. Use this endpoint as a drop-in replacement for `openai.chat.completions.create`.

The response is wire-compatible with OpenAI’s chat completions. Any SDK that points at `https://www.orgo.ai/api/v1` works unchanged - the only required extension is passing a `computer_id` to bind the agent to a running VM.

## [​](#endpoint) Endpoint

```
POST https://www.orgo.ai/api/v1/chat/completions
```

**Auth:** `Authorization: Bearer sk_live_...`

## [​](#request) Request

[​](#param-computer-id)

computer\_id

string

required

UUID of a running Orgo computer - returned as the `id` field by [Create computer](/api-reference/computers/create). The authenticated user must own the computer or be a member of its workspace.

[​](#param-messages)

messages

array

required

Array of `{ role, content }` objects. `role` must be `user` or `assistant`. The first message must have role `user`. When continuing a thread, only the new messages need to be passed - prior history is loaded from the thread.

[​](#param-model)

model

string

default:"claude-sonnet-4.6"

Model identifier. One of `claude-sonnet-4.6` or `claude-opus-4.6`. See [Models](#models) below.

[​](#param-stream)

stream

boolean

default:"false"

If `true`, responses are streamed as OpenAI-format Server-Sent Events. The connection stays open until the agent finishes or the request is cancelled.

[​](#param-thread-id)

thread\_id

string

Continue a previous multi-turn session. When set, the server loads the thread’s history, runs the agent with full context, and appends new messages on completion. If omitted, a new thread is created automatically and its ID returned in the response.

[​](#param-max-steps)

max\_steps

integer

default:"100"

Maximum number of agent steps (screenshot → action → observation) before the run stops. Increase for long, multi-phase workflows.

### [​](#headers) Headers

[​](#param-authorization)

Authorization

string

required

`Bearer sk_live_...` - your Orgo API key. Get one at [orgo.ai/settings/api-keys](https://orgo.ai/settings/api-keys).

[​](#param-x-anthropic-key)

x-anthropic-key

string

Bring-your-own Anthropic key. When present, requests bill directly to your Anthropic account instead of drawing from your Orgo credit balance. Enterprise plans can omit this and still bypass metering.

## [​](#response) Response

### [​](#non-streaming) Non-streaming

[​](#param-id)

id

string

Request identifier (`chatcmpl-...`). Also returned as the `X-Request-Id` response header.

[​](#param-object)

object

string

Always `chat.completion`.

[​](#param-created)

created

integer

Unix timestamp (seconds).

[​](#param-model-1)

model

string

The model ID used for the request.

[​](#param-choices)

choices

array

Single-element array containing the final assistant message.

Show choice

[​](#param-index)

index

integer

Always `0`.

[​](#param-message)

message

object

`{ role: "assistant", content: string }` - the model’s final text response after the agent loop terminates.

[​](#param-finish-reason)

finish\_reason

string

Always `stop` on success.

[​](#param-usage)

usage

object

Token counts for the full agent loop (all intermediate turns, not just the final message).

Show usage

[​](#param-prompt-tokens)

prompt\_tokens

integer

Total input tokens.

[​](#param-completion-tokens)

completion\_tokens

integer

Total output tokens.

[​](#param-total-tokens)

total\_tokens

integer

Sum of input and output tokens.

[​](#param-orgo)

orgo

object

Orgo-specific metadata not in the OpenAI spec.

Show orgo

[​](#param-thread-id-1)

thread\_id

string

ID of the thread this completion belongs to. Pass it back in a later request to continue the conversation.

[​](#param-steps)

steps

integer

Number of agent steps executed (screenshot + action cycles).

[​](#param-cost-cents)

cost\_cents

number

Credits consumed by this request, in cents. `0` for BYOK and enterprise plans.

[​](#param-credit-balance-cents)

credit\_balance\_cents

integer

Remaining credit balance after settlement. Omitted for BYOK and enterprise plans.

### [​](#response-headers) Response headers

| Header | Description |
| --- | --- |
| `X-Request-Id` | Echoes the `id` field. Include it when reporting issues. |
| `X-Thread-Id` | Thread ID. Present when a thread is created or continued. |

## [​](#streaming) Streaming

When `stream: true`, the server returns `text/event-stream` with standard OpenAI `chat.completion.chunk` events:

```
data: {"id":"chatcmpl-01HX...","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"chatcmpl-01HX...","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"Opening Chrome"},"finish_reason":null}]}

data: {"id":"chatcmpl-01HX...","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}],"usage":{"prompt_tokens":1240,"completion_tokens":312,"total_tokens":1552}}

data: [DONE]
```

Only the model’s text output is streamed. Tool calls, screenshots, and intermediate reasoning happen server-side and are not exposed as deltas. The `X-Thread-Id` header is set on the initial response so clients can associate the stream with a thread before the first chunk arrives.

## [​](#examples) Examples

Python (OpenAI SDK)

TypeScript (OpenAI SDK)

cURL

```
from openai import OpenAI

client = OpenAI(
    base_url="https://www.orgo.ai/api/v1",
    api_key="sk_live_a3bb189e8bf93888",
)

response = client.chat.completions.create(
    model="claude-sonnet-4.6",
    messages=[
        {"role": "user", "content": "Open Chrome and search for 'claude computer use'"}
    ],
    extra_body={"computer_id": "a3bb189e-8bf9-3888-9912-ace4e6543002"},
)

print(response.choices[0].message.content)
print(f"Thread: {response.orgo['thread_id']}")
print(f"Cost: ${response.orgo['cost_cents'] / 100:.4f}")
```

### [​](#streaming-with-raw-sse) Streaming with raw SSE

Python

cURL

```
import json, httpx

with httpx.stream(
    "POST",
    "https://www.orgo.ai/api/v1/chat/completions",
    headers={"Authorization": "Bearer sk_live_a3bb189e8bf93888"},
    json={
        "model": "claude-sonnet-4.6",
        "computer_id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
        "messages": [{"role": "user", "content": "Open github.com"}],
        "stream": True,
    },
    timeout=300,
) as r:
    for line in r.iter_lines():
        if not line.startswith("data: "):
            continue
        payload = line[6:]
        if payload == "[DONE]":
            break
        delta = json.loads(payload)["choices"][0].get("delta", {})
        if "content" in delta:
            print(delta["content"], end="", flush=True)
```

### [​](#continuing-a-thread) Continuing a thread

Pass the `thread_id` returned by a previous response. The agent loads the prior conversation and picks up where it left off.

```
first = client.chat.completions.create(
    model="claude-sonnet-4.6",
    messages=[{"role": "user", "content": "Open Chrome and go to github.com"}],
    extra_body={"computer_id": computer_id},
)

follow_up = client.chat.completions.create(
    model="claude-sonnet-4.6",
    messages=[{"role": "user", "content": "Search for 'orgo'"}],
    extra_body={
        "computer_id": computer_id,
        "thread_id": first.orgo["thread_id"],
    },
)
```

### [​](#bring-your-own-anthropic-key) Bring your own Anthropic key

Pass `x-anthropic-key` to bill the request against your own Anthropic account. Orgo credits are not consumed and `orgo.cost_cents` is `0`.

```
curl https://www.orgo.ai/api/v1/chat/completions \
  -H "Authorization: Bearer sk_live_a3bb189e8bf93888" \
  -H "x-anthropic-key: sk-ant-api03-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4.6",
    "computer_id": "a3bb189e-8bf9-3888-9912-ace4e6543002",
    "messages": [{"role": "user", "content": "Take a screenshot"}]
  }'
```

## [​](#example-response) Example response

```
{
  "id": "chatcmpl-01HX8W3Z6PN2Q1MRT7YV9K4BFA",
  "object": "chat.completion",
  "created": 1745136000,
  "model": "claude-sonnet-4.6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Done. Chrome is open on google.com with the search results for 'claude computer use'."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 1240,
    "completion_tokens": 312,
    "total_tokens": 1552
  },
  "orgo": {
    "thread_id": "thr_01HX8W3Z6PN2Q1MRT7YV9K4BFA",
    "steps": 6,
    "cost_cents": 3.84,
    "credit_balance_cents": 9616
  }
}
```

## [​](#models) Models

| Model | Best for | Notes |
| --- | --- | --- |
| `claude-sonnet-4.6` | Default. Fast, cost-effective, handles most workflows. | Tool version `computer_20251124`. |
| `claude-opus-4.6` | Complex, multi-step tasks where reliability matters more than latency. | Tool version `computer_20251124`. More expensive per token. |

Orgo’s OpenAI-compatible endpoint uses dotted model IDs (`claude-sonnet-4.6`). If you’re calling Anthropic’s native SDK directly in the [Claude Computer Use guide](/guides/claude-computer-use), use the hyphenated form (`claude-sonnet-4-6`) - that’s Anthropic’s canonical identifier.

## [​](#billing) Billing

Requests are metered after the agent loop finishes. For non-BYOK, non-enterprise users, Orgo places a credit hold at request start and settles against actual token usage on completion. If the request errors before any tokens are consumed, the hold is refunded. Pricing matches Anthropic’s token rates plus a small platform margin; exact per-request cost is returned in `orgo.cost_cents`.

## [​](#errors) Errors

| Status | Code | When |
| --- | --- | --- |
| 400 | `invalid_json` | Request body is not valid JSON. |
| 400 | `invalid_model` | `model` is not `claude-sonnet-4.6` or `claude-opus-4.6`. |
| 400 | `missing_computer_id` | `computer_id` was not supplied. |
| 400 | `empty_messages` | `messages` array is empty. |
| 400 | `invalid_message_order` | First message does not have role `user`. |
| 400 | `context_overflow` | Conversation exceeds the model’s context window. Start a new thread or prune history. |
| 401 | `invalid_api_key` | Missing or invalid `Authorization` header. |
| 402 | `credits_exhausted` | Credit balance too low. Add credits at [orgo.ai/settings/billing](https://orgo.ai/settings/billing). Includes `balance_cents`. |
| 404 | `computer_not_found` | Computer does not exist, is not accessible, or does not belong to your project. |
| 500 | `internal_error` | Unexpected server error. Retry with exponential backoff. Include the `X-Request-Id` header when reporting. |

All error responses have the shape:

```
{
  "error": {
    "type": "invalid_request",
    "message": "computer_id is required. Pass the ID of a running Orgo computer.",
    "code": "missing_computer_id"
  }
}
```

[Previous](/api-reference/authentication)[ThreadsPersist conversation history across multiple completions

Next](/api-reference/chat/threads)

⌘I