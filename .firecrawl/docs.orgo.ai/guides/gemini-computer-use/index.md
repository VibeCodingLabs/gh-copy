---
url: https://docs.orgo.ai/guides/gemini-computer-use
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

## [​](#overview) Overview

This guide shows how to get started with Google’s Gemini 2.5 Computer Use in minutes using Orgo to control a virtual desktop environment.

## [​](#setup) Setup

Install the required packages:

pip

```
pip install orgo google-genai pillow python-dotenv
```

Set up your API keys in a `.env` file:

.env

```
ORGO_API_KEY=your_orgo_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Or export them as environment variables:

terminal

```
export ORGO_API_KEY=your_orgo_api_key
export GEMINI_API_KEY=your_gemini_api_key
```

## [​](#complete-example) Complete Example

Here’s a full working example that handles the complete agent loop:

example.py

```
import os
import time
import base64
import io
from google import genai
from google.genai import types
from orgo import Computer
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

# Connect to your Orgo computer
# Get your computer_id from https://orgo.ai/workspaces
computer = Computer(computer_id="your-computer-id")

# Screen resolution
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# System prompt with Ubuntu-specific instructions
SYSTEM_PROMPT = f"""You are controlling an Ubuntu Linux virtual machine with a display resolution of {SCREEN_WIDTH}x{SCREEN_HEIGHT}.

<SYSTEM_CAPABILITY>
* You have access to a virtual Ubuntu desktop environment with standard applications
* You can see the current state through screenshots and control the computer through actions
* The environment has Firefox browser and standard Ubuntu applications pre-installed
</SYSTEM_CAPABILITY>

<UBUNTU_DESKTOP_GUIDELINES>
* CRITICAL: When opening applications or files on the Ubuntu desktop, you MUST USE DOUBLE-CLICK, not single-click
* Single-click only selects desktop icons but DOES NOT open them
* Desktop interactions:
  - Desktop icons (apps/folders): DOUBLE-CLICK to open
  - Menu items: SINGLE-CLICK to select
  - Taskbar/launcher icons: SINGLE-CLICK to open
  - Window buttons (close/minimize/maximize): SINGLE-CLICK
  - File browser items: DOUBLE-CLICK to open
* Always start by taking a screenshot to see the current state
* When you need to submit or confirm, use the 'Enter' key
</UBUNTU_DESKTOP_GUIDELINES>

<IMPORTANT_NOTES>
* Be efficient with screenshots - only take them when you need to see the current state
* Wait for pages/applications to load before taking another screenshot
* Batch multiple actions together when possible before checking the result
</IMPORTANT_NOTES>"""

def denormalize_x(x: int) -> int:
    """Convert normalized x coordinate (0-999) to actual pixel."""
    return int(x / 1000 * SCREEN_WIDTH)

def denormalize_y(y: int) -> int:
    """Convert normalized y coordinate (0-999) to actual pixel."""
    return int(y / 1000 * SCREEN_HEIGHT)

def get_screenshot_png() -> bytes:
    """Get screenshot as PNG bytes (Gemini requires PNG format)."""
    jpeg_data = base64.b64decode(computer.screenshot_base64())
    image = Image.open(io.BytesIO(jpeg_data))
    png_buffer = io.BytesIO()
    image.save(png_buffer, format='PNG')
    return png_buffer.getvalue()

def get_current_url() -> str:
    """Get the current URL from the browser."""
    try:
        result = computer.bash("xdotool getactivewindow getwindowname")
        return result if result else "about:blank"
    except:
        return "about:blank"

def execute_function_calls(candidate):
    """Execute function calls from Gemini's response."""
    results = []
    function_calls = [
        part.function_call 
        for part in candidate.content.parts 
        if part.function_call
    ]
    
    for function_call in function_calls:
        fname = function_call.name
        args = function_call.args
        action_result = {}
        
        print(f"  → {fname}")
        
        try:
            if fname == "open_web_browser":
                pass  # Browser already open
            elif fname == "click_at":
                computer.left_click(denormalize_x(args["x"]), denormalize_y(args["y"]))
            elif fname == "type_text_at":
                computer.left_click(denormalize_x(args["x"]), denormalize_y(args["y"]))
                computer.type(args["text"])
                if args.get("press_enter", False):
                    computer.key("Return")
            elif fname == "scroll_document":
                computer.scroll(args["direction"], 3)
            elif fname == "key_combination":
                computer.key(args["keys"])
            elif fname == "go_back":
                computer.key("alt+Left")
            elif fname == "navigate":
                url = args["url"]
                computer.bash(f'firefox "{url}" &')
                action_result["url"] = url
            elif fname == "wait_5_seconds":
                computer.wait(5)
            else:
                print(f"    Warning: Unimplemented function {fname}")
            
            time.sleep(1)  # Wait for UI to update
        except Exception as e:
            print(f"    Error: {e}")
            action_result = {"error": str(e)}
        
        results.append((fname, action_result))
    
    return results

