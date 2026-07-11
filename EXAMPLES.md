# EXAMPLES

## Basic Local Pack
```bash
gh-copy pack . -o context.txt
```

## Remote Pack with XML Style
```bash
gh-copy pack https://github.com/owner/repo --style xml -o output.xml
```

## Advanced Filtering and Minification
```bash
gh-copy pack . --include "*.py" --exclude "tests/" --remove-empty-lines
```

## Custom Template
```bash
gh-copy pack . --template custom_prompt.jinja
```
