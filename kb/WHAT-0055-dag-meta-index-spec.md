# WHAT-0055: DAG Meta-Index Parsing and Validation Specification

This specification defines the parsing syntax, referential constraints, self-dependency checks, acyclicity validations, and CLI rendering requirements for transition of the Path Meta-Index checklist to a Directed Acyclic Graph (DAG).

---

## 1. Dependency Notation & Parsing Syntax

### 1.1 Checklist Line Grammar
A Meta-Index is defined as a Markdown checklist within a Path's GitHub Issue body. Each node in the graph is represented by a single checklist line that conforms to the following regular expression (case-insensitive):

```regex
^\s*-\s+\[([xX /])\]\s+(?:Node|Activity|Discovery|Path)?\s*(\d+):?\s*(.*?)(?:\s*\[Depends:\s*(.*?)\s*\])?\s*$
```

Where:
- Group 1 represents the completion status: `x` or `X` for Completed, ` ` (space) or `/` for Incomplete.
- Group 2 represents the numeric integer ID of the Node (unique within the Meta-Index).
- Group 3 represents the title of the Node, excluding trailing dependency annotations.
- Group 4 (optional) represents a comma-separated list of dependency Node IDs.

### 1.2 Parsing Logic
1. The parser MUST replace literal `\n` characters with actual newline characters prior to line splitting.
2. For each line matching the grammar:
   - Extract the Node ID as a string.
   - Extract the `completed` boolean state (True if status character is `x` or `X`).
   - Extract the Node Title.
   - Parse the `Depends:` field if present, splitting on commas `,` and stripping all surrounding whitespace from each dependency Node ID. Empty dependency definitions (e.g. `[Depends: ]`) MUST resolve to an empty list.

---

## 2. Graph Validation & Integrity Invariants

When the Meta-Index is parsed, the resulting dependency graph $G = (V, E)$—where $V$ is the set of Node IDs and $E$ is the set of directed edges $(u, v)$ indicating that node $u$ depends on node $v$—MUST satisfy the following validation invariants:

### 2.1 Referential Integrity Closure
For every node $u \in V$:
- If $u$ lists a dependency node ID $v$, then $v$ MUST exist in the vertex set $V$ ($v \in V$).
- External references to Node IDs outside the scope of the current Path's Meta-Index checklist are strictly forbidden.
- Violation of this closure rule MUST raise a `DAGValidationError` stating:
  `"Referential Integrity Violation: Node {u} depends on non-existent Node {v}"`

### 2.2 Self-Dependency Prevention
No node $u \in V$ may depend on itself:
- There is no edge $(u, u) \in E$.
- Violation of this self-dependency check MUST raise a `DAGValidationError` stating:
  `"Self-Dependency Violation: Node {u} cannot depend on itself"`

### 2.3 Acyclicity Validation (Cycle Detection)
The dependency graph $G$ must be acyclic. There must be no sequence of vertices $v_0, v_1, \dots, v_k$ such that $v_0 = v_k$ and $(v_i, v_{i+1}) \in E$ for all $0 \le i < k$.
- Detection Algorithm: The parser MUST perform a Depth-First Search (DFS) or Topological Sort (e.g., Kahn's Algorithm) to check for back-edges.
- If a cycle is detected, validation MUST raise a `DAGValidationError` stating:
  `"Cycle Detected: {v_0} -> {v_1} -> ... -> {v_k}"` (detailing the cyclic path).

---

## 3. Operational State Resolution

### 3.1 Node Readiness
A Node $u \in V$ is classified as **Ready** (executable) if and only if:
1. It is incomplete: `completed` is False (status character is ` ` or `/`).
2. All of its dependencies are satisfied: For every $v \in V$ where $(u, v) \in E$, the status of $v$ is Completed (`completed` is True).

If a Node is incomplete but has one or more incomplete dependencies, it is classified as **Blocked**.

### 3.2 Topological Sort Order
To ensure deterministic execution and serialization:
- The next-best-action (NBA) selector MUST topologically sort the nodes.
- If multiple nodes are concurrent and independent (e.g., both are Ready and have no dependency relationship), they MUST be ordered by their numeric Node ID in ascending order to guarantee deterministic resolution.

---

## 4. CLI Rendering Specifications

When running `node view <path_id>` or checking the active path status, the CLI MUST output a topologically sorted visualization of the DAG using the following visual indicators:

### 4.1 Visual Status Indicators
- **Completed**: `[x]` (Green or standard terminal formatting)
- **Ready**: `[Ready]` or `[ ]` (Yellow / Cyan)
- **Blocked**: `[Blocked]` (Red / Grey)

### 4.2 Topological Tree Formatting
The CLI view MUST render the hierarchy showing dependency relationships using ASCII branch indicators:
```text
[x] Node 300: Discovery 300: Discovery: Evaluation of DAG Visualization Requirements
└──► [Ready] Node 523: Discovery 523: Design and Scoping for DAG Meta-Index Support [Depends: 300]
      ├──► [Blocked] Node 524: Activity 524: Implement DAG Parsing [Depends: 523]
      └──► [Blocked] Node 525: Activity 525: Implement CLI Rendering [Depends: 523]
```
Each dependent node is indented and prefixed with branch lines `├──►` or `└──►` mapping back to its parent dependencies to clearly surface the execution topology.
