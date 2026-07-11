---
url: https://docs.orgo.ai/guides/templates/introduction
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

A template is a declarative spec for an Orgo computer. One file describes the hardware, the software to install, the services to run, the secrets it needs, and what the user sees on connect. Orgo builds that file once into a **golden snapshot**, and every launch restores from it in seconds — fully configured, identical every time.
Think of it as a `Dockerfile` for a full desktop VM: write it once, version it, and hand out reproducible computers from it.

## Quickstart

Author, build, and launch your first template.

## Schema reference

Every field in the `orgo.ai/v1` format.

## Secrets

Inject API keys without baking them in.

## API reference

Publish, build, and launch over HTTP.

## [​](#why-templates) Why templates

Without a template, every new computer starts from a base image and you script the setup yourself — install packages, write config, start services, wait for it all to converge. That work runs on every boot and drifts over time.
A template moves all of that to **build time**. The result is a snapshot that boots ready.

|  | Base image + setup script | Template |
| --- | --- | --- |
| Time to ready | Minutes of install on every boot | Seconds — restores a prebuilt snapshot |
| Reproducibility | Drifts as packages and scripts change | Content-addressed, identical every launch |
| Definition | Imperative script you maintain | One declarative file, versioned |
| Services & health | You wire up supervisord and watchdogs | Declared once, managed for you |
| Sharing | Copy the script around | Publish a `ref`, launch anywhere |

## [​](#golden-snapshots) Golden snapshots

When you **build** a template, Orgo boots a real VM, runs your install steps, then pauses the machine and captures its full state — disk, memory, and CPU — as a *golden snapshot*. Launching a computer from the template copies that snapshot and resumes it.

* **Build once** — about two minutes, and only when the template changes.
* **Launch in seconds** — a restore skips the entire install phase.
* **Content-addressed** — the snapshot is keyed by a SHA-256 `digest` of the canonical template. Two identical templates share a build; change one byte and you get a new digest.

This is why a template VM comes up with Node already installed and your service already running, while a base image would still be downloading packages.

## [​](#lifecycle) Lifecycle

1

Write

Author a template in YAML or JSON using the [`orgo.ai/v1`](/guides/templates/schema) format. A short [sugar form](/guides/templates/schema#sugar-form) keeps simple templates tiny.

2

Publish

`POST` the document to your registry. Refs are immutable and content-addressed: `namespace/name@version`.

3

Build

Bake the golden snapshot. Watch it stream, or poll until `ready`.

4

Launch

Create a computer with `template_ref`. It restores from the golden snapshot, pre-configured.

```
WRITE  →  PUBLISH  →  BUILD  →  LAUNCH
 yaml     registry    golden    seconds
          immutable    ~2 min   per computer
```

## [​](#refs) Refs

Every template version is addressed by a **ref**:

```
namespace / name @ version
   default / my-template @ 1.0.0
```

* **namespace** — groups your templates. Your own default to `default`; curated templates published by Orgo live in the `system` namespace (e.g. `system/claude-code@1.0.0`).
* **name** — lowercase kebab-case.
* **version** — semver, immutable once published. Bump it to ship a change.

Pass a ref as `template_ref` to [Create computer](/api-reference/computers/create), or anywhere the API takes a template.

## [​](#curated-vs-your-own) Curated vs. your own

## Curated templates

Published and maintained by Orgo in the `system` namespace — Claude Code, OpenClaw, Hermes Agent, and more. **Any plan can launch them.** Browse with [List curated templates](/api-reference/templates/list-curated).

## Your templates

Author and publish your own on a **Scale** plan. They live in your namespaces and launch into your workspaces.

**Plan requirements.** Launching a computer from a template counts against your plan’s computer quota, like any computer. **Publishing and building** your own templates requires a [Scale plan](https://orgo.ai/pricing). Curated templates are launchable on every paid plan.

## [​](#what-goes-in-a-template) What goes in a template

A quick tour — see the [schema reference](/guides/templates/schema) for every field.

| Field | What it does |
| --- | --- |
| `hardware` | CPU, RAM, disk, GPU, resolution, region, auto-stop |
| `build` | `apt` / `pip` / `npm` / `run` steps baked into the snapshot |
| `apps` | Installed apps with long-running [services and health checks](/guides/templates/schema#apps) |
| `files` | Inline or fetched files written into the VM |
| `env` + `secrets` | Environment variables and [vault-injected secrets](/guides/templates/secrets) |
| `triggers` | [Reactive automation](/guides/templates/triggers): a source fires, actions run |
| `terminal` | Pre-staged tmux sessions the browser terminal attaches to |
| `hooks` | Shell that runs at first boot, every boot, resume, and shutdown |
| `egress_policy` | Per-VM domain/IP allow or block rules |

## [​](#next-steps) Next steps

## Build your first template

A complete walkthrough, end to end.

## See real examples

Annotated curated templates you can copy.

[Previous](/guides/troubleshooting)[Templates quickstartLaunch a curated template, then author and ship your own.

Next](/guides/templates/quickstart)

⌘I