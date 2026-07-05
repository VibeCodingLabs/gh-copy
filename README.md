# gh copy

> A [GitHub CLI](https://cli.github.com) extension to copy files — or whole directories — out of any GitHub repo **without cloning it**.

![gh extension](https://img.shields.io/badge/gh-extension-2088FF?logo=github)
![shell](https://img.shields.io/badge/shell-bash-4EAA25?logo=gnubash&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-blue)

`gh copy` grabs exactly the paths you want from a remote repository and drops them on disk. No `git clone`, no sparse-checkout dance, no `.git` history — just the files. It's a drop-in **superset** of [`mislav/gh-cp`](https://github.com/mislav/gh-cp): same `<repo> <path> <dest>` contract, plus ref pinning, recursive directory copy, batch manifests, and dry-run.

## Quickstart

```console
$ gh extension install VibeCodingLabs/gh-copy

$ gh copy
Usage: gh copy <repo> <path> [dest] ...

$ gh copy cli/cli README.md .
copy cli/cli README.md -> ./README.md

$ gh copy -r v2.40.0 cli/cli docs/ ./cli-docs/    # recursive: every file under docs/, subpaths preserved
```

## Why

Cloning to grab one file (or one folder) is wasteful — you pull history, branches, and everything else. `gh copy` fetches only the paths you name, straight through the authenticated GitHub API, so it works on private repos too and respects your existing `gh auth` session.

## Prerequisites

- [GitHub CLI](https://cli.github.com) `gh` **2.0+**, authenticated (`gh auth login`)
- [`jq`](https://jqlang.github.io/jq/)

## Installation

```console
gh extension install VibeCodingLabs/gh-copy
```

Upgrade / remove later:

```console
gh extension upgrade copy
gh extension remove copy
```

## Usage

```
gh copy <repo> <path> [dest]           # copy a single file (dest defaults to .)
gh copy <repo> <path>/ <dest/>         # copy a directory recursively
gh copy -r <ref> <repo> <path> [dest]  # pin to a branch, tag, or commit SHA
gh copy -m <manifest.tsv>              # batch copy from a manifest
gh copy --dry-run ...                  # print planned copies, write nothing
gh copy -h | --help
```

### Arguments

| Arg | Description |
|---|---|
| `<repo>` | `owner/name` of the source repository. |
| `<path>` | Path to a file inside the repo. A **trailing `/`** means copy that directory recursively. |
| `[dest]` | Destination on disk. Defaults to `.`; a trailing `/` or existing dir appends the basename. |

### Flags

| Flag | Description |
|---|---|
| `-r, --ref <ref>` | Branch, tag, or commit SHA. Defaults to the repo's default branch. Also settable via `GH_COPY_REF`. |
| `-m, --manifest <file>` | TSV of `repo⇥path⇥dest` rows. `#` comments and blank lines ignored. |
| `--dry-run` | Resolve and print every planned copy without writing anything. |
| `-h, --help` | Show usage. |

## Examples

```console
# single file (gh cp compatible)
gh copy cli/cli README.md .

# pin to a tag, copy a whole directory, preserving its subpaths
gh copy -r v2.40.0 cli/cli pkg/cmd/ ./vendor/cli/pkg/cmd/

# preview without writing
gh copy --dry-run cli/cli LICENSE ./licenses/

# batch pull many files/dirs at once
gh copy -m sources.tsv
```

`sources.tsv` (real tabs between columns):

```tsv
# repo⇥path⇥dest
cli/cli	README.md	./vendor/cli/README.md
cli/cli	docs/	./vendor/cli/docs/
jqlang/jq	README.md	./vendor/jq/README.md
```

## How it works

- **File:** `gh api repos/<repo>/contents/<path>?ref=<ref>` with `Accept: application/vnd.github.raw`, streamed to `<dest>`. Raw-accept avoids base64 and the contents-API size cap.
- **Directory:** one `gh api repos/<repo>/git/trees/<ref>?recursive=1` call, filtered to blobs under the requested prefix, each streamed to disk. One tree call — not N per-file calls.

Pure `bash` + `gh api` + `jq`. No clone, no `git`, no temp checkout.

## Compatibility

Every valid `gh cp <repo> <path> <dest>` invocation is a valid `gh copy` invocation with identical behavior. Superset only — no breaking changes from `gh-cp`.

## Development

```console
# clone and install your local copy as the live extension
git clone https://github.com/VibeCodingLabs/gh-copy && cd gh-copy
gh extension install .

# iterate: edit ./gh-copy, then run
gh copy --dry-run cli/cli README.md .

# lint
shellcheck gh-copy
```

A GitHub CLI extension is just an executable named `gh-<name>` at the repo root. This repo is `gh-copy`, so the command is `gh copy`.

## Contributing

Issues and PRs welcome. Keep it dependency-light (bash + `gh` + `jq`), pass `shellcheck`, and preserve `gh-cp` compatibility.

## License

MIT — see [LICENSE](./LICENSE).

## Credits

Inspired by and compatible with [`mislav/gh-cp`](https://github.com/mislav/gh-cp).
