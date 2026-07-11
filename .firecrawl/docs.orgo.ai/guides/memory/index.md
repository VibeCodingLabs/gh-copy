---
url: https://docs.orgo.ai/guides/memory
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Add persistent memory to your computer use agents with [Mem0](https://mem0.ai). The agent remembers user preferences, learns from past interactions, and gets better over time.

## [​](#setup) Setup

```
pip install mem0ai orgo openai
```

.env

```
ORGO_API_KEY=sk_live_...
OPENAI_API_KEY=sk-...
```

## [​](#example) Example

```
from mem0 import Memory
from openai import OpenAI
from orgo import Computer

memory = Memory()
computer = Computer()

client = OpenAI(
    base_url="https://www.orgo.ai/api/v1",
    api_key="sk_live_..."
)

user_id = "alice"

# Teach preferences
memory.add(
    messages=[{"role": "user", "content": "I prefer Firefox over Chrome"}],
    user_id=user_id,
)
memory.add(
    messages=[{"role": "user", "content": "I like dark themes"}],
    user_id=user_id,
)

# Recall memories before a task
results = memory.search(query="open a browser", user_id=user_id, limit=5)
context = "\n".join(f"- {m['memory']}" for m in results.get("results", []))

# Use memories as context
response = client.chat.completions.create(
    model="claude-sonnet-4.6",
    messages=[{
        "role": "user",
        "content": f"User preferences:\n{context}\n\nTask: Open my preferred browser and enable dark mode"
    }],
    extra_body={"computer_id": computer.computer_id},
)

print(response.choices[0].message.content)

# Store the interaction for next time
memory.add(
    messages=[
        {"role": "user", "content": "Open my preferred browser"},
        {"role": "assistant", "content": "Opened Firefox with dark mode"},
    ],
    user_id=user_id,
)

computer.destroy()
```

## [​](#managing-memories) Managing memories

```
from mem0 import Memory

memory = Memory()

# View all memories
for m in memory.get_all(user_id="alice"):
    print(f"  {m['memory']}")

# Search
results = memory.search(query="browser", user_id="alice", limit=5)

# Clear
memory.delete_all(user_id="alice")
```

## [​](#how-it-works) How it works

1. **Search** - Before each task, query Mem0 for relevant memories
2. **Inject** - Add memories as context in the prompt
3. **Execute** - The AI agent acts with full context of past preferences
4. **Store** - Save new interactions so future tasks benefit

Each `user_id` maintains its own separate memory, so you can run multiple users or contexts (e.g. `"work"` vs `"personal"`).

## [​](#learn-more) Learn more

## Mem0 Docs

Memory API reference

## Computer Use API

Orgo completions endpoint

[Previous](/guides/instance-types)[Embed VMsEmbed virtual computers into your applications

Next](/guides/embed-vms)

⌘I