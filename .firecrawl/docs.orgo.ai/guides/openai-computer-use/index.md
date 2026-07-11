---
url: https://docs.orgo.ai/guides/openai-computer-use
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

## [​](#overview) Overview

OpenAI’s Computer Use lets AI agents control computer interfaces through the Responses API. This guide shows how to use it with Orgo’s virtual desktops.

The `computer-use-preview` model remains OpenAI’s dedicated computer-use endpoint. GPT-5 series models can also drive an Orgo computer through the standard tool-calling API - wire up screenshot, click, and type as regular tools.

## [​](#quick-start) Quick Start

1

Install packages

```
pip install orgo openai python-dotenv
```

2

Set up API keys

```
export ORGO_API_KEY=your_orgo_api_key
export OPENAI_API_KEY=your_openai_api_key
```

3

Run your first task

```
import time
from openai import OpenAI
from orgo import Computer

# Initialize
client = OpenAI()
computer = Computer()

# Create request with task
response = client.responses.create(
    model="computer-use-preview",
    tools=[{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "linux"
    }],
    input=[{
        "role": "user",
        "content": [{
            "type": "input_text",
            "text": "Open Chrome and search for OpenAI"
        }]
    }],
    truncation="auto"
)

# Execute the suggested action
actions = [item for item in response.output if item.type == "computer_call"]
if actions:
    action = actions[0].action
    if action.type == "click":
        computer.left_click(action.x, action.y)
    elif action.type == "type":
        computer.type(action.text)

# Clean up
computer.destroy()
```

## [​](#complete-example) Complete Example

Here’s a full working example that handles the complete agent loop:

example.py

```
import time
import base64
from openai import OpenAI
from orgo import Computer
from dotenv import load_dotenv

load_dotenv()

def run_computer_task(task, computer_id=None):
    """Execute a task using OpenAI Computer Use with Orgo."""
    
    # Initialize OpenAI client and Orgo computer
    client = OpenAI()
    computer = Computer(computer_id=computer_id)
    print(f"🖥️  Computer ID: {computer.computer_id}")
    
    # Create initial request with the task
    response = client.responses.create(
        model="computer-use-preview",
        tools=[{
            "type": "computer_use_preview",
            "display_width": 1024,
            "display_height": 768,
            "environment": "linux"  # Orgo provides Linux desktops
        }],
        input=[{
            "role": "user",
            "content": [{
                "type": "input_text", 
                "text": f"""IMPORTANT: You are controlling a Linux desktop. 
- Always double-click desktop icons to open applications
- Use keyboard shortcuts as single commands (e.g., 'ctrl+c' not separate keys)
Task: {task}"""
            }]
        }],
        reasoning={"summary": "concise"},  # Show reasoning steps
        truncation="auto"  # Required for computer use
    )
    
    # Main agent loop
    while True:
        # Display progress
        for item in response.output:
            if item.type == "reasoning" and hasattr(item, "summary"):
                for summary in item.summary:
                    if hasattr(summary, "text"):
                        print(f"💭 {summary.text}")
            elif item.type == "text" and hasattr(item, "text"):
                print(f"💬 {item.text}")
        
        # Get computer actions from response
        actions = [item for item in response.output if item.type == "computer_call"]
        
        # If no actions, task is complete
        if not actions:
            print("✓ Task completed")
            break
            
        # Execute the action
        action = actions[0]
        print(f"→ {action.action.type}")
        
        execute_action(computer, action.action)
        time.sleep(1)  # Allow UI to update
        
        # Capture screenshot and continue
        screenshot = computer.screenshot_base64()
        
        response = client.responses.create(
            model="computer-use-preview",
            previous_response_id=response.id,  # Link to previous response
            tools=[{
                "type": "computer_use_preview",
                "display_width": 1024,
                "display_height": 768,
                "environment": "linux"
            }],
            input=[{
                "call_id": action.call_id,
                "type": "computer_call_output",
                "output": {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{screenshot}"
                }
            }],
            reasoning={"summary": "concise"},
            truncation="auto"
        )
    
    return computer


def execute_action(computer, action):
    """Execute computer actions using Orgo."""
    
    match action.type:
        case "click":
            # Handle left/right clicks
            if getattr(action, 'button', 'left') == "right":
                computer.right_click(action.x, action.y)
            else:
                computer.left_click(action.x, action.y)
                
        case "double_click":
            computer.double_click(action.x, action.y)
            
        case "type":
            computer.type(action.text)
            
        case "key" | "keypress":
            # Handle single keys or key combinations
            keys = getattr(action, 'keys', [getattr(action, 'key', [])])
            if len(keys) > 1:
                # Multiple keys = keyboard shortcut
                computer.key('+'.join(keys).lower())
            else:
                # Single key press
                for key in keys:
                    computer.key(key)
                    
        case "scroll":
            # Convert scroll amount to direction
            scroll_y = getattr(action, 'scroll_y', 0)
            direction = "down" if scroll_y > 0 else "up"
            computer.scroll(direction, abs(scroll_y) // 100)
            
        case "wait":
            computer.wait(getattr(action, 'seconds', 2))
            
        case "screenshot":
            # Screenshot is taken automatically in the loop
            pass


if __name__ == "__main__":
    # Example usage
    computer = run_computer_task("Open a terminal and list files")
    
    # Always clean up
    computer.destroy()
```

