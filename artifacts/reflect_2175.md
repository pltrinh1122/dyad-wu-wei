# Frontier Dyad — Reflection — Node 2175 — Checkout System Crash

## 1. CONTINUE — what worked
**Narrative (Operator):** We successfully identified the root cause of the unhandled exception during checkout.
**Details (Agent):**
- Fast iteration — quickly addressing the unhandled error by introducing a structured exception class (`CheckoutBlockedError`) in Node 2262.

## 2. START — what to do better
**Narrative (Operator):** System should fail gracefully instead of crashing abruptly.
**Details (Agent):**
- Use custom semantic exceptions — implemented `CheckoutBlockedError` to provide clear, actionable feedback when the Git worktree creation fails (e.g., stale local branches).

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):** Unhandled system crashes pollute logs and halt execution unpredictably.
**Details (Agent):**
- Raw subprocess exceptions — allowing `subprocess.CalledProcessError` to bubble up instead of wrapping it in semantic domain exceptions. This breaks the expected flow.

## Forward
The `CheckoutBlockedError` was added in Node 2262, allowing the system to handle stale local git states gracefully and informing the operator without crashing. This solidifies our pattern for handling underlying system command failures with semantic domain exceptions.
