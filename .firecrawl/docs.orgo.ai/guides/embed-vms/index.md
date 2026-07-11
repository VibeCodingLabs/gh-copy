---
url: https://docs.orgo.ai/guides/embed-vms
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

## [​](#overview) Overview

Embed Orgo virtual computers directly into your web apps. Build AI agent interfaces, automation dashboards, or any product with live VM displays.

You can use any VNC client to connect to Orgo computers. The `orgo-vnc` package is a React component for convenience.

## [​](#connection-details) Connection details

Every computer is reachable same-origin under `www.orgo.ai`. The connection base is shown as **Connection URL** in Computer Settings.

|  |  |
| --- | --- |
| **Connection base** | `https://www.orgo.ai/desktops/{instance_id}` (read `instance_id` from `GET /computers/{id}`) |
| **WebSocket VNC** | `wss://www.orgo.ai/desktops/{instance_id}/ws/websockify?token={password}` |
| **Password** | `GET /computers/{id}/vnc-password` - **rotates on restart**, fetch fresh, do not hardcode |

The WebSocket form is what the `orgo-vnc` component, noVNC, and any websockify-compatible client use.

### [​](#connect-with-raw-novnc-no-react) Connect with raw noVNC (no React)

```
import RFB from '@novnc/novnc';

const computer = await fetch(`https://www.orgo.ai/api/computers/${id}`, {
  headers: { Authorization: `Bearer ${apiKey}` }
}).then(r => r.json());

const { password } = await fetch(
  `https://www.orgo.ai/api/computers/${id}/vnc-password`,
  { headers: { Authorization: `Bearer ${apiKey}` } }
).then(r => r.json());

const rfb = new RFB(
  document.getElementById('screen'),
  `wss://www.orgo.ai/desktops/${computer.instance_id}/ws/websockify?token=${encodeURIComponent(password)}`,
  { credentials: { password } }
);

// Adjust after construction
rfb.viewOnly = true;       // read-only mode (no input)
rfb.scaleViewport = true;  // fit display to container
rfb.qualityLevel = 6;      // 0–9 (default 6)
rfb.compressLevel = 2;     // 0–9 (default 2)
```

## [​](#setup) Setup

1

Install

```
    npm install orgo-vnc
```

2

Get credentials

1. Go to [orgo.ai/start](https://www.orgo.ai/start)
2. Open a workspace and select a computer
3. Click the **⋮** menu → **Computer Settings**
4. Copy the **Hostname** and **Password**

3

Configure environment

Create `.env.local` in your project root:

```
    NEXT_PUBLIC_ORGO_COMPUTER_HOST=your-hostname
    NEXT_PUBLIC_ORGO_COMPUTER_PASSWORD=your-password
```

4

Use the ComputerDisplay component

app/page.tsx

```
    'use client';
    import { useState } from 'react';
    import { ComputerDisplay } from 'orgo-vnc';

    const HOST = process.env.NEXT_PUBLIC_ORGO_COMPUTER_HOST!;
    const PASSWORD = process.env.NEXT_PUBLIC_ORGO_COMPUTER_PASSWORD!;

    export default function Home() {
      const [connected, setConnected] = useState(false);
      
      return (
        <div className="grid place-items-center min-h-screen p-8">
          <div className="w-full max-w-4xl flex flex-col gap-3">
            <p className="text-sm text-foreground/60 flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${connected ? 'bg-emerald-500' : 'bg-foreground/30 animate-pulse'}`} />
              {connected ? `Connected to ${HOST}` : 'Connecting...'}
            </p>
            <div className="aspect-[4/3] rounded-lg overflow-hidden bg-foreground/5">
              <ComputerDisplay
                hostname={HOST}
                password={PASSWORD}
                background="transparent"
                readOnly={false}
                onConnect={() => setConnected(true)}
                onDisconnect={() => setConnected(false)}
              />
            </div>
          </div>
        </div>
      );
    }
```

See all 31 lines

## [​](#props) Props

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `hostname` | `string` | required | Computer hostname |
| `password` | `string` | required | Computer password |
| `readOnly` | `boolean` | `false` | Disable user interaction |
| `background` | `string` | `undefined` | Background color |
| `scaleViewport` | `boolean` | `true` | Scale display to fit container |
| `clipViewport` | `boolean` | `false` | Clip display to container bounds |
| `resizeSession` | `boolean` | `false` | Resize remote session to match |
| `showDotCursor` | `boolean` | `false` | Show dot cursor when remote cursor hidden |
| `compressionLevel` | `number` | `2` | Compression level (0-9) |
| `qualityLevel` | `number` | `6` | Image quality (0-9) |
| `onConnect` | `function` | `undefined` | Called when connected |
| `onDisconnect` | `function` | `undefined` | Called when disconnected |
| `onError` | `function` | `undefined` | Called on error |
| `onClipboard` | `function` | `undefined` | Called when clipboard data received |
| `onReady` | `function` | `undefined` | Called with handle for programmatic control |

## [​](#programmatic-control) Programmatic Control

Use the `onReady` callback to get a handle for programmatic control:

```
const [handle, setHandle] = useState<ComputerDisplayHandle | null>(null);

<ComputerDisplay
  hostname={HOST}
  password={PASSWORD}
  onReady={setHandle}
/>

// Later...
handle?.reconnect();
handle?.disconnect();
handle?.sendClipboard('text to send');
await handle?.pasteFromClipboard();
```

## [​](#next-steps) Next Steps

## Quick Start

Full SDK setup

## API Reference

Control computers programmatically

[Previous](/guides/memory)[TroubleshootingMap common API errors to the action that fixes them.

Next](/guides/troubleshooting)

⌘I