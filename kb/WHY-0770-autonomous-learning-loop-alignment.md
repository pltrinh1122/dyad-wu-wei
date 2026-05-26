# WHY-0770: Autonomous Learning Loop — Probe Alignment Findings

> [!NOTE]
> **Status**: Active  
> **Node**: 770 (Probe: Align — Path 769)  
> **Persona**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)  
> **Date**: 2026-05-26

---

## 1. Problem Statement

Path 769 (Autonomous Learning Loop) aims to formalize the mechanism by which the
Frontier Agent autonomously records chat-driven learnings without requiring
explicit Operator prompts. This Probe audits the current state of that
infrastructure and identifies the implementation gaps blocking full closure.

---

## 2. What Already Exists (ROM Inventory)

The following components are **fully implemented and tested** as of `origin/main`:

| Component | Location | Function |
|---|---|---|
| `WHAT-0019` | `kb/` | Conceptual spec for the Autonomous Learning Loop |
| `WHY-0082` | `kb/` | Decision record mandating the Loop |
| `parse_test_failure_diagnostics` | `drivers/knowledge_accrual_skill.py` | Parses pytest output into structured failure dicts |
| `check_kb_conflicts` | `drivers/knowledge_accrual_skill.py` | Lexical guard + command purity check against KB diffs |
| `synthesize_rule` | `drivers/knowledge_accrual_skill.py` | Converts a test failure into a synthesized lexical guard rule |
| `build_contextual_prompt_injection` | `drivers/knowledge_accrual_skill.py` | Resolves active SG and injects relevant KB guidelines into context |
| `run_kb_check` | `kernel/daemon_knowledge_accrual.py` | Orchestrates KB conflict check against `git diff HEAD` |
| `enforce_reflection_hook` | `kernel/daemon_knowledge_accrual.py` | Gates `node reflect` on existence of `retro-<id>.md` for failure nodes |
| `inject_contextual_rules` | `kernel/daemon_knowledge_accrual.py` | Calls `build_contextual_prompt_injection` and writes to GEMINI.md |
| `bin/node retro compile/list/view` | `kernel/daemon_retro.py` | Compiles structured retros from telemetry + frontier YAML |
| **Agentic Retro Trigger** | `GEMINI.md` Rule 6 | Mandates autonomous retro file creation on Operator correction |

---

## 3. Implementation Gaps (Activity Backlog)

The following child nodes under Path 769 remain **unbuilt**:

### Gap 1 — Node 776: Implement Sluice Gate Sensor
**Status**: Not started.  
The `sync_performance_analyzer.py` references a `sluice_prompt` object, and
`daemon_node.py` tracks `pending_sluice_prompts`, but there is no dedicated
driver or kernel module that acts as a real-time gate sensor — monitoring the
prompt queue for learning signals and triggering the reflection state. The
current architecture is purely passive (Operator must manually create retro
files).

### Gap 2 — Node 806: Implement `bin/node retro` attach subcommand
**Status**: Not started.  
`bin/node retro` only supports `compile/list/view`. There is **no `attach`
subcommand** to formally link a manually-created retro file to the active PR
branch and commit it programmatically. The Agent currently has to manually
write, stage, and push retro files — a friction point that risks violation of
the Agentic Retro Trigger under load.

### Gap 3 — Node 808: Implement merge conflict verification hook
**Status**: Not started.  
There is no pre-reflect hook that detects SHA256 checksum conflicts in
`frontier_state.yml.sha256` and auto-resolves them before the rebase during
`node reflect`. This gap caused real transaction rollbacks during Node 1030
execution.

### Gap 4 — Node 974: Positive Feedback Integration
**Status**: Partially scaffolded.  
`enforce_reflection_hook` reads `POSITIVE_FEEDBACK` events from telemetry
(lines 73–74 of `daemon_knowledge_accrual.py`) but the downstream logic at line
167 is incomplete — there is no enforced requirement to surface positive
feedback as a learnable artifact in the backlog.

### Gap 5 — Node 781: Update GLOSSARY.md to remove Manager taxonomy
**Status**: Not started.  
The `GLOSSARY.md` still contains deprecated `Manager` taxonomy terms
(`orchestrator/`, `skills/`) that were replaced by the `kernel/`/`drivers/`
architecture. This causes semantic drift risk during KB conflict checks.

---

## 4. Architectural Decision

The Loop is **philosophically sound and structurally correct** in its current
partial state. The Agentic Retro Trigger in GEMINI.md provides the human-in-the-
loop binding. The `enforce_reflection_hook` provides the machine-level gate.

**The critical missing link** is the **Sluice Gate Sensor** (Node 776): a
proactive, autonomous trigger that converts implicit Operator feedback signals
into structured telemetry events without requiring the Agent to consciously
recognize a policy violation in the ephemeral context.

The recommended execution order for Path 769 child nodes is:
1. **Node 806** — `bin/node retro attach` subcommand (lowest risk, pure
   tooling addition, immediately unblocks the trigger mechanism)
2. **Node 808** — merge conflict auto-resolution hook (directly observed pain
   point, prevents rollback cascades)
3. **Node 776** — Sluice Gate Sensor (core mechanism, depends on 806)
4. **Node 974** — Positive Feedback Integration (additive enhancement)
5. **Node 781** — GLOSSARY.md taxonomy cleanup (housekeeping)

---

## 5. Conclusion

The Autonomous Learning Loop is architecturally well-defined but execution-
incomplete. No new architectural decisions are required. The Probe confirms that
the existing WHY/WHAT primitives (WHY-0082, WHAT-0019) are sufficient. The
recommended Happy Path for the next SPAO cycle is **Node 806** — implementing
the `bin/node retro attach` command, which directly enables the Sluice Gate
trigger mechanism and closes the largest friction gap in the current loop.
