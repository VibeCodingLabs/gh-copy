---
url: https://docs.orgo.ai/guides/agent-s2
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

## [​](#overview) Overview

This guide walks through setting up Agent S2, the open-source SOTA computer use agent by Simular AI. These steps include trying it locally on your own computer or on a virtual desktop through Orgo.

## [​](#setup) Setup

Install the required packages:

pip

requirements.txt

```
pip install gui-agents pyautogui python-dotenv orgo
```

Set up your API keys:

terminal

setup.py

.env

```
# Export as environment variables
export OPENAI_API_KEY=your_openai_api_key
export ANTHROPIC_API_KEY=your_anthropic_api_key
export ORGO_API_KEY=your_orgo_api_key  # Optional for remote
```

## [​](#simple-usage) Simple Usage

Run Agent S2 with natural language commands:

local

remote

interactive

```
# Local mode - controls your computer
python agent_s2.py "Open Chrome and search for weather"
```

This approach uses Agent S2’s compositional framework to execute complex computer use tasks.

## [​](#complete-example) Complete Example

agent\_s2.py

```
#!/usr/bin/env python3

import os
import io
import sys
import time
from dotenv import load_dotenv
from gui_agents.s2.agents.agent_s import AgentS2
from gui_agents.s2.agents.grounding import OSWorldACI
from orgo import Computer
import pyautogui

load_dotenv()

CONFIG = {
    "model": os.getenv("AGENT_MODEL", "gpt-4o"),
    "model_type": os.getenv("AGENT_MODEL_TYPE", "openai"),
    "grounding_model": os.getenv("GROUNDING_MODEL", "claude-sonnet-4-6"),
    "grounding_type": os.getenv("GROUNDING_MODEL_TYPE", "anthropic"),
    "max_steps": int(os.getenv("MAX_STEPS", "10")),
    "step_delay": float(os.getenv("STEP_DELAY", "0.5")),
    "remote": os.getenv("USE_CLOUD_ENVIRONMENT", "false").lower() == "true"
}


class LocalExecutor:
    def __init__(self):
        self.pyautogui = pyautogui
        if sys.platform == "win32":
            self.platform = "windows"
        elif sys.platform == "darwin":
            self.platform = "darwin"
        else:
            self.platform = "linux"
    
    def screenshot(self):
        img = self.pyautogui.screenshot()
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()
    
    def exec(self, code):
        exec(code, {"pyautogui": self.pyautogui, "time": time})
    
    def destroy(self):
        # No cleanup needed for local executor
        pass


class RemoteExecutor:
    def __init__(self):
        self.computer = Computer()
        self.platform = "linux"
    
    def screenshot(self):
        return self.computer.screenshot_base64()
    
    def exec(self, code):
        result = self.computer.exec(code)
        if not result['success']:
            raise Exception(result.get('error', 'Execution failed'))
        if result['output']:
            print(f"Output: {result['output']}")
    
    def destroy(self):
        self.computer.destroy()


def create_agent(executor):
    engine_params = {"engine_type": CONFIG["model_type"], "model": CONFIG["model"]}
    grounding_params = {"engine_type": CONFIG["grounding_type"], "model": CONFIG["grounding_model"]}
    
    grounding_agent = OSWorldACI(
        platform=executor.platform,
        engine_params_for_generation=engine_params,
        engine_params_for_grounding=grounding_params
    )
    
    return AgentS2(
        engine_params=engine_params,
        grounding_agent=grounding_agent,
        platform=executor.platform,
        action_space="pyautogui",
        observation_type="screenshot"
    )


def run_task(agent, executor, instruction):
    print(f"\n🤖 Task: {instruction}")
    print(f"📍 Mode: {'Remote' if CONFIG['remote'] else 'Local'}\n")
    
    for step in range(CONFIG["max_steps"]):
        print(f"Step {step + 1}/{CONFIG['max_steps']}")
        
        obs = {"screenshot": executor.screenshot()}
        info, action = agent.predict(instruction=instruction, observation=obs)
        
        if info:
            print(f"💭 {info}")
        
        if not action or not action[0]:
            print("✅ Complete")
            return True
        
        try:
            print(f"🔧 {action[0]}")
            executor.exec(action[0])
        except Exception as e:
            print(f"❌ Error: {e}")
            instruction = "The previous action failed. Try a different approach."
        
        time.sleep(CONFIG["step_delay"])
    
    print("⏱️ Max steps reached")
    return False


def main():
    executor = RemoteExecutor() if CONFIG["remote"] else LocalExecutor()
    try:
        agent = create_agent(executor)
        
        if len(sys.argv) > 1:
            run_task(agent, executor, " ".join(sys.argv[1:]))
        else:
            print("🎮 Interactive Mode (type 'exit' to quit)\n")
            while True:
                task = input("Task: ").strip()
                if task == "exit":
                    break
                elif task:
                    run_task(agent, executor, task)
    finally:
        # Clean up
        executor.destroy()


if __name__ == "__main__":
    main()
```

See all 140 lines

## [​](#platform-requirements) Platform Requirements

### [​](#macos) macOS

Grant Terminal access: System Settings → Privacy & Security → Accessibility

### [​](#windows) Windows

May require running Terminal as Administrator

### [​](#linux) Linux

Install dependencies:

```
sudo apt-get install python3-tk python3-dev
```

## [​](#environment-variables) Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | - | Anthropic API key |
| `ORGO_API_KEY` | - | Orgo API key (remote mode) |
| `USE_CLOUD_ENVIRONMENT` | `false` | Set to `true` for remote execution |
| `AGENT_MODEL` | `gpt-4o` | Main reasoning model |
| `GROUNDING_MODEL` | `claude-sonnet-4-6` | Visual grounding model |
| `MAX_STEPS` | `10` | Maximum steps per task |
| `STEP_DELAY` | `0.5` | Seconds between actions |

## [​](#architecture) Architecture

Agent S2 uses a compositional framework with specialized modules:
**Mixture of Grounding** - Routes actions to specialized visual grounding models for precise UI localization
**Proactive Hierarchical Planning** - Dynamically refines plans based on evolving observations
**Cross-platform Support** - Works on macOS, Windows, and Linux

## [​](#performance) Performance

Agent S2 achieves state-of-the-art results on computer use benchmarks:

| Benchmark | Success Rate | Rank |
| --- | --- | --- |
| OSWorld | 27.0% | #3 |
| WindowsAgentArena | 29.8% | #1 |
| AndroidWorld | 54.3% | #1 |

## [​](#resources) Resources

* [GitHub Repository](https://github.com/simular-ai/Agent-S)
* [Agent S2 Whitepaper](https://arxiv.org/abs/2504.00906)
* [OSWorld Benchmark](https://os-world.github.io/)

Agent S2 is currently ranked #3 on the OSWorld benchmark, demonstrating leading performance on complex computer use tasks.

## [​](#video-tutorial) Video Tutorial

Here is a video version of this guide:You can follow the video tutorial above or use this written guide.

[Previous

Gemini Computer UseControl virtual desktops with Gemini 2.5](/guides/gemini-computer-use)

⌘I