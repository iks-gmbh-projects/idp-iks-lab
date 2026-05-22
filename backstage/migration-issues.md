# Backstage Migration Issue Breakdown

Use this list to track the cleaned Backstage migration queue. The repository issue forms under `.github/ISSUE_TEMPLATE/` provide the active structure. External issue creation or mutation requires explicit human approval; issue #26 records the approved cleanup follow-up.

## Open Backstage migration issues

1. [#17 `Backstage IDP MVP: Architecture decision and migration anchor`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/17)
   - Scope: ADR 0003, ADR 0001 supersession, and target-platform decision history.
   - Acceptance: wiki decisions clearly point to Backstage as the target.
2. [#19 `Backstage IDP MVP: Scaffold local Backstage app/runtime`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/19)
   - Scope: local Backstage app/runtime or explicit external-runtime instructions.
   - Acceptance: local Backstage is configured/documented to read catalog data from this repository without Kubernetes as an MVP prerequisite; runtime setup is documented under `backstage/runtime/`, with full runtime smoke validation tracked by #24/#15 unless performed in the implementing PR.
3. [#20 `Backstage IDP MVP: Configure service catalog views and filters`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/20)
   - Scope: Backstage catalog overview, service detail pages, and demo navigation/filters.
   - Acceptance: `customer-portal` and `reporting-api` support the demo story.
4. [#21 `Backstage IDP MVP: Implement advisory catalog quality and IKS checks`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/21)
   - Scope: Tech Insights, a scorecard plugin, or local/CI report mapped from `backstage/scorecards/README.md`.
   - Acceptance: every previous rule has a Backstage-compatible field, annotation, or explicit deferred reason.
5. [#22 `Backstage IDP MVP: Replace Port actions with Software Templates and GitHub issue workflows`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/22)
   - Scope: Backstage Software Templates and active GitHub Issue Forms.
   - Acceptance: workflows create advisory GitHub-tracked tasks only.
6. [#23 `Backstage IDP MVP: Finish repository consistency cleanup`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/23)
   - Scope: root README, wiki landing/navigation, domain docs, workflows, issue templates, and agent guidance.
   - Acceptance: target-platform language names Backstage; Port appears only as legacy/migration context.
7. [#24 `Backstage IDP MVP: Package and document local/demo runtime`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/24)
   - Scope: local/demo runtime documentation, demo data loading, secrets documentation, and fallback story.
   - Acceptance: a contributor can run or understand the local Backstage demo path from a clean checkout.
8. [#15 `Backstage IDP MVP: Run validation and complete demo dry-run`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/15)
   - Scope: YAML validation and manual demo consistency pass.
   - Acceptance: demo can be completed without production system changes.
9. [#26 `Backstage IDP MVP: Clean follow-up after target switch`](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/26)
    - Scope: tracker cleanup, stale-language cleanup, and issue mapping updates.
    - Acceptance: this file and the issue tracker agree on the active Backstage migration queue.

## Completed Backstage migration issues

- #18 `Backstage IDP MVP: Finalize catalog schema and GitHub source-of-truth format` is closed as completed. Its catalog-schema scope remains represented by the current Backstage catalog descriptors and demo service `catalog-info.yaml` files.

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
