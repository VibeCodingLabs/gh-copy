# TROUBLESHOOTING

- **High Token Counts**: If the output is massive, run `gh-copy init` to create a `.gh-copyignore` and ensure directories like `.venv` or `node_modules` are excluded.
- **Remote Pack Fails**: Ensure the URL is public. Private repositories require the `gh` CLI to be authenticated if using `clone-less`, but `pack <url>` currently fetches the public ZIP archive.
- **Missing Files**: Check your `.gitignore`. If a file is tracked by git but ignored in `.gitignore`, `gh-copy` will skip it. Use `--include` to override.
