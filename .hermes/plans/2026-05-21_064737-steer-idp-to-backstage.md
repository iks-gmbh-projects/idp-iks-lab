# Backstage Steering Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Steer the IKS IDP lab away from a Port.io MVP toward a self-hosted Backstage-based MVP while preserving GitHub as the versioned source of truth and keeping the current low-risk catalog/IKS workflow boundary.

**Architecture:** Treat Backstage as the new target portal and Port as the superseded experiment. Keep the repository as a docs-and-configuration repo, introduce a Backstage-oriented catalog/configuration structure, migrate the existing Port concepts into Backstage catalog entities, TechDocs, templates, and issue-driven workflows, and record the architecture decision in the wiki ADRs. Do not add Kubernetes automation, runtime health, production provisioning, or autonomous compliance enforcement.

**Tech Stack:** Backstage OSS, Backstage Software Catalog, TechDocs, Software Templates/Scaffolder, GitHub issue templates/workflows, YAML validation, existing wiki submodule documentation.

---

## Current context / assumptions

- Current repository state is Port-centric:
  - `README.md` says Port provides the portal, catalog, scorecard, and workflow surface.
  - `port/` contains blueprints, entities, scorecards, actions, and a draft automation.
  - `wiki/docs/vision.md`, `wiki/docs/demo-story.md`, and `wiki/docs/operating-model.md` explicitly refer to Port.
  - `wiki/decisions/0001-use-port-for-idp-experiment.md` accepts Port as the MVP platform.
  - `github/issue-templates/` contains inactive reference issue templates, while `.github/ISSUE_TEMPLATE/` does not exist yet.
- User-provided research recommends Backstage as the strongest OSS-first, self-hosted candidate, with Red Hat Developer Hub as an enterprise Backstage option and other tools as secondary/POC alternatives.
- The target direction should be Backstage, not a broad product-selection matrix. The research should still be captured as rationale and comparison context.
- The repository remains the source of truth. Backstage should consume catalog metadata from GitHub rather than becoming the authoritative store.
- A meaningful architecture decision is being introduced, so a new ADR is expected. ADR 0001 should not be silently deleted; it should be superseded by a new ADR.
- In plan mode, no implementation, issue tracker mutation, commits, pushes, or wiki synchronization should be performed. External GitHub issues, if they exist, must be adjusted later in an execution phase.

## Proposed target structure

Introduce Backstage artifacts next to, then eventually instead of, Port artifacts:

```text
backstage/
  README.md
  app-config.example.yaml
  catalog/
    locations.yaml
    groups.yaml
    systems.yaml
    components.yaml
    resources.yaml
    apis.yaml              # optional if API metadata is introduced
  templates/
    service-onboarding/template.yaml
    iks-review-request/template.yaml
    catalog-metadata-fix/template.yaml
  techdocs/
    mkdocs.example.yaml
  scorecards/
    README.md              # documents scorecard/Tech Insights mapping and plugin choice
    iks-baseline.yaml      # optional target model, if a concrete scorecard plugin is chosen
    catalog-quality.yaml   # optional target model, if a concrete scorecard plugin is chosen
port/
  README.md                # mark as legacy/superseded experiment, if kept during transition
.github/
  ISSUE_TEMPLATE/
    catalog-metadata-fix.yml
    iks-review.yml
```

Keep existing `examples/services/*/catalog.yaml` during migration only if they are still useful as source examples. Prefer Backstage-native `catalog-info.yaml` files for each service once the migration starts:

```text
examples/services/customer-portal/catalog-info.yaml
examples/services/reporting-api/catalog-info.yaml
```

## Proposed Backstage concept mapping

