---
name: gh-copy slash command
description: Provides a slash command for copying files/directories from GitHub repos using gh-copy. Use when user wants to copy files from GitHub without cloning the entire repository.
---

# gh-copy Slash Command Skill

## Quick start

Create a slash command file at `~/.claude/commands/gh-copy.md` with the following content:

```markdown
---
description: Copy files/directories from GitHub repo without cloning
argument-hint: [owner/repo] [path-in-repo] [local-destination]
allowed-tools: Bash(gh:*,jq:*)
---

Copy files or directories from any GitHub repository using gh-copy.

Usage: /gh-copy <owner/repo> <path-in-repo> [local-destination]

Examples:
- /gh-copy owner/repo README.md .                    # Copy single file
- /gh-copy owner/repo docs/ ./docs/                   # Copy directory
- /gh-copy owner/repo src/main.cpp ./src/             # Copy to specific location
- /gh-copy -r main owner/repo path/ ./dest/           # Specify branch/ref
- /gh-copy --dry-run owner/repo file.txt .            # Preview without copying

The command uses gh-copy GitHub CLI extension under the hood.
See `gh copy --help` for all available options.
```

## Workflows

### Basic file copy
1. User invokes: `/gh-copy owner/repo README.md .`
2. Command executes: `gh api "repos/owner/repo/contents/README.md?ref=MAIN" -H "Accept: application/vnd.github.raw+json" > README.md`
3. File is copied to current directory

### Directory copy
1. User invokes: `/gh-copy owner/repo src/ ./src-copy/`
2. Command uses git trees API to get all files under src/
3. Each file is copied preserving directory structure

### Batch operations
For multiple files, create a manifest file and use:
`gh copy -m manifest.tsv` where manifest contains:
```
owner/repo	path	in-repo	local-destination
```

## Advanced features

### Error handling
The command validates:
- GitHub CLI (gh) is installed
- jq is installed for JSON processing
- Repository and path exist
- Proper argument count provided

### Customization options
Modify the command to:
- Change default destination (currently `.`)
- Add additional gh-copy flags (like `--dry-run`, `-r/--ref`)
- Modify allowed tools based on needs

### Integration notes
This command works as a drop-in replacement for manual gh copy usage.
All gh-copy features are available through argument passthrough.

See [REFERENCE.md](REFERENCE.md) for advanced usage patterns.