---
url: https://docs.orgo.ai/guides/claude-computer-use
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

## [​](#overview) Overview

This guide shows how to get started with Anthropic’s Claude Computer Use in a couple minutes using Orgo to control a virtual desktop environment.

## [​](#setup) Setup

Install the required packages:

pip

npm

yarn

pnpm

```
pip install orgo anthropic
```

Set up your API keys:

terminal

setup.py

setup.ts

```
# Export as environment variables
export ORGO_API_KEY=your_orgo_api_key
export ANTHROPIC_API_KEY=your_anthropic_api_key
```

## [​](#simple-usage) Simple Usage

The simplest way to use Orgo with Claude is through the built-in `prompt()` method:

simple.py

simple.ts

```
from orgo import Computer

# Initialize a computer
computer = Computer()

# Let Claude control the computer with natural language
computer.prompt("Open Chrome and search for pictures of cats")

# Clean up when done
computer.destroy()
```

This approach handles all the complexity of the agent loop automatically, making it easy to get started.

**Tip:** The simplest way to use Orgo is `computer.prompt("your instruction")`. The advanced usage below is only needed if you want to build a custom agent loop.

## [​](#customizing-the-prompt-method) Customizing the Prompt Method

You can customize the prompt with optional parameters:

custom.py

custom.ts

```
# Stream output as it arrives
result = computer.prompt(
    "Find and download the latest Claude paper from Anthropic's website",
    model="claude-opus-4-7",   # Use Opus for complex tasks
    max_steps=50,              # Limit agent steps
    stream=True,               # Stream text chunks
    on_text=lambda t: print(t, end=""),
)

# Multi-turn: continue where you left off
result2 = computer.prompt(
    "Now summarize the paper",
    thread_id=result["thread_id"],
)
```

## [​](#advanced-usage) Advanced Usage

For more control, you can implement your own agent loop using the Anthropic API directly:

advanced.py

advanced.ts

```
import anthropic
from orgo import Computer

def create_agent_loop(instruction, model="claude-sonnet-4-6"):
    # Initialize components
    computer = Computer() 
    client = anthropic.Anthropic()
    
    try:
        # Initialize conversation
        messages = [{"role": "user", "content": instruction}]
        
        # Define tools
        tools = [
            {
                "type": "computer_20251124",  # For Claude Sonnet 4.6+
                "name": "computer",
                "display_width_px": 1024,
                "display_height_px": 768,
                "display_number": 1
            },
            {
                "type": "bash_20250124",
                "name": "bash",
            }
        ]
        
        # Start the conversation with Claude
        response = client.beta.messages.create(
            model=model,
            messages=messages,
            tools=tools,
            betas=["computer-use-2025-11-24", "computer-use-2025-01-24"],
            max_tokens=8192
        )
        
        # Add Claude's response to conversation history
        messages.append({"role": "assistant", "content": response.content})
        
        # Continue the loop until Claude stops requesting tools
        iteration = 0
        max_iterations = 20
        
        while iteration < max_iterations:
            iteration += 1
            
            # Process all tool requests from Claude
            tool_results = []
            
            for block in response.content:
                if block.type == "tool_use":
                    # Execute the requested tool action
                    result = execute_tool_action(computer, block)
                    
                    # Format the result for Claude
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": [result]
                    })
            
            # If no tools were requested, Claude is done
            if not tool_results:
                break
                
            # Send the tool results back to Claude
            messages.append({"role": "user", "content": tool_results})
            
            # Get Claude's next response
            response = client.beta.messages.create(
                model=model,
                messages=messages,
                tools=tools,
                betas=["computer-use-2025-11-24", "computer-use-2025-01-24"],
                max_tokens=8192
            )
            
            # Add Claude's response to conversation history
            messages.append({"role": "assistant", "content": response.content})
        
        return messages
        
    finally:
        # Clean up
        computer.destroy()

def execute_tool_action(computer, tool_block):
    """Execute a tool action based on Claude's request."""
    action = tool_block.input.get("action")
    
    try:
        if action == "screenshot":
            # Capture a screenshot and return as base64
            image_data = computer.screenshot_base64()
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            }
            
        elif action == "left_click":
            x, y = tool_block.input["coordinate"]
            computer.left_click(x, y)
            return {"type": "text", "text": f"Clicked at ({x}, {y})"}
            
        elif action == "right_click":
            x, y = tool_block.input["coordinate"]
            computer.right_click(x, y)
            return {"type": "text", "text": f"Right-clicked at ({x}, {y})"}
            
        elif action == "double_click":
            x, y = tool_block.input["coordinate"]
            computer.double_click(x, y)
            return {"type": "text", "text": f"Double-clicked at ({x}, {y})"}
            
        elif action == "type":
            text = tool_block.input["text"]
            computer.type(text)
            return {"type": "text", "text": f"Typed: {text}"}
            
        elif action == "key":
            key = tool_block.input["text"]
            computer.key(key)
            return {"type": "text", "text": f"Pressed: {key}"}
            
        elif action == "scroll":
            direction = tool_block.input.get("scroll_direction", "down")
            amount = tool_block.input.get("scroll_amount", 1)
            computer.scroll(direction, amount)
            return {"type": "text", "text": f"Scrolled {direction} by {amount}"}
            
        elif action == "wait":
            duration = tool_block.input.get("duration", 1)
            computer.wait(duration)
            return {"type": "text", "text": f"Waited for {duration} seconds"}
            
        else:
            return {"type": "text", "text": f"Unsupported action: {action}"}
            
    except Exception as e:
        return {"type": "text", "text": f"Error executing {action}: {str(e)}"}
```

