# Agent Guide

This repository is an experimental Internal Developer Platform MVP for IKS. Treat it as a docs-and-configuration repo, not an application runtime.

## Mission

- Keep GitHub as the versioned source of truth for Backstage catalog descriptors, configuration examples, demo entities, decisions, and docs.
- Improve service catalog quality, IKS metadata visibility, scorecards/checks, and low-risk workflows.
- Preserve the MVP boundary: no Kubernetes automation, no production infrastructure changes, and no autonomous compliance enforcement.
- Treat `port/` as a legacy migration reference from the initial experiment; Backstage is the target path.

## Working Rules

- Prefer small, reviewable changes that fit the existing structure and language of the touched files.
- Keep new agent-facing mechanics in English. Keep established German domain docs and IKS/Backstage terms intact unless the task asks for translation.
- Update docs, Backstage artifacts, examples, and workflow references together when behavior or metadata shape changes.
- Use ADRs in `wiki/decisions/` for meaningful architectural or governance choices. Do not create an ADR for routine catalog edits.
- Keep generated or external workflow side effects out of scope unless a human explicitly approves them.

## Safe Edit Boundaries

- Safe by default: `wiki/docs/`, `wiki/decisions/`, `examples/`, `backstage/`, `.github/ISSUE_TEMPLATE/`, `agents/`, and root guidance files.
- Be careful with Backstage entity names, refs, annotations, and relations. Existing identifiers are treated as stable API for demo imports and scorecards/checks.
- Do not remove required metadata from example services unless the task is specifically about demonstrating missing data.
- Do not add Kubernetes, runtime health, deployment status, or infrastructure provisioning to the MVP path without a new decision record.
- Avoid new Port-only capabilities; update `port/` only for legacy notes or explicit migration work.

## Validation

Use the lightest checks that prove the touched surface:

- YAML syntax for Backstage, examples, agents, active issue forms, and legacy Port references:
  `yamllint backstage port examples agents .github/ISSUE_TEMPLATE`
- GitHub Actions parity:
  The active validation workflow lives under `.github/workflows/`. Template/reference workflow files may also exist under `github/workflows/`; keep them in sync when changing validation behavior.
- Codex skill validation:
  use the local Codex `quick_validate.py` script for changed skills when available.
- Manual consistency pass:
  verify that new required fields are documented, represented in Backstage descriptors, populated in demo entities, and covered by scorecard/check mapping when relevant.

Wiki docs live in the `wiki` submodule. Before editing them, run `git -C wiki switch master` and `git -C wiki pull --ff-only`. Commit and push wiki changes inside `wiki`, then commit the updated submodule pointer in the main repository.

If a validator is unavailable locally, state that clearly and perform a targeted read-through of the affected YAML and Markdown.

## Change Summaries

Final summaries should include:

- What changed and why.
- Which validation ran.
- Any intentionally deferred work or remaining risk.

For review comments, lead with concrete risks and file references. For implementation work, keep the summary short and practical.

## Developer-Fast Agent Contract

Agents may inspect, plan, edit repo files, and run local validation. Agents must ask before triggering external systems, opening real GitHub issues, changing Port or Backstage workspaces, pushing branches, editing the GitHub wiki through the web UI, or altering anything outside the repository except explicitly requested local Codex skill installation.
