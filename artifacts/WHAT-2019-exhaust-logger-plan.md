# WHAT: Exhaust Logger Primitive Implementation Plan

## 1. Goal
Implement the `ExhaustLogger` primitive within the `drivers/` namespace to enforce the durable serialization of telemetry for transient failures. Update existing CSI guards to utilize this primitive.

## 2. Component Design: `drivers/exhaust_logger.py`
A stateless primitive responsible for capturing and physically persisting exhaust to a JSON/Markdown artifact before a guard raises an exception.

```python
import json
import os
import time

class ExhaustLogger:
    @staticmethod
    def dump_transient_exhaust(guard_name: str, payload: dict, message: str) -> str:
        """
        Serializes the exhaust payload to a physical artifact.
        Returns the absolute pointer path to the artifact.
        """
        timestamp = int(time.time())
        artifact_name = f"exhaust_{guard_name}_{timestamp}.json"
        artifact_path = os.path.join(os.getcwd(), "artifacts", "audit", artifact_name)
        
        os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
        
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
                os.remove(os.path.join(audit_dir, file))
```

## 3. Integration into CSI Guards
CSI Guards (like the Semantic Guard or the Orthogonality Guard) will be refactored.
- On **Pass**: Call `ExhaustLogger.clear_historical_exhaust("GuardName")`
- On **Fail**: Call `ExhaustLogger.dump_transient_exhaust("GuardName", state_dict)` and embed the returned filepath directly into the exception message (the Steering Vector).

Example Steering Vector:
`[🚫 BLOCKED] GuardName failed. Transient exhaust serialized to artifacts/audit/exhaust_GuardName_12345.json. You must read this file to deduce the failure.`

## 4. Test Verification
We will implement `tests/test_exhaust_logger.py` to assert:
- `dump_transient_exhaust` successfully creates the file and returns the correct path.
- `clear_historical_exhaust` purges matching files and ignores others.
- The payload is correctly serialized.