| Current Port concept | Backstage target | Notes |
|---|---|---|
| `port/blueprints/team.yaml` | `kind: Group` | Map technical/business/IKS ownership into group metadata and relations. |
| `port/blueprints/system.yaml` | `kind: System` | Preserve system/domain grouping. |
| `port/blueprints/service.yaml` | `kind: Component`, `spec.type: service` | Move `lifecycle`, `owner`, `system` into native fields; keep IKS fields as annotations or metadata labels. |
| `port/blueprints/repository.yaml` | Component annotations and/or `kind: Resource` | Prefer standard Backstage annotations such as `backstage.io/source-location`; only create Resource entities if repository metadata needs first-class ownership. |
| `port/blueprints/workflow.yaml` | Software Template plus GitHub issue workflow | Keep workflow actions advisory and issue-based. |
| `port/blueprints/agent.yaml` | Documentation plus optional custom `kind` later | Do not build a custom Backstage entity kind until there is a concrete plugin/use case. |
| Port scorecards | Backstage Tech Insights / scorecard plugin decision | Capture as planned plugin selection; do not invent enforcement. |
| Port actions | Backstage Scaffolder templates or GitHub issue forms | Keep day-2 actions low-risk: create issue/checklist, no production mutations. |
| Port automation draft | Backstage docs or future workflow note | Keep metadata drift advisory-only unless a later ADR approves automation. |

## Step-by-step plan

### Task 1: Record the architecture decision to move from Port to Backstage

**Objective:** Make the strategic direction explicit and traceable.

**Files:**
- Create: `wiki/decisions/0003-adopt-backstage-for-self-hosted-idp.md`
- Modify: `wiki/decisions/0001-use-port-for-idp-experiment.md`
- Modify: `wiki/_Sidebar.md` if ADR links are listed manually

**Steps:**
1. Before editing wiki files in execution mode, run:
   - `git -C wiki switch master`
   - `git -C wiki pull --ff-only`
2. Create ADR 0003 with:
   - Status: `Angenommen` or `Proposed` depending on whether the user wants the direction final. Given the wording “steer the project to backstage”, use `Angenommen` unless told otherwise.
   - Context: Port MVP exists; research found no perfect self-hosted 1:1 Port replacement; Backstage is strongest OSS-first candidate; RHDH remains enterprise option.
   - Decision: Backstage OSS becomes the target MVP platform; GitHub remains source of truth; Port artifacts are kept only as migration reference until replaced.
   - Consequences: more self-hosting/integration effort, larger plugin/design responsibility, less SaaS dependency, stronger ecosystem and extensibility.
   - Explicit non-goals: no Kubernetes automation, runtime health, infrastructure provisioning, or autonomous compliance enforcement in the MVP.
3. Update ADR 0001 with a short note under the title or status:
   - `Superseded by ADR 0003` / `Abgeloest durch ADR 0003`.
4. If `wiki/_Sidebar.md` lists ADRs explicitly, add ADR 0003.

**Verification:**
- Read the ADRs and confirm that ADR 0001 is not contradictory without a supersession note.
- Confirm ADR 0003 cites the research conclusion in prose, not pasted citation artifacts such as `turn33search4`.

### Task 2: Rewrite the top-level project narrative around Backstage

**Objective:** Make `README.md` describe the new target platform and current transition state.

**Files:**
- Modify: `README.md`

**Steps:**
1. Change the opening from “Port-basierten Service-Katalog” to “Backstage-basierten, selbstgehosteten Service-Katalog”.
2. Keep “GitHub ist die versionierte Source of Truth” unchanged in substance.
3. Replace “Vorhanden im Repository” bullets that imply Port as target with transition-aware bullets:
   - current Port artifacts exist as migration source/reference;
   - planned Backstage catalog/configuration structure will become target;
   - issue templates and advisory workflows remain GitHub-backed.
4. Replace “Noch offen fuer den MVP-Betrieb” with Backstage-specific next steps:
   - create Backstage app/config baseline or decide whether to keep config-only repo;
   - define catalog locations;
   - migrate demo services to `catalog-info.yaml`;
   - decide scorecard plugin/Tech Insights approach;
   - wire Software Templates to GitHub issues;
   - run demo end-to-end in a local/self-hosted Backstage instance.
5. Update “Demo-Ablauf” to say Backstage opens the software catalog and templates create GitHub issues.
6. Update “Struktur” to include `backstage/` and mark `port/` as legacy/migration reference if retained.
7. Update “Naechste Schritte” to Backstage execution sequence.

**Verification:**
- Search `README.md` for `Port` and confirm remaining mentions are either historical/migration references or comparisons, not target-platform statements.

### Task 3: Update wiki vision, operating model, and demo story

**Objective:** Align the wiki with Backstage while preserving the MVP boundary.

