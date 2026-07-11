# gh-copy Slash Command Examples

## Common Use Cases

### 1. Getting Documentation
```
# Get a project's README
/gh-copy nodejs/node README.md .

# Get API documentation
/gh-copy tensorflow/tensorflow/api_docs/python/tf/keras/layers/Conv2D.md ./ml-docs/

# Get contributing guidelines
/gh-copy microsoft/vscode/CONTRIBUTING.md ./contributing-guides/vscode-contributing.md
```

### 2. Code Examples and Templates
```
# Get a boilerplate or example
/gh-copy facebook/react/README.md ./frontend-dev/react-overview.md
/gh-copy facebook/react-native/examples/WeatherApp/ ./mobile-examples/weather-app/

# Get build configurations
/gh-copy google/go-cloud/samples/gcs/blob/README.md ./go-cloud-examples/gcs-blob-readme.md
```

### 3. Configuration Files
```
# Get popular config templates
/gh-copy github/gitignore/main/Python.gitignore .gitignore
/gh-copy github/gitignore/main/Node.gitignore .gitignore
/gh-copy npm/cli/latest/.npmrc ./npm-config-example.txt

# Get CI configurations
/gh-copy github/super-linter/.github/workflows/linter.yml ./.github/workflows/
```

### 4. Learning Resources
```
# Get tutorial materials
/gh-copy freeCodeCamp/freeCodeCamp/README.md ./learning/freecodecamp-overview.md

# Get workshop materials
/gh-copy githubtraining/hello-world/README.md ./workshops/github-hello-world.md
```

### 5. Reference Materials
```
# Get license templates
/gh-copy github/choosealicense.com/licenses/mit.txt ./LICENSES/MIT.txt
/gh-copy github/choosealicense.com/licenses/gpl-3.0.txt ./LICENSES/GPLv3.txt

# Get contributing guides
/gh-copy cloudflare/wrangler/CONTRIBUTING.md ./dev-guides/wrangler-contributing.md
```

## Advanced Usage

### With Specific Refs/Branches
```
# Get documentation from a specific release
/gh-copy -r v1.0.0 kubernetes/kubernetes/docs/tutorials/kubernetes-basics/ ./k8s-tutorials/

# Get code from a development branch
/gh-copy -r next vercel/next.js/examples/with-tailwindcss ./examples/nextjs-tailwind/
```

### Dry Run for Planning
```
# Preview what would be copied
/gh-copy --dry-run torvalds/linux/tools/perf/Documentation/ ./perf-docs-preview/

# Check file count before copying
/gh-copy --dry-run microsoft/TypeScript/doc/handbook/ ./ts-handbook-preview/ | wc -l
```

### Batch Operations with Manifests
Create a file `assets.manifest`:
```
# Format: <repo><TAB><path><TAB><destination>
twitter/twemoji	assets/72x72	./emojis/twitter/
google/material-design-icons	svg/production/btn_google_light_dark_web_ios.svg	./assets/google-login.svg
fortawesome/Font-Awesome	svgs/brands/github-brands.svg	./assets/fontawesome-github.svg
```

Then use:
```
/gh-copy -m assets.manifest
```

## Error Handling Examples

These demonstrate what happens with incorrect usage:

```
# Missing repository
/gh-copy README.md .
Error: Missing repository argument

# Invalid repo format
/gh-copy invalid-format README.md .
Error: Invalid repository format. Use owner/name

# Non-existent file
/gh-copy owner/repo nonexistent.txt .
Error: Failed to fetch file: 404 Not Found

# Missing required tools
/gh-copy owner/repo file.txt .
Error: Required tool 'jq' not found in PATH
```

## Integration with Other Commands

You can chain this with other commands in your workflow:

```
# 1. Get a template
/gh-copy github/gitignore/main/Python.gitignore .gitignore

# 2. Get a license
/gh-copy github/choosealicense.com/licenses/mit.txt LICENSE

# 3. Get a README template
/gh-copy github/devcontainers/template/.devcontainer/README.md .README-template.md

# 4. Initialize project
git init
git add .
git commit -m "Initial commit with template files"
```

## Customization Tips

### Change default destination
Modify the command to default to a specific directory:
```
# Change [dest] default from . to ./downloads/
Copies $1 $2 ./downloads/${3:-$(basename "$2")}
```

### Add preprocessing
Hook into the command to process files after download:
```
# After copying, run formatter
!`gh copy $1 $2 $3 && prettier --write $3`
```

### Add validation
Check dependencies before running:
```
# Verify tools are available
!`command -v gh >/dev/null 2>&1 && command -v jq >/dev/null 2>&1 || { echo "Error: gh and jq required"; exit 1; }`
gh copy $1 $2 $3
```

## Troubleshooting

### Common Issues

**"gh: command not found"**
- Install GitHub CLI: https://cli.github.com/
- Authenticate: `gh auth login`

**"jq: command not found"**
- Install jq: https://stedolan.github.io/jq/download/
- On macOS: `brew install jq`
- On Ubuntu: `sudo apt-get install jq`

**"Failed to open file: No such file or directory"**
- Check repository name format (owner/repo)
- Verify path exists in repository
- Remember paths are case-sensitive
- Try without trailing slash for files, with for directories

**"API rate limit exceeded"**
- Authenticate with `gh auth login` for higher limits
- Wait for rate limit reset
- Consider using `--dry-run` first to test

### Debugging Tips
- Add `set -x` at the top of the command for debugging
- Use `--dry-run` to see what would happen
- Test the underlying `gh copy` command directly first
- Check `$CLAUDE_PLUGIN_ROOT` if using as plugin command