---
url: https://docs.orgo.ai/guides/models
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Orgo exposes programmatic endpoints for every computer action - screenshot, click, type, key, scroll, bash. You bring the model, Orgo provides the computer.
Any model with computer use support works. Here’s how to wire them up.

## [​](#anthropic-claude) Anthropic Claude

Claude Sonnet 4.6 and Opus 4.6 support computer use via the beta Messages API.

```
import anthropic
from orgo import Computer

computer = Computer()
client = anthropic.Anthropic()

messages = [{"role": "user", "content": "Open Chrome and search for AI news"}]

tools = [
    {
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": 1,
    },
    {
        "type": "bash_20250124",
        "name": "bash",
    },
]

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    tools=tools,
    messages=messages,
    betas=["computer-use-2025-11-24", "computer-use-2025-01-24"],
)

# Process tool_use blocks from response.content
for block in response.content:
    if block.type == "tool_use" and block.name == "computer":
        action = block.input["action"]
        if action == "screenshot":
            image = computer.screenshot_base64()
            # Return as tool_result with base64 image
        elif action == "left_click":
            x, y = block.input["coordinate"]
            computer.left_click(x, y)
        elif action == "type":
            computer.type(block.input["text"])
        elif action == "key":
            computer.key(block.input["text"])
        elif action == "scroll":
            computer.scroll(block.input["scroll_direction"], block.input["scroll_amount"])
    elif block.type == "tool_use" and block.name == "bash":
        output = computer.bash(block.input["command"])

computer.destroy()
```

**Models:** `claude-sonnet-4-6`, `claude-opus-4-6`
**Tool:** `computer_20251124` + `bash_20250124`
**Betas:** `computer-use-2025-11-24`, `computer-use-2025-01-24`
**Docs:** [Anthropic Computer Use](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use)


---

## [​](#openai-gpt) OpenAI GPT

OpenAI’s computer use works through the Responses API with a built-in `computer` tool.

```
from openai import OpenAI
from orgo import Computer

computer = Computer()
client = OpenAI()

response = client.responses.create(
    model="computer-use-preview",
    tools=[{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "linux",
    }],
    input=[{
        "role": "user",
        "content": [{"type": "input_text", "text": "Open Chrome and search for AI news"}],
    }],
    truncation="auto",
)

# Process computer_call actions
for item in response.output:
    if item.type == "computer_call":
        action = item.action
        if action.type == "click":
            computer.left_click(action.x, action.y)
        elif action.type == "double_click":
            computer.double_click(action.x, action.y)
        elif action.type == "type":
            computer.type(action.text)
        elif action.type == "key" or action.type == "keypress":
            keys = getattr(action, "keys", [getattr(action, "key", [])])
            computer.key("+".join(keys).lower() if len(keys) > 1 else keys[0])
        elif action.type == "scroll":
            scroll_y = getattr(action, "scroll_y", 0)
            computer.scroll("down" if scroll_y > 0 else "up", abs(scroll_y) // 100)

computer.destroy()
```

**Model:** `computer-use-preview`
**Tool:** `computer_use_preview`
**Docs:** [OpenAI Computer Use](https://platform.openai.com/docs/guides/tools-computer-use)


---

## [​](#google-gemini) Google Gemini

Gemini uses normalized coordinates (0-999 grid) and supports browser and desktop environments.

```
from google import genai
from google.genai import types
from orgo import Computer

computer = Computer()
client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

config = types.GenerateContentConfig(
    tools=[types.Tool(computer_use=types.ComputerUse(
        environment=types.Environment.ENVIRONMENT_BROWSER,
    ))],
)

response = client.models.generate_content(
    model="gemini-2.5-computer-use-preview-10-2025",
    contents="Open Chrome and search for AI news",
    config=config,
)

# Process computer use actions from response
# Gemini returns actions like click_at, type_text_at, scroll_document, navigate
# Coordinates are normalized (0-999) - scale to your display resolution
for part in response.candidates[0].content.parts:
    if hasattr(part, "executable_code"):
        pass  # Handle action
    if hasattr(part, "function_call"):
        fn = part.function_call
        if fn.name == "click_at":
            # Scale from 0-999 to actual pixels
            x = int(fn.args["x"] * 1024 / 999)
            y = int(fn.args["y"] * 768 / 999)
            computer.left_click(x, y)
        elif fn.name == "type_text_at":
            computer.type(fn.args["text"])

computer.destroy()
```

**Model:** `gemini-2.5-computer-use-preview-10-2025`
**Tool:** `ComputerUse` with `Environment.ENVIRONMENT_BROWSER`
**Coordinates:** Normalized 0-999 (scale to pixel resolution)
**Docs:** [Gemini Computer Use](https://ai.google.dev/gemini-api/docs/computer-use)


---

## [​](#other-models) Other models

Any model that outputs structured actions (click, type, screenshot) can work with Orgo. The pattern is always the same:

1. **Create** a computer with `Computer()`
2. **Screenshot** with `computer.screenshot_base64()`
3. **Send** the screenshot + instruction to your model
4. **Execute** the model’s actions with `computer.left_click()`, `computer.type()`, etc.
5. **Loop** until the task is done

Models like **Kimi K2.5**, **Agent S2**, and other open-source CUA models all follow this pattern.

## [​](#orgo-action-reference) Orgo action reference

| Action | Python | Description |
| --- | --- | --- |
| Screenshot | `computer.screenshot_base64()` | Capture screen as base64 |
| Left click | `computer.left_click(x, y)` | Click at coordinates |
| Right click | `computer.right_click(x, y)` | Right-click |
| Double click | `computer.double_click(x, y)` | Double-click |
| Type | `computer.type("text")` | Type text |
| Key press | `computer.key("Enter")` | Press key or combo (`ctrl+c`) |
| Scroll | `computer.scroll("down", 3)` | Scroll direction + amount |
| Bash | `computer.bash("ls -la")` | Run terminal command |
| Wait | `computer.wait(2)` | Pause in seconds |

Full API details: [API Reference](/api-reference/introduction)

[Previous](/guides/skill)[OpenClawRun OpenClaw on an Orgo cloud computer

Next](/guides/openclaw)

⌘I