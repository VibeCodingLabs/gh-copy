---
url: https://docs.orgo.ai/guides/instance-types
---

[Guides](/introduction)[API Reference](/api-reference/introduction)

Every Orgo computer runs on a dedicated instance with guaranteed resources. Choose the instance type that fits your workload.

## [​](#available-instances) Available instances

| Instance | CPU | RAM | API identifier |
| --- | --- | --- | --- |
| **Standard** | Standard | 4GB | `orgo-computer-small` |
| **Medium** | 2x | 8GB | `orgo-computer-medium` |
| **Large** | 4x | 16GB | `orgo-computer-large` |
| **XL** | 4x | 32GB | `orgo-computer-xl` |

All instances include Linux OS, full API access, and 1280x720 default resolution.


---

## [​](#instance-details) Instance details

orgo-computer-small

**Standard CPU / 4GB RAM**The default instance. Great for lightweight browser automation, simple web scraping, and single-task agents.

| Resource | Value |
| --- | --- |
| CPU | Standard |
| RAM | 4GB |
| Default resolution | 1280x720 |
| OS | Linux |

```
computer = Computer()  # Standard is the default
```

orgo-computer-medium

**2x CPU / 8GB RAM**Handles heavier browser workloads, multi-tab sessions, and agents that run multiple tools concurrently.

| Resource | Value |
| --- | --- |
| CPU | 2x |
| RAM | 8GB |
| Default resolution | 1280x720 |
| OS | Linux |

```
computer = Computer(ram=8, cpu=2)
```

orgo-computer-large

**4x CPU / 16GB RAM**Built for development environments, data processing, and agents running resource-intensive applications.

| Resource | Value |
| --- | --- |
| CPU | 4x |
| RAM | 16GB |
| Default resolution | 1280x720 |
| OS | Linux |

```
computer = Computer(ram=16, cpu=4)
```

orgo-computer-xl

**4x CPU / 32GB RAM**Maximum memory for large-scale processing, memory-heavy applications, and enterprise workloads.

| Resource | Value |
| --- | --- |
| CPU | 4x |
| RAM | 32GB |
| Default resolution | 1280x720 |
| OS | Linux |

```
computer = Computer(ram=32, cpu=4)
```

---

## [​](#choosing-an-instance) Choosing an instance

## Web scraping & simple tasks

**Standard** - Standard CPU / 4GB

## Multi-tab browsing & automation

**Medium** - 2x CPU / 8GB

## Dev environments & data processing

**Large** - 4x CPU / 16GB

## Enterprise & memory-intensive work

**XL** - 4x CPU / 32GB

---

## [​](#usage) Usage

Pass `ram` and `cpu` when creating a computer to select your instance type:

Python

TypeScript

```
from orgo import Computer

# Standard (default)
computer = Computer()

# Medium
computer = Computer(ram=8, cpu=2)

# Large
computer = Computer(ram=16, cpu=4)

# XL
computer = Computer(ram=32, cpu=4)
```

---

## [​](#accepted-values) Accepted values

The API validates `ram`, `cpu`, and `os` on every computer creation request. Passing an invalid value returns an error.

### [​](#ram) RAM

| Value | Description |
| --- | --- |
| `4` | 4GB (default) |
| `8` | 8GB |
| `16` | 16GB |
| `32` | 32GB |
| `64` | 64GB |

Maximum RAM per computer depends on your plan. Hacker: 4GB. Team: 8GB. Scale: 16GB.

### [​](#cpu) CPU

| Value | Description |
| --- | --- |
| `1` | Standard CPU (default) |
| `2` | 2x CPU |
| `4` | 4x CPU |
| `8` | 8x CPU |
| `16` | 16x CPU |

### [​](#os) OS

| Value | Description |
| --- | --- |
| `linux` | Linux (default, only supported OS) |

### [​](#resolution) Resolution

Resolution is passed as a string in `WIDTHxHEIGHTxDEPTH` format. Default is `1280x720x24`.

```
1024x768x24
1280x720x24
1920x1080x24
```

## [​](#persistence) Persistence

A computer’s disk and files persist across stop/start. Stopping a computer archives its disk; starting it again restores your files and installed software on a fresh host (a new IP — in-memory state and running processes are not preserved). Computers run continuously until you explicitly stop them.


---

## [​](#included-with-every-instance) Included with every instance

All instance types share these capabilities:

* Full REST API and SDK access
* Screenshot, mouse, keyboard, and bash execution
* File upload and download
* VNC access

Instance type determines the compute resources per agent. The number of agents, storage, bandwidth, and other limits depend on your [plan](https://www.orgo.ai/pricing).

[Previous](/guides/migrate)[MemoryBuild computer agents that remember across sessions

Next](/guides/memory)

⌘I