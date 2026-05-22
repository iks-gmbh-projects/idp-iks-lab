# Issue #19 Local Backstage Runtime Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Provide a documented minimal local Backstage runtime path that can render this repository's MVP catalog from `backstage/catalog/locations.yaml` without adding production infrastructure or Kubernetes automation.

**Architecture:** Keep this repository primarily as the versioned Backstage catalog/config/docs source of truth, consistent with `AGENTS.md`. For issue #19, prefer an external generated Backstage app in a sibling/local directory and commit only runtime documentation plus non-secret example config in this repo. This satisfies the issue's "scaffold or document external app path" scope while avoiding a large generated application tree inside the docs/config repository.

**Tech Stack:** Backstage OSS, Node.js/Yarn, local file catalog locations, existing repo YAML descriptors, GitHub Actions YAML validation.

---

## Current Context / Assumptions

- Current branch at planning time: `main` synced with `origin/main`.
- Issue: #19 `Backstage IDP MVP: Scaffold local Backstage app/runtime`.
- Open issue acceptance requires:
  - documented local Backstage start path,
  - at least a catalog overview page,
  - catalog data read from this repository rather than hardcoded fixtures,
  - no Kubernetes requirement,
  - basic CI/build validation or documented fallback.
- Existing repository state:
  - `backstage/README.md` explicitly says this repo does not yet contain a runnable Backstage runtime.
  - `backstage/app-config.example.yaml` is a non-secret example config with local file catalog location `./catalog/locations.yaml`.
  - `backstage/catalog/locations.yaml` imports groups, systems, templates, and service-local `examples/services/*/catalog-info.yaml` files.
  - No root `package.json` or `yarn.lock` exists.
  - `README.md` still lists local/self-hosted Backstage provisioning as open MVP work.
- Repository guidance in `AGENTS.md` says this is an experimental docs-and-configuration repo, not an application runtime. Therefore this plan avoids committing a full generated Backstage app unless the user explicitly changes that boundary.
- No ADR is expected for this issue: ADR 0003 already selected Backstage as the target. This story documents the MVP runtime path, not a new strategic platform decision. If implementation decides to commit a full generated Backstage application into this repo, revisit whether an ADR or decision note is needed because that changes the repo boundary.

## Proposed Approach

Document a reproducible local runtime flow:

1. A developer creates a Backstage app outside this repository, for example as a sibling directory `../iks-backstage-runtime`.
2. The developer overlays or references a repo-provided non-secret local config file.
3. Backstage loads the catalog root from this repository's `backstage/catalog/locations.yaml` using a local `file` location.
4. The docs explain how to verify that `customer-portal`, `reporting-api`, groups, systems, and templates appear.
5. The docs keep #20/#21/#22/#24 responsibilities separate: this issue only proves a minimal runtime/catalog import path.

This keeps the branch small and reviewable while giving #20, #21, #22, and #24 a concrete runtime assumption.

## Step-by-Step Plan

### Task 1: Confirm branch and issue context

**Objective:** Start from a clean issue-linked branch and verify the tracker context before editing.

**Files:**
- No repo file edits in this task.

**Steps:**

1. Fetch and sync `main`:

   ```bash
   git fetch origin --prune
   git switch main
   git pull --ff-only
   ```

2. Create or check out the issue-linked branch:

   ```bash
   gh issue develop --list 19
   gh issue develop 19 --base main --checkout
   git status --short --branch
   ```

3. Re-read issue #19:

   ```bash
   gh issue view 19 --json number,title,state,url,body
   ```

**Verification:**

- `git status --short --branch` shows the issue #19 branch and no uncommitted changes.
- Issue #19 is open and still matches the runtime/documentation scope.

**Commit:** none.

### Task 2: Add local runtime instructions

**Objective:** Create a clear, copy-pasteable local runtime guide under `backstage/`.

**Files:**
- Create: `backstage/runtime/README.md`

**Content to add:**

`backstage/runtime/README.md` should include these sections:

1. `# Local Backstage Runtime`
2. `## Scope`
   - State this repo remains the Backstage catalog/config/docs source of truth.
   - State the runnable Backstage app is generated locally outside this repo for the MVP.
   - State this does not add production deployment, Kubernetes, or auth hardening.
3. `## Prerequisites`
   - Node.js LTS compatible with current Backstage requirements.
   - Yarn as required by the generated Backstage app.
   - Git clone of this repository.
4. `## Create the local app`
   - Example command:

     ```bash
     cd ..
     npx @backstage/create-app@latest --path iks-backstage-runtime
     cd iks-backstage-runtime
     ```

   - Note: do not commit the generated app to `idp-iks-lab` for this MVP path.