See all 144 lines

## [​](#using-claude’s-thinking-capability) Using Claude’s Thinking Capability

Claude 4.x models can stream their reasoning process through the `thinking` parameter:

thinking.py

thinking.ts

```
import anthropic
from orgo import Computer

# Initialize components
computer = Computer()
client = anthropic.Anthropic()

try:
    # Start a conversation with thinking enabled
    response = client.beta.messages.create(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": "Find an image of a cat on the web"}],
        tools=[{
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
            "display_number": 1
        },
        {
            "type": "bash_20250124",
            "name": "bash",
        }],
        betas=["computer-use-2025-11-24", "computer-use-2025-01-24"],
        thinking={"type": "enabled", "budget_tokens": 1024}  # Enable thinking
    )

    # Access the thinking content
    for block in response.content:
        if block.type == "thinking":
            print("Claude's reasoning:")
            print(block.thinking)
finally:
    # Clean up
    computer.destroy()
```

## [​](#tool-compatibility) Tool Compatibility

Orgo provides a complete set of methods corresponding to Claude’s computer use tools:

| Claude Tool Action | Orgo Method (Python) | Orgo Method (TypeScript) | Description |
| --- | --- | --- | --- |
| `screenshot` | `computer.screenshot()` | `await computer.screenshot()` | Capture the screen (returns PIL Image/Buffer) |
| `screenshot` | `computer.screenshot_base64()` | `await computer.screenshotBase64()` | Capture the screen (returns base64 string) |
| `left_click` | `computer.left_click(x, y)` | `await computer.leftClick(x, y)` | Left click at coordinates |
| `right_click` | `computer.right_click(x, y)` | `await computer.rightClick(x, y)` | Right click at coordinates |
| `double_click` | `computer.double_click(x, y)` | `await computer.doubleClick(x, y)` | Double click at coordinates |
| `type` | `computer.type(text)` | `await computer.type(text)` | Type text |
| `key` | `computer.key(key_sequence)` | `await computer.key(keySequence)` | Press keys (e.g., “Enter”, “ctrl+c”) |
| `scroll` | `computer.scroll(direction, amount)` | `await computer.scroll(direction, amount)` | Scroll in specified direction |
| `wait` | `computer.wait(seconds)` | `await computer.wait(seconds)` | Wait for specified seconds |

## [​](#picking-a-model) Picking a model

| Model | When to use |
| --- | --- |
| `claude-opus-4-7` | Hardest, multi-step desktop tasks where accuracy and judgment matter most. |
| `claude-sonnet-4-6` | The default for most computer-use agents - fast, capable, and dramatically cheaper than Opus. |
| `claude-haiku-4-5` | Tight latency budgets, simple flows, or high-volume parallel agents. |

All three are computer-use capable and share the same tool surface.

## [​](#tool-versions) Tool versions

Match the tool `type` and `betas` to the model family you’re calling:

* **Claude 4.x (Opus 4.7 / Sonnet 4.6 / Haiku 4.5):** `"type": "computer_20251124"` with betas `["computer-use-2025-11-24", "computer-use-2025-01-24"]`
* **Claude Sonnet 4.5:** `"type": "computer_20250124"` with betas `["computer-use-2025-01-24"]`

TypeScript users: All methods are async and must be awaited. The TypeScript SDK uses camelCase for method names (e.g., `leftClick` instead of `left_click`).

## [​](#video-tutorial) Video Tutorial

Here is a video version showing how to set up Claude Computer Use in 30 seconds:You can follow the video tutorial above or use this written guide

[Previous](/guides/templates/examples)[OpenAI Computer UseControl a computer with GPT using Orgo

Next](/guides/openai-computer-use)

⌘I