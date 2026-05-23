import os
import json
from kernel.ziran_telemetry_parser import TelemetryParser

# Create a mock telemetry file
mock_file = "/tmp/mock_telemetry.jsonl"
with open(mock_file, "w") as f:
    # Turbulent event
    f.write(json.dumps({
        "timestamp": "2026-05-22T21:44:48Z",
        "node_id": "759",
        "stage": "ACT",
        "event": "FINISH",
        "metadata": {
            "status": "error",
            "error": "REFLECTION BLOCKED: Node 759 experienced execution failures. Under SG-0005 (TG-0005-04)"
        }
    }) + "\n")
    
    # Laminar event
    f.write(json.dumps({
        "timestamp": "2026-05-22T21:45:04Z",
        "node_id": "759",
        "stage": "REFLECT",
        "event": "FINISH",
        "metadata": {
            "status": "success",
            "insights": "WHAT-0077, WHY-0076"
        }
    }) + "\n")

# Run parser
parser = TelemetryParser(mock_file)
events = list(parser.parse_stream())

for event in events:
    print(f"Node: {event.node_id}, Status: {event.status}, Target: {event.kb_target}")

if len(events) == 3:
    print("SUCCESS: Parser extracted exactly 3 events (1 turbulent, 2 laminar).")
else:
    print(f"FAILED: Expected 3 events, got {len(events)}")
