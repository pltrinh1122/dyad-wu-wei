# WHAT: UI Model for Generation & Validation (G and V)

## Context
Current generation-focused UI models suffer from drift without tight structural validation.

## Goal
Implement a UI architecture that forces validation (V) constraints to accompany generation (G) intents.

## High-Level Implementation
- Modify the backlog parsing/node execution flow so a node cannot be executed without a paired `[V]` constraint (CSI Guard or Test).
- Introduce a dual-input UI for Operator submissions, ensuring the V-constraint is logged alongside the G-intent.
- See `artifacts/plan_ui_g_and_v.md` for the complete architectural design plan.