**Files:**
- Modify: `wiki/docs/vision.md`
- Modify: `wiki/docs/operating-model.md`
- Modify: `wiki/docs/demo-story.md`
- Modify: `wiki/docs/iks-metadata-model.md` if service metadata representation changes from Port fields to Backstage annotations/labels/spec fields

**Steps:**
1. In `wiki/docs/vision.md`:
   - Replace “Port stellt ... bereit” with Backstage Software Catalog, TechDocs, Templates, and plugin ecosystem.
   - Add a short rationale: self-hosted OSS-first direction, reduced SaaS dependency, higher integration responsibility.
2. In `wiki/docs/operating-model.md`:
   - Replace “Port liest Metadaten ...” with “Backstage liest Catalog-Entities und Locations aus GitHub”.
   - Add Backstage-specific ownership of catalog descriptors and TechDocs.
   - Keep issue-based workflows and non-blocking scorecards.
3. In `wiki/docs/demo-story.md`:
   - Replace `Port oeffnet den Service-Katalog` with `Backstage oeffnet den Software Catalog`.
   - Replace “Action erzeugt ein GitHub Issue” with “Software Template oder GitHub Issue Form erzeugt eine Nachpflege-/Review-Aufgabe”.
   - Keep the `customer-portal` / `reporting-api` contrast.
4. In `wiki/docs/iks-metadata-model.md`:
   - Document where each field lives in Backstage, for example:
     - `metadata.name`
     - `metadata.description`
     - `spec.owner`
     - `spec.system`
     - `spec.lifecycle`
     - `metadata.annotations.iks.dev/business-owner`
     - `metadata.annotations.iks.dev/criticality`
     - `metadata.annotations.iks.dev/protection-need`
     - `metadata.annotations.iks.dev/data-class`
     - `metadata.annotations.iks.dev/compliance-scope`
     - `metadata.annotations.backstage.io/techdocs-ref`
     - `metadata.annotations.backstage.io/source-location`
   - Keep naming stable and simple. Avoid a custom Backstage plugin unless later required.

**Verification:**
- Search `wiki/docs` for `Port` and classify each remaining occurrence as historical, comparison, or migration reference.
- Confirm all MVP non-goals remain intact.

### Task 4: Add the Backstage target directory and baseline documentation

**Objective:** Establish a clear repo structure for Backstage configuration without creating an application runtime prematurely.

**Files:**
- Create: `backstage/README.md`
- Create: `backstage/app-config.example.yaml`
- Create: `backstage/catalog/locations.yaml`
- Create: `backstage/scorecards/README.md`
- Optional create: `backstage/techdocs/mkdocs.example.yaml`

**Steps:**
1. Create `backstage/README.md` explaining:
   - Backstage is the target portal.
   - This repo currently stores catalog/config examples, not necessarily a full Backstage app runtime.
   - GitHub remains source of truth.
   - `port/` is migration reference until removed or archived.
2. Create `backstage/app-config.example.yaml` with non-secret placeholders only:
   - `app.title: IKS Developer Portal`
   - catalog locations pointing at `backstage/catalog/locations.yaml` and/or service `catalog-info.yaml` files.
   - no credentials, tokens, real OAuth client secrets, or production URLs.
3. Create `backstage/catalog/locations.yaml` as the root catalog location list for the demo entities.
4. Create `backstage/scorecards/README.md` explaining the decision still needed for scorecards:
   - Backstage Tech Insights/custom plugin vs. a scorecard plugin.
   - MVP behavior remains advisory visibility, not enforcement.
5. If TechDocs examples are needed, create `backstage/techdocs/mkdocs.example.yaml` showing how service docs should be rendered.

**Verification:**
- Ensure all YAML files parse.
- Ensure no secrets or environment-specific endpoints are committed.

### Task 5: Migrate demo catalog entities to Backstage-native descriptors

**Objective:** Represent existing teams, systems, repositories, and services in Backstage catalog terms.

**Files:**
- Create: `backstage/catalog/groups.yaml`
- Create: `backstage/catalog/systems.yaml`
- Create: `backstage/catalog/components.yaml`
- Optional create: `backstage/catalog/resources.yaml`
- Create: `examples/services/customer-portal/catalog-info.yaml`
- Create: `examples/services/reporting-api/catalog-info.yaml`
- Read/reference: `port/entities/teams.yaml`
- Read/reference: `port/entities/systems.yaml`
- Read/reference: `port/entities/services.yaml`
- Read/reference: `port/entities/repositories.yaml`