5. `## Point the app at this repository catalog`
   - Explain that the committed example config lives in `idp-iks-lab/backstage/app-config.local.example.yaml`.
   - Give two options:
     - copy the example file into the generated app as `app-config.local.yaml`, or
     - pass it with Backstage's config flag if supported by the generated app command.
6. `## Start Backstage`
   - Example command:

     ```bash
     yarn dev
     ```

   - Mention expected URLs:
     - frontend: `http://localhost:3000`
     - backend: `http://localhost:7007`
7. `## Verify catalog import`
   - Go to the Software Catalog.
   - Confirm these entities are visible:
     - Groups: `platform-team`, `iks-review-board`, `customer-success`
     - Systems: `customer-experience`, `management-reporting`
     - Components: `customer-portal`, `reporting-api`
     - Templates: `catalog-metadata-fix`, `iks-review-request`, `service-onboarding`
   - Confirm `reporting-api` intentionally lacks a runbook for later advisory checks.
8. `## Troubleshooting`
   - Relative path problems from generated app to this repo.
   - Backstage file locations need to resolve from the app process working directory.
   - If a file target fails, use an absolute path in the local-only config and do not commit machine-specific paths.
9. `## Follow-up stories`
   - #20 catalog views/filters.
   - #21 advisory checks.
   - #22 template issue creation with credentials.
   - #24 packaged demo runtime.

**Verification:**

- Read the new file top-to-bottom.
- Confirm it does not imply the generated app should be committed into this repo.
- Confirm it does not introduce production/Kubernetes/deployment commitments.

**Commit:** defer until Task 7.

### Task 3: Add local Backstage config example for external runtime

**Objective:** Provide a non-secret config file that a generated local Backstage app can use to load this repository's catalog.

**Files:**
- Create: `backstage/app-config.local.example.yaml`
- Possibly modify: `backstage/app-config.example.yaml` only if wording/comments need clarification.

**Implementation guidance:**

Create `backstage/app-config.local.example.yaml` with a local runtime-oriented config. It should be non-secret and should avoid machine-specific absolute paths by default.

Suggested content:

```yaml
app:
  title: IKS Developer Portal
  baseUrl: http://localhost:3000

backend:
  baseUrl: http://localhost:7007
  listen:
    port: 7007

organization:
  name: IKS

catalog:
  locations:
    - type: file
      target: ../idp-iks-lab/backstage/catalog/locations.yaml
      rules:
        - allow:
            - Location
            - Group
            - System
            - Component
            - Template

techdocs:
  builder: local
  generator:
    runIn: local
  publisher:
    type: local
```

Add comments only if they are useful and YAML-safe. If comments are added, explain that `target` assumes this layout:

```text
<workspace>/idp-iks-lab
<workspace>/iks-backstage-runtime
```

If the implementer finds Backstage's generated app expects config paths relative to the generated app directory, keep the target as `../idp-iks-lab/backstage/catalog/locations.yaml`. If the implementer validates with a different local layout, document how to replace it with an absolute local-only path without committing that path.

**Verification:**

- Run YAML syntax validation if available:

  ```bash
  yamllint backstage/app-config.local.example.yaml
  ```

- If `yamllint` is unavailable, parse with another local YAML parser if present, otherwise perform a manual read-through and document the limitation.
- Confirm the config imports `backstage/catalog/locations.yaml`, not `backstage/catalog/components.yaml`.

**Commit:** defer until Task 7.

### Task 4: Update Backstage docs to point to the runtime guide

**Objective:** Make the new runtime path discoverable from existing Backstage documentation.

**Files:**
- Modify: `backstage/README.md`
- Possibly modify: `backstage/catalog/README.md`

**Changes:**

1. In `backstage/README.md`, update the opening paragraph from "does not yet contain a runnable Backstage application runtime" to a more precise statement:
   - This repo does not commit a full generated Backstage app.
   - It now documents a local external runtime path under `backstage/runtime/`.
2. Add `runtime/` to the Contents list:

   ```markdown
   - `runtime/`: instructions for generating a local Backstage app outside this repository and pointing it at this repository's catalog data.
   ```

3. Add `app-config.local.example.yaml` to the Contents list, distinct from `app-config.example.yaml`:

   ```markdown
   - `app-config.local.example.yaml`: local runtime config example for a generated Backstage app in a sibling directory.
   ```

4. In `backstage/catalog/README.md`, optionally add one sentence under `Active catalog imports`:

   ```markdown
   The local runtime guide in `../runtime/README.md` shows how a generated Backstage app can load this root location.
   ```

**Verification:**

