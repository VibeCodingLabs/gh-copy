---
url: https://docs.orgo.ai/guides/templates/quickstart
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Two paths. Launching a curated template is one API call on any paid plan. Authoring your own takes a few minutes and a Scale plan. We’ll do both.

```
export ORGO_API_KEY=sk_live_...
```

## [​](#launch-a-curated-template) Launch a curated template

The fastest way to see templates in action: launch a computer from one Orgo maintains. Pass its `ref` as `template_ref` to [Create computer](/api-reference/computers/create) — the VM restores from the prebuilt golden snapshot with everything already installed.
Curated templates live in the `system` namespace. The current catalog is `system/claude-code@1.0.0`, `system/openclaw@1.0.0`, and `system/hermes-agent@1.0.0`.

cURL

Python

JavaScript

```
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "claude-1",
    "template_ref": "system/claude-code@1.0.0"
  }'
```

That’s it — the computer boots with Claude Code already installed and waiting in the terminal. Browse the full catalog with [List curated templates](/api-reference/templates/list-curated).

Hardware in the request overrides the template’s defaults. Add `"ram": 8, "cpu": 4` to launch the same template on a bigger box.

---

## [​](#author-your-own) Author your own

Now build a template from scratch. We’ll recreate a minimal Claude Code environment so you can see every step. It publishes to your own `default` namespace as `default/claude-code@1.0.0` — your private template, separate from the curated `system/claude-code@1.0.0` above.

Publishing and building require a [Scale plan](https://orgo.ai/pricing). Launching what you build counts against your normal computer quota.

1

Write the template

Save this as `claude-code.yaml`. It declares the hardware, an optional secret, a build-time install, and the terminal session the browser attaches to.

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

# The launching user supplies this from their vault; injected at create time.
secrets:
  - name: anthropic_api_key
    description: Anthropic API key, used by Claude Code when set.
    optional: true

# Baked into the golden snapshot at build time.
apps:
  - name: claude-code
    title: Claude Code
    install: |
      curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
      apt-get install -y nodejs
      npm install -g @anthropic-ai/claude-code

# The tmux session the browser terminal attaches to by name.
terminal:
  - name: claude-code
    cwd: /root
```

2

Validate it

Catch mistakes before publishing. [Validate](/api-reference/templates/validate) has no side effects.

```
curl -X POST https://www.orgo.ai/api/templates/validate \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/yaml" \
  --data-binary @claude-code.yaml
```

A clean template returns `{ "ok": true, "template": { ... } }`. Otherwise you get a list of `errors`, each with the exact `field` and a `message`.

3

Publish and build

[Publish](/api-reference/templates/publish) with `?auto_build=true` to register the ref and start baking the golden snapshot in one call.

```
curl -X POST "https://www.orgo.ai/api/templates?auto_build=true" \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/yaml" \
  --data-binary @claude-code.yaml
```

```
{
  "ref": "default/claude-code@1.0.0",
  "digest": "a1b2c3d4e5f6...",
  "published": "2026-06-08T17:00:00Z",
  "auto_build": "building"
}
```

4

Watch the build

A build takes about two minutes. Stream the log live, or poll until `ready`.

Stream (SSE)

Poll

```
curl -N https://www.orgo.ai/api/templates/default/claude-code/1.0.0/build/events \
  -H "Authorization: Bearer $ORGO_API_KEY"
```

5

Launch a computer from it

Once the build is `ready`, create a computer with your `template_ref`.

```
curl -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "claude-dev",
    "template_ref": "default/claude-code@1.0.0"
  }'
```

The computer restores from the golden snapshot — Node and Claude Code already installed, your terminal session ready. Poll `https://www.orgo.ai/api/desktops/{instance_id}/proxy/health` until it returns `200`, then connect. See [Create computer](/api-reference/computers/create) for the full response and connection details.

## [​](#iterate) Iterate

Refs are immutable, so you have two ways to ship a change:

* **Bump the version** — `1.0.0` → `1.0.1`. The clean path for anything you’ve shared.
* **Force-replace** — re-publish the same version with [`?force=true`](/api-reference/templates/publish) while you’re still iterating locally.

```
curl -X POST "https://www.orgo.ai/api/templates?auto_build=true&force=true" \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/yaml" \
  --data-binary @claude-code.yaml
```

## [​](#next-steps) Next steps

## Add secrets

Let users supply their own API keys.

## Run services

Long-running processes with health checks.

## React to events

Cron, file, HTTP, and metric triggers.

## Full API

Every templates endpoint.

[Previous](/guides/templates/introduction)[Template schemaEvery field in the orgo.ai/v1 template format.

Next](/guides/templates/schema)

⌘I