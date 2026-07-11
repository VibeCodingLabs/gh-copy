import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from gh_copy.packer import pack_repo, pack_remote_repo
import tempfile
import urllib.request
import zipfile
import re
import json
import pyperclip

console = Console()

@click.group()
def main():
    """gh-copy: A tool to pack repositories into AI-friendly files and copy without cloning."""
    pass

def is_github_url(url: str) -> bool:
    return url.startswith("https://github.com/") or url.startswith("github.com/")

@main.command()
@click.argument("path")
@click.option("-o", "--output", type=click.Path(), default="repacked_repo.txt", help="Output file path")
@click.option("--style", type=click.Choice(["markdown", "xml"]), default="markdown", help="Output formatting style")
@click.option("--template", type=click.Path(exists=True, dir_okay=False), default=None, help="Custom Jinja2 template file")
@click.option("--remove-empty-lines", is_flag=True, help="Remove empty lines from output to save tokens")
@click.option("--include", multiple=True, help="Include files matching glob patterns (e.g., '*.py')")
@click.option("--exclude", multiple=True, help="Exclude files matching glob patterns (e.g., 'tests/')")
@click.option("--mask-secrets", is_flag=True, help="Mask potential secrets (API keys, passwords)")
@click.option("-c", "--copy", is_flag=True, help="Copy the generated output to the clipboard")
def pack(path, output, style, template, remove_empty_lines, include, exclude, mask_secrets, copy):
    # Load config file if it exists
    config_path = Path("gh-copy.json")
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            # Override defaults if not explicitly passed (click doesn't distinguish well here, 
            # but we can apply config where logical)
            if style == "markdown" and "style" in config:
                style = config["style"]
            if not remove_empty_lines and config.get("remove_empty_lines"):
                remove_empty_lines = True
            if not mask_secrets and config.get("mask_secrets"):
                mask_secrets = True
            if not include and "include" in config:
                include = config["include"]
            if not exclude and "exclude" in config:
                exclude = config["exclude"]
        except json.JSONDecodeError:
            console.print("[yellow]Warning: Could not parse gh-copy.json[/yellow]")
            
    out_path = Path(output)
    
    if is_github_url(path):
        console.print(f"[bold blue]Fetching and packing remote repository at {path} (Style: {style})...[/bold blue]")
        try:
            template_str = Path(template).read_text() if template else None
            result = pack_remote_repo(path, style=style, template=template_str, remove_empty_lines=remove_empty_lines, include_patterns=list(include), exclude_patterns=list(exclude), mask_secrets=mask_secrets)
            
            if copy:
                try:
                    pyperclip.copy(result["content"])
                    console.print("[green]Output copied to clipboard![/green]")
                except Exception as e:
                    console.print(f"[yellow]Could not copy to clipboard: {e}[/yellow]")
            
            console.print(Panel(
                f"[green]Successfully packed remote repository![/green]\n"
                f"Output file: {out_path.absolute()}\n"
                f"Token count (cl100k_base): [bold yellow]{result['token_count']}[/bold yellow]",
                title="Success"
            ))
        except Exception as e:
            console.print(f"[bold red]Error packing remote repository: {e}[/bold red]")
            raise click.Abort()
    else:
        repo_path = Path(path)
        if not repo_path.exists() or not repo_path.is_dir():
            console.print(f"[bold red]Error: Local path {path} does not exist or is not a directory.[/bold red]")
            raise click.Abort()
        template_str = Path(template).read_text() if template else None
        result = pack_repo(repo_path, style=style, template=template_str, remove_empty_lines=remove_empty_lines, include_patterns=list(include), exclude_patterns=list(exclude), mask_secrets=mask_secrets)
        if copy:
            try:
                pyperclip.copy(result["content"])
                console.print("[green]Output copied to clipboard![/green]")
            except Exception as e:
                console.print(f"[yellow]Could not copy to clipboard: {e}[/yellow]")
        out_path.write_text(result["content"])
        
        console.print(Panel(
            f"[green]Successfully packed local repository![/green]\n"
            f"Output file: {out_path.absolute()}\n"
            f"Token count (cl100k_base): [bold yellow]{result['token_count']}[/bold yellow]",
            title="Success"
        ))

@main.command()
@click.argument("repo")
@click.argument("path")
@click.argument("dest", required=False, default=".")
@click.option("-r", "--ref", help="Pin to a branch, tag, or commit SHA")
@click.option("--dry-run", is_flag=True, help="Show planned copies, write nothing")
def clone_less(repo, path, dest, ref, dry_run):
    """Copy files/dirs from a GitHub repo locally without cloning. (Uses gh CLI)"""
    console.print("[yellow]Note: clone-less currently delegates to the original script or requires implementation.[/yellow]")
    pass

@main.command()
def init():
    """Initialize default config and ignore files in the current directory."""
    
    config_path = Path("gh-copy.json")
    if config_path.exists():
        console.print("[yellow]gh-copy.json already exists.[/yellow]")
    else:
        config_data = {
            "style": "markdown",
            "remove_empty_lines": False,
            "mask_secrets": False,
            "include": [],
            "exclude": []
        }
        config_path.write_text(json.dumps(config_data, indent=2))
        console.print("[green]Created gh-copy.json successfully.[/green]")
    ignore_path = Path(".gh-copyignore")
    if ignore_path.exists():
        console.print("[yellow].gh-copyignore already exists.[/yellow]")
        return
        
    default_ignore = """# gh-copy ignore file
# Add patterns to exclude files from being packed

# Common exclusions
node_modules/
__pycache__/
venv/
.venv/
.env
*.lock
*.pdf
*.jpg
*.png
"""
    ignore_path.write_text(default_ignore)
    console.print("[green]Created .gh-copyignore successfully.[/green]")

if __name__ == "__main__":
    main()