- Read both files and ensure the source-of-truth rule is unchanged.
- Confirm no doc says to import both `components.yaml` and service-local `catalog-info.yaml` files.

**Commit:** defer until Task 7.

### Task 5: Update root README next steps and structure

**Objective:** Surface the local runtime path from the repository landing page.

**Files:**
- Modify: `README.md`

**Changes:**

1. In `Projektstatus`, update the open MVP item:

   From:

   ```markdown
   - Entscheiden, ob dieses Repository nur Backstage-Katalog-/Konfigurationsquelle bleibt oder spaeter auch eine lauffaehige Backstage-App enthaelt.
   - Backstage-Instanz lokal oder selbstgehostet bereitstellen.
   ```

   To wording like:

   ```markdown
   - Lokalen Backstage-MVP ueber die dokumentierte externe Runtime unter `backstage/runtime/` starten und validieren.
   - Spaeter entscheiden, ob eine lauffaehige Backstage-App dauerhaft in dieses Repository aufgenommen wird oder extern bleibt.
   ```

2. In `Struktur`, update `backstage/` line to mention runtime docs:

   ```markdown
   - `backstage/`: Backstage-Zielstruktur fuer Catalog-Locations, Beispielkonfiguration, lokale Runtime-Hinweise, Templates, TechDocs und Scorecard-Mapping.
   ```

3. In `Naechste Schritte`, update the first steps:

   ```markdown
   1. Lokale Backstage-Runtime gemaess `backstage/runtime/README.md` erzeugen oder vorhandene Instanz verwenden.
   2. `backstage/catalog/locations.yaml` als Catalog-Location einbinden.
   ```

**Verification:**

- Confirm README still identifies GitHub as source of truth.
- Confirm README does not claim a full Backstage app is committed in the repo.
- Confirm Port remains legacy/migration context only.

**Commit:** defer until Task 7.

### Task 6: Update migration map and issue traceability docs

**Objective:** Keep repository tracking docs aligned with the new runtime documentation.

**Files:**
- Modify: `backstage/migration-issues.md`
- Possibly modify: `wiki/docs/demo-story.md` only if runtime setup is necessary for demo clarity.

**Changes:**

1. In `backstage/migration-issues.md`, update #19 acceptance line from future tense to the intended deliverable:

   ```markdown
   - Acceptance: local Backstage can read catalog data from this repository without Kubernetes as an MVP prerequisite; runtime setup is documented under `backstage/runtime/`.
   ```

2. Do not close or mark #19 complete in docs manually; the PR closing keyword can close it when merged if the implementation satisfies it.
3. Avoid wiki edits unless absolutely necessary. The wiki demo story already says Backstage is the demo surface, and #24 will package the full demo path.

**Verification:**

- Confirm #19 remains represented accurately.
- Confirm #20/#21/#22/#24 remain separate follow-up stories.
- Confirm no stale Port runtime wording is introduced.

**Commit:** defer until Task 7.

### Task 7: Validate docs/config changes and commit

**Objective:** Prove the runtime documentation/config changes are consistent and create a reviewable commit.

**Files:**
- Stage only the files changed for #19.

**Validation commands:**

```bash
git status --short
git diff --check
yamllint backstage .github/ISSUE_TEMPLATE examples agents port
```

If `yamllint` is unavailable locally, run:

```bash
command -v yamllint || echo "yamllint unavailable locally; rely on GitHub Actions and manual YAML read-through"
```

Then manually inspect changed YAML and Markdown:

```bash
git diff -- README.md backstage/README.md backstage/catalog/README.md backstage/app-config.local.example.yaml backstage/runtime/README.md backstage/migration-issues.md
```

Additional targeted checks:

```bash
grep -RInE 'Kubernetes|production|prod|Port workspace|validate-port-config' README.md backstage || true
grep -RInE 'components.yaml' backstage/catalog/README.md backstage/catalog/locations.yaml backstage/runtime/README.md || true
```

Expected:

- `git diff --check` passes.
- YAML validation passes, or unavailable validator is documented.
- No docs imply Kubernetes or production deployment is required.
- No docs imply `components.yaml` is imported as the authoritative service source.
- `backstage/catalog/locations.yaml` remains unchanged unless a real import-path issue is found.

**Commit:**

```bash
git add README.md backstage/README.md backstage/catalog/README.md backstage/app-config.local.example.yaml backstage/runtime/README.md backstage/migration-issues.md
git diff --cached --check
git commit -m "docs: document local Backstage runtime path"
```

If the implementation also includes this plan file by user request later, stage it explicitly in a separate or same reviewable commit as requested. Do not commit in plan mode.

