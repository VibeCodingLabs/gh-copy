#!/usr/bin/env bash
set -Eeuo pipefail

# pull-mcp.sh
# Selectively acquire likely MCP implementation/docs files from a GitHub repository.
#
# Usage:
#   ./pull-mcp.sh OWNER/REPO [REF] [DEST]
#
# Examples:
#   ./pull-mcp.sh modelcontextprotocol/servers
#   ./pull-mcp.sh OWNER/REPO v1.2.3 ./sources/provider

repo="${1:?usage: $0 OWNER/REPO [REF] [DEST]}"
ref="${2:-}"
dest="${3:-./sources/${repo//\//__}}"

command -v gh >/dev/null || {
  printf 'error: GitHub CLI (gh) is required\n' >&2
  exit 127
}

if ! gh extension list | grep -Fq 'VibeCodingLabs/gh-copy'; then
  gh extension install VibeCodingLabs/gh-copy
fi

mkdir -p "$dest"

paths=(
  README.md
  LICENSE
  SECURITY.md
  AGENTS.md
  package.json
  pnpm-lock.yaml
  pyproject.toml
  uv.lock
  requirements.txt
  go.mod
  go.sum
  Cargo.toml
  src
  server
  mcp
  tools
  schemas
  openapi.json
  openapi.yaml
  examples
  tests
  docs
)

copy_one() {
  local path="$1"
  local target="$dest/$path"
  mkdir -p "$(dirname "$target")"

  if [[ -n "$ref" ]]; then
    gh copy -r "$ref" "$repo" "$path" "$target"
  else
    gh copy "$repo" "$path" "$target"
  fi
}

printf 'repo: %s\nref: %s\ndest: %s\n' "$repo" "${ref:-default}" "$dest"

for path in "${paths[@]}"; do
  printf '\n==> %s\n' "$path"
  if ! copy_one "$path"; then
    printf 'skip: %s not copied\n' "$path" >&2
  fi
done

printf '\nDone. Review licenses, provenance, secrets, and generated files in:\n%s\n' "$dest"