See all 140 lines

## [​](#usage-examples) Usage Examples

### [​](#basic-tasks) Basic Tasks

```
# Open a browser
computer = run_computer_task("Open Chrome")

# Navigate to a website
computer = run_computer_task("Go to github.com and search for orgo")

# Fill out a form
computer = run_computer_task("Fill out the contact form with test data")

# Always clean up
computer.destroy()
```

### [​](#complex-workflows) Complex Workflows

```
# Multi-step task
task = """
1. Open a text editor
2. Write a Python hello world program
3. Save it as hello.py
4. Open a terminal
5. Run the program
"""
computer = run_computer_task(task)
computer.destroy()
```

### [​](#reusing-sessions) Reusing Sessions

```
# First task
computer = run_computer_task("Open VS Code")
computer_id = computer.computer_id

# Continue in same session
computer = run_computer_task(
    "Create a new Python file", 
    computer_id=computer_id
)

# Clean up when done
computer.destroy()
```

## [​](#key-concepts) Key Concepts

### [​](#the-agent-loop) The Agent Loop

OpenAI Computer Use works in a continuous loop:

1. **Request** → Send task to the model
2. **Action** → Model suggests an action (click, type, etc.)
3. **Execute** → Your code executes the action
4. **Screenshot** → Capture the result
5. **Repeat** → Continue until task is complete

### [​](#action-types) Action Types

| Action | Description | Example |
| --- | --- | --- |
| `click` | Click at coordinates | Click button at (100, 200) |
| `double_click` | Double-click | Open desktop icon |
| `type` | Type text | Enter username |
| `key` | Press key(s) | Press Enter, Ctrl+C |
| `scroll` | Scroll page | Scroll down 3 units |
| `wait` | Pause execution | Wait 2 seconds |
| `screenshot` | Take screenshot | Capture current state |

### [​](#safety-features) Safety Features

OpenAI includes safety checks to prevent misuse:

```
# Handle safety checks if they occur
if hasattr(action, 'pending_safety_checks'):
    for check in action.pending_safety_checks:
        print(f"⚠️  Safety check: {check.message}")
        # Acknowledge in next request if proceeding
```

## [​](#best-practices) Best Practices

### [​](#1-clear-instructions) 1. Clear Instructions

```
# ✅ Good - Specific and clear
task = "Open Chrome, go to github.com, and star the orgo repository"

# ❌ Avoid - Too vague
task = "Do some web stuff"
```

### [​](#2-error-handling) 2. Error Handling

```
def safe_run_task(task):
    """Run task with error handling."""
    computer = None
    try:
        computer = run_computer_task(task)
        return computer
    except Exception as e:
        print(f"❌ Error: {e}")
        if computer:
            computer.destroy()
        raise
```

### [​](#3-session-management) 3. Session Management

```
# Use context manager pattern
class ComputerSession:
    def __init__(self, task):
        self.task = task
        self.computer = None
        
    def __enter__(self):
        self.computer = run_computer_task(self.task)
        return self.computer
        
    def __exit__(self, *args):
        if self.computer:
            self.computer.destroy()

# Usage
with ComputerSession("Open calculator") as computer:
    print(f"Session ID: {computer.computer_id}")
```

### [​](#4-timing-considerations) 4. Timing Considerations

```
# Add delays for UI updates
time.sleep(1)  # After clicks
time.sleep(2)  # After opening applications
time.sleep(0.5)  # After typing
```

## [​](#comparison-with-claude) Comparison with Claude

| Feature | OpenAI Computer Use | Claude Computer Use |
| --- | --- | --- |
| API | Responses API | Messages API |
| Model | `computer-use-preview` | `claude-sonnet-4-6` |
| Beta Tag | Built-in | `computer-use-2025-11-24` |
| Reasoning | Optional summaries | Thinking blocks |
| Environment | Multiple (browser, OS) | Single tool definition |

## [​](#limitations) Limitations

* **Beta Status**: OpenAI Computer Use is in preview and may have unexpected behaviors
* **Rate Limits**: The model has constrained rate limits
* **Environment**: Best suited for browser-based and desktop tasks

## [​](#next-steps) Next Steps

## OpenAI Docs

Official OpenAI Computer Use documentation

## Orgo Quickstart

Learn more about Orgo’s virtual desktops

[Previous](/guides/claude-computer-use)[Gemini Computer UseControl virtual desktops with Gemini 2.5

Next](/guides/gemini-computer-use)

⌘I