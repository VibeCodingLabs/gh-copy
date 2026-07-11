# API-REFERENCE.md

## Python API Reference

You can use `gh-copy` as a Python library within your own scripts to dynamically generate prompt context.

### Module: `gh_copy.packer`

#### `pack_repo(root_dir: pathlib.Path) -> dict`
The primary function for packing a repository.

**Arguments:**
- `root_dir` (Path): An absolute or relative `pathlib.Path` pointing to the root of the directory you wish to pack.

**Returns:**
A dictionary containing:
- `tree` (str): The visual string representation of the directory tree.
- `content` (str): The full packed file content, including the tree and all file contents separated by headers.
- `token_count` (int): The estimated number of tokens in the `content` string, calculated using the `cl100k_base` encoding.

#### `is_binary(file_path: pathlib.Path) -> bool`
Utility function to check if a file is binary.

**Arguments:**
- `file_path` (Path): The path to the file.

**Returns:**
- `True` if the file contains null bytes in its first 1024 bytes, `False` otherwise.