def get_function_responses(results):
    """Create function responses with screenshot and URL."""
    screenshot_png = get_screenshot_png()
    current_url = get_current_url()
    function_responses = []
    
    for name, result in results:
        response_data = {
            "status": "completed",
            "url": result.get("url", current_url)
        }
        response_data.update(result)
        
        function_responses.append(
            types.FunctionResponse(
                name=name,
                response=response_data,
                parts=[
                    types.FunctionResponsePart(
                        inline_data=types.FunctionResponseBlob(
                            mime_type="image/png",
                            data=screenshot_png
                        )
                    )
                ]
            )
        )
    
    return function_responses

try:
    # Configure Computer Use tool with system instruction
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[
            types.Tool(
                computer_use=types.ComputerUse(
                    environment=types.Environment.ENVIRONMENT_BROWSER
                )
            )
        ]
    )
    
    # Define task
    task = "Open Chrome and search for 'gemini ai'"
    print(f"Task: {task}\n")
    
    # Get initial screenshot
    initial_screenshot = get_screenshot_png()
    
    # Create initial request
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=task),
                types.Part.from_bytes(
                    data=initial_screenshot,
                    mime_type='image/png'
                )
            ]
        )
    ]
    
    # Agent loop
    for iteration in range(20):
        print(f"\n--- Turn {iteration + 1} ---")
        
        # Get response from Gemini
        response = client.models.generate_content(
            model='gemini-2.5-computer-use-preview-10-2025',
            contents=contents,
            config=config
        )
        
        candidate = response.candidates[0]
        contents.append(candidate.content)
        
        # Display progress
        for part in candidate.content.parts:
            if part.text:
                print(f"💬 {part.text}")
        
        # Check for function calls
        has_function_calls = any(
            part.function_call 
            for part in candidate.content.parts
        )
        
        if not has_function_calls:
            print("\n✓ Task completed")
            break
        
        # Execute actions
        print("→ Executing actions...")
        results = execute_function_calls(candidate)
        
        # Get responses with screenshot and URL
        function_responses = get_function_responses(results)
        
        # Continue conversation
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(function_response=fr) 
                    for fr in function_responses
                ]
            )
        )

except Exception as e:
    print(f"\n❌ Error: {e}")

finally:
    print("\nDone!")
    # Note: computer.destroy() not called to keep computer running
    # Call computer.destroy() if you want to clean up
```

See all 244 lines

## [​](#usage-examples) Usage Examples

### [​](#basic-tasks) Basic Tasks

```
# Change the task variable to control what Gemini does
task = "Open Chrome and search for 'gemini ai'"

# Navigate to a website
task = "Go to github.com and search for 'orgo'"

# Fill a form
task = "Fill out the contact form with test data"
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
```

## [​](#key-concepts) Key Concepts

### [​](#system-prompt) System Prompt

The system prompt provides crucial context to Gemini about the Ubuntu environment:

```
SYSTEM_PROMPT = f"""You are controlling an Ubuntu Linux virtual machine...

<UBUNTU_DESKTOP_GUIDELINES>
* CRITICAL: When opening applications or files on the Ubuntu desktop, 
  you MUST USE DOUBLE-CLICK, not single-click
* Single-click only selects desktop icons but DOES NOT open them
* Desktop icons (apps/folders): DOUBLE-CLICK to open
* Menu items: SINGLE-CLICK to select
</UBUNTU_DESKTOP_GUIDELINES>
"""
```

This ensures Gemini knows to:

* Double-click desktop icons to open applications
* Single-click menu items and buttons
* Use appropriate keyboard shortcuts

### [​](#getting-your-computer-id) Getting Your Computer ID

Get your `computer_id` from the [Orgo dashboard](https://orgo.ai/workspaces):

1. Go to <https://orgo.ai/workspaces>
2. Click on your project
3. Find your computer ID in the computer list
4. Use it in: `Computer(computer_id="your-computer-id")`

### [​](#the-agent-loop) The Agent Loop

Gemini Computer Use works in a continuous loop:

1. **Request** → Send task with screenshot to the model
2. **Action** → Model suggests actions (click, type, etc.)
3. **Execute** → Your code executes the actions
4. **Screenshot** → Capture the result
5. **Repeat** → Continue until task is complete

### [​](#image-format-conversion) Image Format Conversion

**Important:** Orgo returns screenshots in JPEG format, but Gemini requires PNG format:

```
def get_screenshot_png() -> bytes:
    """Get screenshot as PNG bytes (Gemini requires PNG format)."""
    jpeg_data = base64.b64decode(computer.screenshot_base64())
    image = Image.open(io.BytesIO(jpeg_data))
    png_buffer = io.BytesIO()
    image.save(png_buffer, format='PNG')
    return png_buffer.getvalue()
```

### [​](#url-tracking) URL Tracking

**Important:** Gemini Computer Use requires the current URL in every function response:

```
response_data = {
    "status": "completed",
    "url": result.get("url", current_url)  # Always include URL
}
```

### [​](#coordinate-system) Coordinate System

Gemini uses **normalized coordinates (0-999)** that must be converted to actual pixels:

```
def denormalize_x(x: int) -> int:
    return int(x / 1000 * SCREEN_WIDTH)

