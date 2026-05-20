# Plan: Implement GitHub Issue #1 — Service-Katalog als erster IDP-Schritt

## Goal

Implement GitHub issue #1: establish a versioned Port service catalog MVP that shows services, ownership, system/domain assignment, repository links, documentation/runbook metadata, criticality, lifecycle, and IKS relevance while staying inside the repository-only MVP boundary.

Issue: https://github.com/iks-gmbh-projects/idp-iks-lab/issues/1

## Current context / assumptions

- Repository: `https://github.com/iks-gmbh-projects/idp-iks-lab.git`
- Issue #1 is open and describes a German user story for a first IDP service catalog step.
- Existing repo content already covers much of the story:
  - Service blueprint: `port/blueprints/service.yaml`
  - Demo services: `port/entities/services.yaml`
  - Systems: `port/entities/systems.yaml`
  - Repositories: `port/entities/repositories.yaml`
  - Teams: `port/entities/teams.yaml`
  - Catalog quality scorecard: `port/scorecards/catalog-quality.yaml`
  - IKS baseline scorecard: `port/scorecards/iks-baseline.yaml`
  - Per-service examples: `examples/services/customer-portal/catalog.yaml`, `examples/services/reporting-api/catalog.yaml`
  - Wiki docs: `wiki/docs/iks-metadata-model.md`, `wiki/docs/demo-story.md`
- Current working tree has unrelated uncommitted changes:
  - `.devcontainer/Dockerfile`
  - `.devcontainer/devcontainer.json`
  - `package-lock.json`
  These should not be touched unless the user explicitly includes them.
- The wiki is a submodule. Before editing wiki docs, follow `AGENTS.md`: run `git -C wiki switch master` and `git -C wiki pull --ff-only`. Because this is a plan only, do not run those mutating commands now.
- MVP boundary from `AGENTS.md` and issue #1 must be preserved:
  - no Kubernetes automation
  - no production infrastructure changes
  - no autonomous compliance enforcement
  - keep GitHub as source of truth

## Proposed approach

Treat the issue as a repository artifact alignment task rather than an app/runtime change. First compare acceptance criteria against the existing Port model and demo data. Then make small, reviewable updates only where gaps remain.

The likely implementation is to tighten and document the current service catalog model, ensure the demo entities clearly prove the user story, and add lightweight Port catalog/scorecard artifacts for filtering or visibility if the repository has an established place for them.

## Acceptance criteria mapping

| Issue criterion | Current status | Planned action |
|---|---|---|
| Services can be displayed as catalog entities | Mostly present via `port/blueprints/service.yaml` and `port/entities/services.yaml` | Verify Port entity format and document import/demo path |
| Service can be assigned to a system or domain | Present via `relations.system`; systems include `domain` | Keep stable identifiers; document relation in wiki |
| Service can be assigned to technical owner/team | Present via `relations.owner` | Keep; ensure docs call this technical owner |
| Service can be assigned to business owner | Present via `properties.businessOwner` | Keep; ensure docs align with property name |
| Service can link at least one repository | Present as required `relations.repository`, but currently `many: false` | Decide whether to keep one required repo for MVP or change relation to `many: true`; prefer smallest change unless multi-repo support is required by the issue owner |
| Documentation and runbook links can be maintained | Present via `documentation` and `runbook`; `reporting-api` intentionally has empty runbook | Keep intentional gap; ensure scorecard catches it |
| Criticality and lifecycle are visible | Present via required fields | Keep; ensure examples and docs describe allowed values |
| IKS relevance can be maintained as service metadata | Present indirectly via `complianceScope: [iks]` | Consider adding an explicit `iksRelevant` boolean only if clarity outweighs duplication; otherwise document `complianceScope` as the IKS relevance field |
| Catalog supports first filtering/view for IKS-relevant or critical services | Partly covered by metadata and scorecards, no explicit view artifact seen under `port/` | Add documentation for the demo filter, or add a Port page/dashboard/search artifact only if the repo already supports such artifacts |
| MVP boundary preserved | Present in issue/docs | Add/verify explicit boundary statement in demo docs |

## Step-by-step plan