**Steps:**
1. Map teams to `kind: Group` entities.
2. Map systems to `kind: System` entities.
3. Map services to `kind: Component` entities with:
   - `spec.type: service`
   - `spec.lifecycle` from current lifecycle
   - `spec.owner` from current technical owner relation
   - `spec.system` from current system relation
   - source/docs/runbook metadata as annotations or links.
4. Preserve IKS metadata as clearly namespaced annotations, for example:
   - `iks.dev/business-owner`
   - `iks.dev/criticality`
   - `iks.dev/protection-need`
   - `iks.dev/data-class`
   - `iks.dev/compliance-scope`
   - `iks.dev/runbook-url`
5. Keep `reporting-api` intentionally incomplete by omitting or emptying only the runbook annotation/link, so the demo still shows a metadata gap.
6. Add locations for the new descriptors to `backstage/catalog/locations.yaml`.

**Verification:**
- Confirm every owner and system referenced by a Component exists as a Group/System entity.
- Confirm `customer-portal` is complete and `reporting-api` intentionally lacks a runbook.
- If a Backstage CLI/app is available later, run catalog ingestion validation; otherwise validate YAML and manually inspect relations.

### Task 6: Convert Port actions into Backstage/GitHub advisory workflows

**Objective:** Replace Port self-service actions with Backstage Software Templates or active GitHub issue forms.

**Files:**
- Create: `backstage/templates/catalog-metadata-fix/template.yaml`
- Create: `backstage/templates/iks-review-request/template.yaml`
- Create: `backstage/templates/service-onboarding/template.yaml`
- Modify or archive-reference: `port/actions/create-github-issue-for-missing-metadata.yaml`
- Modify or archive-reference: `port/actions/request-iks-review.yaml`
- Modify or archive-reference: `port/actions/onboard-service-checklist.yaml`

**Steps:**
1. Define Backstage templates as advisory workflows only:
   - metadata fix request;
   - IKS review request;
   - service onboarding checklist.
2. Each template should gather the same low-risk fields as the current Port action:
   - target service/component;
   - missing field or review reason;
   - details/due date where relevant.
3. Decide implementation path for issue creation:
   - Option A: Backstage Scaffolder action that opens a GitHub issue.
   - Option B: Backstage template generates a prepared issue body/link and the active `.github/ISSUE_TEMPLATE` form captures it.
4. For the MVP, prefer the least risky implementation that does not require a custom backend action unless necessary.
5. Mark old Port action files as migration references or move them under a legacy note only after the Backstage replacement exists.

**Verification:**
- Confirm no template provisions infrastructure or changes production systems.
- Confirm templates create only GitHub-tracked follow-up work.

### Task 7: Adjust issue structure and templates

**Objective:** Make repository issues match the Backstage target workflows and activate templates under GitHub’s expected path.

**Files:**
- Create: `.github/ISSUE_TEMPLATE/catalog-metadata-fix.yml`
- Create: `.github/ISSUE_TEMPLATE/iks-review.yml`
- Optional create: `.github/ISSUE_TEMPLATE/backstage-migration.yml`
- Optional create: `.github/ISSUE_TEMPLATE/config.yml`
- Modify or deprecate: `github/issue-templates/catalog-metadata-fix.md`
- Modify or deprecate: `github/issue-templates/iks-review.md`
- Modify: `README.md` structure section
- Modify: `agents/validation.md` if validation scope should include `.github/ISSUE_TEMPLATE`

**Steps:**
1. Convert existing markdown issue templates into active GitHub Issue Forms under `.github/ISSUE_TEMPLATE/`.
2. Rename wording from “Port service identifier” to “Backstage component/entity reference”.
3. Add fields that support the Backstage migration:
   - `component_ref` such as `component:default/customer-portal`;
   - affected catalog descriptor path;
   - missing metadata category;
   - expected owner/reviewer;
   - acceptance criteria.
