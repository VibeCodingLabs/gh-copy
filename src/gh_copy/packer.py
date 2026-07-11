import os
from pathlib import Path
import pathspec
import tiktoken
import tempfile
import urllib.request
import zipfile
import re
import shutil


def is_binary(file_path: Path) -> bool:
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        return True

def generate_tree(dir_path: Path, ignore_spec, is_included_func=None, prefix=""):
    tree_lines = []
    try:
        entries = sorted(list(dir_path.iterdir()), key=lambda e: (e.is_file(), e.name))
    except PermissionError:
        return ""

    valid_entries = []
    for entry in entries:
        if entry.name == ".git":
            continue
        rel_path = str(entry.relative_to(ignore_spec.root))
        if entry.is_dir():
            rel_path += "/"
        if ignore_spec.match_file(rel_path):
            continue
        if entry.is_file() and is_included_func and not is_included_func(rel_path):
            continue
        valid_entries.append(entry)

    for i, entry in enumerate(valid_entries):
        connector = "└── " if i == len(valid_entries) - 1 else "├── "
        tree_lines.append(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            extension = "    " if i == len(valid_entries) - 1 else "│   "
            tree_lines.append(generate_tree(entry, ignore_spec, is_included_func, prefix + extension))
            
    return "\n".join(filter(None, tree_lines))

class IgnoreSpec:
    def __init__(self, root: Path):
        self.root = root
        self.spec = self._load_gitignore()

    def _load_gitignore(self):
        gitignore_path = self.root / ".gitignore"
        customignore_path = self.root / ".gh-copyignore"
        lines = []
        
        for p in (gitignore_path, customignore_path):
            if p.exists():
                with open(p, 'r', encoding='utf-8') as f:
                    lines.extend(f.readlines())
        return pathspec.PathSpec.from_lines('gitwildmatch', lines)

    def match_file(self, path: str) -> bool:
        return self.spec.match_file(path)
def pack_repo(root_dir: Path, style: str = "markdown", template: str = None, remove_empty_lines: bool = False, include_patterns: list = None, exclude_patterns: list = None, mask_secrets: bool = False) -> dict:
    from jinja2 import Template
    
    include_spec = pathspec.PathSpec.from_lines('gitwildmatch', include_patterns) if include_patterns else None
    exclude_spec = pathspec.PathSpec.from_lines('gitwildmatch', exclude_patterns) if exclude_patterns else None
    
    def is_included(rel_p: str) -> bool:
        if exclude_spec and exclude_spec.match_file(rel_p):
            return False
        if include_spec:
            return include_spec.match_file(rel_p)
        return True
        
    root_dir = Path(root_dir).resolve()
    ignore_spec = IgnoreSpec(root_dir)
    
    tree_str = f"{root_dir.name}/\n" + generate_tree(root_dir, ignore_spec, is_included)
    
    files_data = []
    total_size = 0
    dir_count = 0
    file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dir_count += 1
        dirnames[:] = [
            d for d in dirnames 
            if d != ".git" and not ignore_spec.match_file(str(Path(dirpath, d).relative_to(root_dir)) + "/")
        ]
        
        for filename in filenames:
            file_path = Path(dirpath, filename)
            rel_path = str(file_path.relative_to(root_dir))
            
            if ignore_spec.match_file(rel_path):
                continue
                
            if not is_included(rel_path):
                continue
                
            if is_binary(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                if mask_secrets:
                    file_content = re.sub(r'(?i)(api[_-]?key|secret|token|password)[\s:=]+[\'\"]?([a-zA-Z0-9_\-]{16,})[\'\"]?', r'\1 = ***MASKED***', file_content)
                
                if remove_empty_lines:
                    file_content = "\n".join(line for line in file_content.splitlines() if line.strip())
                    
                files_data.append({"path": rel_path, "content": file_content})
                total_size += len(file_content.encode('utf-8'))
                file_count += 1
            except UnicodeDecodeError:
                pass 

    if template:
        jinja_template = Template(template)
        full_content = jinja_template.render(
            repo_name=root_dir.name, 
            tree=tree_str, 
            files=files_data
        )
    else:
        content_lines = []
        if style == "xml":
            content_lines.append("<repository>")
            content_lines.append(f"  <summary>")
            content_lines.append(f"    <files>{file_count}</files>")
            content_lines.append(f"    <directories>{dir_count}</directories>")
            content_lines.append(f"    <size_bytes>{total_size}</size_bytes>")
            content_lines.append(f"  </summary>")
            content_lines.append(f"  <directory_tree>\n{tree_str}\n  </directory_tree>")
            content_lines.append("  <files>")
            for f in files_data:
                content_lines.append(f'    <file path="{f["path"]}">\n{f["content"]}\n    </file>')
            content_lines.append("  </files>")
            content_lines.append("</repository>")
        else:
            content_lines.append(f"# Repository: {root_dir.name}\n")
            content_lines.append(f"## Summary\n- Files: {file_count}\n- Directories: {dir_count}\n- Size: {total_size} bytes\n")
            content_lines.append(f"## Directory Tree\n```\n{tree_str}\n```\n")
            content_lines.append(f"## Files\n")
            for f in files_data:
                content_lines.append(f"================================================")
                content_lines.append(f"File: {f['path']}")
                content_lines.append(f"================================================")
                content_lines.append(f["content"])
                content_lines.append("")
        full_content = "\n".join(content_lines)
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = len(enc.encode(full_content, disallowed_special=()))
    
    return {
        "tree": tree_str,
        "content": full_content,
        "token_count": tokens
    }

def pack_remote_repo(url: str, style: str = "markdown", template: str = None, remove_empty_lines: bool = False, include_patterns: list = None, exclude_patterns: list = None, mask_secrets: bool = False) -> dict:
    # Clean URL
    url = url.rstrip('/')
    if url.startswith("github.com"):
        url = "https://" + url
        
    # Parse owner/repo
    match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
    if not match:
        raise ValueError("Invalid GitHub URL")
        
    owner, repo = match.groups()
    # Remove .git suffix if present
    if repo.endswith(".git"):
        repo = repo[:-4]
        
    zip_url = f"https://github.com/{owner}/{repo}/archive/HEAD.zip"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        zip_path = temp_path / "repo.zip"
        
        req = urllib.request.Request(zip_url, headers={'User-Agent': 'gh-copy-tool'})
        with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_path)
            
        # The zip usually contains a single top-level directory like "repo-HEAD"
        extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
        if not extracted_dirs:
            raise ValueError("No directory found in zip archive")
            
        repo_root = extracted_dirs[0]
        return pack_repo(repo_root, style=style, template=template, remove_empty_lines=remove_empty_lines, include_patterns=include_patterns, exclude_patterns=exclude_patterns, mask_secrets=mask_secrets)