1. Baseline and protect unrelated work
   - Run `git status --short`.
   - Note unrelated local changes and avoid modifying them.
   - Inspect issue #1 again if needed with `gh issue view 1`.

2. Refresh wiki submodule before documentation edits
   - Run:
     - `git -C wiki switch master`
     - `git -C wiki pull --ff-only`
   - If this fails because of local wiki changes or auth/network problems, stop and report before editing wiki files.

3. Verify the existing Port model against the issue
   - Review:
     - `port/blueprints/service.yaml`
     - `port/blueprints/system.yaml`
     - `port/blueprints/repository.yaml`
     - `port/blueprints/team.yaml`
   - Confirm that required fields and relations cover the story.
   - Decide on these model adjustments:
     - Repository relation: keep `many: false` for MVP simplicity or change to `many: true` for exact “at least one repository” semantics.
     - IKS relevance: keep `complianceScope` as the source of truth or add explicit `iksRelevant` boolean.
   - Preferred MVP approach: avoid redundant fields; document `complianceScope` clearly and keep a single required repository unless stakeholders expect multi-repo services immediately.

4. Update service blueprint if needed
   - Likely file: `port/blueprints/service.yaml`
   - Possible changes:
     - Add clearer titles/descriptions if Port supports description fields in this repo’s style.
     - Optionally add required `complianceScope` if IKS relevance must be mandatory for every demo service.
     - Optionally change `relations.repository.many` from `false` to `true` only after updating all service entities to list syntax.
   - Avoid renaming stable identifiers such as `service`, `businessOwner`, `complianceScope`, `owner`, `system`, and `repository` unless unavoidable.

5. Align demo entities
   - Files likely to change:
     - `port/entities/services.yaml`
     - `port/entities/systems.yaml` only if domain/system examples need clearer coverage
     - `port/entities/repositories.yaml` only if repository relation changes require additional examples
     - `examples/services/customer-portal/catalog.yaml`
     - `examples/services/reporting-api/catalog.yaml`
   - Preserve the intended contrast:
     - `customer-portal`: complete, high-criticality, IKS-relevant service with documentation and runbook.
     - `reporting-api`: IKS-relevant service with intentionally missing runbook to demonstrate scorecards and follow-up workflows.
   - If relation `repository` becomes many-valued, update every service relation consistently, for example:
     - `repository: [customer-portal-repo]`
     - `repository: [reporting-api-repo]`

6. Strengthen scorecards for the user story
   - Files likely to change:
     - `port/scorecards/catalog-quality.yaml`
     - `port/scorecards/iks-baseline.yaml`
   - Verify current scorecards cover:
     - technical owner
     - repository
     - documentation
     - runbook
     - business owner
     - criticality
     - protection need
     - data class
     - IKS scope
   - Consider adding a rule for lifecycle if the demo should prove lifecycle visibility as a quality requirement:
     - identifier: `has-lifecycle`
     - query: `$.properties.lifecycle != null && $.properties.lifecycle != ""`
     - level: `bronze`
   - Consider adding a system/domain relation rule if the catalog quality scorecard should directly validate system assignment:
     - identifier: `has-system`
     - query: `$.relations.system != null`
     - level: `bronze`

7. Document the catalog model and demo flow
   - Wiki files likely to change:
     - `wiki/docs/iks-metadata-model.md`
     - `wiki/docs/demo-story.md`
     - possibly `wiki/docs/operating-model.md` if ownership responsibilities need clarification
   - Documentation updates should remain in German where existing domain docs are German.
   - Add or clarify:
     - `owner` relation = technical owner/team
     - `businessOwner` = fachliche Verantwortung
     - `system` relation plus system `domain` = Zuordnung zu System/Domäne
     - `repository` relation = verknüpftes Repository
     - `documentation` and `runbook` links
     - `criticality`, `lifecycle`, and `complianceScope` / `iks` meaning
     - first demo filter: “IKS-relevante Services” means `complianceScope` contains `iks`; “kritische Services” means `criticality` is `high` or `critical`
     - explicit MVP exclusions from issue #1

