# AGENTS.md

## Context for AI Agents
If you are an AI agent operating within or upon this repository, adhere to the following guidelines:

1. **Architecture**: This is a Python-based CLI tool utilizing `click`. The core logic resides in `src/gh_copy/packer.py`.
2. **Testing**: All new features must be accompanied by `pytest` tests located in the `tests/` directory. Run tests via `uv run pytest`.
3. **Purpose**: This tool is an amalgam of `code2prompt`, `gitingest`, and `repomix`. Its goal is to create highly optimized context files for LLMs.
4. **Dependencies**: Managed via `pyproject.toml`. Core dependencies are `pathspec` (for gitignore parsing), `tiktoken` (for LLM token counting), `click` (CLI framework), and `rich` (terminal formatting).

When asked to extend this tool, ensure you maintain the clear separation between the CLI interface (`cli.py`) and the core packing logic (`packer.py`). Always update `CLI-REFERENCE.md` when adding new commands.
