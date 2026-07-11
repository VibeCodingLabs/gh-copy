---
url: https://docs.orgo.ai/guides/templates/triggers
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Triggers turn a computer into a reactive system. Each trigger pairs a **source** that produces events with one or more **actions** that run in response, plus optional **dedup** to suppress noise. They run continuously inside the VM, managed for you.

```
triggers:
  - name: heartbeat
    title: "Minute heartbeat"
    source:
      type: cron
      schedule: "* * * * *"
    actions:
      - type: command
        run: "echo beat >> /var/lib/orgo/heartbeat.log"
```

## [​](#sources) Sources

A source’s `type` selects which fields apply.

| Type | Fires when | Key fields |
| --- | --- | --- |
| `cron` | A schedule elapses | `schedule` (5-field cron) |
| `file` | A path is created, modified, or deleted | `path`, `events: [create, modify, delete]` |
| `http` | Polling a URL returns an unexpected status | `url`, `method`, `expect_code`, `interval` |
| `process` | A process starts or stops | `process` |
| `metric` | A system metric crosses a threshold | `metric`, `op`, `value`, `duration` |
| `log` | A service log line matches | `service`, `match`, `parse: text|json` |
| `event` | A custom event is emitted in the VM | `event` |
| `desktop` | A desktop event occurs | `event` (`window_focus`, `clipboard`, `idle`, …) |

Metric sources cover `cpu_percent`, `ram_percent`, `disk_percent`, `net_in_mbps`, `net_out_mbps`, and the `gpu_*` family, compared with `>`, `>=`, `<`, `<=`, `==`, or `!=`.

```
# Restart a service if memory stays high for two minutes
triggers:
  - name: mem-guard
    source:
      type: metric
      metric: ram_percent
      op: ">"
      value: 90
      duration: 2m
    actions:
      - type: service
        op: restart
        target: my-app-server
```

## [​](#actions) Actions

A trigger runs one or more actions in order. The `type` selects the fields.

| Type | Does | Key fields |
| --- | --- | --- |
| `webhook` | HTTP request out | `url`, `method`, `headers`, `body` |
| `command` | Run a shell command | `run`, `cwd`, `timeout` |
| `service` | Control a service | `op: start|stop|restart`, `target` |
| `notify` | In-VM notification | `title`, `level: info|warning|critical` |
| `log` | Write to the trigger log | `message` |
| `api` | Call the in-VM desktop API | `endpoint` |

Action `body`, `run`, and similar fields support `{{...}}` templating, so you can include event data in a webhook payload.

```
# Post to Slack when a file lands in the inbox
triggers:
  - name: new-upload
    source:
      type: file
      path: /data/inbox
      events: [create]
    actions:
      - type: webhook
        url: https://hooks.slack.com/services/...
        method: POST
        body: '{"text": "new file: {{ event.path }}"}'
```

## [​](#dedup) Dedup

Bursty sources can fire constantly. Add at most one dedup strategy per trigger.

| Strategy | Effect |
| --- | --- |
| `debounce` | Collapse a burst, fire once after it settles. |
| `cooldown` | Enforce a minimum gap between fires. |
| `rate_limit` | Cap fires, e.g. `10/1m`. |

```
triggers:
  - name: config-reload
    source:
      type: file
      path: /etc/my-app/config.yaml
      events: [modify]
    dedup:
      debounce: 2s
    actions:
      - type: service
        op: restart
        target: my-app-server
```

## [​](#triggers-vs-health-checks) Triggers vs. health checks

They complement each other:

* A [health check](/guides/templates/schema#apps) is a per-app **watchdog** — it polls one service and auto-heals it (`on_fail: restart_service:…`).
* A trigger is **general automation** — any source to any action, across the whole VM.

Reach for a health check to keep a service alive; reach for a trigger to react to files, schedules, metrics, or desktop activity.

## [​](#next-steps) Next steps

## Schema reference

Every source and action field.

## Examples

Triggers in real templates.

[Previous](/guides/templates/secrets)[ExamplesComplete, runnable templates you can copy, publish, and build.

Next](/guides/templates/examples)

⌘I