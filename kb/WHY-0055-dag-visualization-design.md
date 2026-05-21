# WHY-0055: DAG Meta-Index Representation and Visualization Design

## Context
Under Path 299, the system is transitioning the Path Meta-Index from a flat list to a Directed Acyclic Graph (DAG). This ensures that dependencies among child nodes (Activities and Probes) are honored during orchestration. 

As part of Node 300 (Probe: Evaluation of DAG Visualization Requirements), this document evaluates design patterns for representing, enforcing, and visualizing DAG structures within GitHub issues and CLI interfaces.

## Problem Statement
A flat list format does not convey dependency order, forcing developers and agent systems to manually track execution sequencing. To support a DAG, we must:
1. Parse node dependencies programmatically from human-editable markdown issue bodies.
2. Render the DAG structure visually on GitHub for human operators.
3. Render the DAG structure in CLI views (`node view` and `backlog list`) to maintain inner-loop visibility without requiring external web access.

---

## Proposed Solutions

### 1. Markdown Dependency Notation
To parse the DAG programmatically, the system must recognize dependencies defined inline within the `## Meta-Index` checklist.

#### Option A: HTML/JSON Metadata Block
Embed dependencies in a hidden HTML comment or JSON block at the bottom of the issue body.
- *Pros*: Completely clean checklist formatting.
- *Cons*: Higher edit friction for humans; prone to becoming out-of-sync when checkboxes are manually rearranged.

#### Option B: Inline Checklist Annotations (Status Quo Support)
Use inline annotations at the end of each checkbox line, matching the pattern `[Depends: <comma-separated list of Node IDs>]`.
- *Example*: `- [ ] Node 301: Probe: Plan - DAG Parsing [Depends: 300]`
- *Pros*: Extremely intuitive; matches the existing parsing capability in `gh_graph_skill.py`.
- *Cons*: Minor textual clutter at the end of checklist lines.

**Decision**: Implement Option B, as it leverages existing parsing patterns, is easy to edit, and maintains single-source-of-truth alignment.

---

### 2. GitHub Visual Representation
For visual clarity in the GitHub web UI, we need a diagramming standard.

#### Option A: Mermaid Graph Rendering
Automatically generate and embed a native `mermaid` block below or above the checklist.
- *Example*:
  ```mermaid
  graph TD
      300[Node 300] --> 301[Node 301]
      301 --> 302[Node 302]
  ```
- *Pros*: Native, interactive visual rendering inside GitHub issues.
- *Cons*: Requires updating the issue body dynamically during node generation and status updates.

#### Option B: Raw ASCII Tree Text Block
Embed an ASCII graph block in the issue body.
- *Pros*: Works everywhere.
- *Cons*: Does not render as cleanly as Mermaid; difficult to dynamically update.

**Decision**: Implement Option A. The backlog and node creation tools will generate a Mermaid diagram automatically, updating it as nodes are marked completed.

---

### 3. CLI Visual Representation (`node view`)
When running `./bin/node view <path_id>`, the terminal should render the DAG structure.

#### Option A: ASCII Indented Tree Visualization
Print the DAG as an indented hierarchical tree matching execution paths.
- *Pros*: Visually mimics git graph or directory trees.
- *Cons*: Complex to lay out and implement in robust Python code for generic DAGs (especially with multi-parent nodes).

#### Option B: Partitioned/Categorized Status Lists
Partition the nodes into logical status buckets:
- **Completed**: Nodes that are finished.
- **Ready**: Incomplete nodes whose dependencies are all completed (next-best-actions).
- **Blocked**: Incomplete nodes with pending dependencies.
- *Pros*: Highly robust, simple to implement, and directly maps to operational decision-making.

#### Option C: Hybrid Topological Output
Print a topologically sorted list of all nodes, showing status and dependencies inline, and prefixing with light ASCII indicators.
- *Example*:
  ```
  [x] Node 300: Probe 300: Probe: Evaluation of DAG Visualization Requirements
  └──► [Ready] Node 523: Probe 523: Design and Scoping for DAG Meta-Index Support [Depends: 300]
        ├──► [Blocked] Node 524: Activity 524: Implement DAG Parsing [Depends: 523]
        └──► [Blocked] Node 525: Activity 525: Implement CLI Rendering [Depends: 523]
  ```

**Decision**: Implement Option C. A lightweight topological printer with status indicators and dependency paths balances visual depth with coding simplicity.

---

## Strategic Backlog Node Population

Following the **Dual-Probe Initialization Rule** (documented in `kb/WHY-0014`), this Probe A (Node 300) will be followed by Probe B (Plan/Activity Scoping) and then implementation tasks.

The following subsequent nodes will be added to the backlog and linked to Path 299:
1. **Probe 523: Probe: Design and Scoping for DAG Meta-Index Support** (Probe B: Scoping and Technical Specifications)
2. **Activity 524: Activity: Implement DAG parsing in gh_graph_skill** (Implementation of parsing and validation rules)
3. **Activity 525: Activity: Implement CLI DAG rendering in node view** (Implementation of the topological CLI tree output)
4. **Activity 526: Activity: Reflect - Elevate Path Meta-Index from List to DAG** (Final validation, cleanup, and path reflection)
