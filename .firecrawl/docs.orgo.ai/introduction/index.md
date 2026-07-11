---
url: https://docs.orgo.ai/introduction
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

![Orgo Hero Light](https://mintcdn.com/orgo/i0HN53mFBmljZF6E/images/hero-light.png?fit=max&auto=format&n=i0HN53mFBmljZF6E&q=85&s=c8d82827a56685ac057bd417c9a21e7a)
![Orgo Hero Dark](https://mintcdn.com/orgo/i0HN53mFBmljZF6E/images/hero-dark.png?fit=max&auto=format&n=i0HN53mFBmljZF6E&q=85&s=490aa7548c38aaa5fdc137fdf07ec0c6)

## [​](#what-orgo-is) What Orgo is

Launch cloud computers that AI agents can control and interact with. Every Orgo computer is a full Linux desktop with a browser and the standard userland, reachable over HTTP and VNC. Computers boot in under 500 ms and run continuously until you stop them.
People use Orgo computers in three common ways:

* **Drive a computer with a model provider.** Wire an Anthropic, OpenAI, Google, or any OpenAI-compatible model to an Orgo computer and let it screenshot, click, type, and run commands. Useful for automating data entry, combining several tools into one interface, or driving software that doesn’t expose an API.
* **Install an agent inside the computer.** Run [OpenClaw](/guides/openclaw), [Hermes Agent](/guides/hermes), or any other CLI agent inside the desktop so it has a persistent 24/7 home instead of a laptop.
* **Run developer CLIs continuously.** Run Claude Code, Codex, or similar agentic CLIs on an Orgo computer so they stay online across sessions and can be reached from any device.

[![](/images/hero-dark.png)](https://mintcdn.com/orgo/hFlf7o0qXph7_UgY/images/orgo-short-video.mp4?fit=max&auto=format&n=hFlf7o0qXph7_UgY&q=85&s=42c757fbfaa7d5358d03651283d61551)
A new computer in about fifteen seconds. The clip shows the dashboard flow; the same thing happens when an agent calls `POST /computers` from your code.

## Quickstart

Launch a computer and control it in under five minutes.

## Get an API key

Create an account and grab a key.

## [​](#what-orgo-is-not) What Orgo is not

**Not a browser.** Tools like Browserbase give an agent a browser tab. Orgo gives it a full computer, so a single machine can browse the web, save files, run code, and install desktop applications. Use a browser tool if you only need the browser. Use Orgo if you need a computer.
**Not an AI agent.** Orgo provides the computer; it does not provide the agent. Bring Claude Computer Use, OpenAI’s CUA, Hermes Agent, OpenClaw, or your own loop — Orgo is what they run on.
**Not a general cloud platform.** Orgo runs one thing: persistent desktops for AI agents. That focus shapes the rest — sub-second boots, defaults tuned for computer use, and an API designed around what agents actually do.

## [​](#how-it-works) How it works

Orgo is a plain HTTP API. Any language with an HTTP client works. The example below creates a computer, then hands it to a Claude agent through the OpenAI-compatible endpoint.

cURL

Python

TypeScript

```
# 1. Create a computer (one HTTP call, boots in under 500 ms)
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id": "$WORKSPACE_ID", "name": "agent-1"}'

# 2. Let Claude drive it (OpenAI-compatible, any SDK works)
curl https://www.orgo.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "computer_id": "$COMPUTER_ID",
    "messages": [
      {"role": "user", "content": "Find a funny cat image and save it to the desktop"}
    ]
  }'
```

The agent takes screenshots, clicks, types, and runs commands until the task is done. You can also call individual actions directly. See the [API Reference](/api-reference/introduction) for every endpoint. The Python and TypeScript SDKs wrap this same surface.

## [​](#agent-loop) Agent loop

Computer use agents typically operate in a loop:


1. **See.** Capture a screenshot.
2. **Decide.** The model analyzes the screen and chooses an action.
3. **Act.** Perform a mouse, keyboard, or shell action.
4. **Repeat.** Continue until the task is complete.

## [​](#key-capabilities) Key capabilities

## Fast boot

Computers boot in under 500 ms.

## Full control

Mouse, keyboard, shell, and code execution.

## Persistent state

Disk and desktop session survive stops and restarts.

## Bring any model

Claude, GPT, Gemini, Hermes, or any OpenAI-compatible model.

## [​](#get-started) Get started

## Quickstart

Launch your first computer.

## Use any model

Claude, GPT, Gemini, Hermes, and more.

## Templates

Reproducible computers, defined once and launched in seconds.

## Embed VMs

Drop a live computer into your own app.

## API Reference

Every endpoint, every field.

[QuickstartLaunch a computer and control it over HTTP in under 5 minutes

Next](/quickstart)

⌘I