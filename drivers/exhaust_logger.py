import json
import os
import time
from typing import Dict, Any

class ExhaustLogger:
    @staticmethod
    def dump_transient_exhaust(guard_name: str, payload: dict, message: str) -> str:
        """
        Serializes the exhaust payload to a physical artifact.
        Returns the absolute pointer path to the artifact.
        """
        timestamp = int(time.time())
        artifact_name = f"exhaust_{guard_name}_{timestamp}.json"
        
        # We always dump inside the active workspace's artifacts/audit/ directory
        audit_dir = os.path.join(os.getcwd(), "artifacts", "audit")
        os.makedirs(audit_dir, exist_ok=True)
        
        artifact_path = os.path.join(audit_dir, artifact_name)
        
        with open(artifact_path, "w") as f:
            json.dump({
                "guard": guard_name,
                "message": message,
                "payload": payload,
                "timestamp": timestamp
            }, f, indent=2)
            
        return artifact_path
        
    @staticmethod
    def clear_historical_exhaust(guard_name: str):
        """
        Purges old exhaust logs for a specific guard to prevent contamination.
        """
        audit_dir = os.path.join(os.getcwd(), "artifacts", "audit")
        if not os.path.exists(audit_dir):
            return
            
        for file in os.listdir(audit_dir):
            if file.startswith(f"exhaust_{guard_name}_") and file.endswith(".json"):
                try:
                    os.remove(os.path.join(audit_dir, file))
                except OSError:
                    pass  # Graceful fallback if file locked or removed concurrently
