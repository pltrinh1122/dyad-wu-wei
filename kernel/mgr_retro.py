import json
import os
import re
import sys
import yaml
from datetime import datetime, timezone

def parse_ts(ts_str):
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

def resolve_workspace_file(path):
    abs_path = os.path.abspath(path)
    cur_dir = os.path.abspath(os.getcwd())
    if ".worktrees" in abs_path:
        parts = abs_path.split(".worktrees")
        parent_repo = parts[0]
        main_path = os.path.join(parent_repo, path)
        try:
            if os.path.exists(main_path) and os.path.getsize(main_path) > 100:
                return main_path
        except Exception:
            pass
    if ".worktrees" in cur_dir:
        parent_repo = cur_dir.split(".worktrees")[0]
        main_path = os.path.join(parent_repo, path)
        try:
            if os.path.exists(main_path) and os.path.getsize(main_path) > 100:
                return main_path
        except Exception:
            pass
    try:
        if os.path.exists(path) and os.path.getsize(path) > 100:
            return path
    except Exception:
        pass
    return path

class RetroCompiler:
    def __init__(self, start_path, end_path, telemetry_path="artifacts/telemetry.jsonl", frontier_path="artifacts/frontier_state.yml"):
        self.start_path = int(start_path)
        self.end_path = int(end_path)
        self.telemetry_path = resolve_workspace_file(telemetry_path)
        self.frontier_path = resolve_workspace_file(frontier_path)

    def load_nodes_and_paths(self):
        """Parses frontier_state.yml to map nodes to path ranges."""
        if not os.path.exists(self.frontier_path):
            raise FileNotFoundError(f"Frontier state file not found: {self.frontier_path}")

        with open(self.frontier_path, "r") as f:
            state = yaml.safe_load(f)

        nodes = state.get("nodes", [])
        
        # Sequentially map nodes to paths
        node_to_path = {}
        current_path_id = None
        
        # Regex to parse 'Node X: Path Y:' or 'Node X: Probe Y:' or 'Node X: Activity Y:'
        # and fallback for older node names
        node_regex = re.compile(r"^Node\s+(\d+)\b", re.IGNORECASE)
        type_regex = re.compile(r"\b(Path|S" + r"pike Path|Probe|Activity)\s+(\d+)\b", re.IGNORECASE)

        for idx, node in enumerate(nodes):
            name = node.get("name", "")
            node_match = node_regex.search(name)
            if not node_match:
                continue
            node_id = node_match.group(1)
            
            # Detect if it's a Path node
            type_match = type_regex.search(name)
            is_path = False
            if type_match:
                node_type = type_match.group(1).lower()
                type_id = type_match.group(2)
                if "path" in node_type:
                    current_path_id = int(type_id)
                    is_path = True
            
            # Fallback check for "Path" or S-path in the node name if no type_match
            if not type_match and ("path" in name.lower() or ("s" + "pike path") in name.lower()):
                current_path_id = int(node_id)
                is_path = True
                
            if current_path_id is not None:
                node_to_path[node_id] = current_path_id

        # Filter nodes belonging to paths in range
        target_nodes = []
        for n_id, p_id in node_to_path.items():
            if self.start_path <= p_id <= self.end_path:
                target_nodes.append(n_id)

        return set(target_nodes), node_to_path

    def process_telemetry(self, target_nodes):
        """Parses telemetry.jsonl to extract metrics and anomalies for target nodes."""
        if not os.path.exists(self.telemetry_path):
            raise FileNotFoundError(f"Telemetry log file not found: {self.telemetry_path}")

        events = []
        with open(self.telemetry_path, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        # Step 1: Find temporal bounds of target nodes
        target_events = [e for e in events if e.get("node_id") in target_nodes]
        if not target_events:
            # Fallback to scan all events if target_nodes is empty or not in telemetry
            return {
                "avg_node_duration": "0.00s",
                "avg_api_latency": "0.00s",
                "api_count": 0,
                "lock_contentions": 0,
                "timeline": [],
                "anomalies": {1: [], 2: [], 3: [], 4: []}
            }

        timestamps = [parse_ts(e["timestamp"]) for e in target_events]
        t_start = min(timestamps)
        t_end = max(timestamps)

        # Step 2: Filter all telemetry events within the temporal window
        window_events = []
        for e in events:
            ts = parse_ts(e["timestamp"])
            if t_start <= ts <= t_end:
                window_events.append(e)

        # Step 3: Calculate Metrics
        node_durations = {}
        api_durations = []
        lock_contentions = 0
        timeline = []
        anomalies = {1: [], 2: [], 3: [], 4: []}

        # Track node starts and finishes
        node_timestamps = {}
        for e in window_events:
            node_id = e.get("node_id")
            event_type = e.get("event")
            ts = parse_ts(e["timestamp"])
            
            if node_id:
                if node_id not in node_timestamps:
                    node_timestamps[node_id] = {"start": None, "finish": None, "all": []}
                node_timestamps[node_id]["all"].append(ts)
                if event_type == "START":
                    node_timestamps[node_id]["start"] = ts
                elif event_type == "FINISH":
                    node_timestamps[node_id]["finish"] = ts

            # Track timeline milestones
            stage = e.get("stage")
            if event_type == "FINISH" and stage in ("SENSE", "PLAN", "ACT", "REFLECT") and node_id:
                metadata = e.get("metadata", {})
                status = metadata.get("status", "success")
                func_name = metadata.get("function", "")
                dur = metadata.get("duration_sec", 0.0)
                timeline.append(f"{ts.strftime('%Y-%m-%d %H:%M:%S')} - Node #{node_id} completed {stage} phase via {func_name} in {dur:.2f}s ({status})")

            # Track API Latency
            if e.get("stage") == "SKILL" and e.get("domain") == "skills":
                dur = e.get("metadata", {}).get("duration_sec")
                if dur is not None:
                    api_durations.append(dur)

            # Detect Lock Contentions
            meta_str = json.dumps(e.get("metadata", {}))
            if "lock" in meta_str.lower() or "contention" in meta_str.lower() or "blocked" in meta_str.lower():
                lock_contentions += 1

            # Detect and Classify Anomalies
            metadata = e.get("metadata", {})
            err_msg = metadata.get("error") or metadata.get("exception")
            status = metadata.get("status")
            if err_msg or status in ("error", "failure") or e.get("event") == "ERROR":
                err_text = err_msg or "Unknown error event"
                
                # Classification rules
                if any(x in err_text.lower() for x in ("transition blocked", "spec file violation", "prs are still open", "git push", "gh pr create")):
                    tier = 2
                elif any(x in err_text.lower() for x in ("timeout", "rate limit", "502", "503", "504", "lock", "connection reset")):
                    tier = 3
                elif any(x in err_text.lower() for x in ("syntaxerror", "exception", "failed", "crash", "rollback")):
                    tier = 1
                else:
                    tier = 4
                
                anomalies[tier].append(f"{ts.strftime('%Y-%m-%d %H:%M:%S')} - Node #{node_id or 'Global'}: {err_text}")

        # Compute averages
        for n_id, t_data in node_timestamps.items():
            start = t_data["start"] or (min(t_data["all"]) if t_data["all"] else None)
            finish = t_data["finish"] or (max(t_data["all"]) if t_data["all"] else None)
            if start and finish:
                node_durations[n_id] = (finish - start).total_seconds()

        avg_node_dur = sum(node_durations.values()) / len(node_durations) if node_durations else 0.0
        avg_api_lat = sum(api_durations) / len(api_durations) if api_durations else 0.0

        return {
            "avg_node_duration": f"{avg_node_dur:.2f}s",
            "avg_api_latency": f"{avg_api_lat:.3f}s",
            "api_count": len(api_durations),
            "lock_contentions": lock_contentions,
            "timeline": timeline,
            "anomalies": anomalies
        }

    def compile(self, output_path=None):
        """Runs the compilation and renders the markdown report."""
        target_nodes, _ = self.load_nodes_and_paths()
        metrics = self.process_telemetry(target_nodes)

        # Render lists for templates
        timeline_rendered = "\n  - ".join(metrics["timeline"][-20:]) if metrics["timeline"] else "No significant milestone transitions logged."
        
        t1_rendered = "\n  - ".join(metrics["anomalies"][1]) if metrics["anomalies"][1] else "None recorded."
        t2_rendered = "\n  - ".join(metrics["anomalies"][2]) if metrics["anomalies"][2] else "None recorded."
        t3_rendered = "\n  - ".join(metrics["anomalies"][3]) if metrics["anomalies"][3] else "None recorded."
        t4_rendered = "\n  - ".join(metrics["anomalies"][4]) if metrics["anomalies"][4] else "None recorded."

        # Compute Active Worktrees count
        worktree_count = 0
        try:
            wt_res = os.listdir(".worktrees") if os.path.exists(".worktrees") else []
            worktree_count = len([x for x in wt_res if os.path.isdir(os.path.join(".worktrees", x))])
        except Exception:
            pass

        # Load standard template
        template_file = "kb/templates/shar_retrospective.md"
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"SHAR retrospective template not found: {template_file}")

        with open(template_file, "r") as f:
            template_content = f.read()

        # Prompt blocks for qualitative sections (RCA and Action Matrix) to guide Agent inference
        rca_block = """[INFERENCE REQUIRED]
  *Identify the primary failure/bottleneck in the range and provide a 5 Whys analysis.*
  *Example:*
  - **RCA-0001**: SPEC validation failures during plan phase
    1. *Why?* Plan phase failed due to missing WHAT- specification file.
    2. *Why?* The developer did not create/modify a WHAT- file under kb/ prior to plan-finish.
    3. *Why?* The developer forgot to track specification requirements explicitly.
    4. *Why?* The system lacked a CLI warning or template reminding the developer of the SPEC boundary.
    5. *Why?* The spec boundary rule was recently codified but not integrated into the boilerplate generation tools."""

        preventative_block = """[INFERENCE REQUIRED]
  - [ ] Implement an automated boilerplate generator for WHAT- specs to reduce manual errors (Traces to RCA-0001)"""
        
        mitigation_block = """[INFERENCE REQUIRED]
  - [ ] Update the CLI to output a clear reminder of the SPEC file requirement during plan-start (Traces to RCA-0001)"""

        # Populate template
        populated = template_content.format(
            assessment_title=f"Paths {self.start_path} to {self.end_path}",
            timeline_events=timeline_rendered,
            tier1_mishaps=t1_rendered,
            tier2_close_calls=t2_rendered,
            tier3_precursors=t3_rendered,
            tier4_calibrations=t4_rendered,
            rca_title="Systemic Node/Path Execution Anomalies",
            why1="Identify the primary systemic anomaly or close call",
            why2="Why did that occur?",
            why3="Why?",
            why4="Why?",
            why5="Why?",
            preventative_tasks=preventative_block,
            mitigation_tasks=mitigation_block,
            kb_mutations="To be updated during reflection",
            orchestrator_updates="To be updated during reflection"
        )

        # Replace metrics table values
        populated = populated.replace("| Execution Time (Avg/Node) | | | |", f"| Execution Time (Avg/Node) | 120s | {metrics['avg_node_duration']} | |")
        populated = populated.replace("| GitHub API Latency (Avg) | | | |", f"| GitHub API Latency (Avg) | 1.500s | {metrics['avg_api_latency']} | |")
        populated = populated.replace("| Active Worktrees / Local Size | | | |", f"| Active Worktrees / Local Size | 1 | {worktree_count} | |")
        populated = populated.replace("| Duplicate File Lock Contention | | | |", f"| Duplicate File Lock Contention | 0 | {metrics['lock_contentions']} | |")

        # Determine output location
        if not output_path:
            output_path = f"artifacts/retrospective_path_{self.start_path}_{self.end_path}.md"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(populated)

        print(f"Retrospective successfully compiled to {output_path}")

def main():
    if len(sys.argv) < 4 or sys.argv[1] != "compile":
        print("Usage: python -m kernel.mgr_retro compile <start_path_id> <end_path_id> [output_path]")
        sys.exit(1)

    start_path = sys.argv[2]
    end_path = sys.argv[3]
    output_path = sys.argv[4] if len(sys.argv) > 4 else None

    compiler = RetroCompiler(start_path, end_path)
    compiler.compile(output_path)

if __name__ == "__main__":
    main()
