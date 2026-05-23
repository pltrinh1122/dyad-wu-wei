import json
import os
import re

class ZiranEvent:
    def __init__(self, node_id, event_type, status, kb_target, context=""):
        self.node_id = node_id
        self.event_type = event_type
        self.status = status
        self.kb_target = kb_target
        self.context = context

    def __repr__(self):
        return f"ZiranEvent(node={self.node_id}, status={self.status}, kb={self.kb_target})"

class TelemetryParser:
    """Parses raw telemetry.jsonl into actionable Ziran events."""
    
    KB_PATTERN = re.compile(r'(WHAT-\d{4}|WHY-\d{4}|HOW-\d{4}|SG-\d{4}|TG-\d{4})')

    def __init__(self, ledger_path=None):
        if ledger_path:
            self.ledger_path = ledger_path
        else:
            self.ledger_path = self._get_default_ledger_path()

    def _get_default_ledger_path(self):
        # Anchor to the workspace root
        from drivers import path_resolver
        return path_resolver.resolve_workspace_path("artifacts", "telemetry.jsonl")

    def parse_stream(self):
        """Reads the telemetry log and yields ZiranEvent objects."""
        if not os.path.exists(self.ledger_path):
            return

        with open(self.ledger_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                event = obj.get("event", "").upper()
                stage = obj.get("stage", "").upper()
                metadata = obj.get("metadata", {})
                status = metadata.get("status", "")
                node_id = obj.get("node_id")

                # Turbulent events: errors
                if event == "FINISH" and status == "error":
                    error_msg = str(metadata.get("error", ""))
                    # Extract KB targets from the error string
                    matches = self.KB_PATTERN.findall(error_msg)
                    # Use a set to avoid emitting duplicates for the same log line
                    for kb in set(matches):
                        yield ZiranEvent(
                            node_id=node_id,
                            event_type="AUDIT_HOOK_TRIGGERED" if "REFLECTION BLOCKED" in error_msg else "EXECUTION_CRASH",
                            status="TURBULENT",
                            kb_target=kb,
                            context=error_msg
                        )

                # Laminar events: successful reflect
                if event == "FINISH" and stage == "REFLECT" and status == "success":
                    insights = metadata.get("insights", [])
                    if isinstance(insights, str):
                        # Attempt to parse if it was passed as a string representation of a list
                        try:
                            insights = json.loads(insights)
                        except Exception:
                            insights = [i.strip() for i in insights.split(",") if i.strip()]
                    
                    if not isinstance(insights, list):
                        insights = [insights]

                    for insight in insights:
                        matches = self.KB_PATTERN.findall(insight)
                        for kb in matches:
                            yield ZiranEvent(
                                node_id=node_id,
                                event_type="NODE_COMPLETION",
                                status="LAMINAR",
                                kb_target=kb,
                                context="Successful Node execution governed by insight."
                            )

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else None
    parser = TelemetryParser(path)
    for event in parser.parse_stream():
        print(event)
