# OVERVIEW.md

## What is gh-copy?
`gh-copy` is a powerful, dual-purpose CLI tool designed for the AI era. It transforms any codebase (local or remote) into a single, highly-optimized, token-counted file designed specifically to be fed into Large Language Models (LLMs) like Claude, GPT-4, and Gemini. 

It replicates and improves upon the core functionalities of tools like `repomix`, `gitingest`, and `code2prompt`.

## Major Features
1. **Repository Packing**: Compresses entire directories into a single file.
2. **AI-Optimized Output**: Generates a file containing the directory tree structure followed by file contents clearly separated by delimiters.
3. **Smart Ignoring**: Automatically respects `.gitignore` rules and strips out common binary files (images, compiled assets) to save token space.
4. **Token Counting**: Integrates `tiktoken` to give you an exact count (using `cl100k_base`) of how large your prompt will be before you send it to an LLM.
5. **Clone-less Copying**: (Legacy) Ability to copy specific files/folders directly from GitHub without running `git clone`.

## Prerequisites
- Python 3.9+
- `uv` (recommended) or `pip`
- GitHub CLI (`gh`) if using the remote fetch features.

## Installation
```bash
# Clone the repository
git clone https://github.com/VibeCodingLabs/gh-copy.git
cd gh-copy

# Install using uv
uv venv
uv pip install -e .

# Or install using pip
pip install -e .
```
