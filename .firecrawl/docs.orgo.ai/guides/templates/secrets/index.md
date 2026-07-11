---
url: https://docs.orgo.ai/guides/templates/secrets
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

A template often needs credentials — an Anthropic key, a database URL, an OAuth token. Secrets let a template **declare** what it needs without ever containing the value. The launching user supplies it from their vault, and Orgo injects it into the VM at create time. The value never lives in the template, the registry, or the golden snapshot.

## [​](#the-model) The model

1

Declare

The template lists the secrets it needs under `secrets`. Names only — no values.

2

Supply

The launching user stores the value in their vault (once, per account).

3

Inject

At create, Orgo writes the user’s matching secrets into the VM at `/root/.env` (mode `0600`). They are never baked into the shared snapshot.

## [​](#declare) Declare

```
secrets:
  - name: anthropic_api_key       # lowercase; maps to the ANTHROPIC_API_KEY vault entry
    description: Anthropic API key, used by Claude Code.
    example: "sk-ant-..."
    docs_url: https://console.anthropic.com/settings/keys
    optional: true                # template still launches when absent
```

| Field | Description |
| --- | --- |
| `name` | Lowercase, alphanumeric with `-` or `_`. Orgo maps it to its `UPPER_SNAKE_CASE` form (e.g. `ANTHROPIC_API_KEY`) and looks that name up in your vault. **Required.** |
| `description` | Shown to the launching user. |
| `example` | Example value shape, e.g. `sk-ant-...`. |
| `docs_url` | Where to obtain the secret. |
| `optional` | If `true`, the template still launches when the secret is absent. Defaults to `false`. |

## [​](#reference) Reference

A declared secret can be referenced two ways.
**As an environment variable** — `{secret: <name>}` in `env`:

```
secrets:
  - name: anthropic_api_key

env:
  ANTHROPIC_API_KEY:
    secret: anthropic_api_key
```

**As a file** — `secret://<name>` in `files`:

```
files:
  - to: /root/.config/app/credentials.json
    from: secret://app_credentials
    mode: "0600"
```

At launch, every injected secret is also written to `/root/.env` as its `UPPER_SNAKE_CASE` name — so `anthropic_api_key` becomes `ANTHROPIC_API_KEY`. The base shell sources `/root/.env`, so interactive terminals see the variable automatically.

## [​](#secrets-and-golden-snapshots) Secrets and golden snapshots

This is the one subtlety worth understanding. A template VM boots by **restoring the golden snapshot**, which was built *before any particular user launched it*. The user’s secret is injected per-VM at create — after the snapshot was baked.
So a process baked into the snapshot won’t see the secret unless it (re)reads it after injection. The fix is the [`on_resume` hook](/guides/templates/schema#hooks), which runs on every restore, after `/root/.env` is written:

```
secrets:
  - name: anthropic_api_key
    optional: true

terminal:
  - name: claude-code            # a bare session for on_resume to drive
    cwd: /root

hooks:
  on_resume: |
    tmux has-session -t claude-code 2>/dev/null || \
      tmux new-session -d -s claude-code -c /root
    tmux send-keys -t claude-code \
      'set -a; . /root/.env 2>/dev/null; set +a; clear; claude' C-m
```

This is the pattern the curated `claude-code` template uses to launch the CLI with the launcher’s own key. For an [app service](/guides/templates/schema#apps), reference the secret through the service’s `env` instead, and supervisord starts it with the value in place.

## [​](#managing-your-vault) Managing your vault

Add and update secret values in the dashboard at [orgo.ai/workspaces](https://www.orgo.ai/workspaces). The vault is per-account: store a key once and every template you launch can request it by name.

## [​](#security) Security

* Values are **encrypted at rest** and never returned to a client in plaintext.
* A secret is **never** part of the template document, its `digest`, or the golden snapshot.
* Build logs never print secret values.
* Only secrets a template explicitly declares are injected, and only if you have them set.

## [​](#next-steps) Next steps

## Schema reference

`env`, `files`, and `secrets` in full.

## Examples

See the `on_resume` pattern in a real template.

[Previous](/guides/templates/schema)[TriggersReactive automation inside a template: a source fires, actions run.

Next](/guides/templates/triggers)

⌘I