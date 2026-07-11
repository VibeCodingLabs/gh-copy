---
url: https://docs.orgo.ai/api-reference/computers/audio
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Stream real-time audio from a computer’s virtual speaker over WebSocket. Audio is captured from PulseAudio and delivered as raw PCM data in 20 ms frames - low-latency enough for live monitoring.

## [​](#connection-url) Connection URL

```
wss://www.orgo.ai/desktops/{computer_id}/ws/audio?token={password}
```

### [​](#authentication) Authentication

The audio WebSocket requires the computer’s password as the `token` query parameter. Retrieve it from the [Get VNC Password](/api-reference/computers/vnc-password) endpoint before connecting.
Connections without a valid token are rejected with close code `4401`.

### [​](#query-parameters) Query Parameters

[​](#param-token)

token

string

required

Computer password. Retrieve via the [Get VNC Password](/api-reference/computers/vnc-password) endpoint.

[​](#param-sample-rate)

sample\_rate

number

default:"24000"

Audio sample rate in Hz.

[​](#param-channels)

channels

number

default:"1"

Number of audio channels. `1` for mono, `2` for stereo.

## [​](#audio-format) Audio Format

| Property | Value |
| --- | --- |
| Encoding | `s16le` (signed 16-bit little-endian PCM) |
| Sample rate | 24,000 Hz |
| Channels | 1 (mono) |
| Frame duration | 20 ms |
| Frame size | 960 bytes |
| Bitrate | ~48 KB/s |

Raw PCM - no codec, no container format. Each binary WebSocket frame contains one or more audio frames ready for playback.

## [​](#protocol) Protocol

### [​](#connection-flow) Connection Flow

1. Client connects with `?token=` parameter
2. Server validates the token
3. Server sends a JSON text frame confirming the audio configuration:

   ```
   { "type": "started", "sample_rate": 24000, "channels": 1 }
   ```
4. Server continuously sends **binary frames** containing raw PCM audio data
5. Client decodes and plays via Web Audio API or any PCM-capable player

### [​](#client-→-server-messages) Client → Server Messages

stop

Stop audio capture and close the connection.

```
{
  "type": "stop"
}
```

ping

Send a heartbeat ping to keep the connection alive.

```
{
  "type": "ping"
}
```

### [​](#server-→-client-messages) Server → Client Messages

started

Sent immediately after connection. Confirms the audio stream configuration.

```
{
  "type": "started",
  "sample_rate": 24000,
  "channels": 1
}
```

[​](#param-type)

type

string

Always `"started"`.

[​](#param-sample-rate-1)

sample\_rate

number

Audio sample rate in Hz.

[​](#param-channels-1)

channels

number

Number of audio channels.

Binary frames

Raw PCM audio data. Each binary frame contains signed 16-bit little-endian samples.At the default 24 kHz mono, each 20 ms frame is 960 bytes (480 samples × 2 bytes per sample).

pong

Response to a ping message.

```
{
  "type": "pong"
}
```

error

Error starting or maintaining the audio stream.

```
{
  "type": "error",
  "message": "Failed to start audio capture"
}
```

[​](#param-type-1)

type

string

Always `"error"`.

[​](#param-message)

message

string

Human-readable error description.

## [​](#examples) Examples

JavaScript (Web Audio API)

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

// Step 2: Connect to audio stream
const ws = new WebSocket(
  `wss://www.orgo.ai/desktops/${computerId}/ws/audio?token=${password}`
);
ws.binaryType = 'arraybuffer';

// Step 3: Set up Web Audio API playback
const ctx = new AudioContext({ sampleRate: 24000 });
let nextPlayTime = 0;

ws.onmessage = (event) => {
  // Text frames are JSON control messages
  if (typeof event.data === 'string') {
    const msg = JSON.parse(event.data);
    if (msg.type === 'started') {
      console.log(`Audio stream: ${msg.sample_rate}Hz, ${msg.channels}ch`);
    }
    return;
  }

  // Binary frames are raw PCM audio
  const pcm = new Int16Array(event.data);
  const floats = new Float32Array(pcm.length);
  for (let i = 0; i < pcm.length; i++) {
    floats[i] = pcm[i] / 32768;
  }

  const buffer = ctx.createBuffer(1, floats.length, 24000);
  buffer.getChannelData(0).set(floats);

  const source = ctx.createBufferSource();
  source.buffer = buffer;
  source.connect(ctx.destination);

  // Schedule with drift correction
  const now = ctx.currentTime;
  if (nextPlayTime < now || nextPlayTime > now + 0.15) {
    nextPlayTime = now + 0.02;
  }
  source.start(nextPlayTime);
  nextPlayTime += buffer.duration;
};
```

## [​](#playback-tips) Playback Tips

## Browser Autoplay

Browsers require a user gesture (click, keypress) before `AudioContext` can play. Create the context inside a click handler, or call `ctx.resume()` after a user interaction.

## Drift Correction

Schedule buffers slightly ahead of real time and reset when drift exceeds ~150 ms. This prevents gaps and keeps latency below 50 ms.

## Heartbeat

Send periodic `ping` messages (every 30 seconds) to keep the connection alive and detect disconnections early.

## Sample Rate

The default 24 kHz mono is optimized for voice and system sounds. Pass `sample_rate=48000` for higher fidelity if needed.

Audio streaming requires the computer to be running. If the computer is stopped, the WebSocket connection will be rejected. Audio is captured from the VM’s virtual PulseAudio speaker - any sound the desktop produces (browser media, system alerts, application audio) is streamed.

## [​](#close-codes) Close codes

| Code | Meaning |
| --- | --- |
| `1000` | Normal closure (client sent `stop` or disconnected). |
| `1001` | Server shutting down or computer stopping. |
| `4401` | Missing or invalid `token`. |
| `4404` | Computer not found or not running. |
| `4500` | Failed to start audio capture. |

[Previous](/api-reference/computers/terminal)[Events WebSocketSubscribe to desktop events - window focus, clipboard, files, processes, idle state.

Next](/api-reference/computers/events)

⌘I