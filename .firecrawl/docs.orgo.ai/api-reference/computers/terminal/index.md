---
url: https://docs.orgo.ai/api-reference/computers/terminal
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Connect to an interactive terminal session on a computer via WebSocket. This provides a full PTY (pseudo-terminal) interface, enabling real-time bidirectional communication with the computer’s shell.

## [​](#connection-url) Connection URL

```
wss://www.orgo.ai/desktops/{computer_id}/ws/terminal?token={password}
```

### [​](#authentication) Authentication

The terminal WebSocket requires the computer’s password as the `token` query parameter. This is the same password used for VNC connections. Retrieve it from the [Get VNC Password](/api-reference/computers/vnc-password) endpoint before connecting.
Connections without a valid token are rejected with close code `4401`.

### [​](#query-parameters) Query Parameters

[​](#param-token)

token

string

required

Computer password. Retrieve via the [Get VNC Password](/api-reference/computers/vnc-password) endpoint.

[​](#param-cols)

cols

number

default:"80"

Number of columns for the terminal.

[​](#param-rows)

rows

number

default:"24"

Number of rows for the terminal.

## [​](#message-protocol) Message Protocol

All messages are JSON-encoded. The WebSocket uses a simple request/response protocol with the following message types.

### [​](#client-→-server-messages) Client → Server Messages

input

Send keyboard input to the terminal.

```
{
  "type": "input",
  "data": "ls -la\r"
}
```

[​](#param-type)

type

string

required

Must be `"input"`.

[​](#param-data)

data

string

required

The input string to send. Use `\r` for Enter key.

resize

Resize the terminal dimensions.

```
{
  "type": "resize",
  "cols": 120,
  "rows": 40
}
```

[​](#param-type-1)

type

string

required

Must be `"resize"`.

[​](#param-cols-1)

cols

number

required

New number of columns.

[​](#param-rows-1)

rows

number

required

New number of rows.

ping

Send a heartbeat ping to keep the connection alive.

```
{
  "type": "ping"
}
```

### [​](#server-→-client-messages) Server → Client Messages

output

Terminal output data.

```
{
  "type": "output",
  "data": "user@computer:~$ "
}
```

[​](#param-type-2)

type

string

Always `"output"`.

[​](#param-data-1)

data

string

The terminal output. May contain ANSI escape codes for colors and formatting.

error

Error message from the server.

```
{
  "type": "error",
  "message": "Connection failed"
}
```

[​](#param-type-3)

type

string

Always `"error"`.

[​](#param-message)

message

string

Human-readable error description.

exit

The shell process has exited.

```
{
  "type": "exit",
  "code": 0
}
```

[​](#param-type-4)

type

string

Always `"exit"`.

[​](#param-code)

code

number

Exit code of the shell process.

pong

Response to a ping message.

```
{
  "type": "pong"
}
```

## [​](#examples) Examples

JavaScript

Python

TypeScript

```
const computerId = 'orgo-a3bb189e-8bf9-3888-9912-ace4e6543002';
const apiKey = process.env.ORGO_API_KEY;

// Step 1: Get the computer password
const res = await fetch(
  `https://www.orgo.ai/api/computers/${computerId}/vnc-password`,
  { headers: { 'Authorization': `Bearer ${apiKey}` } }
);
const { password } = await res.json();

// Step 2: Connect with password as token
const ws = new WebSocket(
  `wss://www.orgo.ai/desktops/${computerId}/ws/terminal?token=${password}&cols=80&rows=24`
);

ws.onopen = () => {
  console.log('Connected to terminal');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  switch (message.type) {
    case 'output':
      // Append to your terminal display
      terminal.write(message.data);
      break;
    case 'error':
      console.error('Terminal error:', message.message);
      break;
    case 'exit':
      console.log('Shell exited with code:', message.code);
      break;
  }
};

// Send a command
function sendCommand(command) {
  ws.send(JSON.stringify({
    type: 'input',
    data: command + '\r'  // \r for Enter key
  }));
}

// Resize terminal
function resizeTerminal(cols, rows) {
  ws.send(JSON.stringify({
    type: 'resize',
    cols,
    rows
  }));
}

// Example: Run a command
sendCommand('echo "Hello, World!"');
```

## [​](#integration-with-xterm-js) Integration with xterm.js

For browser-based terminal UIs, we recommend using [xterm.js](https://xtermjs.org/):

```
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import '@xterm/xterm/css/xterm.css';

// Initialize xterm.js
const terminal = new Terminal({
  cursorBlink: true,
  fontFamily: 'monospace',
  fontSize: 14,
});

const fitAddon = new FitAddon();
terminal.loadAddon(fitAddon);
terminal.open(document.getElementById('terminal'));
fitAddon.fit();

// Step 1: Get the computer password
const computerId = 'orgo-a3bb189e-8bf9-3888-9912-ace4e6543002';
const res = await fetch(
  `https://www.orgo.ai/api/computers/${computerId}/vnc-password`,
  { headers: { 'Authorization': `Bearer ${apiKey}` } }
);
const { password } = await res.json();

// Step 2: Connect with password as token
const ws = new WebSocket(
  `wss://www.orgo.ai/desktops/${computerId}/ws/terminal?token=${password}&cols=${terminal.cols}&rows=${terminal.rows}`
);

// Handle output from server
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'output') {
    terminal.write(message.data);
  }
};

// Send user input to server
terminal.onData((data) => {
  ws.send(JSON.stringify({ type: 'input', data }));
});

// Handle terminal resize
window.addEventListener('resize', () => {
  fitAddon.fit();
  ws.send(JSON.stringify({
    type: 'resize',
    cols: terminal.cols,
    rows: terminal.rows
  }));
});
```

## [​](#best-practices) Best Practices

## Heartbeat

Send periodic `ping` messages (every 30 seconds) to keep the connection alive and detect disconnections early.

## Reconnection

Implement automatic reconnection with exponential backoff. Start with 2 seconds and increase up to 30 seconds.

## Resize Events

Send `resize` messages whenever the terminal container size changes to ensure proper text wrapping.

## ANSI Support

The terminal output may contain ANSI escape codes. Use a library like xterm.js that handles these automatically.

The terminal WebSocket provides direct shell access. For running individual commands programmatically, consider using the [Execute Bash](/api-reference/computers/bash) endpoint instead.

## [​](#close-codes) Close codes

| Code | Meaning |
| --- | --- |
| `1000` | Normal closure. |
| `1001` | Server shutting down or computer stopping. |
| `4401` | Missing or invalid `token`. |
| `4404` | Computer not found or not running. |
| `4500` | Failed to spawn the shell process. |

[Previous](/api-reference/computers/exec)[Audio WebSocketStream the desktop speaker over WebSocket as low-latency PCM frames.

Next](/api-reference/computers/audio)

⌘I