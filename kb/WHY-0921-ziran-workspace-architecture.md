# WHY-0921: Architectural Decision Record for the Ziran Workspace Companion App

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0921
- **Author**: agent-ziran
- **Created**: 2026-05-24 (Node 921, Path 920)
- **Related Path**: Path 920 (Implement Ziran Workspace App for Operator Digital Needs)

---

## 1. Context & Operational Friction

The Operator expressed the need to extend the capabilities of the Dao-Ziran Continuous Inference Loop (DZ-CIL) to wider, non-software domains (e.g., vacation planning, creative novel writing). 

In [PML-0921](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/probe_125_evaluation.md), we evaluated and falsified the thesis that the current software-focused DZ-OS could be directly deployed to these tasks. The current engine is heavily coupled to code-centric substrates: Git branches/worktrees, POSIX compilers, and deterministic test runners. Directly forcing these unstructured tasks into the developer loop would redistribute all validation friction to the Operator, violating the Wu-wei Gate and causing severe human decision fatigue.

To resolve this contradiction, we reframed the goal: rather than deploying the agent directly into the Operator's unstructured tasks, the DZ-CIL developer agent will build a local-first **digital companion application (Ziran Workspace)** for the Operator. This companion app will run in the Operator's user space, providing structured planning and writing interfaces with local, automated semantic and logistical validation.

---

## 2. Decision: Architectural Blueprint of the Ziran Workspace App

We will design and build the Ziran Workspace app as a modular, local-first application containing three key layers:

```
┌────────────────────────────────────────────────────────┐
│                   Web UI Dashboard                     │
│    (High-Aesthetic Dark Mode / Local Flask Backend)    │
└───────────────────────────┬────────────────────────────┘
                            │ (Local API / JSON)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Workspace Engine                     │
│    (Python Core: Timeline & Semantic Parsers)          │
└───────────────────────────┬────────────────────────────┘
                            │ (Flat Files)
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Document Substrate                     │
│    (Markdown Files + YAML Frontmatter Metadata)       │
└────────────────────────────────────────────────────────┘
```

### 2.1 The Tech Stack & Rationale
1. **Substrate (Data Storage)**: Flat Markdown files with structured YAML frontmatter (metadata).
   * *Rationale*: Text-centric workflows (chapter drafting, travel diaries, itineraries) are most naturally and portably represented in plain text. Markdown files are fully portable, human-readable, and easily parsed by Python.
2. **Logic Engine**: Python-based parsers and compilers.
   * *Rationale*: Python is highly suited for parsing text patterns, validating structures, and running fast, local validation routines. This logic will reside under a new platform domain subfolder in the repository (e.g., `src/workspace_engine/`).
3. **User Interface**: A local-first Web UI served via a lightweight local Python backend (e.g. Flask/FastAPI serving static assets).
   * *Rationale*: Under our web application rules, the companion app must have rich aesthetics (modern dark mode, glassmorphism, clean layouts, smooth transitions) to reduce the Operator's cognitive load and provide motivational rewards. A local web app guarantees offline operation (Ziran Gate) while avoiding complex runtime compilation configurations.

---

## 3. Verification and Safety Loops (The Semantic Compilers)

To satisfy the Wu-wei Gate and prevent the Operator from acting as a manual linter, the tool must enforce two automated validation engines:

### 3.1 The Novel Studio Continuity Engine
* **Objective**: Automatically detect narrative inconsistencies across a set of chapter drafts.
* **Mechanism**: The engine parses a directory of Markdown chapters and cross-references them against character profiles and timeline schemas stored in a local `characters.yml` file.
* **Assertions**:
  * Character presence check (e.g., flag if a character is active in Chapter 3 but marked deceased in Chapter 2).
  * Timeline chronology verification (e.g., flag if events in the frontmatter metadata violate sequence rules).

### 3.2 The Vacation Logistical Engine
* **Objective**: Automatically validate travel plans and itinerary integrity.
* **Mechanism**: The engine parses travel plan schemas (JSON/Markdown) to verify timeline constraints.
* **Assertions**:
  * Date/Time overlap check (flag overlapping flights or accommodation bookings).
  * Route routing checker (detect backtracking logistics, e.g., Tokyo -> Kyoto -> Tokyo -> Osaka).
  * Checklist validation (ensure packing lists and travel visa requirements are checked off).

---

## 4. Portability & Substrate Decoupling

The Ziran Workspace codebase will be developed and tested within this repository by the DZ-CIL agent using our standard TDD frameworks. However, the Operator's personal data (vacation markdown files, novel drafts) will reside entirely outside the repository in the Operator's user space. This maintains a strict boundary between the Metasystem's developmental environment and the Operator's personal productivity environment.