### Task 8: Prepare PR and CI follow-up

**Objective:** Make the branch ready for review after implementation.

**Files:**
- No additional edits unless validation fails.

**Steps after implementation approval:**

1. Push the issue branch:

   ```bash
   git push -u origin HEAD
   ```

2. Open a PR against `main` with a body that includes:
   - Summary of external local runtime documentation.
   - New config example path.
   - Validation results and any local validator caveats.
   - `Closes #19`.

3. Check CI:

   ```bash
   gh pr checks --watch=false
   ```

**Verification:**

- PR is open against `main` from the issue #19 branch.
- `validate-yaml` passes.
- PR body clearly says the full generated Backstage app is not committed in this repo.

## Files Likely to Change

Expected changes:

- Create: `backstage/runtime/README.md`
- Create: `backstage/app-config.local.example.yaml`
- Modify: `backstage/README.md`
- Modify: `README.md`
- Modify: `backstage/migration-issues.md`

Possible changes if useful during implementation:

- Modify: `backstage/catalog/README.md`
- Modify: `wiki/docs/demo-story.md` only if the runtime docs need a demo link; avoid wiki edits unless needed because wiki changes require separate submodule workflow.

Files that should not change for #19 unless requirements change:

- Do not add a full generated Backstage app tree inside this repo.
- Do not modify `backstage/catalog/locations.yaml` unless validation proves the existing root location cannot be loaded by a local runtime config.
- Do not modify `examples/services/*/catalog-info.yaml` unless Backstage ingestion reveals a schema/path problem.
- Do not add Kubernetes manifests, deployment charts, production secrets, or auth hardening.

## Documentation / ADR Notes

- Update repository docs so a new contributor can find the local runtime guide from `README.md` and `backstage/README.md`.
- No ADR is expected for the external-runtime documentation path because ADR 0003 already selected Backstage and this story stays within the docs/config MVP boundary.
- If implementation pivots to committing a full generated Backstage app under this repo, pause and consider whether to add a lightweight decision record or issue comment because it changes the repository from docs/config-only toward app runtime ownership.

## Tests / Validation

Minimum local validation:

```bash
git diff --check
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
```

If available during implementation, optional runtime smoke test:

```bash
# from a sibling generated Backstage app, not from this repository
cd ../iks-backstage-runtime
yarn dev
```

Manual runtime smoke checklist:

- Backstage opens at `http://localhost:3000`.
- Catalog page loads.
- Entities from this repository appear:
  - `customer-portal`
  - `reporting-api`
  - `platform-team`
  - `iks-review-board`
  - `customer-success`
  - `customer-experience`
  - `management-reporting`
- `reporting-api` remains intentionally incomplete for later advisory-check story #21.
- No production systems are mutated.

If no runtime smoke test is performed in #19, document that as a fallback and leave full demo run to #24/#15.

## Risks, Tradeoffs, and Open Questions

### Risks

- Backstage generated app commands and package-manager expectations may vary by Backstage version.
- Relative file locations may fail if the generated app is not placed as a sibling to this repository.
- Local runtime smoke testing may be slow or unavailable in the agent environment.
- Adding a full generated app to this repo would be large and could conflict with the current docs/config boundary.

### Tradeoffs

- External generated app path keeps this repo small and aligned with current guidance, but it means the exact generated app code is not versioned here.
- Committing a full app would make the runtime reproducible from one checkout, but creates a much larger maintenance surface and should be an explicit choice.

### Open Questions

- Should the team later commit a generated Backstage app into this repo, or keep it as an external runtime consuming this repo's catalog/config?
- Which exact Node/Yarn versions should be recommended once a local smoke test is performed?
- Should #24 add a containerized local demo wrapper, or is generated-app documentation enough?
- Will #22 require a specific GitHub integration configuration for Software Templates, and should that be documented in #19 or deferred?

## Artifact Inventory / Traceability

- Plan file: `.hermes/plans/2026-05-22_084247-issue-19-local-backstage-runtime.md`
  - Created in plan mode.
  - Should be committed later only if the user asks to track/commit the plan.
- External tracker item: GitHub issue #19
  - Read in plan mode.
  - Not edited, commented on, assigned, or closed in plan mode.
- No companion scratch snapshot is required for this plan.
- No implementation files were changed in plan mode.
- No branch, commit, push, PR, or external tracker mutation was performed in plan mode.

## Handoff Recommendation

After this plan is accepted, execute with `subagent-driven-development`:

1. Use one implementer subagent per task.
2. Run spec compliance review after each task.
3. Run quality review after spec passes.
4. Commit only after validation passes.
5. Ask before pushing/opening the PR.
