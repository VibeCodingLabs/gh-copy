---
url: https://docs.orgo.ai/guides/templates/examples
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Each template below is a full `orgo.ai/v1` document — copy it, [publish and build](/guides/templates/quickstart#author-your-own) it, then launch a computer from its ref. The first four use the short [sugar form](/guides/templates/schema#sugar-form); the last uses the canonical form.

Publishing and building templates requires a [Scale plan](https://orgo.ai/pricing). Curated templates are launchable on every paid plan.

## [​](#minimal) Minimal

The smallest valid template — a blank Linux desktop. Everything except `api_version` and the name/version is optional.

my-template.yaml

```
api_version: orgo.ai/v1
name:    my-template@1.0.0
cpu:     2
ram:     4gb
display: 1280x800
```

## [​](#static-site-nginx) Static site (nginx)

A single HTTP service on port 8000, served by nginx, with Chrome set to auto-open the page when the desktop starts. The headline is driven by a compile-time [variable](/guides/templates/schema#vars-and-interpolation), so changing it is a one-line edit.

static-site.yaml

```
api_version: orgo.ai/v1
name:    static-site@1.0.0
cpu:     2
ram:     4gb
display: 1280x800

vars:
  headline: "Hello from Orgo"

files:
  /opt/site/index.html: |
    <!doctype html>
    <html>
      <head><title>${var.headline}</title></head>
      <body style="font-family: sans-serif; padding: 2rem;">
        <h1>${var.headline}</h1>
        <p>Edit the template and rebuild.</p>
      </body>
    </html>

  /etc/nginx/sites-available/orgo:
    mode: "0644"
    inline: |
      server {
        listen 8000 default_server;
        root /opt/site;
        index index.html;
        location / { try_files $uri $uri/ =404; }
      }

apps:
  - name: nginx
    title: "nginx"
    install: |
      apt-get update -qq
      apt-get install -y --no-install-recommends nginx
      ln -sf /etc/nginx/sites-available/orgo /etc/nginx/sites-enabled/orgo
      rm -f /etc/nginx/sites-enabled/default
    services:
      - name: nginx
        run: "nginx -g 'daemon off;'"
        user: root
        restart: always
    health:
      type: http
      url: http://127.0.0.1:8000/
      every: 15s
      retries: 3
      on_fail: restart_service:nginx
    ports:
      - { internal: 8000, public: true }

  # A second "app" with no install or service — just an autostart entry
  # that opens Chrome on the page once the desktop is up. The 4s delay
  # gives nginx a moment to bind before Chrome hits the page.
  - name: chrome
    title: "Chrome"
    autostart:
      - run: "google-chrome-stable --no-sandbox --disable-gpu --no-first-run --no-default-browser-check http://127.0.0.1:8000"
        delay: 4
```

## [​](#browser-desktop) Browser desktop

Chrome launches automatically on boot. Chrome is already in the base image, so there’s no install step — just an [`autostart`](/guides/templates/schema#apps) entry.

browser-desktop.yaml

```
api_version: orgo.ai/v1
name:    browser-desktop@1.0.0
cpu:     2
ram:     4gb
display: 1280x800

apps:
  - name: chrome
    title: "Chrome"
    autostart:
      - run: "google-chrome-stable --no-sandbox --disable-gpu --no-first-run --no-default-browser-check https://orgo.ai"
        delay: 2
```

## [​](#background-worker-with-triggers) Background worker with triggers

A long-running [service](/guides/templates/schema#apps) that logs a tick every 10 seconds, kept alive by a process [health check](/guides/templates/schema#apps), plus two [triggers](/guides/templates/triggers): a cron heartbeat and a CPU watchdog that notifies on sustained load.

heartbeat-worker.yaml

```
api_version: orgo.ai/v1
name:    heartbeat-worker@1.0.0
cpu:     2
ram:     4gb
display: 1280x800

vars:
  worker_name: "heartbeat"

env:
  WORKER_NAME: "${var.worker_name}"

files:
  /opt/worker/run.sh:
    mode: "0755"
    inline: |
      #!/bin/bash
      set -e
      while true; do
        echo "[$(date -Iseconds)] ${WORKER_NAME} tick"
        sleep 10
      done

apps:
  - name: worker
    title: "Heartbeat worker"
    services:
      - name: heartbeat-worker
        run: "/opt/worker/run.sh"
        restart: always
    health:
      type: process
      process: run.sh
      every: 30s
      retries: 3
      on_fail: restart_service:heartbeat-worker

triggers:
  - name: minute-mark
    source: { type: cron, schedule: "* * * * *" }
    actions:
      - type: log
        message: "minute mark"

  - name: cpu-watchdog
    source:
      type: metric
      metric: cpu_percent
      op: ">"
      value: 80
      duration: 30s
    dedup: { cooldown: 2m }
    actions:
      - type: notify
        title: "CPU hot"
        level: warning
```

## [​](#agent-with-a-user-supplied-key) Agent with a user-supplied key

The canonical form, with a [secret](/guides/templates/secrets) the launching user supplies from their vault. The CLI is installed at build time; the [`on_resume` hook](/guides/templates/schema#hooks) starts it with the launcher’s own key after `/root/.env` is injected at create. This is the pattern the curated `system/claude-code` template uses.

claude-code.yaml

```
api_version: orgo.ai/v1

template:
  name: claude-code
  version: 1.0.0
  description: Claude Code CLI, ready in the terminal.

hardware:
  cpu: 2
  ram_gb: 4
  resolution: 1280x720x24

secrets:
  - name: anthropic_api_key
    description: Anthropic API key, used by Claude Code when set.
    optional: true

apps:
  - name: claude-code
    title: Claude Code
    install: |
      curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
      apt-get install -y nodejs
      npm install -g @anthropic-ai/claude-code

terminal:
  - name: claude-code
    cwd: /root

hooks:
  on_resume: |
    tmux has-session -t claude-code 2>/dev/null || \
      tmux new-session -d -s claude-code -c /root
    tmux send-keys -t claude-code \
      'set -a; . /root/.env 2>/dev/null; set +a; clear; claude' C-m
```

## [​](#publish-build-launch) Publish, build, launch

The flow is the same for any of the above:

```
# Publish + build the golden snapshot in one call
curl -X POST "https://www.orgo.ai/api/templates?auto_build=true" \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/yaml" \
  --data-binary @static-site.yaml

# Poll until the build is ready
curl https://www.orgo.ai/api/templates/default/static-site/1.0.0/build \
  -H "Authorization: Bearer $ORGO_API_KEY"

# Launch a computer from it
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id": "WORKSPACE_ID", "name": "site-1", "template_ref": "default/static-site@1.0.0"}'
```

## Quickstart

The full walkthrough, end to end.

## Schema reference

Every field explained.

## Secrets

The full secret-injection model.

## Publish API

Ship a template over HTTP.

[Previous](/guides/templates/triggers)[Claude Computer UseLet Claude control a virtual desktop

Next](/guides/claude-computer-use)

⌘I