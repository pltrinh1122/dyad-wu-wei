import re

def clean_node_title(title: str) -> str:
    """
    Recursively strips redundant prefixes from a node title to prevent cascading redundancy.
    Removes patterns like:
    - PR for Node 123:
    - Node 123:
    - Activity 123:
    - Activity:
    - Discovery 123:
    - Discovery:
    - Path 123:
    - Path:
    """
    if not title:
        return title
        
    cleaned = str(title).strip()
    # Match any prefix like 'Node:', 'Node 123:', 'PR for Node 123:', etc.
    pattern = re.compile(r"^(PR for Node|Node|Activity|Discovery|Path)(?:\s*\d*)?:\s*", flags=re.IGNORECASE)
    
    while True:
        new_title = pattern.sub("", cleaned).strip()
        if new_title == cleaned:
            break
        cleaned = new_title
        
    return cleaned