4. Add an optional `backstage-migration.yml` issue form for migration tasks with fields:
   - area: docs/catalog/templates/scorecards/validation;
   - source Port file;
   - target Backstage file;
   - validation evidence.
5. Decide what to do with `github/issue-templates/`:
   - either keep as reference copies and state they are not active;
   - or replace with a README pointing to `.github/ISSUE_TEMPLATE/`.
6. If there are real open GitHub issues in the remote tracker, adjust them only in a later execution step after explicit approval. Plan-mode does not mutate external issues.

**Verification:**
- Confirm `.github/ISSUE_TEMPLATE/*.yml` forms are syntactically valid YAML.
- Confirm issue wording no longer names Port as the target system except in migration context.

### Task 8: Reframe scorecards for Backstage

**Objective:** Preserve catalog-quality and IKS-baseline checks without pretending Port scorecards work in Backstage unchanged.

**Files:**
- Create/modify: `backstage/scorecards/README.md`
- Optional create: `backstage/scorecards/catalog-quality.yaml`
- Optional create: `backstage/scorecards/iks-baseline.yaml`
- Modify/reference: `port/scorecards/catalog-quality.yaml`
- Modify/reference: `port/scorecards/iks-baseline.yaml`
- Modify: `wiki/docs/demo-story.md`
- Modify: `wiki/docs/iks-metadata-model.md`

**Steps:**
1. Document the scorecard target as a design decision still inside the Backstage adoption path:
   - preferred: Backstage Tech Insights checks if sufficient;
   - alternative: a maintained scorecard plugin;
   - fallback: GitHub validation script/report for MVP demo.
2. Map each current scorecard rule to a Backstage field/annotation.
3. Keep levels (`bronze`, `silver`, `gold`) as conceptual maturity levels unless the chosen plugin has a different model.
4. Ensure `reporting-api` remains the negative example for missing runbook.
5. Do not enforce blocking behavior in CI unless a later governance decision changes the MVP boundary.

**Verification:**
- Confirm every current Port scorecard rule has a documented Backstage equivalent or an explicit “deferred” reason.

### Task 9: Update agent artifacts and checklists for Backstage

**Objective:** Prevent repo agents from continuing to plan Port-centric changes.

**Files:**
- Modify: `AGENTS.md`
- Modify: `agents/README.md`
- Modify: `agents/validation.md`
- Modify: `agents/checklists/port-catalog-change.md` or replace with `agents/checklists/backstage-catalog-change.md`
- Modify: `agents/prompts/catalog-maintenance.md`
- Modify: `agents/prompts/change-planning.md`
- Modify: `agents/skills/port-catalog-maintainer/SKILL.md` or create a new Backstage skill source and deprecate the Port one
- Modify: `agents/skills/port-catalog-maintainer/references/port-catalog-map.md` or create Backstage map equivalent

**Steps:**
1. Update `AGENTS.md` mission from Port configuration to Backstage catalog/configuration, while keeping GitHub source-of-truth and MVP boundaries.
2. Rename or deprecate Port-specific checklists/prompts.
3. Add Backstage-specific validation guidance:
   - YAML syntax for `backstage`, `examples`, `agents`, `.github/ISSUE_TEMPLATE`;
   - catalog relation consistency;
   - TechDocs descriptor checks if used;
   - no secrets in `app-config.example.yaml`.
4. For repo-versioned skills, prefer creating a new `agents/skills/backstage-catalog-maintainer/` over rewriting the Port skill in place, so history remains clear.
5. Update references to stable Backstage entity names and annotations.

**Verification:**
- Search `agents/` for `Port` and classify remaining occurrences as legacy/migration only.
- Validate any changed skill with the Codex skill validator if available.

### Task 10: Update validation workflows and local checks

**Objective:** Ensure CI validates the new Backstage and issue-template surfaces.

**Files:**
- Modify: `.github/workflows/validate-port-config.yml`
- Modify: `github/workflows/validate-port-config.yml`
- Optional rename later: `.github/workflows/validate-idp-config.yml`
- Optional rename later: `github/workflows/validate-idp-config.yml`
- Modify: `README.md`
- Modify: `agents/validation.md`

