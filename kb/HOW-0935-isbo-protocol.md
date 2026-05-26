# HOW-0935: Execution Protocol for the ISBO Journey

## Classification
- **Type**: HOW (Execution Playbook / Runbook)
- **ID**: HOW-0935
- **Author**: agent-frontier
- **Created**: 2026-05-26
- **Implements decisions from**: WHY-0935, WHAT-0935

---

### The Initiation Ritual

To establish a new, autonomous application built upon the DZ-CIL Engine, the Operator (whether the Creator or a Disciple) must execute the ISBO sequence in strict order. Deviating from this ritual risks contaminating the Engine and violating the separation of domains.

#### Step 1: [I]nstall (Procure the Loom)
1. Open a terminal.
2. Clone the core Dao Engine repository to a designated engine path:
   ```bash
   git clone <repo_url> /mnt/shared_data/git_repos/dz-cil
   ```
3. Install base OS-level dependencies (Python3, Git).

#### Step 2: [S]etup (Provision the Temple)
1. Ensure you are in the Engine directory:
   ```bash
   cd /mnt/shared_data/git_repos/dz-cil
   ```
2. Provision the new child workspace using the engine's bootstrapper:
   ```bash
   ./bin/workspace init /mnt/shared_data/dzw/dz-ta
   ```
   *(This safely creates the `.workspace/` baseline, the empty `kb/` and `artifacts/` pillars, and the isolated virtual environments required for the new application. The Engine directory remains pristine).*

#### Step 3: [B]ootstrap (Inject the Telos)
1. Open a **New Terminal Window** strictly dedicated to the child workspace. Do not mix contexts.
2. Navigate to the child workspace:
   ```bash
   cd /mnt/shared_data/dzw/dz-ta
   ```
3. Invoke the Agent:
   ```bash
   agy
   ```
4. **The Bootstrap Trigger**: The Agent will immediately detect the absence of `artifacts/strategic_intent.yml` (The Bootstrapping Invariant). It will refuse to act, demanding the Disciple provide the Domain Telos.
5. Provide your high-level goal (e.g., "I want to build a Travel Agent API that generates flight itineraries").
6. The Agent will compile this into the North Star document and establish the initial Backlog Path.

#### Step 4: [O]perate (The Flow State)
1. Once the Bootstrap sequence completes, the Agent enters the standard SPAO loop.
2. The Operator now assumes the role of "Director," operating entirely within the child terminal. You will respond to HITL (Human-in-the-Loop) gates, approve PRs, and provide strategic feedback based on the established `strategic_intent.yml`.
3. All future interactions within this terminal window execute domain logic exclusively, honoring the *Dao* and preserving *Wu-wei*.
