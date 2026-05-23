import os
import yaml
import json
from collections import defaultdict
from typing import Dict, List

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

def parse_telemetry(repo_root: str, max_events: int = 1000) -> Dict[str, List[Dict]]:
    """
    Reads the trailing telemetry events from artifacts/telemetry/events.jsonl.
    Groups them by kb_target.
    Gracefully handles missing telemetry directory or file.
    """
    telemetry_path = os.path.join(repo_root, "artifacts", "telemetry", "events.jsonl")
    grouped_events = defaultdict(list)
    
    if not os.path.exists(telemetry_path):
        return dict(grouped_events)
        
    try:
        with open(telemetry_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        recent_lines = lines[-max_events:] if max_events > 0 else lines
        
        for line in recent_lines:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                kb_target = event.get("kb_target")
                if kb_target:
                    grouped_events[kb_target].append(event)
            except json.JSONDecodeError:
                continue
    except Exception as e:
        print(f"Warning: Failed to parse telemetry: {e}")
        
    return dict(grouped_events)

def calculate_gradient(laminar_count: int, turbulent_count: int) -> float:
    """
    Implements the Daoist formula: delta = S / (S + T)
    where S is Laminar completions and T is Turbulent events.
    """
    total = laminar_count + turbulent_count
    if total == 0:
        return 1.0
    return float(laminar_count) / float(total)

def evaluate_and_apply_gradients(repo_root: str) -> None:
    """
    Retrieves grouped events, calculates gradients, and mutates the ledger.
    - Promotes to Laminar if delta > 0.9.
    - Demotes to Turbulent if delta < 0.6.
    """
    grouped_events = parse_telemetry(repo_root)
    if not grouped_events:
        return
        
    current_ledger = read_ledger(repo_root)
    
    for kb_target, events in grouped_events.items():
        laminar_count = sum(1 for e in events if str(e.get("status")).upper() == "LAMINAR")
        turbulent_count = sum(1 for e in events if str(e.get("status")).upper() == "TURBULENT")
        
        total_events = laminar_count + turbulent_count
        if total_events == 0:
            continue
            
        delta = calculate_gradient(laminar_count, turbulent_count)
        confidence = min(total_events / 10.0, 1.0)
        
        new_gradient = None
        if delta > 0.9:
            new_gradient = "Laminar"
        elif delta < 0.6:
            new_gradient = "Turbulent"
            
        if new_gradient:
            existing_prim = current_ledger.get("primitives", {}).get(kb_target, {})
            current_state = existing_prim.get("state", "Active")
            mutate_primitive(repo_root, kb_target, current_state, new_gradient, confidence)
