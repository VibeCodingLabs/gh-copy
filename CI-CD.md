# CI/CD

Continuous Integration should run the `pytest` suite on every PR.
Since `gh-copy` uses `uv` for dependency management, the CI workflow should install `uv`, run `uv sync`, and execute `uv run pytest`.

No automated deployments are currently configured.
