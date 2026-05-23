import os
import yaml

def get_ledger_path(repo_root: str) -> str:
    """Returns the absolute path to the kb_ledger.yml artifact."""
    return os.path.join(repo_root, "artifacts", "kb_ledger.yml")

def read_ledger(repo_root: str) -> dict:
    """
    Safely loads the central KB ledger. Returns an empty structure if it doesn't exist.
    """
    ledger_path = get_ledger_path(repo_root)
    if not os.path.exists(ledger_path):
        return {"primitives": {}}
    
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        if not data or not isinstance(data, dict) or "primitives" not in data:
            return {"primitives": {}}
        
        # Ensure primitives is a dict
        if not isinstance(data.get("primitives"), dict):
            data["primitives"] = {}
            
        return data
    except Exception as e:
        print(f"Warning: Failed to read kb_ledger.yml: {e}")
        return {"primitives": {}}

def write_ledger(repo_root: str, data: dict) -> None:
    """
    Writes the provided data dictionary to the central KB ledger.
    """
    ledger_path = get_ledger_path(repo_root)
    
    # Ensure artifacts directory exists
    os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
    
    with open(ledger_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)

def mutate_primitive(repo_root: str, primitive_id: str, state: str, gradient: str, confidence: float) -> None:
    """
    Mutates the gradient metadata for a specific knowledge primitive.
    Reads the current ledger, updates the specific ID, and writes it back.
    """
    data = read_ledger(repo_root)
    
    data["primitives"][primitive_id] = {
        "state": state,
        "gradient": gradient,
        "confidence": round(float(confidence), 3)
    }
    
    write_ledger(repo_root, data)
