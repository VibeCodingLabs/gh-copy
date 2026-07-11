# TEMPLATES

`gh-copy` supports Jinja2 templates via the `--template` flag.

## Available Variables
- `repo_name`: The name of the repository.
- `tree`: The directory tree string.
- `files`: A list of dictionaries, each containing `path` and `content`.

## Example Template
```jinja2
Please analyze this repository: {{repo_name}}

Directory Structure:
{{tree}}

Files:
{% for f in files %}
### {{f.path}}
{{f.content}}
{% endfor %}
```
