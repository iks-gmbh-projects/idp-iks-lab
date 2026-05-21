# Backstage Migration Issue Breakdown

Use this list to create or adjust external GitHub issues after human approval. The repository issue forms under `.github/ISSUE_TEMPLATE/` provide the active structure.

1. `ADR: Adopt Backstage as self-hosted IDP target`
   - Scope: ADR 0003 and ADR 0001 supersession.
   - Acceptance: wiki decisions clearly point to Backstage as the target.
2. `Docs: Reframe README and wiki from Port MVP to Backstage MVP`
   - Scope: root README, vision, operating model, demo story, IKS metadata model.
   - Acceptance: target-platform language names Backstage; Port appears only as legacy/migration context.
3. `Catalog: Add Backstage catalog structure and migrate demo entities`
   - Scope: `backstage/catalog/` and `examples/services/*/catalog-info.yaml`.
   - Acceptance: demo Components have valid owners, systems, source locations, TechDocs refs, and IKS annotations.
4. `Workflows: Replace Port actions with Backstage/GitHub issue workflows`
   - Scope: Backstage Software Templates and active GitHub Issue Forms.
   - Acceptance: workflows create advisory GitHub-tracked tasks only.
5. `Scorecards: Map IKS baseline and catalog quality to Backstage approach`
   - Scope: `backstage/scorecards/README.md`.
   - Acceptance: every previous rule has a Backstage field or annotation mapping.
6. `Agents: Update repo guidance, prompts, checklists, and skills for Backstage`
   - Scope: `AGENTS.md` and `agents/`.
   - Acceptance: new work points to Backstage; Port guidance is legacy-only.
7. `CI: Validate Backstage catalog and GitHub issue forms`
   - Scope: active and reference validation workflows.
   - Acceptance: YAML validation covers `backstage`, `port`, `examples`, `agents`, and `.github/ISSUE_TEMPLATE`.
8. `Cleanup: Decide lifecycle of legacy Port artifacts`
   - Scope: `port/` retention, archive, or removal.
   - Acceptance: a later decision or cleanup PR removes ambiguity once Backstage import is proven.

Plan-mode note: external issue creation or mutation remains a follow-up action and should not be performed without explicit approval.
