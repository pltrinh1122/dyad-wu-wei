# WHAT-1694: Job Discipline Template Specification

## Context & Axioms
As established in Node 1693 and `DISCIPLINE.md`, the Job Discipline construct must enforce that problems are bounded by Root Functional Jobs (JTBD) rather than sub-constraints of a larger problem. Furthermore, it must formalize decision-framing using Dialectical Falsification (Thesis -> Antithesis -> Synthesis).

## Architecture & Schema
This specification mandates the structure of a Job Discipline Template (`artifacts/job-discipline-template.md`). The template must contain the following mandatory sections:

### 1. Job To Be Done (JTBD) Identification
The template must include a section to articulate the root functional job.
* **Goal**: Clearly state the functional outcome the system must achieve.
* **Constraint Falsification**: Explicitly validate that this problem is not merely a constraint of another larger problem. If it is, the problem scope must be expanded to the true root job.

### 2. Dialectical Falsification Process
The template must enforce the dialectical decision-framing process:
* **Thesis**: The initial hypothesis or proposed solution for the JTBD.
* **Antithesis**: The falsification or systemic tension that challenges the thesis. This is critical for uncovering hidden constraints and preventing premature convergence.
* **Synthesis**: The harmonized resolution that addresses the antithesis while achieving the core JTBD.

### 3. Y-N Validation
The template must conclude with binary validation criteria:
* **Success Criteria (Y)**: What precise, observable state indicates the Synthesis has been successfully materialized?
* **Failure Criteria (N)**: What observable state indicates failure or regression?

## Constraints & Invariants
* **Invariant 1**: A Job Discipline instance cannot proceed without an explicitly articulated Antithesis. An unopposed Thesis is considered unvalidated.
* **Invariant 2**: The JTBD must be falsified against being a mere sub-constraint.

## Downstream Instantiation
The defined template schema will be physically materialized in `artifacts/job-discipline-template.md` and utilized as a standard artifact for all new Pathways in the Engine.
