# gh-copy Slash Command Reference

## Command Structure

The slash command follows this structure:
```
/gh-copy [options] <owner/repo> <path-in-repo> [local-destination]
```

## Argument Handling

### Positional Arguments
1. `<owner/repo>` - GitHub repository in format `owner/repo`
2. `<path-in-repo>` - Path to file or directory in the repository
3. `[local-destination]` - Optional local destination (defaults to current directory)

### Flag Support
The command passes through all standard gh-copy flags:
- `-r, --ref <ref>` - Specify branch, tag, or commit
- `-m, --manifest <file>` - Batch mode with TSV manifest
- `--dry-run` - Preview without copying
- `-h, --help` - Show help

## Implementation Details

### Tool Requirements
The command requires:
- `gh` (GitHub CLI) - for API access
- `jq` - for JSON processing

These are declared in `allowed-tools: Bash(gh:*,jq:*)` to ensure they're available.

### Path Handling Logic
The command implements the same logic as gh-copy:
- Path ending with `/` indicates directory copy
- Destination ending with `/` or existing directory appends basename
- Default destination is current directory (`.`)
- If destination is directory, source basename is appended

### Error Handling
The command provides basic error handling through:
- Tool availability checks (via allowed-tools)
- Argument count validation (implicit in usage)
- GitHub API error propagation (via gh-copy)

## Advanced Usage Patterns

### Environment Variables
You can configure default behavior using environment variables:
- `GH_COPY_REF` - Default ref when `-r` not specified

### Integration with Other Commands
The slash command can be combined with others:
```
/gh-copy owner/repo README.md . && \
/gh-copy owner/repo LICENSE ./licenses/ && \
git add README.md LICENSE && \
git commit -m "Add documentation and license"
```

### Custom Variations
Create specialized versions by copying and modifying:
- `gh-copy-dry.md` - Always includes `--dry-run`
- `gh-copy-ref.md` - Pre-configured for specific branches
- `gh-copy-manifest.md` - Optimized for manifest batch mode

## Security Considerations

### Permission Model
The command inherits permissions from the current gh auth session:
- Can access public repositories without authentication
- Can access private repositories if authenticated with appropriate scopes
- Respects GitHub's rate limits and permissions

### Data Handling
- Streams data directly from GitHub API to local files
- No intermediate storage or caching
- Raw media transfer avoids base64 overhead
- Respects GitHub's 100MB file size limit for contents API

## Performance Characteristics

### File Transfers
- Uses GitHub Contents API for single files
- Streams data directly with `> "$dest"` redirection
- No base64 decoding overhead (uses `Accept: application/vnd.github.raw+json`)

### Directory Transfers
- Uses Git Trees API with `recursive=1`
- Filters results with grep for efficiency
- Processes files in streaming fashion
- Handles truncated responses appropriately

### Network Efficiency
- Single API call per file/directory
- No repository cloning or checkpoint downloads
- Respects existing gh connection pooling
- Benefits from gh's built-in retry logic

## Troubleshooting Guide

### Common Error Messages

#### "GitHub CLI (gh) not found on PATH"
**Solution**: Install GitHub CLI from https://cli.github.com/
**Verification**: `gh --version` should show version info

#### "jq not found on PATH"
**Solution**: Install jq package
**macOS**: `brew install jq`
**Ubuntu/Debian**: `sudo apt-get install jq`
**Verification**: `jq --version` shows version info

#### "repository not found" or "404"
**Causes**:
- Incorrect owner/repo format
- Private repo without access
- Repository doesn't exist
**Solutions**:
- Verify format: `owner/repo` (no slashes beyond first)
- Ensure authenticated with `gh auth login`
- Check repository URL on github.com

#### "path not found in repository"
**Causes**:
- Path typo
- Case sensitivity mismatch
- Path doesn't exist in specified ref
**Solutions**:
- Verify exact path casing
- Check path exists at specified ref/branch
- Use `-r` to specify correct ref if needed

#### "API rate limit exceeded"
**Indicators**: 403 responses with rate limit headers
**Solutions**:
- Authenticate with `gh auth login` for higher limits
- Wait for rate limit reset
- Use `--dry-run` to test before actual copies
- Consider GitHub Enterprise Server if self-hosted

## Debugging Techniques

### Enable Verbose Output
Add debugging to the command:
```
# In the slash command file, add:
set -x  # Uncomment for debugging
```

### Test API Calls Directly
Verify connectivity:
```
# Test repository access
gh api repos/owner/repo

# Test path access
gh api repos/owner/repo/contents/path/to/file

# Test raw content retrieval
gh api repos/owner/repo/contents/path/to/file -H "Accept: application/vnd.github.raw+json"
```

### Check Tool Availability
Verify prerequisites:
```
which gh
which jq
gh --version
jq --version
```

## Maintenance and Updates

### Keeping Current
The command automatically uses whatever version of gh-copy is installed:
- Update gh-copy: `gh extension upgrade copy`
- Get latest features: Updates flow through automatically

### Modifying the Command
To customize:
1. Copy `~/.claude/commands/gh-copy.md` to new name
2. Modify the content as needed
3. Save and use immediately (no reload required)

### Version Compatibility
Works with:
- GitHub CLI 2.0+
- gh-copy extension (any recent version)
- Standard Unix shell tools (grep, mkdir, etc.)

## References

### External Documentation
- [gh-copy GitHub Repository](https://github.com/VibeCodingLabs/gh-copy)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)

### Related Commands
- Native gh commands: `gh release`, `gh issue`, `gh pr`
- Similar utilities: `gh clone` (full repo), `gh browse` (web interface)
- File operations: `gh api` (direct API access), `gh edit` (file editing)

## Glossary

**Manifest File**: TSV file with columns: repo<TAB>path<TAB>dest for batch operations

**Raw Media**: GitHub API format that returns file contents directly without base64 encoding

**Ref**: Git reference - branch name, tag name, or commit SHA

**Default Branch**: Repository's primary branch (usually main or master)

**Rate Limit**: GitHub API request limit based on authentication status