import os
from pathlib import Path
from gh_copy.packer import pack_repo, is_binary

def test_is_binary(tmp_path):
    text_file = tmp_path / "text.txt"
    text_file.write_text("hello world")
    assert not is_binary(text_file)
    
    bin_file = tmp_path / "bin.dat"
    bin_file.write_bytes(b"\x00\x01\x02\x03\x04\x05")
    assert is_binary(bin_file)

def test_pack_repo_basic(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')\n")
    (tmp_path / "README.md").write_text("# Project\n")
    
    result = pack_repo(tmp_path)
    assert "main.py" in result["tree"]
    assert "README.md" in result["tree"]
    assert "print('hello')" in result["content"]
    assert "Files: 2" in result["content"]

def test_pack_repo_ignores_git(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("secret")
    (tmp_path / "main.py").write_text("code")
    
    result = pack_repo(tmp_path)
    assert ".git" not in result["tree"]
    assert "secret" not in result["content"]
    assert "code" in result["content"]

def test_pack_repo_gitignore(tmp_path):
    (tmp_path / ".gitignore").write_text("ignored_dir/\n*.log\n")
    (tmp_path / "ignored_dir").mkdir()
    (tmp_path / "ignored_dir" / "secret.txt").write_text("secret")
    (tmp_path / "app.log").write_text("log data")
    (tmp_path / "main.py").write_text("code")
    
    result = pack_repo(tmp_path)
    assert "ignored_dir" not in result["tree"]
    assert "app.log" not in result["tree"]
    assert "main.py" in result["tree"]
    assert "code" in result["content"]
    assert "secret" not in result["content"]
    assert "log data" not in result["content"]
    assert "- Files: 2" in result["content"]
def test_pack_repo_xml_style(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')\n")
    
    result = pack_repo(tmp_path, style="xml")
    assert "<repository>" in result["content"]
    assert "<summary>" in result["content"]
    assert "<files>1</files>" in result["content"]
    assert "<directories>2</directories>" in result["content"]
    assert "<directory_tree>" in result["content"]
    assert '<file path="src/main.py">' in result["content"]
    assert "print('hello')" in result["content"]
    assert "</repository>" in result["content"]

from unittest.mock import patch
from gh_copy.packer import pack_remote_repo

@patch('gh_copy.packer.urllib.request.urlopen')
@patch('gh_copy.packer.zipfile.ZipFile')
@patch('gh_copy.packer.shutil.copyfileobj')
def test_pack_remote_repo(mock_copy, mock_zip, mock_urlopen, tmp_path):
    # We just need to mock the extraction to create a dummy directory
    def mock_extractall(path):
        dummy_dir = Path(path) / "dummy-repo-HEAD"
        dummy_dir.mkdir()
        (dummy_dir / "remote.py").write_text("print('remote')")
        
    mock_zip.return_value.__enter__.return_value.extractall.side_effect = mock_extractall
    
    result = pack_remote_repo("https://github.com/owner/repo", style="markdown")
    
    assert "remote.py" in result["tree"]
    assert "print('remote')" in result["content"]

def test_pack_repo_template(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')\n")
    
    template_str = "REPO: {{repo_name}}\nTREE:\n{{tree}}\nFILES:\n{% for f in files %}{{f.path}}->{{f.content}}{% endfor %}"
    result = pack_repo(tmp_path, template=template_str)
    
    assert f"REPO: {tmp_path.name}" in result["content"]
    assert "main.py" in result["content"]
    assert "src/main.py->print('hello')" in result["content"]

def test_pack_repo_custom_ignore(tmp_path):
    (tmp_path / ".gh-copyignore").write_text("custom_secret.txt\n")
    (tmp_path / "custom_secret.txt").write_text("top_secret_data")
    (tmp_path / "main.py").write_text("code")
    
    result = pack_repo(tmp_path)
    assert "custom_secret.txt" not in result["tree"]
    assert "top_secret_data" not in result["content"]
    assert "main.py" in result["tree"]

def test_pack_repo_remove_empty_lines(tmp_path):
    (tmp_path / "main.py").write_text("print('hello')\n\n\nprint('world')\n")
    
    result = pack_repo(tmp_path, remove_empty_lines=True)
    assert "print('hello')\nprint('world')" in result["content"]
    assert "print('hello')\n\n\nprint('world')" not in result["content"]

def test_pack_repo_include_exclude(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')\n")
    (tmp_path / "src" / "test.py").write_text("print('test')\n")
    (tmp_path / "README.md").write_text("readme")
    
    # Test include only
    result1 = pack_repo(tmp_path, include_patterns=["*.py"])
    assert "main.py" in result1["content"]
    assert "test.py" in result1["content"]
    assert "README.md" not in result1["content"]
    
    # Test exclude only
    result2 = pack_repo(tmp_path, exclude_patterns=["test.py"])
    assert "main.py" in result2["content"]
    assert "test.py" not in result2["content"]
    assert "README.md" in result2["content"]
    
    # Test both include and exclude
    result3 = pack_repo(tmp_path, include_patterns=["*.py"], exclude_patterns=["test.py"])
    assert "main.py" in result3["content"]
    assert "test.py" not in result3["content"]
    assert "README.md" not in result3["content"]

def test_pack_repo_mask_secrets(tmp_path):
    (tmp_path / "main.py").write_text("API_KEY = 'sk-1234567890abcdef1234567890abcdef'\nprint('hello')\n")
    
    result = pack_repo(tmp_path, mask_secrets=True)
    assert "API_KEY = ***MASKED***" in result["content"]
    assert "sk-1234567890" not in result["content"]
    assert "print('hello')" in result["content"]
