# Issue #20 Catalog Views and Filters Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Configure the repository-owned Backstage catalog metadata and demo documentation so the MVP can demonstrate all services, IKS-relevant services, critical services, and service detail metadata without committing a generated Backstage app.

**Architecture:** Keep `idp-iks-lab` as a docs/config/catalog repository. Use portable Backstage catalog metadata (`metadata.tags` plus existing IKS annotations, owners, systems, links, and source-location annotations) to support default Catalog UI filters where possible, and document a deterministic demo navigation path for views that require custom Backstage UI columns/filters later. Do not add Kubernetes automation, production runtime code, or a generated Backstage app tree.

**Tech Stack:** Backstage catalog YAML (`Component`, `Group`, `System`, `Location`), Markdown docs, GitHub Actions `validate-idp-config.yml` YAML validation, optional local `yamllint`.

---

## Current Context / Assumptions

- Target issue: #20 `Backstage IDP MVP: Configure service catalog views and filters`
  - URL: `https://github.com/iks-gmbh-projects/idp-iks-lab/issues/20`
  - State at planning time: open.
- Issue #20 requires demo paths for:
  - all services,
  - IKS-relevant services where `complianceScope` contains `iks`,
  - critical services where `criticality` is `high` or `critical`,
  - service detail page showing owner, business owner, system, repository, lifecycle, documentation, runbook, criticality, protection need, data class, and compliance scope.
- The repository currently does **not** commit a generated Backstage app. PR #31 documented an external generated runtime path under `backstage/runtime/`.
- Existing authoritative Component entities are service-local:
  - `examples/services/customer-portal/catalog-info.yaml`
  - `examples/services/reporting-api/catalog-info.yaml`
- Existing demo services:
  - `customer-portal`: complete demo service; has runbook annotation/link; `iks.dev/criticality: high`; `iks.dev/compliance-scope: iks,gdpr`.
  - `reporting-api`: intentionally incomplete; missing runbook annotation/link; `iks.dev/criticality: medium`; `iks.dev/compliance-scope: iks`.
- Existing demo story already says the demo filters by `iks.dev/compliance-scope` and `iks.dev/criticality`, but default Backstage Catalog UI may not provide arbitrary annotation filters without app customization.
- Plan-mode constraint for this turn:
  - This plan file is the only project file changed.
  - No implementation, commits, pushes, issue comments, issue edits, PR creation, or tracker mutation were performed.

## Proposed Approach

Implement issue #20 as a small docs/catalog PR with two layers:

1. **Default Backstage UI support:** add stable `metadata.tags` to the demo `Component` entities so the standard Catalog UI can support simple demo filtering/search without app customization.
   - Both services get `iks`.
   - `customer-portal` gets a criticality tag such as `criticality-high` because its annotation has `iks.dev/criticality: high`.
   - `reporting-api` gets a non-critical tag such as `criticality-medium` to show why it should not appear in the critical-service view.
2. **Repository-owned demo navigation docs:** create a concise catalog demo view guide explaining:
   - which Backstage catalog page/filter/search to use for all services,
   - how to identify IKS-relevant services via `metadata.tags: iks` and/or `iks.dev/compliance-scope`,
   - how to identify critical services via `metadata.tags: criticality-high` / `criticality-critical` and/or `iks.dev/criticality`,
   - which detail-page fields prove the demo story for `customer-portal` and `reporting-api`,
   - what remains deferred to a future generated-app customization if stakeholders require custom table columns or first-class annotation filters.
3. **Keep config source-of-truth aligned:** update catalog schema docs and top-level/demo docs to point to the new guide and tag convention.

This avoids adding an app plugin or generated Backstage source tree while still making #20 demonstrable from the repository and local runtime path.

## Step-by-Step Plan

### Task 1: Create a feature branch and confirm current tracker/repo state

**Objective:** Start implementation from clean `main` and make the branch traceable to #20.

**Files:**
- No file edits in this task.

**Steps:**

1. Confirm local state:

   ```bash
   git fetch --prune origin
   git status --short --branch
   gh issue view 20 --json number,title,state,url
   gh pr list --state open --limit 20 --json number,title,headRefName,baseRefName,url
   ```

   Expected:
   - on `main`, aligned with `origin/main`, clean working tree,
   - issue #20 is open,
   - no conflicting open PR for #20.

