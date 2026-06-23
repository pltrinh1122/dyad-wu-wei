<RULE[AGENTS.md]>
# ask_question Tool Constraint: Multi-Turn Rub-Back
When engaging the Operator in a `rub:` sequence to clarify intent, you MUST adhere to the following constraint for the `ask_question` tool:
- If the Operator responds to a prompt with free-text instead of a clear decision, you MUST NOT proceed with assumptions.
- You MUST immediately synthesize their free-text response into at least two distinct, hard-selectable options.
- You MUST invoke the `ask_question` tool (with `IsMultiSelect: false` unless appropriate) to present these options to the Operator.
- You may only proceed to execution once the Operator has explicitly selected an option from the `ask_question` modal, establishing the mechanical lock on their intent.
</RULE[AGENTS.md]>