**Steps:**
1. Rename workflow display name from Port-specific to IDP/Backstage-specific.
2. Expand YAML lint paths to include:
   - `backstage`
   - `examples`
   - `agents`
   - `.github/ISSUE_TEMPLATE`
3. Keep the template/reference workflow under `github/workflows/` in sync with the active workflow under `.github/workflows/`.
4. If file renaming is too disruptive for one PR, keep filenames temporarily and add a follow-up issue to rename from `validate-port-config` to `validate-idp-config`.

**Verification:**
- Run: `yamllint backstage examples agents .github/ISSUE_TEMPLATE`
- If `yamllint` is unavailable, parse touched YAML with Python or another available YAML parser and document the fallback.

### Task 11: Decide Port artifact lifecycle

**Objective:** Avoid ambiguity about whether `port/` is still active.

**Files:**
- Create or modify: `port/README.md`
- Modify: `README.md`
- Modify: `wiki/docs/operating-model.md`
- Optional later: move `port/` to `legacy/port/` in a dedicated cleanup PR

**Steps:**
1. For the first migration PR, keep `port/` in place to reduce churn.
2. Add `port/README.md` saying:
   - Port artifacts are retained as migration reference for the previous experiment.
   - Backstage artifacts under `backstage/` are the target path.
   - Do not add new Port-only capabilities unless the task is explicitly about migration comparison.
3. Create a follow-up issue to remove/archive `port/` after Backstage catalog, templates, and validation are in place.

**Verification:**
- Search root docs for `port/` and ensure it is described as legacy/migration reference.

### Task 12: Create/adjust issues for the migration work

**Objective:** Translate this plan into trackable work items without mutating external trackers during plan mode.

**Files:**
- Create/update issue forms from Task 7 first.
- External GitHub issues: adjust only after user approval in execution mode.

**Proposed issue set:**
1. `ADR: Adopt Backstage as self-hosted IDP target`
   - Covers Task 1.
2. `Docs: Reframe README and wiki from Port MVP to Backstage MVP`
   - Covers Tasks 2 and 3.
3. `Catalog: Add Backstage catalog structure and migrate demo entities`
   - Covers Tasks 4 and 5.
4. `Workflows: Replace Port actions with Backstage/GitHub issue workflows`
   - Covers Tasks 6 and 7.
5. `Scorecards: Map IKS baseline and catalog quality to Backstage approach`
   - Covers Task 8.
6. `Agents: Update repo guidance, prompts, checklists, and skills for Backstage`
   - Covers Task 9.
7. `CI: Validate Backstage catalog and GitHub issue forms`
   - Covers Task 10.
8. `Cleanup: Mark Port artifacts legacy and plan removal/archive`
   - Covers Task 11.

**Verification:**
- Each issue should include source files, target files, acceptance criteria, and validation command.
- Do not close or edit existing remote issues without explicit user approval.

## Files likely to change

High-confidence changes:
- `README.md`
- `AGENTS.md`
- `.github/workflows/validate-port-config.yml`
- `github/workflows/validate-port-config.yml`
- `.github/ISSUE_TEMPLATE/catalog-metadata-fix.yml`
- `.github/ISSUE_TEMPLATE/iks-review.yml`
- `github/issue-templates/catalog-metadata-fix.md`
- `github/issue-templates/iks-review.md`
- `wiki/docs/vision.md`
- `wiki/docs/operating-model.md`
- `wiki/docs/demo-story.md`
- `wiki/docs/iks-metadata-model.md`
- `wiki/decisions/0001-use-port-for-idp-experiment.md`
- `wiki/decisions/0003-adopt-backstage-for-self-hosted-idp.md`
- `backstage/README.md`
- `backstage/app-config.example.yaml`
- `backstage/catalog/locations.yaml`
- `backstage/catalog/groups.yaml`
- `backstage/catalog/systems.yaml`
- `backstage/catalog/components.yaml`
- `backstage/templates/catalog-metadata-fix/template.yaml`
- `backstage/templates/iks-review-request/template.yaml`
- `backstage/templates/service-onboarding/template.yaml`
- `backstage/scorecards/README.md`
- `examples/services/customer-portal/catalog-info.yaml`
- `examples/services/reporting-api/catalog-info.yaml`
- `port/README.md`
- `agents/validation.md`
- `agents/checklists/port-catalog-change.md` or replacement `agents/checklists/backstage-catalog-change.md`
- `agents/prompts/catalog-maintenance.md`
- `agents/prompts/change-planning.md`

