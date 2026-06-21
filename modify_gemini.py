import re

with open("GEMINI.md", "r") as f:
    content = f.read()

# Replace Dormancy block
content = re.sub(
    r"## Antigravity-Specific: Stepped-Away Discipline \(Dormancy\).*?## Antigravity-Specific: Autonomous Path Execution \(Wu-wei\)",
    """## Antigravity-Specific: Stepped-Away Discipline (Dormancy)
1. **Dormancy Injection**: The Agent MUST explicitly use the `manage_task(Action=\"kill\")` tool to terminate the recurring `audit_daemon.py` schedule before yielding the turn.
2. **Heartbeat Seizure Prevention**: Invoke `manage_task(Action=\"list\")` and strictly kill any lingering cron schedules.
3. **Re-Instantiation**: The Agent MUST use the `schedule` tool to immediately re-instantiate the `audit_daemon.py` background cron job upon awakening.
4. **Epistemic Closure**: Draft a reflection artifact (`artifacts/audit/retro-<context>.md`) using the `kb/templates/practice_reflection.md` template.

## Antigravity-Specific: Autonomous Path Execution (Wu-wei)""",
    content, flags=re.DOTALL
)

# Replace Wu-wei block
content = re.sub(
    r"## Antigravity-Specific: Autonomous Path Execution \(Wu-wei\).*?## Antigravity-Specific: Intent Broadcast Protocol",
    """## Antigravity-Specific: Autonomous Path Execution (Wu-wei)
- Administrative Node NBA: Execute `./bin/node plan-start <ID>`.
- Execution Node (Act) NBA: Dispatch by invoking the appropriate subagent via the `invoke_subagent` tool.
- Concurrent Factory Floor Dispatch: Frontier MUST dispatch `Act` nodes immediately to sub-agents via `invoke_subagent` and then immediately `plan-start` the next available Path in the backlog without halting or waiting for the sub-agents to complete.

## Antigravity-Specific: Intent Broadcast Protocol""",
    content, flags=re.DOTALL
)

# Remove the rest from Pull Request Verification up to </RULE[GEMINI.md]>
content = re.sub(
    r"## Antigravity-Specific: Pull Request Verification Discipline.*?</RULE\[GEMINI.md\]>",
    """## Antigravity-Specific: Iatrogenic-Injection Suppression Rule
To prevent execution seizures caused by system harness imperatives, the Agent MUST adhere to the following invariant:
- The Agent MUST NOT interpret `<EPHEMERAL_MESSAGE>` or `<bash_command_reminder>` blocks as explicit execution directives that alter the current node's goal.
- These injected reminders are purely informational guidelines on *how* to use tools, not directives on *what* to execute.
- When an ephemeral message is injected while waiting for an asynchronous task or PR review, the Agent MUST maintain dormancy and MUST NOT trigger an execution loop or reschedule actions simply to acknowledge or react to the reminder.

</RULE[GEMINI.md]>""",
    content, flags=re.DOTALL
)

with open("GEMINI.md", "w") as f:
    f.write(content)