8. Add a concise implementation note or checklist if useful
   - If the repo lacks a clear place for catalog import/demo instructions, consider adding a small doc under `wiki/docs/` or extending `wiki/docs/demo-story.md` rather than adding new machinery.
   - Do not create an ADR unless the implementation introduces a meaningful architectural/governance decision. Routine catalog alignment does not need an ADR.

9. Validate locally
   - Run YAML validation:
     - `yamllint port examples agents`
   - If `yamllint` is unavailable, state that clearly and do a targeted read-through of changed YAML.
   - Validate consistency manually:
     - every required service property is populated in `port/entities/services.yaml`
     - demo per-service `catalog.yaml` files match the central service entities where intended
     - relation targets exist in the corresponding entity files
     - scorecard queries reference existing properties/relations
     - docs mention fields exactly as implemented
   - Run `git diff --check` to catch whitespace issues.

10. Review final diff and issue coverage
   - Run `git diff -- port examples wiki`.
   - Confirm no `.devcontainer/*` or `package-lock.json` edits are included.
   - Prepare a summary mapped to issue #1 acceptance criteria.
   - If making a PR later, include `Closes #1` or `Resolves #1` in the PR body only after implementation is complete and verified.

## Files likely to change

High likelihood:
- `port/blueprints/service.yaml`
- `port/entities/services.yaml`
- `examples/services/customer-portal/catalog.yaml`
- `examples/services/reporting-api/catalog.yaml`
- `port/scorecards/catalog-quality.yaml`
- `port/scorecards/iks-baseline.yaml`
- `wiki/docs/iks-metadata-model.md`
- `wiki/docs/demo-story.md`

Possible, only if consistency requires it:
- `port/entities/systems.yaml`
- `port/entities/repositories.yaml`
- `wiki/docs/operating-model.md`
- `wiki/Home.md` or `wiki/_Sidebar.md` if a new wiki page is added

Should not change for this issue:
- `.devcontainer/Dockerfile`
- `.devcontainer/devcontainer.json`
- `package-lock.json`
- Runtime/deployment/Kubernetes files, unless a human explicitly expands the scope

## Tests / validation

Primary:
- `yamllint port examples agents`
- `git diff --check`

Manual consistency checks:
- Service blueprint required properties match demo services.
- Relation targets exist:
  - service `owner` values exist in `port/entities/teams.yaml`
  - service `system` values exist in `port/entities/systems.yaml`
  - service `repository` values exist in `port/entities/repositories.yaml`
- Scorecard queries only reference implemented service fields/relations.
- `customer-portal` demonstrates complete metadata.
- `reporting-api` intentionally fails the runbook quality rule but still remains a valid demo service if `runbook` is optional.
- Wiki docs and demo flow use the same field names as YAML artifacts.

Optional if Port validation/import tooling exists in the repo or environment:
- Run the repository’s Port config validation/import dry-run command.
- If no such command exists, do not invent one; document that validation was limited to YAML syntax and manual consistency.

## Risks and tradeoffs

- `repository` relation cardinality:
  - Keeping `many: false` is simpler and already satisfies “at least one repository” for the MVP, but it cannot represent multi-repo services.
  - Changing to `many: true` is semantically closer to the issue wording but requires updating all current entities and may affect downstream demo imports.
- IKS relevance representation:
  - Reusing `complianceScope` avoids duplicate metadata.
  - Adding `iksRelevant` would make filtering obvious but risks inconsistency with `complianceScope`.
- Wiki submodule workflow can introduce operational friction. Do not edit wiki docs until the submodule is on `master` and fast-forwarded.
- Scorecard query syntax should be kept consistent with existing Port examples; if changing relation cardinality, queries may need adjustment.
- The issue asks for filtering/viewing. If no Port page/dashboard artifact pattern exists in this repo, documenting the filter may be preferable to introducing an unvalidated artifact type.

## Open questions

1. Should a service support multiple repositories now, or is one required repository enough for the MVP?
2. Should IKS relevance remain `complianceScope contains "iks"`, or should the catalog expose a dedicated boolean such as `iksRelevant`?
3. Does the repository have or want a Port page/dashboard/search artifact for predefined catalog views, or should the initial filter remain a documented demo action?
4. Should `lifecycle` and `system` be added to scorecards as explicit quality rules, or is visibility in the service entity sufficient for issue #1?
