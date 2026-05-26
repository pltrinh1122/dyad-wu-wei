# WHY-0062: Hybrid Persona Domain Gate — Architectural Decision Record

## Classification
- **Type**: WHY (Decision Record)
- **ID**: WHY-0062
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-21 (Node 602, Path 591)
- **Implements**: WHAT-0062 (ownership index), Activity 600 (agent_id standard)
- **Status**: Accepted

---

## 1. Context — The Triggering Incident

On 2026-05-21, agent-SG5 incorrectly claimed Node 525 under Path 299, which is
owned by agent-SG1. Simultaneously, agent-SG2 also expressed interest in the
same path. This produced a three-way domain collision: agent-SG5, agent-SG2, and
agent-SG1 all held partial claims on the same strategic goal (SG-0001).

Root cause: the system had **no mechanism to link the executing agent's identity
to the strategic goal owner** at plan-start time. The only concurrency control
was the `status: in-progress` GitHub label lock, which prevents two agents from
executing the *same node simultaneously*, but does not prevent two agents from
*claiming nodes in the same domain at different times*.

---

## 2. Options Considered

### Option A — Dynamic-Only (GitHub Label Locks per Path)

**Mechanism**: Add an `owner: agent-sg{N}` label to each Path issue. At
plan-start, read the label and compare against `SPAO_PERSONA_ID`.

**Failure modes**:
- **Fail-open on missing label**: If a new Path is created and the operator
  forgets to add the owner label, the gate has no data and must choose between
  blocking all work (too strict) or allowing all agents (fail-open, unsafe).
- **Label mutability**: GitHub labels can be added/removed by any agent or
  operator. The ownership source of truth is mutable at runtime — any typo or
  mis-labeling silently bypasses the gate.
- **O(N) lookup cost**: Fetching issue labels requires a GitHub API call per
  plan-start, adding network latency to every transition.
- **No auditability**: There is no single document listing all path-to-owner
  mappings; the state is distributed across hundreds of GitHub issue labels.

**Verdict**: ❌ Insufficient alone — fails open on unregistered paths.

---

### Option B — Static-Only (KB ROM Ownership Index)

**Mechanism**: Maintain `kb/WHAT-0062` as a static table mapping SG IDs to
agent personas. At plan-start, resolve the target node's SG, look it up in the
table, and compare against `SPAO_PERSONA_ID`.

**Failure modes**:
- **No concurrency control**: Two agents with the same SG (e.g., if SG-0001 is
  temporarily assigned to two personas during a handover) can both pass the ROM
  check and execute the same node simultaneously — the `status: in-progress`
  label lock is still required.
- **Stale index**: If a new SG or path is created but WHAT-0062 is not updated,
  the gate blocks all work on that SG (strict) but produces a confusing error
  with no path to resolution.

**Verdict**: ❌ Insufficient alone — no runtime concurrency guard.

---

### Option C — Hybrid (ROM Authorization + Label Concurrency Lock) ✅ CHOSEN

**Mechanism**: Two independent layers that must both pass:

| Layer | Mechanism | Owner | What it guards |
|-------|-----------|-------|----------------|
| **Static ROM** | `kb/WHAT-0062` ownership index | agent-sg5 (SG-0005) | *Which* agent is authorized for a goal |
| **Dynamic lock** | `status: in-progress` GitHub label | agent-sg2 (SG-0002) | *Whether* a node is already being worked |

At plan-start:
1. Read `agent_id` from `dz-cil.yml` (ROM identity — set once per deployment)
2. Resolve target node → Path → SG ID
3. Look up SG ID in `WHAT-0062` → get `owner_persona`
4. If `owner_persona == "unassigned"` → **block** (fail-closed)
5. If `owner_persona == "shared"` → **allow** (NS-0001 is cross-agent)
6. If `agent_id ≠ owner_persona` → **block** (`PersonaScopeConflictException`)
7. Check `status: in-progress` label → **block** if already locked

**Why this combination works**:
- The ROM layer prevents cross-domain *authorization* (wrong agent, wrong goal)
- The label layer prevents concurrent *execution* (same agent or any agent, same node)
- Neither layer alone is sufficient; together they are complete

---

## 3. The Decision

**Adopt Option C — the Hybrid Persona Domain Gate.**

**Layer separation is intentional and enforced by domain ownership:**
- agent-SG5 (SG-0005) owns and maintains the ROM (WHAT-0062, agent_id standard)
- agent-SG2 (SG-0002) owns and maintains the enforcement code (daemon_strategic.py,
  node_lifecycle.py, PersonaScopeConflictException)
- agent-SG1 (SG-0001) extends the NBA evaluator to filter path recommendations
  by ownership, preventing incorrect goal surfacing before plan-start is even
  attempted

This division means each agent can evolve its layer independently without
crossing the architectural boundary.

---

## 4. Fail-Closed Invariant

The gate MUST block (not skip, not warn) in all of the following cases:
- `SPAO_PERSONA_ID` environment variable is absent
- `agent_id` field is absent from `dz-cil.yml`
- Target node's SG ID is not present in `WHAT-0062`
- `owner_persona` in `WHAT-0062` is `unassigned`
- `agent_id ≠ owner_persona`

The only **allow** conditions are:
- `agent_id == owner_persona` (exact match)
- `owner_persona == "shared"` (intentional cross-agent goal)

---

## 5. Falsification Criteria

This decision is invalidated if:
1. A concrete scenario is found where the hybrid gate fails-open (allows an
   unauthorized transition) under any combination of missing labels, missing
   env vars, or missing WHAT-0062 entries.
2. The ROM layer becomes a bottleneck — i.e., WHAT-0062 updates are so frequent
   that the static file approach creates more friction than it prevents.
3. A simpler single-layer mechanism is proven sufficient for all failure modes
   documented in Section 2.

If any of the above are demonstrated, this ADR should be superseded with a new
WHY-* document citing this one.

---

## 6. Consequences

| Stakeholder | Impact |
|-------------|--------|
| agent-SG5 | Owns WHAT-0062 — must update it when SG ownership changes |
| agent-SG2 | Implements gate — must read WHAT-0062 at plan-start; cannot skip |
| agent-SG1 | Filters NBA — surfaces only own-domain paths to avoid wasted plan-starts |
| Operator | Must assign SG-0003 and SG-0004 owners before those goals can be worked |
| All agents | `SPAO_PERSONA_ID` env var must be set in every execution context |
