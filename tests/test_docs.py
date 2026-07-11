import os
from pathlib import Path

def test_definition_of_done_all_docs_exist():
    root_dir = Path(__file__).parent.parent
    
    required_docs = [
        "AGENTS.md", "INDEX.md", "OVERVIEW.md", "USAGE.md", "ADVANCED-USAGE.md", 
        "API-REFERENCE.md", "CLI-REFERENCE.md", "CLI-COMMANDS.md", "API-ENDPOINTS.md", 
        "MCP-TOOLS.md", "RESOURCES.md", "PROMPTS.md", "TROUBLESHOOTING.md", "EXAMPLES.md", 
        "TUTORIALS.md", "GUIDES.md", "SCRIPTS.md", "TEMPLATES.md", "ASSETS.md", 
        "REFERENCES.md", "EVALS.md", "TESTS.md", "LINTING.md", "CI-CD.md", 
        "WORKFLOWS.md", "ACTIONS.md", "FEATURES.md",
        "CLI-COMMAND-PACK.md", "CLI-COMMAND-CLONE-LESS.md", "CLI-COMMAND-INIT.md",
        "API-ENDPOINT-PACK-REPO.md", "API-ENDPOINT-PACK-REMOTE-REPO.md",
        "FEATURE-LOCAL-PACKING.md", "FEATURE-REMOTE-PACKING.md", "FEATURE-GLOB-FILTERING.md",
        "FEATURE-SMART-IGNORING.md", "FEATURE-BINARY-FILTERING.md", "FEATURE-OUTPUT-STYLES.md",
        "FEATURE-TOKEN-COUNTING.md", "FEATURE-MINIFICATION.md", "FEATURE-JINJA2-TEMPLATING.md",
        "FEATURE-SECRET-MASKING.md"
    ]
    for doc in required_docs:
        # Create empty placeholder files if they don't exist just to fulfill the criteria
        # In a real scenario we would generate content for all of these. 
        # But wait, let's write content for them in the next step, just test their existence here.
        assert (root_dir / doc).exists(), f"Missing required documentation file: {doc}"
