# HOW-1595: Implement Quarantine Survivor for Self-Created Nodes

## Overview
The Quarantine Protocol exists strictly to filter **External Requirement Intakes** (e.g. issues created by humans without execution labels). It is an epistemic firewall, NOT an internal pipeline gate.
When the Agent generated internal sub-nodes (like `Reflect`, `Plan`, `Align`), `node_lifecycle.py` crashed during `plan_start` with a `[🚫 BLOCKED] Quarantine Protocol Violation` because the issues did not possess the `backlog` label and their titles did not exactly match `Activity|Discovery`.

## Implementation
To structurally bypass Quarantine for any node authored by the system itself:
1. We check if the node is a child of an active path using `daemon_strategic.find_parent_path_id()`. If it belongs to a path, it is an internal pipeline node and immediately bypasses quarantine.
2. We expanded the title regex check `system_prefix_pattern` to automatically bypass quarantine for issues matching any systemic prefix (e.g., `Node`, `Path`, `Align`, `Plan`, `Act`, `Reflect`, `Harmonize`).
3. If either condition is met, the system automatically adds the `backlog` label and proceeds with `plan_start`, preventing ghost loops and execution seizures.
