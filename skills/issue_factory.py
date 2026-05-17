import os
from typing import Dict, Any

def render_template(template_name: str, kwargs: Dict[str, Any]) -> str:
    """Reads a markdown template from kb/templates/ and renders it with the provided kwargs.
    
    Raises:
        FileNotFoundError: If the template does not exist.
        KeyError: If the template requires a key that is missing from kwargs.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(repo_dir, "kb", "templates", f"{template_name}.md")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}")
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # Python's str.format() automatically raises KeyError if a placeholder is missing in kwargs
    return template_content.format(**kwargs)

# Note: The actual wrappers calling github_client using these templates can be composed by the orchestrator 
# or wrapped here later, but the foundational templating mechanism belongs here.
