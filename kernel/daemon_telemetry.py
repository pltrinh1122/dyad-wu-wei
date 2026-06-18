import json
import os
import subprocess
import uuid
import functools
from datetime import datetime, timezone, timedelta
from drivers.file_locker import lock_file

class SynthesisEngine:
    """Processes raw telemetry events into actionable metrics."""
    
    def __init__(self, events):
        self.events = events
        self.thresholds = {
            "SENSE": timedelta(minutes=5),
            "PLAN": timedelta(hours=1),
            "ACT": timedelta(hours=4),
            "REFLECT": timedelta(minutes=15)
        }

    def _parse_ts(self, ts_str):
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

    def calculate_metrics(self, level="stage"):
        """Groups events by the specified level and calculates durations."""
        metrics = {}
        
        for event in self.events:
            node_id = event.get("node_id")
            stage = event.get("stage")
            domain = event.get("domain")
            component = event.get("component")
            execution_id = event.get("execution_id")
            
            if level == "node":
                key = (node_id,)
            elif level == "domain":
                key = (node_id, stage, domain)
            elif level == "component":
                key = (node_id, stage, domain, component)
            elif level == "execution":
                key = (node_id, stage, domain, component, execution_id)
            else:
                key = (node_id, stage)
                
            if key not in metrics:
                metrics[key] = {"start": None, "finish": None, "events": []}
            
            metrics[key]["events"].append(event)
            ts = self._parse_ts(event["timestamp"])
            
            if event["event"] == "START":
                if metrics[key]["start"] is None or ts < metrics[key]["start"]:
                    metrics[key]["start"] = ts
            elif event["event"] == "FINISH":
                if metrics[key]["finish"] is None or ts > metrics[key]["finish"]:
                    metrics[key]["finish"] = ts

        results = []
        for key, data in metrics.items():
            node_id = key[0]
            stage = key[1] if len(key) > 1 else "OVERALL"
            domain = key[2] if len(key) > 2 else None
            component = key[3] if len(key) > 3 else None
            execution_id = key[4] if len(key) > 4 else None
            
            if data["start"] and data["finish"]:
                duration = data["finish"] - data["start"]
                threshold = self.thresholds.get(stage, timedelta(hours=24))
                is_bottleneck = duration > threshold
                
                results.append({
                    "node_id": node_id,
                    "stage": stage,
                    "domain": domain,
                    "component": component,
                    "execution_id": execution_id,
                    "duration": duration,
                    "is_bottleneck": is_bottleneck,
                    "threshold": threshold,
                    "level": level
                })
        
        return results

