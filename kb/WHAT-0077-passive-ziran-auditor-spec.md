# WHAT-0077: Passive Ziran Auditor Specification

## 1. Intent & Purpose
The Antigravity Metasystem is governed by `kb/` primitives (WHAT/WHY/HOW). Historically, these rules were statically enforced via manual Operator anchoring or pre-defined "Marker" PR titles. This is the "Old-Dao" approach of static engineering.

The **Passive Ziran Auditor** introduces Daoist physics into the Metasystem: replacing static intent with empirical, telemetry-driven observation. The Auditor observes the "wake" of an Agent's execution and continuously promotes or demotes the confidence gradients of `kb/` primitives based on their physical adherence rates.

## 2. The Core Metaphor (Laminar vs Turbulent Flow)
In Ziran mechanics:
- **Laminar Flow**: A rule that the agent executes flawlessly, generating zero friction. The rule is perfectly aligned with the Agent's nature.
- **Turbulent Flow**: A rule that causes the agent to crash, fail tests, or trigger environmental audits. The rule is generating friction and fracturing the flow.

## 3. Telemetry Ingestion
The Auditor passively ingest data from the following physical streams:
1. **Node Sync Wake**: Output from `bin/node sync` which detects PR merges.
2. **Offline Execution Logs**: Traces from `./bin/run-tests` or other deterministic Skill executions.
3. **Audit Signals**: Specific flags raised during the `Act` phase when an invariant is breached.

## 4. Gradient Metrics
The confidence of any `kb/` primitive is calculated using an empirical gradient formula. 
Let $N$ be the total number of Node loops where a specific rule was theoretically applicable.
Let $S$ be the number of successful, friction-free navigations.
Let $T$ be the number of Turbulent collisions.

Confidence $\delta = f(S, T)$. High $\delta$ indicates a Laminar primitive. Low $\delta$ indicates a Turbulent primitive.

## 5. Promotion / Demotion Engine
Primitives are born as `Draft`. Based on the Confidence $\delta$ over $X$ iterations, the Auditor will automatically mutate the YAML `frontmatter` (or a dedicated `metadata.yml`) to change the state:
- `Draft` $\rightarrow$ `Active`: The primitive has been formally injected into the system.
- `Active` $\rightarrow$ `Laminar`: The primitive has survived $N$ loops with near-zero turbulence. It is now a core law of nature.
- `Active` $\rightarrow$ `Turbulent`: The primitive consistently generates friction. It is flagged for manual Operator review or Agentic rescoping.

## 6. Execution Constraints
The Auditor must strictly remain **passive**. It does not *enforce* the rules (that is the job of Skills and environmental gates). It only *observes* the wake and mutates the gradients.
