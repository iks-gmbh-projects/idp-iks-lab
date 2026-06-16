# Backstage Migration Issue Breakdown

Use this list to track the cleaned Backstage migration queue. The repository issue forms under `.github/ISSUE_TEMPLATE/` provide the active structure. External issue creation or mutation requires explicit human approval; issue #26 records the completed cleanup follow-up.

## Open Backstage migration issues

1. [#22 `Backstage IDP MVP: Replace Port actions with Software Templates and GitHub issue workflows`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/22)
   - Scope: Backstage Software Templates and active GitHub Issue Forms.
   - Acceptance: workflows create advisory GitHub-tracked tasks only.
2. [#24 `Backstage IDP MVP: Package and document local/demo runtime`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/24)
   - Scope: local/demo runtime documentation, demo data loading, secrets documentation, and fallback story.
   - Acceptance: a contributor can run or understand the local Backstage demo path from a clean checkout.
3. [#15 `Backstage IDP MVP: Run validation and complete demo dry-run`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/15)
   - Scope: YAML validation and manual demo consistency pass.
   - Acceptance: demo can be completed without production system changes.

## Completed Backstage migration issues

- #21 `Backstage IDP MVP: Implement advisory catalog quality and IKS checks` is closed as completed. PR #34 added executable check definitions, a Python report generator, and CI integration under `backstage/scorecards/`. The MVP implementation uses local/CI Markdown reports; future Backstage Tech Insights or scorecard plugin integration remains optional.
- #18 `Backstage IDP MVP: Finalize catalog schema and GitHub source-of-truth format` is closed as completed. Its catalog-schema scope remains represented by the current Backstage catalog descriptors and demo service `catalog-info.yaml` files.
- #17 `Backstage IDP MVP: Architecture decision and migration anchor` is closed as completed. ADR 0003, ADR 0001 supersession, and the decision history point to Backstage as the target.
- #19 `Backstage IDP MVP: Scaffold local Backstage app/runtime` is closed as completed. The external generated-runtime setup is documented under `backstage/runtime/`; full demo smoke validation remains tracked by #24/#15 unless performed earlier.
- #20 `Backstage IDP MVP: Configure service catalog views and filters` is closed as completed. PR #32 added portable catalog tags and documented the catalog view/filter demo path under `backstage/catalog/demo-views.md`.
- #23 `Backstage IDP MVP: Finish repository consistency cleanup` is closed as completed. Active docs, workflows, issue templates, and agent guidance name Backstage as the target while keeping Port as legacy/migration context.
- #26 `Backstage IDP MVP: Clean follow-up after target switch` is closed as completed. PR #28 performed the target-switch cleanup, and this follow-up reconciles the issue map after #20 landed.

## Superseded Port issues

The following issues were closed as `not planned` because Backstage is now the target path and `port/` is retained only as a legacy migration reference:

- #8 `MVP: Create Port workspace for the IDP catalog demo` -> replaced by #17, #19, and #24.
- #9 `MVP: Import Port blueprints` -> replaced by #18.
- #10 `MVP: Import demo catalog entities` -> replaced by #18 and service-local `catalog-info.yaml` imports.
- #11 `MVP: Configure catalog quality and IKS baseline scorecards` -> replaced by #21.
- #12 `MVP: Configure Port catalog demo views` -> replaced by #20.
- #13 `MVP: Wire low-risk GitHub issue self-service actions` -> replaced by #22.
- #14 `MVP: Decide whether metadata drift automation stays draft or enters demo` -> deferred to future advisory Backstage checks/workflows if still needed.

## Cleanup rule

Do not create new Port-only work unless a task explicitly asks for migration comparison or legacy cleanup. New target work should use Backstage catalog descriptors, TechDocs, Software Templates, GitHub Issue Forms, or documented Backstage-compatible checks.