2. Inspect or create the issue-linked branch:

   ```bash
   gh issue develop --list 20
   ```

   If no linked branch exists, create/check out one:

   ```bash
   gh issue develop 20 --base main --checkout
   ```

   If a linked branch already exists, check it out and fast-forward/rebase only if safe.

**Verification:**

```bash
git status --short --branch
gh issue develop --list 20
```

Expected:
- branch is linked to issue #20,
- working tree is clean before edits.

**Commit:** none.

### Task 2: Add portable catalog filter tags to demo Components

**Objective:** Make default Backstage Catalog filtering/search usable for the IKS and critical-service demo paths without custom app code.

**Files:**
- Modify: `examples/services/customer-portal/catalog-info.yaml`
- Modify: `examples/services/reporting-api/catalog-info.yaml`

**Steps:**

1. In `examples/services/customer-portal/catalog-info.yaml`, add `metadata.tags` directly under `metadata.description` and before `metadata.annotations`:

   ```yaml
   tags:
     - iks
     - criticality-high
     - data-personal
   ```

   Rationale:
   - `iks` mirrors `iks.dev/compliance-scope: iks,gdpr` for default UI filtering.
   - `criticality-high` mirrors `iks.dev/criticality: high` for the critical-services view.
   - `data-personal` is optional but useful context for demo filtering; keep it only if it does not feel like over-modeling during implementation.

2. In `examples/services/reporting-api/catalog-info.yaml`, add `metadata.tags` directly under `metadata.description` and before `metadata.annotations`:

   ```yaml
   tags:
     - iks
     - criticality-medium
     - data-confidential
   ```

   Rationale:
   - `iks` mirrors `iks.dev/compliance-scope: iks`.
   - `criticality-medium` makes the service visibly non-critical for the critical-services demo view.
   - `data-confidential` is optional; keep only if `customer-portal` also gets a data tag.

3. Do **not** remove or rename existing annotations. The annotations remain the IKS metadata source of truth; tags are a Backstage UI aid.

**Verification:**

```bash
git diff -- examples/services/customer-portal/catalog-info.yaml examples/services/reporting-api/catalog-info.yaml
```

Expected:
- only `metadata.tags` are added,
- `customer-portal` still has `iks.dev/runbook-url` and Runbook link,
- `reporting-api` still intentionally lacks runbook annotation/link,
- `spec.owner` and `spec.system` remain unchanged.

**Commit:** defer until related docs are updated.

### Task 3: Document tag semantics in catalog schema docs

**Objective:** Explain that tags are a demo/UI aid and annotations remain the authoritative IKS metadata.

**Files:**
- Modify: `backstage/catalog/README.md`

**Steps:**

