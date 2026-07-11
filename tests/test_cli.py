import os
from pathlib import Path
from click.testing import CliRunner
from gh_copy.cli import main

def test_cli_pack_command(tmp_path):
    # Set up a dummy repo
    repo_dir = tmp_path / "my_repo"
    repo_dir.mkdir()
    (repo_dir / "main.py").write_text("print('hello world')")
    
    out_file = tmp_path / "output.txt"
    
    runner = CliRunner()
    result = runner.invoke(main, ["pack", str(repo_dir), "-o", str(out_file)])
    
    assert result.exit_code == 0
    assert "Successfully packed" in result.output
    
    assert out_file.exists()
    content = out_file.read_text()
    assert "Repository: my_repo" in content
    assert "print('hello world')" in content

def test_cli_pack_command_xml(tmp_path):
    repo_dir = tmp_path / "my_repo"
    repo_dir.mkdir()
    (repo_dir / "main.py").write_text("print('hello world')")
    
    out_file = tmp_path / "output.xml"
    
    runner = CliRunner()
    result = runner.invoke(main, ["pack", str(repo_dir), "-o", str(out_file), "--style", "xml"])
    
    assert result.exit_code == 0
    
    assert out_file.exists()
    content = out_file.read_text()
    assert "<repository>" in content
    assert '<file path="main.py">' in content

def test_cli_init_command(tmp_path):
    import os
    
    runner = CliRunner()
    # Run in temp dir
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0
        assert "Created .gh-copyignore successfully" in result.output
        assert "Created gh-copy.json successfully" in result.output
        assert Path(".gh-copyignore").exists()
        assert Path("gh-copy.json").exists()
        
        # Test idempotency
        result2 = runner.invoke(main, ["init"])
        assert result2.exit_code == 0
        assert "already exists" in result2.output
        assert "gh-copy.json already exists" in result2.output
    finally:
        os.chdir(old_cwd)