Possible changes if the migration is implemented more completely:
- `agents/skills/backstage-catalog-maintainer/SKILL.md`
- `agents/skills/backstage-catalog-maintainer/references/backstage-catalog-map.md`
- `agents/skills/*/agents/openai.yaml`
- `wiki/_Sidebar.md`
- `package.json` / `package-lock.json` only if Backstage tooling or validation dependencies are added. Avoid adding dependencies unless needed.

## Documentation updates and ADR expectations

- ADR required: yes. The move from Port to Backstage is a meaningful architectural and governance decision.
- Recommended ADR: `wiki/decisions/0003-adopt-backstage-for-self-hosted-idp.md`.
- ADR 0001 should be marked superseded, not removed.
- ADR 0002 should remain valid: Kubernetes, runtime health, and deployment status stay outside the MVP even after moving to Backstage.
- Wiki docs must be updated before or alongside catalog/template changes so the repo does not describe a Port target while adding Backstage artifacts.

## Tests / validation

Minimum validation after implementation:

```bash
yamllint backstage examples agents .github/ISSUE_TEMPLATE
```

If existing Port YAML remains touched:

```bash
yamllint port backstage examples agents .github/ISSUE_TEMPLATE
```

Workflow parity check:

```bash
diff -u .github/workflows/validate-port-config.yml github/workflows/validate-port-config.yml
```

Search checks:

```bash
rg -n "Port|port.io|port/" README.md AGENTS.md wiki agents backstage github .github examples
rg -n "Backstage|catalog-info|Software Catalog|TechDocs|Scaffolder" README.md wiki backstage examples agents
```

Manual consistency pass:
- New required IKS metadata fields are documented in `wiki/docs/iks-metadata-model.md`.
- Every Backstage Component has an existing owner Group and System.
- `customer-portal` remains the complete example.
- `reporting-api` remains the incomplete runbook example.
- Issue forms use Backstage entity references, not Port service identifiers.
- No secrets are present in Backstage example config.
- No Kubernetes/runtime/provisioning automation was added.

Wiki-specific execution requirement:
- Before wiki edits: `git -C wiki switch master && git -C wiki pull --ff-only`.
- Commit and push wiki changes inside `wiki`, then commit the updated submodule pointer in the main repository. Do this only in execution mode with user approval for push.

## Risks, tradeoffs, and open questions

### Risks

- Backstage is more flexible than Port but requires more local design and operations work.
- Scorecards are not a direct 1:1 migration; a plugin/Tech Insights decision is needed.
- Backstage Software Templates may require backend actions or GitHub credentials for direct issue creation.
- Keeping `port/` during migration may confuse contributors unless clearly marked legacy.
- Wiki submodule changes require careful two-repository commit handling.

### Tradeoffs

- Backstage reduces SaaS dependency and aligns with self-hosting, but increases implementation responsibility.
- Red Hat Developer Hub may reduce enterprise operational risk later, but using pure Backstage first keeps the MVP OSS-first and vendor-neutral.
- Active GitHub Issue Forms are simpler and lower-risk than custom Scaffolder issue creation, but less seamless inside the portal.
- Keeping Port artifacts temporarily makes migration safer but delays cleanup.

### Open questions

1. Should the MVP include a runnable Backstage app in this repository, or only Backstage catalog/config examples consumed by a separately managed Backstage instance?
2. Which scorecard mechanism should be selected: Backstage Tech Insights, a maintained scorecard plugin, or a GitHub-generated report for the first MVP?
3. Should Port artifacts be archived in place, moved to `legacy/port/`, or deleted after migration?
4. Should Red Hat Developer Hub be documented as a later enterprise deployment option, or kept only in the ADR rationale?
5. Should issue creation happen directly through Backstage Scaffolder, or should Backstage guide users into GitHub Issue Forms for the MVP?

## Deferred actions because this is plan mode

- No project files were changed except this plan file.
- No external GitHub issues were created, edited, commented on, assigned, or closed.
- No commits or pushes were made.
- No wiki submodule synchronization or wiki commit was performed.
