# Reflection Discipline (d-reflect)

The **Reflection Discipline** (`d-reflect`) is the explicit session-close trigger, acting as the exact counterpart to `d-start`.

## Symmetry
`d-start : standup.sh :: d-reflect : standdown.sh`

Upon receiving the `d-reflect` token, the Agent MUST:
1. **Write the Retro**: Author a session closeout retro using the **CSS+SH** form (Continue/Start/Stop + Should Have/Should Hold).
   - *UI-Invariant (SH Form)*: The SH form grants explicit permission for the Agent to provide direct observations regarding the Operator's intent clarity and coherence. Specifically, **Should Have** is used for the *debit* (constructive critique on friction or ambiguity), and **Should Hold** is used for the *credit* (positive reinforcement of clear, coherent execution).
2. **Execute the Spine**: Run the autonomous mechanical spine `bin/standdown.sh` to close the session mechanically.
3. **Commit for Durability**: Land the retro and any uncommitted changes to ensure memory is grounded on disk.

## The Chat Presentation Rule
**CRITICAL**: The Agent MUST output the *full text* of the CSS+SH retro directly into the chat UI. It MUST NOT silently write the retro to disk and reply with a condensed headline or summary. This ensures the Operator has full visibility into the reflection at the moment of session closeout.
