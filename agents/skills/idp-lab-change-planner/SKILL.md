---
name: idp-lab-change-planner
description: Plan and review focused changes in the IDP IKS lab repository without overengineering. Use when Codex needs to scope docs, Backstage catalog/configuration, governance, demo, or agent-artifact changes, decide whether an ADR is needed, preserve MVP boundaries, and define validation before implementation.
---

# IDP Lab Change Planner

## Workflow

1. Read `README.md`, `wiki/docs/vision.md`, and any touched domain docs before planning.
2. Keep the change small enough for a docs-and-configuration MVP unless the user asks for a larger expansion.
3. Identify affected surfaces: wiki docs, wiki decisions, Backstage artifacts, legacy Port migration references, examples, agent artifacts, or GitHub workflow templates.
4. Decide whether an ADR is needed. Use an ADR for scope, governance, source-of-truth, or integration decisions; skip it for routine maintenance.
5. Define validation using `agents/validation.md`.
6. Avoid adding runtime systems, Kubernetes behavior, or production automation unless the task explicitly changes the MVP scope.

## Reference Loading

- Read `references/planning-boundaries.md` when a task touches MVP scope, governance, ADRs, or external workflow behavior.

## Output Expectations

- Provide a concise implementation plan with affected surfaces and tests.
- State assumptions and deliberate non-goals.
- Prefer action-ready steps over generic architecture commentary.
