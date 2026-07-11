# CLI-REFERENCE.md

## Command Line Interface Reference

The `gh-copy` tool uses `click` to provide a robust CLI.

### `gh-copy` (Main Group)
```bash
Usage: gh-copy [OPTIONS] COMMAND [ARGS]...

  gh-copy: A tool to pack repositories into AI-friendly files and copy without cloning.

Options:
  --help  Show this message and exit.
```

### `gh-copy pack`
Packs a local repository into a single AI-Agent readable file.

```bash
Usage: gh-copy pack [OPTIONS] PATH

Options:
  -o, --output PATH  Output file path (default: repacked_repo.txt)
  --help             Show this message and exit.
```
**Arguments:**
- `PATH`: The directory path of the repository to pack. Must exist.

### `gh-copy clone-less`
Copies files/dirs from a GitHub repo locally without cloning. (Requires the `gh` CLI installed on the host system).

```bash
Usage: gh-copy clone-less [OPTIONS] REPO PATH [DEST]

Options:
  -r, --ref TEXT  Pin to a branch, tag, or commit SHA
  --dry-run       Show planned copies, write nothing
  --help          Show this message and exit.
```
**Arguments:**
- `REPO`: The GitHub repository (e.g., `owner/repo`).
- `PATH`: The path within the remote repository to copy.
- `DEST`: (Optional) The local destination path. Defaults to `.`.
