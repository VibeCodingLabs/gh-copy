# USAGE.md

## Basic Usage

The primary function of `gh-copy` is to pack a local repository into a single file that can be uploaded to an AI chat interface (like ChatGPT or Claude).

### Packing a Local Repository

Navigate to the project you want to pack, or provide the path:

```bash
gh-copy pack /path/to/your/project
```

By default, this will create a file named `repacked_repo.txt` in your current directory.

### Specifying an Output File

Use the `-o` or `--output` flag to specify where the packed file should be saved:

```bash
gh-copy pack ./my-web-app -o prompt_context.txt
```

### What gets ignored?
- The `.git` directory is always ignored.
- Any files matching patterns in your `.gitignore` file are automatically skipped.
- Binary files (like `.png`, `.jpg`, `.exe`, `.dll`) are detected and skipped to save tokens and prevent garbage text in the output.

## Output Format
The resulting file will contain:
1. The repository name.
2. A visual tree representation of the directory structure.
3. The contents of each file, clearly separated by headers.
4. (In the console) The total token count of the generated file.
