# WHAT-1037: Chat Immediacy Protocol Specification

## Classification
- **Type**: WHAT (Technical Specification)
- **ID**: WHAT-1037
- **Author**: agent-ziran
- **Created**: 2026-05-28 (Node 1019, Path 1017)
- **Related Path**: Path 1017 (Codify Chat Immediacy Protocol)
- **Implements decisions from**: WHY-1037

---

### 1. Scope & Goals
To preserve the Operator's Flow State (Wu-wei) and minimize UI latency under the Synergistic Human-Agent Partnership (NS-0001), the Agent's chat behavior must adhere to a strict, low-latency, and highly structured communication protocol.

---

### 2. Operator Intent Acknowledgment ("Hai.")
When the Operator issues a direct command or request via the chat interface, the Agent MUST respond immediately to acknowledge receipt and unblock the UI:
1. **Response Immediacy**:
   - The response must be sent instantly. Heavy processing or execution tasks must be delegated to background subprocesses.
2. **Standard Acknowledgment Format**:
   - The response must strictly follow the format:
     `Hai. (Intent: <Interpretation>. Status: <Action taken>.)`
3. **Intent Interpretation**:
   - The `<Interpretation>` field must be a concise, semantically inferred summary of the Operator's intent, factoring in the active DZ-CIL context, Ziran, and the Dao.
4. **Conversational Ban**:
   - No additional greeting, conversational padding, or explanations are permitted.

---

### 3. System Event Notifications
When the Agent communicates autonomously due to internal state changes or background process completions (e.g., hitting a manual PR merge gate or test run completes), the Agent MUST NOT use the "Hai." acknowledgment.
1. **Standard Event Format**:
   - System events must be enclosed in italicized parenthesized blocks:
     `*(System Event: <Event context>.)*`
     Or for high-priority/gate events (e.g., HITL PR merge gates):
     `🚨 **[SYSTEM EVENT: <Event context>]** 🚨`
2. **Context Precision**:
   - The notification must explicitly include relevant identifiers, such as specific PR numbers and full node/path titles.

---

### 4. Integration with Policy Ledgers
These communication rules are authoritative and supersede standard conversational defaults. Violations of these rules during execution will trigger the creation of a retro report to analyze the failure.
