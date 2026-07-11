# TESTS

Testing is handled via `pytest`. The suite verifies:
- Pathspec matching and ignore rules.
- Output formatting (XML/Markdown).
- CLI invocation and argument parsing.
- Remote repository ZIP fetching and extraction (mocked).
- Existence of Definition-of-Done documentation.

To run:
```bash
uv run pytest tests/ -v
```