def denormalize_y(y: int) -> int:
    return int(y / 1000 * SCREEN_HEIGHT)
```

Orgo’s default screen resolution is **1024x768**.

### [​](#action-types) Action Types

| Action | Description | Example |
| --- | --- | --- |
| `open_web_browser` | Opens the browser | Start Firefox |
| `click_at` | Click at coordinates | Click button at (500, 300) |
| `type_text_at` | Type text at location | Enter “hello” in search box |
| `scroll_document` | Scroll page | Scroll down |
| `key_combination` | Press key combos | Press ctrl+c |
| `navigate` | Go to URL | Load <https://example.com> |
| `go_back` | Browser back | Previous page |
| `wait_5_seconds` | Pause execution | Wait for page load |

## [​](#tool-compatibility) Tool Compatibility

Orgo provides methods corresponding to Gemini’s computer use tools:

| Gemini Tool Action | Orgo Method | Description |
| --- | --- | --- |
| `click_at` | `computer.left_click(x, y)` | Click at coordinates |
| `type_text_at` | `computer.type(text)` | Type text |
| `key_combination` | `computer.key(keys)` | Press keys (e.g., “ctrl+c”) |
| `scroll_document` | `computer.scroll(direction, amount)` | Scroll page |
| `navigate` | `computer.bash('firefox "url" &')` | Open URL |
| Screenshot | `computer.screenshot_base64()` | Capture screen (JPEG) |
| `wait_5_seconds` | `computer.wait(5)` | Wait 5 seconds |

## [​](#best-practices) Best Practices

### [​](#1-clear-instructions) 1. Clear Instructions

```
# ✅ Good - Specific and clear
task = "Go to amazon.com and find the top 3 rated laptops under $1000"

# ❌ Avoid - Too vague
task = "Find some laptops"
```

### [​](#2-use-system-prompts) 2. Use System Prompts

Always include a system prompt with Ubuntu-specific instructions:

```
config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,  # Include OS-specific guidance
    tools=[...]
)
```

### [​](#3-convert-coordinates) 3. Convert Coordinates

Always denormalize Gemini’s normalized coordinates (0-999):

```
actual_x = denormalize_x(args["x"])
actual_y = denormalize_y(args["y"])
```

### [​](#4-handle-image-format) 4. Handle Image Format

Always convert JPEG screenshots to PNG:

```
screenshot_png = get_screenshot_png()
```

### [​](#5-include-url-in-responses) 5. Include URL in Responses

Always include the current URL:

```
response_data = {
    "status": "completed",
    "url": current_url
}
```

### [​](#6-add-delays) 6. Add Delays

```
time.sleep(1)  # Wait for UI to update after actions
```

## [​](#comparison-with-claude-and-openai) Comparison with Claude and OpenAI

| Feature | Gemini Computer Use | Claude Computer Use | OpenAI Computer Use |
| --- | --- | --- | --- |
| API | Generate Content API | Messages API | Responses API |
| Model | `gemini-2.5-computer-use-preview` | `claude-sonnet-4-6` | `computer-use-preview` |
| System Prompt | Supported | Supported | Supported |
| Coordinates | Normalized (0-999) | Actual pixels | Actual pixels |
| Image Format | PNG required | JPEG/PNG | PNG |
| URL Requirement | Required in response | Optional | Optional |
| Parallel Actions | Yes | No | No |

## [​](#limitations) Limitations

* **Preview Status**: Computer Use is in preview and may have unexpected behaviors
* **Browser Focus**: Optimized for browser-based tasks
* **Coordinate System**: Requires conversion from normalized to actual pixels
* **Image Format**: Requires PNG format (Orgo returns JPEG, must convert)
* **URL Requirement**: Must include URL in every function response
* **Rate Limits**: Subject to Gemini API rate limits

## [​](#troubleshooting) Troubleshooting

### [​](#model-doesn’t-double-click-desktop-icons) Model doesn’t double-click desktop icons

Make sure you’re including the system prompt with Ubuntu-specific instructions:

```
config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,  # This is critical!
    tools=[...]
)
```

### [​](#invalid_argument-unable-to-process-input-image) INVALID\_ARGUMENT: Unable to process input image

This error occurs when Gemini receives a JPEG image instead of PNG. Make sure you’re using the `get_screenshot_png()` function.

### [​](#invalid_argument-requires-url-in-function-response) INVALID\_ARGUMENT: Requires URL in function response

Always include the `url` field in your response data:

```
response_data = {
    "status": "completed",
    "url": result.get("url", current_url)
}
```

### [​](#missing-api-key) Missing API Key

Ensure both environment variables are set in your `.env` file:

```
ORGO_API_KEY=your_orgo_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## [​](#next-steps) Next Steps

## Gemini Docs

Official Gemini API documentation

## Orgo Quickstart

Learn more about Orgo’s virtual desktops

## API Reference

Complete Orgo API documentation

[Previous](/guides/openai-computer-use)[Agent S2Let Agent S2 control a virtual desktop

Next](/guides/agent-s2)

⌘I