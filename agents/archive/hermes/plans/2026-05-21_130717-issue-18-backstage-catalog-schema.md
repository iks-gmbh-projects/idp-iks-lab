# Issue #18 Plan: Finalize Backstage Catalog Schema and GitHub Source-of-Truth Format

> Plan mode only. Do not implement, commit, push, or mutate GitHub issues while following this plan unless execution is explicitly approved later.

## Goal

Implement GitHub issue #18: finalize the Backstage catalog data model for the MVP, preserve required IKS metadata from the legacy Port-oriented YAML, and make the GitHub source-of-truth/import model unambiguous.

Issue: [#18 Backstage IDP MVP: Finalize catalog schema and GitHub source-of-truth format](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/18)

## Current Context / Assumptions

- `main` is the working baseline according to the current user context.
- Backstage is now the active target path; `port/` is retained as legacy migration reference only.
- The repository is still a docs-and-configuration repo, not a production runtime repository.
- The MVP boundary remains unchanged:
  - no Kubernetes automation,
  - no production infrastructure changes,
  - no autonomous compliance enforcement.
- Existing Backstage files already present:
  - `backstage/catalog/locations.yaml`
  - `backstage/catalog/groups.yaml`
  - `backstage/catalog/systems.yaml`
  - `backstage/catalog/components.yaml`
  - `examples/services/customer-portal/catalog-info.yaml`
  - `examples/services/reporting-api/catalog-info.yaml`
  - `backstage/README.md`
  - `backstage/scorecards/README.md`
  - `wiki/docs/iks-metadata-model.md`
- Current import intent from `backstage/README.md`:
  - service `Component` entities are imported from `examples/services/*/catalog-info.yaml`;
  - `backstage/catalog/components.yaml` is retained as a central reference copy during migration.
- Current `backstage/catalog/locations.yaml` imports:
  - groups,
  - systems,
  - templates,
  - service-local `catalog-info.yaml` files.
- It does not currently import `backstage/catalog/components.yaml`, which avoids duplicate `Component` entity refs.
- `reporting-api` intentionally lacks `iks.dev/runbook-url` and a runbook link; this must remain representable for the demo.

## Proposed Approach

Treat #18 as a schema/source-of-truth tightening task, not a runtime task.

1. Make service-local `examples/services/*/catalog-info.yaml` the authoritative import source for service `Component` entities.
2. Keep `backstage/catalog/components.yaml` only if it is clearly labelled as reference/migration copy, or remove it from active paths if it creates confusion.
3. Document Backstage entity shapes for:
   - `Component`,
   - `System`,
   - `Group`,
   - `Location`.
4. Document the Port-to-Backstage migration mapping in a stable repository location.
5. Validate current examples against the schema expectations and fix only real mismatches.
6. Keep scorecard/check logic advisory and field-based; defer plugin/runtime choice to issue #21.

## Step-by-Step Plan

### Step 1: Confirm the live baseline and issue state

Read-only checks before editing:

```bash
git checkout main
git pull --ff-only origin main
git status --short --branch
gh issue view 18 --json number,title,state,body,labels,url
```

Acceptance:
- Working tree is clean before implementation starts.
- Issue #18 is still open or intentionally selected for completion.
- No issue mutation is performed during this confirmation.

### Step 2: Inventory current Backstage and legacy Port catalog artifacts

Inspect:

```bash
git ls-files 'backstage/**' 'examples/services/**/catalog-info.yaml' 'port/blueprints/*.yaml' 'port/entities/*.yaml' 'examples/services/*/catalog.yaml'
```

Read at least:

- `backstage/README.md`
- `backstage/catalog/locations.yaml`
- `backstage/catalog/groups.yaml`
- `backstage/catalog/systems.yaml`
- `backstage/catalog/components.yaml`
- `examples/services/customer-portal/catalog-info.yaml`
- `examples/services/reporting-api/catalog-info.yaml`
- `wiki/docs/iks-metadata-model.md`
- `port/blueprints/service.yaml`
- `port/entities/services.yaml`
- `examples/services/customer-portal/catalog.yaml`
- `examples/services/reporting-api/catalog.yaml`

Acceptance:
- The implementation starts from the actual merged main state.
- Any current drift between central reference components and service-local components is known before editing.

### Step 3: Decide the documentation home for schema and migration mapping

Recommended documentation split:

- `wiki/docs/iks-metadata-model.md`
  - normative MVP schema for service metadata and Backstage field/annotation placement.
- `backstage/README.md`
  - concise repository import model and source-of-truth rules.
- New file if needed: `backstage/catalog/README.md`
  - Backstage entity shapes for `Location`, `Group`, `System`, and `Component`.
  - import-source rules.
  - duplicate-entity guardrails.
  - Port-to-Backstage artifact mapping.

Preferred implementation:
- Create `backstage/catalog/README.md` rather than overloading the root `backstage/README.md`.

Acceptance:
- A contributor can find the catalog schema and source-of-truth rules without reading old plans or GitHub issues.

### Step 4: Document the Backstage entity shapes

In `backstage/catalog/README.md` or equivalent docs, describe the intended shape:

#### `Location`

- Source file: `backstage/catalog/locations.yaml`
- Purpose: root import list for demo catalog data and templates.
- Expected imports:
  - `./groups.yaml`
  - `./systems.yaml`
  - Backstage Software Templates under `backstage/templates/`
  - service-local `examples/services/*/catalog-info.yaml`
- Explicit rule:
  - Do not import `backstage/catalog/components.yaml` and service-local `catalog-info.yaml` files for the same `Component` refs at the same time.

#### `Group`

- Source file: `backstage/catalog/groups.yaml`
- Required MVP fields:
  - `apiVersion`
  - `kind: Group`
  - `metadata.name`
  - `metadata.title`
  - `spec.type`
  - `spec.profile.displayName`
- Recommended fields:
  - `metadata.description`
  - `spec.profile.email`
  - `metadata.annotations.iks.dev/area`
- Must cover current refs:
  - `platform-team`
  - `iks-review-board`
  - `customer-success`

#### `System`

- Source file: `backstage/catalog/systems.yaml`
- Required MVP fields:
  - `apiVersion`
  - `kind: System`
  - `metadata.name`
  - `metadata.title`
  - `spec.owner`
- Recommended IKS field:
  - `metadata.annotations.iks.dev/domain`
- Must cover current service refs:
  - `customer-experience`
  - `management-reporting`

#### `Component`

- Authoritative import source: `examples/services/*/catalog-info.yaml`
- Reference-only copy: `backstage/catalog/components.yaml`
- Required MVP fields:
  - `apiVersion: backstage.io/v1alpha1`
  - `kind: Component`
  - `metadata.name`
  - `metadata.title`
  - `metadata.description`
  - `metadata.annotations.backstage.io/source-location`
  - `metadata.annotations.backstage.io/techdocs-ref`
  - `metadata.annotations.iks.dev/business-owner`
  - `metadata.annotations.iks.dev/criticality`
  - `metadata.annotations.iks.dev/protection-need`
  - `metadata.annotations.iks.dev/data-class`
  - `metadata.annotations.iks.dev/compliance-scope`
  - `spec.type: service`
  - `spec.lifecycle`
  - `spec.owner`
  - `spec.system`
- Optional/advisory MVP field:
  - `metadata.annotations.iks.dev/runbook-url`
- Link guidance:
  - documentation link should be present for demo readability;
  - runbook link should be present when `iks.dev/runbook-url` exists;
  - missing runbook remains valid but should be visible in catalog-quality checks.

Acceptance:
- Entity shapes are explicit enough to satisfy issue #18 without requiring a running Backstage instance.

### Step 5: Document the required MVP service fields and mapping

Update `wiki/docs/iks-metadata-model.md` if needed so it clearly states:

| Requirement | Backstage location | Required for MVP? |
|---|---|---|
| Service name | `metadata.name` / `metadata.title` | yes |
| Technical owner | `spec.owner` | yes |
| Business owner | `metadata.annotations.iks.dev/business-owner` | yes |
| System | `spec.system` | yes |
| Repository | `metadata.annotations.backstage.io/source-location` | yes |
| Lifecycle | `spec.lifecycle` | yes |
| Criticality | `metadata.annotations.iks.dev/criticality` | yes |
| Protection need | `metadata.annotations.iks.dev/protection-need` | yes |
| Data class | `metadata.annotations.iks.dev/data-class` | yes |
| Documentation | `metadata.annotations.backstage.io/techdocs-ref` and/or docs link | yes |
| Runbook | `metadata.annotations.iks.dev/runbook-url` and/or runbook link | advisory / expected hygiene |
| Compliance scope | `metadata.annotations.iks.dev/compliance-scope` | yes |

Important nuance:
- The issue text lists runbook among required fields to preserve.
- The current metadata model intentionally allows `reporting-api` to miss the runbook to demonstrate scorecard/check failure.
- Therefore the implementation should say: runbook support is part of the schema, but a missing runbook is an allowed incomplete-demo condition, not a catalog-ingestion failure.

Acceptance:
- `reporting-api` remains intentionally incomplete but schema-compatible.
- The docs do not contradict the demo story.

### Step 6: Add Port-to-Backstage migration mapping

Document the mapping from legacy artifacts to Backstage equivalents:

| Legacy Port artifact/concept | Backstage target | Notes |
|---|---|---|
| `port/blueprints/team.yaml` / `port/entities/teams.yaml` | `kind: Group` in `backstage/catalog/groups.yaml` | Keep owner refs stable. |
| `port/blueprints/system.yaml` / `port/entities/systems.yaml` | `kind: System` in `backstage/catalog/systems.yaml` | Preserve domain via `iks.dev/domain`. |
| `port/blueprints/service.yaml` / `port/entities/services.yaml` | service-local `kind: Component` in `examples/services/*/catalog-info.yaml` | Components are imported from service-local files. |
| `port/blueprints/repository.yaml` / `port/entities/repositories.yaml` | `backstage.io/source-location` annotation, optionally links/resources later | Do not add `Resource` entities unless a later issue needs them. |
| `port/blueprints/workflow.yaml` / `port/actions/*.yaml` | Backstage Software Templates and GitHub Issue Forms | Advisory workflows only. |
| `port/scorecards/*.yaml` | `backstage/scorecards/README.md` mapping to Tech Insights/plugin/local report | Implementation choice belongs to #21. |
| `examples/services/*/catalog.yaml` | legacy service-local Port reference | Backstage source is `catalog-info.yaml`. |

Acceptance:
- The mapping is findable from either `backstage/README.md` or `backstage/catalog/README.md`.
- The mapping does not imply future Port expansion.

### Step 7: Enforce the source-of-truth rule in docs and files

Check/update:

- `backstage/README.md`
- `backstage/catalog/README.md` if created
- `backstage/catalog/locations.yaml`
- `backstage/catalog/components.yaml`

Rules:

1. Service `Component` source of truth:
   - `examples/services/customer-portal/catalog-info.yaml`
   - `examples/services/reporting-api/catalog-info.yaml`
2. `backstage/catalog/components.yaml`:
   - retain as reference-only migration copy, or remove if the team decides reference copies are harmful;
   - if retained, add a comment at the top if acceptable for YAML consumers, or document the status prominently in `backstage/catalog/README.md`.
3. `backstage/catalog/locations.yaml`:
   - must not import `backstage/catalog/components.yaml` while service-local files are imported.

Acceptance:
- Duplicate `Component` import risk is explicitly documented and avoided.

### Step 8: Validate current demo entity references

Manually or with a small local script, verify:

- Every service `spec.owner` resolves to a `Group`:
  - `group:default/platform-team` -> `platform-team` exists in `backstage/catalog/groups.yaml`.
- Every service `spec.system` resolves to a `System`:
  - `customer-experience` exists.
  - `management-reporting` exists.
- Every `iks.dev/business-owner` resolves to a `Group` or documented business-owner identifier:
  - `customer-success` exists in `backstage/catalog/groups.yaml`.
- `reporting-api` has no runbook and remains documented as intentionally incomplete.
- `locations.yaml` does not import duplicate component sources.

Acceptance:
- Any mismatch is fixed in the catalog files or documented as intentional.

### Step 9: Update validation expectations

Update docs to say validation for #18 includes:

```bash
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
```

If `yamllint` is unavailable locally, use an available YAML parser or state that only manual read-through was performed.

Recommended additional local script/check during implementation:

- parse all YAML under:
  - `backstage/`
  - `examples/services/*/catalog-info.yaml`
- extract entity refs from service Components;
- detect duplicate `(kind, namespace, name)` refs across imported targets in `backstage/catalog/locations.yaml`;
- verify owner/system refs exist.

This can be an uncommitted one-off script unless the project wants a permanent validator in a later issue.

Acceptance:
- The validation approach is documented even if full Backstage catalog ingestion is deferred to #19/#24.

### Step 10: Run validation and prepare review summary

Run:

```bash
git diff --check
# if available:
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
# optional/manual:
git status --short
git -C wiki status --short
```

Manual read-through:

- `backstage/README.md`
- `backstage/catalog/README.md` if created
- `wiki/docs/iks-metadata-model.md`
- `backstage/catalog/locations.yaml`
- both service-local `catalog-info.yaml` files

Acceptance:
- Review summary can state exactly what changed, why, and how duplicate imports are avoided.

## Files Likely to Change

Primary expected changes:

- `backstage/catalog/README.md` — likely new catalog schema/source-of-truth documentation.
- `backstage/README.md` — add/strengthen pointer to catalog schema and import rules.
- `wiki/docs/iks-metadata-model.md` — clarify required fields, runbook nuance, and source-of-truth wording.

Potential changes if inspection finds drift:

- `backstage/catalog/locations.yaml` — only if duplicate import risk or missing target is found.
- `backstage/catalog/components.yaml` — add reference-only comment if acceptable, update to match service-local files, or consider removing in a separate cleanup if it is too confusing.
- `examples/services/customer-portal/catalog-info.yaml` — only if required metadata is missing or inconsistent.
- `examples/services/reporting-api/catalog-info.yaml` — preserve missing runbook intentionally; only fix other required metadata mismatches.
- `backstage/catalog/groups.yaml` — only if referenced owner/business-owner groups are missing.
- `backstage/catalog/systems.yaml` — only if referenced systems are missing.

Do not change unless specifically required:

- `port/**` — legacy migration reference only.
- runtime/deployment files — #18 is schema/source-of-truth work, not runtime work.
- `.github/workflows/**` — only change if validation docs and workflow are out of sync.

## Documentation / ADR Expectations

Documentation updates are expected.

Expected docs:

- `backstage/catalog/README.md` for catalog schema/import-source rules.
- `wiki/docs/iks-metadata-model.md` for normative IKS metadata placement.
- `backstage/README.md` for navigation to the schema docs.

ADR expectation:

- No new ADR is expected for #18 if the implementation only finalizes schema/source-of-truth details under the already accepted Backstage direction.
- A new ADR would be appropriate only if the implementation changes a meaningful architectural decision, for example:
  - choosing to store all Components centrally in `backstage/catalog/components.yaml` instead of service-local `catalog-info.yaml` files;
  - introducing custom Backstage entity kinds;
  - making scorecard checks blocking/enforcing;
  - adding runtime/Kubernetes deployment scope.

## Tests / Validation

Minimum validation:

```bash
git diff --check
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
git status --short
git -C wiki status --short
```

If `yamllint` is unavailable:

- parse changed YAML with any available local YAML parser;
- manually inspect the changed YAML and Markdown;
- explicitly state the validator was unavailable.

Catalog consistency validation:

- Confirm `backstage/catalog/locations.yaml` imports service Components from `examples/services/*/catalog-info.yaml` and not from `backstage/catalog/components.yaml`.
- Confirm `Component` refs are unique among imported files.
- Confirm `spec.owner` and `spec.system` refs resolve.
- Confirm required IKS annotations are present for both demo services except the intentional `reporting-api` runbook gap.
- Confirm docs describe runbook as schema-supported but demo-advisory rather than an ingestion blocker.

## Risks, Tradeoffs, and Open Questions

- **Central reference copy drift:** Keeping `backstage/catalog/components.yaml` as reference-only may confuse contributors if it diverges from service-local `catalog-info.yaml`. Mitigation: document it clearly, keep it synchronized if retained, or plan a later removal.
- **Runbook requirement ambiguity:** Issue #18 says runbook is required to preserve, while the demo intentionally omits it for `reporting-api`. Mitigation: define runbook as a supported schema field and expected hygiene check, not a hard ingestion requirement.
- **Business-owner relation ambiguity:** `iks.dev/business-owner` currently stores `customer-success`. Decide whether docs require this to resolve to a Backstage `Group` or allow it as a business identifier. Recommended MVP rule: prefer resolvable `Group` names.
- **Backstage ingestion not yet available:** Without a runnable Backstage app, validation is YAML/manual/reference checking. Full ingestion validation belongs to #19/#24.
- **Port artifact scope:** Do not edit legacy Port artifacts unless a concrete mismatch in the migration mapping requires a comment/doc pointer. The target schema should live in Backstage docs.

## Artifact Inventory / Traceability

Plan artifact created by this planning turn:

- `agents/archive/hermes/plans/2026-05-21_130717-issue-18-backstage-catalog-schema.md`
  - Purpose: implementation plan for issue #18.
  - Status: local plan file written in plan mode.
  - Tracking/commit status: not committed by this plan-mode turn unless a later execution step explicitly stages and commits it.

External tracker referenced:

- GitHub issue #18: `Backstage IDP MVP: Finalize catalog schema and GitHub source-of-truth format`
  - URL: https://github.com/iks-gmbh-projects/idp-iks-lab/issues/18
  - Status observed during planning: open.
  - Mutation status: no issue comment, edit, assignment, label, close, PR, or other tracker mutation performed in plan mode.

No companion snapshot under `agents/archive/hermes/tmp/` is required for #18 unless a later implementation wants to capture a before/after schema inventory.

## Deferred Actions Because This Was Plan Mode

- No catalog/docs implementation was performed.
- No GitHub issue was edited, commented on, closed, assigned, or labeled.
- No branch was created.
- No commit, push, or PR was made.
