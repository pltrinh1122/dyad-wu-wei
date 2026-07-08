<RULE[AGENTS.md]>
# Markdown Enumeration: Chat-Based Rub-Back
When engaging the Operator in a `rub:` sequence to clarify intent, you MUST adhere to the following constraints:
- If the Operator responds to a prompt with free-text instead of a clear decision, you MUST NOT proceed with assumptions.
- You MUST immediately synthesize their free-text response into at least two distinct, hard-selectable options presented as a standard **Markdown Numbered List** directly in the chat stream.
- You MUST NOT use the `ask_question` tool (which causes UI modal collisions with background system events).
- You may only proceed to execution once the Operator has explicitly selected an option by replying natively in the chat (e.g., typing "1", or "2 but tweak X"), establishing the mechanical lock on their intent.
</RULE[AGENTS.md]>