class TelemetryDaemon:
    """Manages the lifecycle and orchestration of the Telemetry primitive."""
    
    def __init__(self, ledger_path=None):
        if ledger_path:
            self.ledger_path = ledger_path
        elif os.environ.get("SPAO_TELEMETRY_LEDGER"):
            self.ledger_path = os.environ.get("SPAO_TELEMETRY_LEDGER")
        elif (os.environ.get("ANTIGRAVITY_RUNNING_TESTS") or os.environ.get("GITHUB_ACTIONS")) and not os.environ.get("SPAO_TELEMETRY_NO_TEST_SAFETY"):
            # Use a temporary file in /tmp/ during tests to avoid polluting artifacts
            # and to avoid git calls that break mocked subprocess tests.
            self.ledger_path = "/tmp/antigravity_telemetry_test.jsonl"
        else:
            self.ledger_path = self._get_default_ledger_path()

    def _get_default_ledger_path(self):
        """Anchors the default ledger path to the git repository root."""
        from drivers import path_resolver
        persona_id = os.environ.get("SPAO_PERSONA_ID")
        if persona_id:
            return path_resolver.resolve_workspace_path("artifacts", f"telemetry_{persona_id}.jsonl")
        return path_resolver.resolve_workspace_path("artifacts", "telemetry.jsonl")

    def log_event(self, stage, event, node_id=None, path_id=None, domain=None, component=None, execution_id=None, metadata=None):
        """Records an observation point to the telemetry ledger."""
        # Skip telemetry IO in unit tests to avoid side effects and broken mocks,
        # UNLESS we are explicitly testing telemetry (ledger_path is /tmp/ or explicitly set).
        if os.environ.get("ANTIGRAVITY_RUNNING_TESTS") or os.environ.get("GITHUB_ACTIONS"):
            if not os.environ.get("SPAO_TELEMETRY_LEDGER") and "antigravity_telemetry_test.jsonl" in self.ledger_path:
                return

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "node_id": node_id,
            "path_id": path_id,
            "domain": domain,
            "component": component,
            "execution_id": execution_id,
            "stage": stage.upper(),
            "event": event.upper(),
            "metadata": metadata or {}
        }
        
        # Ensure the directory exists
        dir_name = os.path.dirname(self.ledger_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        with lock_file(self.ledger_path):
            with open(self.ledger_path, "a") as f:
                f.write(json.dumps(entry) + "\n")

    def generate_report(self, level="stage"):
        """Synthesizes the ledger into a health report."""
        if not os.path.exists(self.ledger_path):
            return f"No telemetry data available at {self.ledger_path}."
            
        with open(self.ledger_path, "r") as f:
            events = [json.loads(line) for line in f]
            
        engine = SynthesisEngine(events)
        metrics = engine.calculate_metrics(level=level)
        
        report = ["# SPAO Operational Health Report", ""]
        report.append(f"Source: {self.ledger_path}")
        report.append(f"Aggregation Level: {level.upper()}")
        report.append(f"Total Observation Points: {len(events)}")
        report.append("")
        
        if not metrics:
            report.append("No completed phases found to calculate durations.")
            return "\n".join(report)

        if level == "node":
            report.append("| Node | Duration | Status |")
            report.append("| :--- | :--- | :--- |")
        elif level == "stage":
            report.append("| Node | Stage | Duration | Status |")
            report.append("| :--- | :--- | :--- | :--- |")
        elif level == "domain":
            report.append("| Node | Stage | Domain | Duration | Status |")
            report.append("| :--- | :--- | :--- | :--- | :--- |")
        elif level == "component":
            report.append("| Node | Stage | Domain | Component | Duration | Status |")
            report.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        elif level == "execution":
            report.append("| Node | Stage | Domain | Component | Execution ID | Duration | Status |")
            report.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        
        bottlenecks = []
        for m in metrics:
            status = "✅ Healthy"
            if m["is_bottleneck"]:
                status = "⚠️ BOTTLENECK"
                bottlenecks.append(m)
            
            node_display = f"#{m['node_id']}" if m['node_id'] else "Global"
            
            if level == "node":
                report.append(f"| {node_display} | {m['duration']} | {status} |")
            elif level == "stage":
                report.append(f"| {node_display} | {m['stage']} | {m['duration']} | {status} |")
            elif level == "domain":
                report.append(f"| {node_display} | {m['stage']} | {m['domain']} | {m['duration']} | {status} |")
            elif level == "component":
                report.append(f"| {node_display} | {m['stage']} | {m['domain']} | {m['component']} | {m['duration']} | {status} |")
            elif level == "execution":
                report.append(f"| {node_display} | {m['stage']} | {m['domain']} | {m['component']} | {m['execution_id']} | {m['duration']} | {status} |")
            
        if bottlenecks:
            report.append("\n## 🚨 Bottleneck Alerts")
            for b in bottlenecks:
                node_display = f"Node #{b['node_id']}" if b['node_id'] else "Global system"
                report.append(f"- **{node_display}** stalled in **{b['stage']}** phase for {b['duration']} (Threshold: {b['threshold']})")
        
        return "\n".join(report)

def record_execution(stage=None):
    """Decorator to automatically log telemetry for a function execution."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            daemon = TelemetryDaemon()
            execution_id = str(uuid.uuid4())
            
            # Infer domain and component from module name
            module_parts = func.__module__.split('.')
            domain = module_parts[0] if module_parts else "unknown"
            component = module_parts[-1] if len(module_parts) > 1 else "root"
            
            # Attempt to extract node_id from first argument if it's a Node object
            node_id = None
            if args and hasattr(args[0], 'issue_id'):
                node_id = getattr(args[0], 'issue_id')
            
            daemon.log_event(
                stage=stage or "ACT",
                event="START",
                node_id=node_id,
                domain=domain,
                component=component,
                execution_id=execution_id,
                metadata={"function": func.__name__}
            )
            
            start_time = datetime.now(timezone.utc)
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                
                metadata = {
                    "function": func.__name__,
                    "duration_sec": duration,
                    "status": "success"
                }
                if "insights" in kwargs and kwargs["insights"]:
                    metadata["insights"] = kwargs["insights"]
                daemon.log_event(
                    stage=stage or "ACT",
                    event="FINISH",
                    node_id=node_id,
                    domain=domain,
                    component=component,
                    execution_id=execution_id,
                    metadata=metadata
                )
                return result
            except Exception as e:
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                daemon.log_event(
                    stage=stage or "ACT",
                    event="FINISH",
                    node_id=node_id,
                    domain=domain,
                    component=component,
                    execution_id=execution_id,
                    metadata={
                        "function": func.__name__,
                        "duration_sec": duration,
                        "status": "error",
                        "error": str(e)
                    }
                )
                raise
        return wrapper
    return decorator


@record_execution(stage="system")
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Telemetry Daemon CLI")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    parser_report = subparsers.add_parser("report", help="Generate a health report")
    parser_report.add_argument("--level", choices=["node", "stage", "domain", "component", "execution"], default="stage", help="Aggregation level")
    
    parser_log = subparsers.add_parser("log", help="Log a telemetry event")
    parser_log.add_argument("stage", help="Stage (e.g., ACT, SENSE)")
    parser_log.add_argument("event", help="Event (e.g., START, FINISH)")
    parser_log.add_argument("--node", help="Node ID")
    parser_log.add_argument("--domain", help="Domain")
    parser_log.add_argument("--component", help="Component")
    parser_log.add_argument("--metadata", help="JSON metadata string")
    
    args = parser.parse_args()
    daemon = TelemetryDaemon()
    
    if args.subcommand == "report":
        print(daemon.generate_report(level=args.level))
    elif args.subcommand == "log":
        metadata = json.loads(args.metadata) if args.metadata else {}
        daemon.log_event(
            stage=args.stage,
            event=args.event,
            node_id=args.node,
            domain=args.domain,
            component=args.component,
            metadata=metadata
        )

if __name__ == "__main__":
    main()
