# CLI COMMANDS

This file provides the detailed help output for all CLI commands in `gh-copy`.

## Main Command (`gh-copy`)
```
Usage: gh-copy [OPTIONS] COMMAND [ARGS]...

  gh-copy: A tool to pack repositories into AI-friendly files and copy without
  cloning.

Options:
  --help  Show this message and exit.

Commands:
  clone-less  Copy files/dirs from a GitHub repo locally without cloning.
  init        Initialize a default .gh-copyignore file in the current...
  pack
```

## `gh-copy pack`
```
Usage: gh-copy pack [OPTIONS] PATH

Options:
  -o, --output PATH       Output file path
  --style [markdown|xml]  Output formatting style
  --template FILE         Custom Jinja2 template file
  --remove-empty-lines    Remove empty lines from output to save tokens
  --include TEXT          Include files matching glob patterns (e.g., '*.py')
  --exclude TEXT          Exclude files matching glob patterns (e.g.,
                          'tests/')
  --help                  Show this message and exit.
```

## `gh-copy clone-less`
```
Usage: gh-copy clone-less [OPTIONS] REPO PATH [DEST]

  Copy files/dirs from a GitHub repo locally without cloning. (Uses gh CLI)

Options:
  -r, --ref TEXT  Pin to a branch, tag, or commit SHA
  --dry-run       Show planned copies, write nothing
  --help          Show this message and exit.
```

## `gh-copy init`
```
Usage: gh-copy init [OPTIONS]

  Initialize a default .gh-copyignore file in the current directory.

Options:
  --help  Show this message and exit.
```
