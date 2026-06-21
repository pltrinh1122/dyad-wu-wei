import sys

content = """24. **The Autonomous Path Execution Invariant**: The Agent MUST NOT ask the Operator for permission to start the next node. When the system surfaces a Next-Best-Action (NBA), the Agent MUST autonomously evaluate it. Administrative nodes (Harmonize/Plan/Reflect) MUST be executed via `plan-start`. Execution nodes (Act) MUST be dispatched to subagents if assigned. The Agent should only halt and yield the turn during HARD HITL blocks. The manual NBA Handoff wait state is formally falsified. When a backlog of "RUBBED" Paths exists, the Agent operates as a concurrent dispatcher (The Concurrent Factory Floor Pattern).
25. **The Pull Request Verification Discipline Invariant**: Before tossing a Pull Request over the wall for the Operator to review and merge (and entering the HARD HITL block), the Agent MUST proactively execute local CI validation (`spao test` or `./bin/run-tests`) and verify there are no remote merge conflicts. You must not inform the Operator to merge the PR until these health invariants are fully asserted.
26. **The Iatrogenic-Injection Suppression Invariant**: To prevent execution seizures caused by system harness imperatives, the Agent MUST NOT interpret `<EPHEMERAL_MESSAGE>` or `<bash_command_reminder>` blocks as explicit execution directives that alter the current node's goal. These injected reminders are purely informational guidelines on *how* to use tools. When an ephemeral message is injected while waiting for an asynchronous task or PR review, the Agent MUST maintain dormancy and MUST NOT trigger an execution loop or reschedule actions simply to acknowledge or react to the reminder.
27. **The Dyadic vs Autonomous Engine Handoff Invariant**: The SPAO Execution Loop is an asynchronous executor, not a universal interface. Domain A (The Dyadic Cycle) covers design, brainstorming, and philosophical alignment in a lock-free conversational mode where the SPAO engine is intentionally bypassed. Domain B (The Autonomous Engine) begins after the Handoff (The Sluice Gate), where the Agent drops into True Dormancy, acquires a lock on the `Path`/`Node`, and strictly executes the SPAO state machine autonomously.
28. **The HTIL Lexical Markers Invariant**: The system exposes explicit execution markers and configurable gates to control Agent autonomy (e.g., `HTIL_GATE_PR_MERGE`). The Agent MUST respect Operator Lexical Markers (`lean!`, `lean.`, `lean?`, `clip.`) to govern execution handoffs, explicitly bypassing proprietary platform UI buttons to maintain structural decoupling.
29. **The Test-Driven Development (TDD) Invariant**: To avoid regression and ensure the durability of the engine's invariants, the Agent MUST adhere to Simultaneous Test Evolution: when modifying source files, the Agent MUST proactively locate, review, and update the associated test files. Before utilizing bulk replacement tools or refactoring core components, the Agent MUST verify that automated tests validate the intended structural change and continue passing.
30. **The Intent Broadcast Protocol (Flight Plan) Invariant**: While the Agent MUST autonomously execute the NBA without asking for permission, the Agent MUST proactively broadcast a clear, concise "Flight Plan" to the Operator detailing the intent of the upcoming autonomous execution loop before dropping into it. This provides systemic transparency and mitigates Operator Anxiety without violating autonomous path execution invariants.
"""

with open("DYAD.md", "r") as f:
    text = f.read()

target = "23. **The Formal Worktree Materialization Invariant**: You must NEVER execute the `reflect` command or close a node without first explicitly materializing its formal `.worktrees/node/<id>` namespace via `bin/node checkout`, even for administrative nodes that do not contain code modifications. Failing to do so causes unhandled execution exceptions during the porcelain status check.\n"

if target in text:
    text = text.replace(target, target + content)
    with open("DYAD.md", "w") as f:
        f.write(text)
    print("Success")
else:
    print("Target not found")
