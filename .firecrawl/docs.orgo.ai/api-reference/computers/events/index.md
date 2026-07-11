---
url: https://docs.orgo.ai/api-reference/computers/events
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Subscribe to real-time desktop events over WebSocket. Monitor window focus changes, clipboard updates, file modifications, process lifecycle, screen resolution changes, and idle/active state - all pushed to your client as they happen.

## [​](#connection-url) Connection URL

```
wss://www.orgo.ai/desktops/{computer_id}/ws/events?token={password}
```

### [​](#authentication) Authentication

The events WebSocket requires the computer’s password as the `token` query parameter. Retrieve it from the [Get VNC Password](/api-reference/computers/vnc-password) endpoint before connecting.
Connections without a valid token are rejected with close code `4401`.

### [​](#query-parameters) Query Parameters

[​](#param-token)

token

string

required

Computer password. Retrieve via the [Get VNC Password](/api-reference/computers/vnc-password) endpoint.

## [​](#event-catalog) Event Catalog

You can also fetch the event catalog as JSON without a WebSocket connection:

```
curl https://www.orgo.ai/api/computers/{id}/events
```

### [​](#available-event-types) Available Event Types

| Type | Description | Detection |
| --- | --- | --- |
| `window_focus` | Active window changed | Polled every 100 ms |
| `window_open` | New window opened | Polled every 100 ms |
| `window_close` | Window closed | Polled every 100 ms |
| `clipboard` | Clipboard content changed | Polled every 250 ms |
| `file_change` | File created, modified, or deleted on Desktop or Downloads | inotify (instant) |
| `screen_change` | Display resolution changed | Polled every 1 s |
| `audio_stream_start` | Audio playback started | Polled every 500 ms |
| `audio_stream_stop` | Audio playback stopped | Polled every 500 ms |
| `process_start` | New process started | Polled every 2 s |
| `process_stop` | Process exited | Polled every 2 s |
| `idle` | No user input for 30 seconds | Polled every 1 s |
| `active` | User input resumed after idle | Polled every 1 s |

## [​](#subscription-model) Subscription Model

New connections receive **no events** until they send a `subscribe` message. This lets you opt in to only the event types you care about, reducing noise and bandwidth.
Subscriptions are:

* **Per-connection** - each WebSocket connection has its own subscription set
* **Additive** - subscribe to more types at any time
* **Selective** - unsubscribe from specific types without disconnecting

## [​](#message-protocol) Message Protocol

### [​](#client-→-server-messages) Client → Server Messages

subscribe

Start receiving specific event types. You can call this multiple times to add more types.

```
{
  "type": "subscribe",
  "event_types": ["window_focus", "clipboard", "file_change"]
}
```

[​](#param-type)

type

string

required

Must be `"subscribe"`.

[​](#param-event-types)

event\_types

string[]

required

Array of event type names to subscribe to. See the [event catalog](#available-event-types) for valid types.

unsubscribe

Stop receiving specific event types.

```
{
  "type": "unsubscribe",
  "event_types": ["clipboard"]
}
```

[​](#param-type-1)

type

string

required

Must be `"unsubscribe"`.

[​](#param-event-types-1)

event\_types

string[]

required

Array of event type names to unsubscribe from.

ping

Send a heartbeat ping to keep the connection alive.

```
{
  "type": "ping"
}
```

### [​](#server-→-client-messages) Server → Client Messages

event

A desktop event matching one of your subscribed types.

```
{
  "type": "event",
  "event": {
    "type": "window_focus",
    "timestamp": "2026-03-03T12:00:00.123Z",
    "data": {
      "window_id": "0x3200004",
      "title": "Google Chrome"
    }
  }
}
```

[​](#param-type-2)

type

string

Always `"event"`.

[​](#param-event)

event

object

The event payload.

[​](#param-event-type)

event.type

string

Event type name (e.g., `"window_focus"`, `"clipboard"`).

[​](#param-event-timestamp)

event.timestamp

string

ISO 8601 timestamp of when the event occurred.

[​](#param-event-data)

event.data

object

Event-specific data. See [Event Data Schemas](#event-data-schemas) below.

subscribed

Confirmation that your subscription was updated.

```
{
  "type": "subscribed",
  "message": "ok"
}
```

unsubscribed

Confirmation that event types were removed from your subscription.

```
{
  "type": "unsubscribed",
  "message": "ok"
}
```

pong

Response to a ping message.

```
{
  "type": "pong"
}
```

error

Error message from the server.

```
{
  "type": "error",
  "message": "Unknown event type: invalid_type"
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

## [​](#event-data-schemas) Event Data Schemas

Each event type includes a `data` object with type-specific fields:

### [​](#window-events) Window events

```
// window_focus
{ "window_id": "0x3200004", "title": "Google Chrome" }

// window_open
{ "window_id": "0x3200008", "title": "Terminal" }

// window_close
{ "window_id": "0x3200008" }
```

### [​](#clipboard) Clipboard

```
// clipboard
{ "content": "copied text from the clipboard" }
```

### [​](#file-changes) File changes

```
// file_change
{ "path": "/home/user/Desktop/report.pdf", "action": "created" }
{ "path": "/home/user/Downloads/data.csv", "action": "modified" }
{ "path": "/home/user/Desktop/old.txt", "action": "deleted" }
```

Monitored directories: `/home/user/Desktop` and `/home/user/Downloads`. Detection is via Linux inotify - file events are delivered instantly.

### [​](#screen) Screen

```
// screen_change
{ "width": 1920, "height": 1080 }
```

### [​](#audio) Audio

```
// audio_stream_start
{}

// audio_stream_stop
{}
```

### [​](#process-lifecycle) Process lifecycle

```
// process_start
{ "pid": 1234, "name": "chrome" }

// process_stop
{ "pid": 1234, "name": "chrome" }
```

### [​](#idle-/-active) Idle / Active

```
// idle
{ "idle_seconds": 30 }

// active
{}
```

## [​](#examples) Examples

JavaScript

Python

TypeScript

```
const computerId = 'a3bb189e-8bf9-3888-9912-ace4e6543002';
const apiKey = process.env.ORGO_API_KEY;

// Step 1: Get the computer password
const res = await fetch(
  `https://www.orgo.ai/api/computers/${computerId}/vnc-password`,
  { headers: { 'Authorization': `Bearer ${apiKey}` } }
);
const { password } = await res.json();

// Step 2: Connect to events stream
const ws = new WebSocket(
  `wss://www.orgo.ai/desktops/${computerId}/ws/events?token=${password}`
);

ws.onopen = () => {
  // Subscribe to the events you care about
  ws.send(JSON.stringify({
    type: 'subscribe',
    event_types: ['window_focus', 'clipboard', 'file_change', 'idle', 'active']
  }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  switch (msg.type) {
    case 'event':
      const { type, timestamp, data } = msg.event;
      console.log(`[${timestamp}] ${type}:`, data);

      // React to specific events
      if (type === 'window_focus') {
        console.log(`User switched to: ${data.title}`);
      }
      if (type === 'clipboard') {
        console.log(`Clipboard: ${data.content}`);
      }
      if (type === 'idle') {
        console.log(`Desktop idle for ${data.idle_seconds}s`);
      }
      break;

    case 'subscribed':
      console.log('Subscription confirmed');
      break;

    case 'error':
      console.error('Event error:', msg.message);
      break;
  }
};

// Later: add more subscriptions
ws.send(JSON.stringify({
  type: 'subscribe',
  event_types: ['process_start', 'process_stop']
}));

// Or unsubscribe from some
ws.send(JSON.stringify({
  type: 'unsubscribe',
  event_types: ['idle', 'active']
}));
```

## [​](#use-cases) Use Cases

## Agent Awareness

Subscribe to `window_focus` and `idle` to give your AI agent context about what the user is doing and when to act.

## File Monitoring

Watch `file_change` events to detect when downloads complete, documents save, or files are created on the Desktop.

## Clipboard Sync

Monitor `clipboard` events to sync clipboard content between the VM and your application in real time.

## Process Tracking

Use `process_start` and `process_stop` to track application lifecycle - know when Chrome launches, when builds finish, etc.

## [​](#best-practices) Best Practices

## Subscribe Selectively

Only subscribe to event types you need. This reduces message volume and keeps your handler logic simple.

## Heartbeat

Send periodic `ping` messages (every 30 seconds) to keep the connection alive and detect disconnections early.

## Handle Backpressure

Events are dropped for slow consumers (buffer size: 256). Process events quickly or offload to a queue.

## Reconnection

Implement automatic reconnection with exponential backoff. Re-send your `subscribe` message after reconnecting.

Events require the computer to be running. If the computer is stopped, the WebSocket connection will be rejected. After reconnecting, you must re-subscribe - subscriptions are not persisted across connections.

## [​](#close-codes) Close codes

| Code | Meaning |
| --- | --- |
| `1000` | Normal closure. |
| `1001` | Server shutting down or computer stopping. |
| `4401` | Missing or invalid `token`. |
| `4404` | Computer not found or not running. |

[Previous](/api-reference/computers/audio)[Start streamStart an RTMP stream of the computer display.

Next](/api-reference/computers/stream-start)

⌘I