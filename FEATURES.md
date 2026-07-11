# FEATURES

`gh-copy` provides the following core features:
1. **Local & Remote Packing**: Pack local directories or remote GitHub URLs into a single file.
2. **Glob Filtering**: Use `--include` and `--exclude` for granular control.
3. **Smart Ignoring**: Respects `.gitignore` and custom `.gh-copyignore`.
4. **Binary Filtering**: Automatically detects and skips binary files to save tokens.
5. **Output Styles**: Choose between `markdown` and `xml` (Claude-optimized) formats.
6. **Token Counting**: Uses `tiktoken` (cl100k_base) to estimate LLM context window usage.
7. **Minification**: Use `--remove-empty-lines` to compress code vertically.
8. **Jinja2 Templating**: Define custom output structures using `--template`.
