# WHAT-0047: SHAR Retrospective Compiler Design

This document specifies the technical design, data parsing rules, and operational requirements for the automated High-Reliability Agentic Retrospective (SHAR) compiler.

## 1. Technical Architecture
The system follows a two-tier hybrid model:
1. **Deterministic Processing (Tier 1)**: A CLI utility `bin/retro` parses raw `artifacts/telemetry.jsonl` and `artifacts/frontier_state.yml` to generate quantitative metrics, timelines, and anomaly logs.
2. **Heuristic Inference (Tier 2)**: The agent uses LLM inference to synthesize the qualitative **5 Whys** and **Action Matrix** based on structured markdown context generated in Tier 1.

```
┌─────────────────────────┐      ┌─────────────────────────┐
│ telemetry.jsonl (Raw)   │ ───> │  daemon_retro.py (Parser)   │
└─────────────────────────┘      └───────────┬─────────────┘
                                             │ (Generates metrics/timeline)
                                             ▼
┌─────────────────────────┐      ┌─────────────────────────┐
│ agentic LLM (Inference) │ <─── │ shar_retrospective.md   │
└───────────┬─────────────┘      └─────────────────────────┘
            │ (Completes 5 Whys & Action Matrix)
            ▼
┌─────────────────────────┐
│ Final Retrospective PR  │
└─────────────────────────┘
```

## 2. CLI Invocation Specification
The compiler must be directly executable from the repository root:
```bash
./bin/retro compile <start_path_id> <end_path_id>
```
* **Positional Arguments**:
  * `start_path_id`: The integer ID of the starting Path to assess.
  * `end_path_id`: The integer ID of the ending Path to assess (inclusive).
* **Outputs**:
  * Creates or overwrites `artifacts/retrospective_path_<start>_<end>.md` utilizing the `kb/templates/shar_retrospective.md` layout.

## 3. Data Processing & Metric Formulation
* **Node Range Selection**: Retrieve all nodes whose parent paths lie between `start_path_id` and `end_path_id` (inclusive) by parsing `artifacts/frontier_state.yml`.
* **Telemetry Boundary**: Determine the time window $T = [T_{start}, T_{end}]$, where $T_{start}$ is the timestamp of the first `START` event of the first node in the range, and $T_{end}$ is the timestamp of the last `FINISH` event of the last node.
* **Metric Formulas**:
  * **Execution Time per Node**: For each node, find the difference between its overall start and finish event timestamps.
  * **API Latencies**: Filter for events with `stage: SKILL` and `domain: skills` (e.g., `github_client.get_issue_details`). Sum the durations and count occurrences.
  * **Anomaly Counts (ACT Log)**: Group exceptions in log metadata according to the Anomaly Classification Taxonomy (ACT) rules.

## 4. AI-Inference Prompts & Placeholders
For Section 4 (5 Whys) and Section 5 (Action Matrix), the compiler must generate a structured prompt block embedded in the markdown file containing:
- All raw error/exception messages recorded in telemetry for the range.
- The `learnings` and `invariants` of all nodes from `frontier_state.yml`.
- A template prompt directing the LLM to complete the analysis blamelessly.

## 5. Verification Invariants
- **Offline Invariant**: The compiler must run completely offline without executing any network calls.
- **Idempotency Invariant**: Multiple runs of `bin/retro compile` over the same telemetry inputs must generate byte-for-byte identical output.
- **Velocity Invariant**: Compilation of a 50-node range must complete in less than 2.0 seconds.
<!-- Checked and verified during Discovery 467 Plan phase -->