1. In `backstage/catalog/README.md`, in the `### Component` section, add `metadata.tags` as a recommended MVP field after `metadata.description` and before annotations:

   ```markdown
   Recommended MVP fields:

   - `metadata.tags` for portable default Backstage Catalog filtering/search. Tags should mirror selected IKS annotations for demo navigation, for example `iks`, `criticality-high`, or `criticality-medium`. The authoritative metadata remains in `metadata.annotations.iks.dev/*`.
   ```

   If the file already has a recommended/optional field subsection, place this there rather than creating duplicate headings.

2. Add a small `Demo view tags` subsection near the existing Component guidance:

   ```markdown
   ## Demo view tags

   The MVP uses tags as a low-cost way to support default Backstage Catalog filtering without committing a generated app customization:

   - `iks`: service has `iks` in `iks.dev/compliance-scope`.
   - `criticality-high` / `criticality-critical`: service belongs in the critical-services demo view.
   - `criticality-medium` / `criticality-low`: service remains visible for comparison but should not appear in the critical-services view.

   Keep tag values synchronized with the corresponding `iks.dev/*` annotations when service metadata changes.
   ```

3. Keep existing source-of-truth wording intact: service-local `catalog-info.yaml` files are authoritative; `backstage/catalog/components.yaml` remains reference-only.

**Verification:**

```bash
git diff -- backstage/catalog/README.md
```

Expected:
- docs distinguish tags from authoritative annotations,
- no text implies Backstage custom UI code is committed in this repo.

**Commit:** defer until demo guide is added.

### Task 4: Add a catalog demo views/navigation guide

**Objective:** Provide a concrete stakeholder/demo path for issue #20 acceptance criteria.

**Files:**
- Create: `backstage/catalog/demo-views.md`

**Content outline:**

```markdown
# Catalog Demo Views

This guide describes the MVP catalog views for issue #20. It assumes a generated Backstage runtime is already pointed at `backstage/catalog/locations.yaml` as described in `../runtime/README.md`.

## Scope

- Use default Backstage Catalog UI capabilities and repository-owned metadata first.
- Do not require committing a generated Backstage app customization for the MVP.
- Treat custom columns or first-class annotation filters as optional follow-up if stakeholder demo clarity requires them.

## View: all services

1. Open Backstage at `http://localhost:3000`.
2. Open the Software Catalog.
3. Select kind/type filters for `Component` / `service` if available.
4. Confirm both demo services are present:
   - `customer-portal`
   - `reporting-api`

## View: IKS-relevant services

Default UI path:
- Filter/search by tag `iks` if the generated Backstage app exposes tag filtering.
- Fallback: open each service and inspect `iks.dev/compliance-scope`; it must contain `iks`.

Expected services:
- `customer-portal` (`iks.dev/compliance-scope: iks,gdpr`)
- `reporting-api` (`iks.dev/compliance-scope: iks`)

## View: critical services

Default UI path:
- Filter/search by tag `criticality-high` or `criticality-critical` if available.
- Fallback: inspect `iks.dev/criticality` on service details.

Expected services:
- `customer-portal` (`iks.dev/criticality: high`)

Non-critical comparison service:
- `reporting-api` (`iks.dev/criticality: medium`)

## Service detail check: customer-portal

Confirm the service detail page or entity YAML exposes:

| Demo field | Backstage source | Expected value |
|---|---|---|
| Technical owner | `spec.owner` | `group:default/platform-team` |
| Business owner | `metadata.annotations.iks.dev/business-owner` | `customer-success` |
| System | `spec.system` | `customer-experience` |
| Repository | `metadata.annotations.backstage.io/source-location` | `url:https://github.com/example-org/customer-portal` |
| Lifecycle | `spec.lifecycle` | `experimental` |
| Documentation | `metadata.links[Documentation]` / `backstage.io/techdocs-ref` | present |
| Runbook | `iks.dev/runbook-url` / `metadata.links[Runbook]` | present |
| Criticality | `iks.dev/criticality` | `high` |
| Protection need | `iks.dev/protection-need` | `high` |
| Data class | `iks.dev/data-class` | `personal-data` |
| Compliance scope | `iks.dev/compliance-scope` | `iks,gdpr` |

## Service detail check: reporting-api

Confirm the incomplete metadata demo case:

| Demo field | Backstage source | Expected value |
|---|---|---|
| Technical owner | `spec.owner` | `group:default/platform-team` |
| Business owner | `metadata.annotations.iks.dev/business-owner` | `customer-success` |
| System | `spec.system` | `management-reporting` |
| Repository | `metadata.annotations.backstage.io/source-location` | `url:https://github.com/example-org/reporting-api` |
| Lifecycle | `spec.lifecycle` | `experimental` |
| Documentation | `metadata.links[Documentation]` / `backstage.io/techdocs-ref` | present |
| Runbook | `iks.dev/runbook-url` / `metadata.links[Runbook]` | intentionally missing |
| Criticality | `iks.dev/criticality` | `medium` |
| Protection need | `iks.dev/protection-need` | `normal` |
| Data class | `iks.dev/data-class` | `confidential` |
| Compliance scope | `iks.dev/compliance-scope` | `iks` |

## Optional generated-app customization

If default Backstage filtering is not clear enough for the stakeholder demo, a future runtime/app issue can add custom Catalog table columns or annotation filters in the generated app. Keep that outside this repository unless a decision explicitly changes the repository boundary.
```

**Verification:**

```bash
git diff -- backstage/catalog/demo-views.md
```

Expected:
- the guide satisfies every issue #20 required view/path,
- the guide does not claim custom Backstage UI code exists,
- the guide explicitly preserves the incomplete `reporting-api` runbook case.

**Commit:** defer until references are wired.

### Task 5: Wire the new guide into repository docs

**Objective:** Make the demo view guide discoverable from existing entry points.

**Files:**
- Modify: `backstage/catalog/README.md`
- Modify: `backstage/README.md`
- Modify: `README.md`
- Optional modify: `wiki/docs/demo-story.md`

**Steps:**

1. In `backstage/catalog/README.md`, near `## Active catalog imports` or after the source-of-truth rule, add:

   ```markdown
   The issue #20 demo navigation for catalog views and filters is documented in `demo-views.md`.
   ```

2. In `backstage/README.md`, update the `catalog/` bullet to mention demo views:

   ```markdown
   - `catalog/`: Backstage catalog locations, shared demo entities, demo view/filter guidance, and the catalog schema/source-of-truth rules...
   ```

3. In root `README.md`, update the `Noch offen fuer den MVP-Betrieb` or `Naechste Schritte` section so issue #20 is no longer described only as vague future work. Suggested targeted change:

   - Replace the generic catalog import/check bullets with a pointer to the demo view guide once implemented:

     ```markdown
     - Catalog-Views und Demo-Navigation gemaess `backstage/catalog/demo-views.md` pruefen.
     ```

4. Optionally update `wiki/docs/demo-story.md` to reference the repo-owned guide after the `## Ablauf` filter steps:

   ```markdown
   Die konkreten Backstage-Katalogpfade und Fallbacks fuer die MVP-Demo sind im Repository unter `backstage/catalog/demo-views.md` dokumentiert.
   ```

   If editing the wiki submodule, follow the repository rule:
   - before editing: `git -C wiki switch master && git -C wiki pull --ff-only`,
   - commit and push inside `wiki` first,
   - then commit the updated submodule pointer in the parent repo.

   **Recommendation:** avoid wiki edits for the first #20 implementation unless the root/demo docs feel insufficient. A repository-local guide plus root/backstage README references likely satisfy the issue with less submodule risk.

**Verification:**

```bash
git diff -- README.md backstage/README.md backstage/catalog/README.md wiki/docs/demo-story.md
```

Expected:
- new guide is discoverable,
- no stale Port-as-active-target language is introduced,
- no wiki submodule pointer changes unless intentionally editing wiki docs.

**Commit:** defer until validation.

### Task 6: Update migration issue mapping for completed housekeeping and current #20 scope

**Objective:** Keep `backstage/migration-issues.md` aligned with issue state and the #20 plan if not already handled by separate #26 cleanup.

**Files:**
- Modify: `backstage/migration-issues.md`

**Steps:**

1. Inspect current issue states before editing:

   ```bash
   gh issue view 17 --json number,state,title
   gh issue view 19 --json number,state,title
   gh issue view 20 --json number,state,title
   gh issue view 23 --json number,state,title
   gh issue view 26 --json number,state,title
   ```

2. If `backstage/migration-issues.md` still lists closed issues #17, #19, or #23 as open, move them into `## Completed Backstage migration issues` with concise completion notes.

3. Keep #20 in `## Open Backstage migration issues` until the implementing PR closes it. For #20, update the acceptance line to mention documented/default catalog view paths if the new `demo-views.md` is added:

   ```markdown
   - Acceptance: `customer-portal` and `reporting-api` support the demo story, with default Backstage catalog navigation and fallback metadata checks documented under `backstage/catalog/demo-views.md`.
   ```

4. Do not close #26 in this implementation unless the user explicitly asks for broader tracker cleanup. #26 may remain the umbrella for final issue-map alignment.

**Verification:**

```bash
git diff -- backstage/migration-issues.md
```

Expected:
- migration map does not contradict known issue state,
- #20 remains open in the map until PR merge,
- no old Port runtime work is revived.

**Commit:** include with docs/catalog changes if changed.

### Task 7: Run targeted local validation

**Objective:** Prove the YAML and docs changes are safe before committing/pushing.

**Files:**
- No direct edits in this task.

**Commands:**

```bash
git diff --check
```

Expected:
- no output, exit 0.

Run YAML validation if locally available:

```bash
if command -v yamllint >/dev/null 2>&1; then
  yamllint backstage port examples agents .github/ISSUE_TEMPLATE
else
  echo "yamllint unavailable locally; rely on GitHub Actions validate-yaml and manual YAML read-through"
fi
```

Expected:
- pass, or a clear local-tooling caveat.

Run a lightweight YAML parse fallback if Python YAML support is available:

```bash
python3 - <<'PY'
from pathlib import Path
try:
    import yaml
except Exception as exc:
    print(f"PyYAML unavailable: {exc}")
    raise SystemExit(0)
for path in [
    Path('examples/services/customer-portal/catalog-info.yaml'),
    Path('examples/services/reporting-api/catalog-info.yaml'),
    Path('backstage/catalog/locations.yaml'),
    Path('backstage/catalog/groups.yaml'),
    Path('backstage/catalog/systems.yaml'),
]:
    list(yaml.safe_load_all(path.read_text()))
    print(f"parsed {path}")
PY
```

Run targeted metadata consistency check:

```bash
python3 - <<'PY'
from pathlib import Path
try:
    import yaml
except Exception as exc:
    print(f"PyYAML unavailable: {exc}")
    raise SystemExit(0)
services = []
for path in [Path('examples/services/customer-portal/catalog-info.yaml'), Path('examples/services/reporting-api/catalog-info.yaml')]:
    doc = yaml.safe_load(path.read_text())
    services.append((path, doc))
for path, doc in services:
    name = doc['metadata']['name']
    tags = set(doc['metadata'].get('tags', []))
    annotations = doc['metadata'].get('annotations', {})
    scope = annotations.get('iks.dev/compliance-scope', '')
    criticality = annotations.get('iks.dev/criticality')
    if 'iks' in scope.split(',') and 'iks' not in tags:
        raise SystemExit(f"{name}: missing iks tag")
    expected_criticality_tag = f"criticality-{criticality}"
    if criticality and expected_criticality_tag not in tags:
        raise SystemExit(f"{name}: missing {expected_criticality_tag} tag")
    print(f"{name}: tags match IKS annotations")
PY
```

Run security/generated-file scans:

```bash
git diff | grep '^+' | grep -viE '^\+\+\+' | grep -Ei '(api[_-]?key|secret|password|passwd|token|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^[:space:]]+' || true

git diff --name-only | grep -Ei '(^package.json$|yarn.lock|package-lock.json|pnpm-lock.yaml|app-config.yaml$|packages/|plugins/|backstage.json)' || true

git diff | grep -nE '^(\+.*)?(<<<<<<<|=======|>>>>>>>)' || true
```

Expected:
- no secret hits,
- no generated Backstage app files,
- no conflict markers.

**Commit:** after validation passes or caveats are recorded.

### Task 8: Commit the implementation and open/update PR

**Objective:** Make the #20 work reviewable and linked to the issue.

**Files:**
- Stage only intended files, likely:
  - `.hermes/plans/2026-05-22_131832-issue-20-catalog-views-filters.md`
  - `examples/services/customer-portal/catalog-info.yaml`
  - `examples/services/reporting-api/catalog-info.yaml`
  - `backstage/catalog/demo-views.md`
  - `backstage/catalog/README.md`
  - `backstage/README.md`
  - `README.md`
  - optionally `backstage/migration-issues.md`
  - optionally `wiki` submodule pointer if wiki docs are intentionally edited and committed first.

**Commands:**

```bash
git status --short
git add .hermes/plans/2026-05-22_131832-issue-20-catalog-views-filters.md \
  examples/services/customer-portal/catalog-info.yaml \
  examples/services/reporting-api/catalog-info.yaml \
  backstage/catalog/demo-views.md \
  backstage/catalog/README.md \
  backstage/README.md \
  README.md \
  backstage/migration-issues.md

git diff --cached --check
git commit -m "docs: document Backstage catalog demo views"
```

If `backstage/migration-issues.md` is not changed, omit it from `git add`.
If wiki docs are changed, commit/push inside `wiki` first and stage the parent `wiki` pointer separately.

Push only after explicit approval if required by current project workflow:

```bash
git push -u origin HEAD
```

Open or update PR:

```bash
gh pr list --head "$(git branch --show-current)" --state open --json number,title,url
```

If no PR exists:

```bash
gh pr create \
  --base main \
  --head "$(git branch --show-current)" \
  --title "docs: document Backstage catalog demo views" \
  --body-file /tmp/idp-iks-lab-pr20-body.md
```

Suggested PR body content:

```markdown
## Summary
- Adds Backstage catalog tags for the default UI demo filters.
- Documents all-services, IKS-relevant, critical-service, and service-detail demo paths.
- Clarifies that custom Backstage columns/annotation filters remain optional runtime follow-up unless needed for stakeholder demo clarity.

Closes #20

## Validation
- [ ] git diff --check
- [ ] yamllint backstage port examples agents .github/ISSUE_TEMPLATE, or local unavailable + CI validate-yaml
- [ ] metadata tag consistency check
- [ ] secret/generated-app/conflict-marker scans
```

**Verification:**

```bash
gh pr view --json number,title,url,headRefName,baseRefName,isDraft

gh pr checks --watch=false || true
```

Expected:
- PR exists and targets `main`,
- PR body closes #20,
- CI starts or passes.

## Files Likely to Change

Expected:

- `.hermes/plans/2026-05-22_131832-issue-20-catalog-views-filters.md`
  - this plan; include in PR for traceability if user wants tracked plans.
- `examples/services/customer-portal/catalog-info.yaml`
  - add `metadata.tags` for IKS/default demo filtering.
- `examples/services/reporting-api/catalog-info.yaml`
  - add `metadata.tags` for IKS/default demo filtering and non-critical comparison.
- `backstage/catalog/demo-views.md`
  - new issue #20 demo navigation and verification guide.
- `backstage/catalog/README.md`
  - document tag convention and link demo guide.
- `backstage/README.md`
  - mention demo view/filter guidance under `catalog/`.
- `README.md`
  - point MVP next steps/demo flow at the new catalog demo guide.

Possible:

- `backstage/migration-issues.md`
  - align #20 acceptance wording and move already-closed #17/#19/#23 if that cleanup has not happened elsewhere.
- `wiki/docs/demo-story.md` plus parent `wiki` submodule pointer
  - only if the implementation intentionally updates wiki demo docs; otherwise avoid submodule churn.

Should not change:

- Generated Backstage app files: `package.json`, lockfiles, `packages/`, `plugins/`, `backstage.json`, generated `app-config.yaml`.
- `backstage/catalog/components.yaml` import behavior; it remains reference-only.
- Entity names/refs for existing demo services, systems, and groups.
- `port/` except explicit legacy/migration notes, not expected for #20.

## Documentation Updates / ADR Decision

- Documentation updates are expected:
  - new `backstage/catalog/demo-views.md`,
  - updates to `backstage/catalog/README.md`, `backstage/README.md`, and `README.md`,
  - optional `wiki/docs/demo-story.md` if the wiki demo story should link to the exact repository demo guide.
- No ADR is expected for this issue because it does not change architecture or governance:
  - Backstage remains the target path,
  - GitHub remains source of truth,
  - the generated runtime remains external for MVP,
  - no production deployment, Kubernetes automation, auth hardening, or autonomous compliance enforcement is added.
- If implementation switches to committing custom Backstage app code, pause and create/update a decision record first because that changes the repository boundary established by PR #31.

## Tests / Validation

Minimum validation:

```bash
git diff --check
```

YAML validation:

```bash
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
```

If unavailable locally, record the caveat and rely on GitHub Actions `validate-yaml` after PR push.

YAML parse and tag consistency fallback:

```bash
python3 - <<'PY'
from pathlib import Path
try:
    import yaml
except Exception as exc:
    print(f"PyYAML unavailable: {exc}")
    raise SystemExit(0)
paths = [
    Path('examples/services/customer-portal/catalog-info.yaml'),
    Path('examples/services/reporting-api/catalog-info.yaml'),
    Path('backstage/catalog/locations.yaml'),
    Path('backstage/catalog/groups.yaml'),
    Path('backstage/catalog/systems.yaml'),
]
for path in paths:
    list(yaml.safe_load_all(path.read_text()))
    print(f"parsed {path}")
for path in paths[:2]:
    doc = yaml.safe_load(path.read_text())
    name = doc['metadata']['name']
    tags = set(doc['metadata'].get('tags', []))
    annotations = doc['metadata'].get('annotations', {})
    scope = [s.strip() for s in annotations.get('iks.dev/compliance-scope', '').split(',')]
    criticality = annotations.get('iks.dev/criticality')
    if 'iks' in scope and 'iks' not in tags:
        raise SystemExit(f"{name}: missing iks tag")
    if criticality and f"criticality-{criticality}" not in tags:
        raise SystemExit(f"{name}: missing criticality-{criticality} tag")
    print(f"{name}: tags match IKS annotations")
PY
```

Manual consistency pass:

- `customer-portal` is still the complete service and remains linked to:
  - owner `group:default/platform-team`,
  - business owner `customer-success`,
  - system `customer-experience`,
  - source-location repo, docs, runbook, criticality/protection/data/compliance annotations.
- `reporting-api` is still visible and still intentionally lacks runbook annotation/link.
- Demo view guide covers all issue #20 acceptance criteria.
- Docs distinguish default UI/tag-based demo support from optional custom Backstage app columns/filters.
- No instruction commits or requires a generated Backstage app tree.
- No Kubernetes, production deployment, secrets, or autonomous compliance enforcement are introduced.

Post-push validation:

```bash
gh pr checks <PR_NUMBER> --watch=false
```

Expected:
- `validate-yaml` passes.

## Risks, Tradeoffs, and Open Questions

### Risks

- Default Backstage Catalog UI capabilities vary by Backstage version and app configuration. Tag filtering/search is more portable than arbitrary annotation filters, but the exact UI labels may differ.
- Tags can drift from authoritative IKS annotations if future metadata changes do not keep them synchronized.
- Documentation-only demo navigation may satisfy #20 for MVP, but stakeholders may later ask for custom table columns or first-class annotation filters in the generated app.
- Editing the wiki submodule adds workflow overhead and a second commit/push; avoid unless needed.

### Tradeoffs

- Adding `metadata.tags` is low-cost and portable, but duplicates selected annotation semantics.
- Building custom Backstage UI filters would be closer to a polished product, but it would require committing or managing generated app code, which is outside the current repo boundary.
- Keeping `reporting-api` intentionally incomplete helps the demo, but the guide must be explicit so reviewers do not “fix” the missing runbook.

### Open Questions

- Are default Backstage tag filters available in the generated runtime version the team will use, or should the docs phrase tag filtering as “filter/search by tag if available” with metadata-inspection fallback?
- Should `metadata.tags` include only `iks` and `criticality-*`, or also data-class tags such as `data-personal` / `data-confidential`?
- Should the wiki demo story link to the new repository guide now, or should that wait for #24 demo packaging?
- Should #26 tracker cleanup be handled separately before/after #20, or should `backstage/migration-issues.md` be opportunistically aligned in the #20 PR?

## Artifact Inventory / Traceability

- Plan file created in plan mode:
  - `.hermes/plans/2026-05-22_131832-issue-20-catalog-views-filters.md`
  - local repository file only at creation time;
  - not committed or pushed in plan mode.
- External issue referenced:
  - #20 `Backstage IDP MVP: Configure service catalog views and filters`
  - `https://github.com/iks-gmbh-projects/idp-iks-lab/issues/20`
  - read-only lookup performed; no issue comment/edit/close/assignment was performed in plan mode.
- Existing runtime dependency:
  - #19 is closed by PR #31 and provides the local external runtime path under `backstage/runtime/`.
- Companion scratch files:
  - none created.

## Deferred Actions Because Plan Mode Is Active

The user requested a plan for issue #20. Plan mode forbids implementation and external tracker mutation, so the following actions are intentionally deferred:

- editing catalog YAML or docs beyond this plan file,
- creating/checking out an issue-linked branch,
- committing the plan or implementation changes,
- pushing a branch,
- opening or editing a PR,
- commenting on or closing issue #20.
