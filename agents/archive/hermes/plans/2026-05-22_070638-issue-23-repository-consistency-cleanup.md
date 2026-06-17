# Issue 23 Repository Consistency Cleanup Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Finish repository documentation and validation cleanup so the active MVP direction consistently points to Backstage, while Port remains only legacy migration context.

**Architecture:** This is a docs-and-configuration cleanup, not an application/runtime change. The implementation should remove post-merge Port-as-target drift from active landing pages and workflows, keep legacy Port artifacts explicitly marked as migration references, and preserve GitHub as the versioned source of truth.

**Tech Stack:** Markdown documentation, GitHub Actions YAML, Backstage catalog/configuration descriptors, Git submodule workflow for `wiki/`, `yamllint` validation.

---

## External tracker

- GitHub issue: #23 `Backstage IDP MVP: Finish repository consistency cleanup`
- Issue URL: https://github.com/iks-gmbh-projects/idp-iks-lab/issues/23
- Current state at plan time: open
- Labels at plan time: `documentation`

## Current context / assumptions

- The repo is on `main` and clean at plan time: `## main...origin/main`.
- Issue #18 was merged, so Backstage catalog schema/source-of-truth work is already in `main`.
- Issue #23 is the next blocking cleanup because active docs/workflows still contain resurrected Port-target wording.
- Concrete findings from read-only inspection:
  - `README.md:30-55` contains a duplicated old Port-centered source-of-truth/project-status/next-step block after the newer Backstage section.
  - `.github/workflows/validate-port-config.yml` exists as an active workflow with `name: Validate Port configuration`; this conflicts with the intended active workflow `.github/workflows/validate-idp-config.yml`.
  - `wiki/Home.md` and `wiki/_Sidebar.md` already point to Backstage as active target from the inspected version, but they still need a final read-through during implementation.
  - `AGENTS.md` already frames `port/` as legacy and Backstage as target, but it should be included in the final stale-language audit.
- The repository has a `wiki` submodule. If implementation touches `wiki/*`, changes must be committed and pushed inside `wiki` first, then the parent repo must commit the updated submodule pointer.
- No new ADR is expected for this issue. ADR 0003 already records the Backstage target decision; #23 is consistency cleanup for an existing decision.

## Proposed approach

1. Create/use the GitHub-linked development branch for issue #23.
2. Remove or rewrite stale Port-as-target text from active root docs.
3. Remove the resurrected active Port validation workflow, keeping the Backstage/IDP workflow active and the reference copy in sync.
4. Audit active docs, wiki pages, issue templates, agent prompts/checklists, and workflow references for stale target language.
5. Only edit `port/` if a file needs a legacy banner or explicit migration-reference wording; do not add new Port behavior.
6. Validate YAML and manually verify Markdown consistency.
7. Commit, push, and open a PR only after user approval outside plan mode.

## Step-by-step plan

### Task 1: Prepare the issue branch

**Objective:** Start implementation from a clean, issue-linked branch without mutating unrelated work.

**Files:**
- No file edits in this task.

**Commands:**

```bash
git fetch --prune origin
git switch main
git pull --ff-only origin main
gh issue develop --list 23
gh issue develop 23 --base main --checkout
git status --short --branch
```

**Expected result:**
- Working tree is clean.
- Current branch is linked to issue #23.
- No unrelated local changes are present.

**Commit:**
- No commit for this task.

### Task 2: Remove duplicated Port-target block from README

**Objective:** Make the root landing page describe only the Backstage target direction and current runtime gap.

**Files:**
- Modify: `README.md`

**Exact edits:**

1. Delete the stale duplicate block that starts with:

```markdown
GitHub ist die versionierte Source of Truth fuer Port-Konfiguration, Demo-Entities, Entscheidungen, Dokumentation und Agenten-Artefakte.
```

and ends with:

```markdown
- Demo end-to-end trocken laufen lassen.
```

In the inspected file this was `README.md:30-55`.

2. Keep the newer Backstage-oriented section at the top, especially:

```markdown
GitHub ist die versionierte Source of Truth fuer Backstage-Katalogdaten, Konfiguration, Demo-Entities, Entscheidungen, Dokumentation und Agenten-Artefakte.
```

3. Ensure `README.md` still explicitly states the runtime gap, for example the existing Backstage-oriented open items:

```markdown
- Entscheiden, ob dieses Repository nur Backstage-Katalog-/Konfigurationsquelle bleibt oder spaeter auch eine lauffaehige Backstage-App enthaelt.
- Backstage-Instanz lokal oder selbstgehostet bereitstellen.
```

**Verification:**

```bash
grep -nE 'Port Workspace|Blueprints und Entities in Port|Scorecards in Port|Port-Actions|Port-Konfiguration' README.md || true
grep -nE 'Backstage|validate-idp-config|Legacy-Migrationsreferenz' README.md
```

**Expected result:**
- No Port-as-target next steps remain in `README.md`.
- Port may appear only as legacy migration context.
- README still documents current Backstage runtime gap and next steps.

**Commit:**
- Defer commit until all root/workflow cleanup tasks are complete, unless implementation is split for review.

### Task 3: Remove stale active Port validation workflow

**Objective:** Ensure only the IDP/Backstage validation workflow is active under `.github/workflows/`.

**Files:**
- Delete or move out of active workflow path: `.github/workflows/validate-port-config.yml`
- Keep/verify: `.github/workflows/validate-idp-config.yml`
- Keep/verify reference copy: `github/workflows/validate-idp-config.yml`

**Exact edits:**

1. Remove `.github/workflows/validate-port-config.yml` from the active workflow directory.
2. Do not create a replacement active Port workflow.
3. Verify `.github/workflows/validate-idp-config.yml` validates the intended paths:
   - `backstage`
   - `port`
   - `examples`
   - `agents`
   - `.github/ISSUE_TEMPLATE`
4. Verify `github/workflows/validate-idp-config.yml` remains a template/reference copy of the active workflow. If the two differ, sync them unless there is a documented reason.

**Verification:**

```bash
find .github/workflows github/workflows -maxdepth 1 -type f -print | sort
grep -RIn 'validate-port-config\|Validate Port configuration' .github/workflows github/workflows || true
diff -u .github/workflows/validate-idp-config.yml github/workflows/validate-idp-config.yml
```

**Expected result:**
- `.github/workflows/validate-port-config.yml` no longer exists.
- No active workflow is named `Validate Port configuration`.
- Active and reference IDP validation workflows match, or any intentional difference is documented in the PR summary.

### Task 4: Audit and adjust GitHub issue templates

**Objective:** Confirm active issue forms use Backstage-compatible wording and do not instruct users to create/configure Port workspaces.

**Files:**
- Inspect/possibly modify: `.github/ISSUE_TEMPLATE/*`
- Inspect/possibly modify: `github/issue-templates/README.md`
- Inspect/possibly modify: `github/issue-templates/*`

**Commands:**

```bash
grep -RInE 'Port|port/|workspace|blueprint|action|validate-port-config' .github/ISSUE_TEMPLATE github/issue-templates || true
```

**Edit rules:**
- In `.github/ISSUE_TEMPLATE/*`, rewrite active workflow wording to use Backstage entity/component/catalog language.
- If `github/issue-templates/*` are historical references, make sure the directory README clearly says they are historical and not active. Do not over-edit archived reference text unless it actively misleads.
- Keep `GitHub Issue Forms` and low-risk GitHub issue workflows in scope; do not add production automation.

**Verification:**
- Active `.github/ISSUE_TEMPLATE/*` files do not ask for Port workspace/import/action work.
- Historical template references are explicitly marked as historical if they retain Port wording.

### Task 5: Audit agent guidance and prompts

**Objective:** Ensure contributors and agents are steered to Backstage for new work and to `port/` only for legacy migration references.

**Files:**
- Inspect/possibly modify: `AGENTS.md`
- Inspect/possibly modify: `agents/README.md`
- Inspect/possibly modify: `agents/prompts/*.md`
- Inspect/possibly modify: `agents/checklists/*.md`
- Inspect/possibly modify: `agents/skills/**/SKILL.md`
- Inspect/possibly modify: `agents/skills/**/references/*.md`

**Commands:**

```bash
grep -RInE 'Port|port/|workspace|blueprint|action|validate-port-config' AGENTS.md agents || true
```

**Edit rules:**
- Acceptable Port mentions:
  - Legacy migration reference notices.
  - Port-specific maintainer skill explicitly marked legacy.
  - Validation that includes `port/` as legacy syntax coverage.
- Suspicious Port mentions to fix:
  - Any default prompt implying Port is the target for new work.
  - Any checklist titled or phrased as the default catalog-change path without a legacy warning.
  - Any agent guidance that says to create/configure a Port workspace for the MVP.

**Verification:**
- `AGENTS.md` keeps Backstage as target and `port/` as legacy.
- `agents/checklists/port-catalog-change.md` and `agents/skills/port-catalog-maintainer/*` remain clearly marked legacy if retained.
- Backstage-oriented prompts/checklists are the default path for new catalog/workflow tasks.

### Task 6: Sync and audit wiki docs if needed

**Objective:** Ensure wiki landing/navigation/domain docs align with Backstage as active target.

**Files:**
- Inspect/possibly modify: `wiki/Home.md`
- Inspect/possibly modify: `wiki/_Sidebar.md`
- Inspect/possibly modify: `wiki/docs/vision.md`
- Inspect/possibly modify: `wiki/docs/demo-story.md`
- Inspect/possibly modify: `wiki/docs/operating-model.md`
- Inspect/possibly modify: `wiki/docs/iks-metadata-model.md`
- Inspect/possibly modify: `wiki/decisions/0001-use-port-for-idp-experiment.md`
- Inspect/possibly modify: `wiki/decisions/0003-adopt-backstage-for-self-hosted-idp.md`

**Pre-edit commands:**

```bash
git -C wiki status --short --branch
git -C wiki switch master
git -C wiki pull --ff-only
```

**Audit command:**

```bash
grep -RInE 'Port|port/|self-hosted portal|workspace|blueprint|action' wiki/Home.md wiki/_Sidebar.md wiki/docs wiki/decisions || true
```

**Edit rules:**
- `wiki/Home.md` should say Backstage is active target and Port is legacy migration context.
- `wiki/_Sidebar.md` should point to ADR 0003 as active target and ADR 0001 as superseded.
- `wiki/docs/demo-story.md` should describe Backstage Software Catalog, detail pages, advisory checks/scorecards, and GitHub issue workflow/fallback.
- `wiki/docs/operating-model.md` should preserve GitHub as versioned source of truth and avoid Port workspace operation as an active responsibility.
- `wiki/docs/iks-metadata-model.md` should align with Backstage annotations and `catalog-info.yaml` source of truth.
- `wiki/decisions/0001-*` may keep Port content because it is a superseded ADR, but its status must be clearly superseded by ADR 0003.
- `wiki/decisions/0003-*` should remain the active Backstage decision anchor.

**Wiki commit requirement if changed:**

```bash
git -C wiki add Home.md _Sidebar.md docs/vision.md docs/demo-story.md docs/operating-model.md docs/iks-metadata-model.md decisions/0001-use-port-for-idp-experiment.md decisions/0003-adopt-backstage-for-self-hosted-idp.md
git -C wiki commit -m "docs: align wiki with Backstage target cleanup"
git -C wiki push origin master
```

Then return to parent repo and stage `wiki` submodule pointer in a later parent commit.

**Verification:**
- `git -C wiki status --short` is clean after wiki commit/push if wiki changed.
- Parent repo shows `wiki` submodule pointer modified only if wiki changed.

### Task 7: Audit Backstage and migration mapping docs

**Objective:** Ensure Backstage docs and migration mapping agree with issue #23 and do not reintroduce duplicate source-of-truth or Port-target language.

**Files:**
- Inspect/possibly modify: `backstage/README.md`
- Inspect/possibly modify: `backstage/catalog/README.md`
- Inspect/possibly modify: `backstage/migration-issues.md`
- Inspect/possibly modify: `backstage/scorecards/README.md`
- Inspect/possibly modify: `backstage/templates/**/template.yaml`

**Commands:**

```bash
grep -RInE 'Port|port/|workspace|blueprint|action|validate-port-config' backstage || true
```

**Edit rules:**
- Keep Port references in migration mapping and scorecard comparison as legacy/reference context.
- Ensure `backstage/migration-issues.md` still lists #23 and #26 accurately.
- Ensure `backstage/catalog/README.md` keeps `examples/services/*/catalog-info.yaml` as authoritative Component source and `backstage/catalog/components.yaml` as reference-only.
- Do not add Backstage runtime scaffolding here; that belongs to #19.

**Verification:**
- Backstage docs describe one target direction.
- No Backstage doc says to import both central `components.yaml` and service-local `catalog-info.yaml` for the same entities.

### Task 8: Run stale-language classification search

**Objective:** Produce evidence for issue #23 acceptance criteria without blindly removing all Port references.

**Commands:**

```bash
grep -RInE 'Port|port/|self-hosted portal|workspace|blueprint|action|validate-port-config' \
  README.md AGENTS.md .github github agents backstage examples wiki port || true
```

**Classification checklist:**

Mark each hit as one of:
- Acceptable legacy/migration context:
  - `port/` legacy artifacts.
  - Superseded ADR 0001.
  - `backstage/migration-issues.md` superseded issue mapping.
  - Port maintainer agent/skill explicitly marked legacy.
  - Validation path including `port/` as legacy syntax coverage.
- Must fix:
  - Root README stale Port source-of-truth or next-step language.
  - Active `.github/workflows/validate-port-config.yml` or any active workflow named for Port.
  - Active issue templates asking for Port workspace/import/action work.
  - Wiki landing/navigation/doc pages presenting Port as active target.
  - Agent default prompts steering normal catalog work to Port instead of Backstage.

**Verification:**
- No unclassified suspicious hits remain.
- PR summary includes a short stale-language audit result.

### Task 9: Validate YAML and docs consistency

**Objective:** Prove the cleanup did not break YAML syntax or doc/source-of-truth consistency.

**Commands:**

```bash
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
```

If `yamllint` is unavailable locally:

```bash
command -v yamllint || echo "yamllint unavailable locally; rely on GitHub Actions and manual YAML read-through"
```

Additional checks:

```bash
git status --short
git submodule status
git diff --check
grep -RInE 'validate-port-config|Validate Port configuration' .github/workflows github/workflows || true
```

Manual consistency pass:
- Read `README.md` top-to-bottom and confirm it has no duplicated `Projektstatus` section.
- Read `wiki/Home.md` and `wiki/_Sidebar.md` if changed or if wiki pointer changed.
- Read `.github/workflows/validate-idp-config.yml` and `github/workflows/validate-idp-config.yml` for path parity.
- Confirm `backstage/migration-issues.md` still matches open issue queue and superseded Port issue mapping.

**Expected result:**
- YAML validation passes, or missing local validator is explicitly documented.
- No whitespace errors from `git diff --check`.
- Active workflow drift is removed.

### Task 10: Commit implementation changes

**Objective:** Create a reviewable commit that includes only issue #23 cleanup.

**Files likely to stage:**
- `agents/archive/hermes/plans/2026-05-22_070638-issue-23-repository-consistency-cleanup.md`
- `README.md`
- `.github/workflows/validate-port-config.yml` deletion
- `.github/workflows/validate-idp-config.yml` if synced/edited
- `github/workflows/validate-idp-config.yml` if synced/edited
- `.github/ISSUE_TEMPLATE/*` if edited
- `AGENTS.md` and/or `agents/**` if edited
- `backstage/**` if edited
- `wiki` submodule pointer if wiki docs changed and were already committed/pushed inside `wiki`

**Commands:**

```bash
git status --short
git add README.md .github/workflows github/workflows .github/ISSUE_TEMPLATE AGENTS.md agents backstage agents/archive/hermes/plans/2026-05-22_070638-issue-23-repository-consistency-cleanup.md
# If wiki changed and was committed inside the submodule:
git add wiki
git diff --cached --stat
git diff --cached --check
git commit -m "docs: finish Backstage repository cleanup"
```

**Expected result:**
- One focused commit for issue #23.
- No unrelated local changes staged.

### Task 11: Push and open PR after explicit approval

**Objective:** Publish the branch for review and link it to issue #23.

**Commands:**

```bash
git push -u origin HEAD
cat > /tmp/idp-iks-lab-pr-23-body.md <<'EOF'
## Summary
- Removes stale Port-as-target language from active repository docs.
- Removes the resurrected active Port validation workflow in favor of `validate-idp-config.yml`.
- Reviews active docs, workflows, issue templates, agent guidance, and Backstage migration references for Backstage/Port consistency.

## Validation
- `yamllint backstage port examples agents .github/ISSUE_TEMPLATE`
- `git diff --check`
- Manual stale-language classification for `Port`, `port/`, `self-hosted portal`, `workspace`, `blueprint`, `action`, and `validate-port-config`

Closes #23
EOF
gh pr create --base main --head "$(git branch --show-current)" --title "docs: finish Backstage repository cleanup" --body-file /tmp/idp-iks-lab-pr-23-body.md
```

**Expected result:**
- PR opens against `main`.
- PR body includes `Closes #23`.
- No PR should be opened in plan mode; this is a deferred execution step.

## Files likely to change

Likely required:
- `agents/archive/hermes/plans/2026-05-22_070638-issue-23-repository-consistency-cleanup.md`
- `README.md`
- `.github/workflows/validate-port-config.yml` deleted

Likely inspected and changed only if stale wording exists:
- `.github/workflows/validate-idp-config.yml`
- `github/workflows/validate-idp-config.yml`
- `.github/ISSUE_TEMPLATE/*`
- `github/issue-templates/README.md`
- `AGENTS.md`
- `agents/README.md`
- `agents/prompts/*.md`
- `agents/checklists/*.md`
- `agents/skills/**`
- `backstage/README.md`
- `backstage/catalog/README.md`
- `backstage/migration-issues.md`
- `backstage/scorecards/README.md`
- `backstage/templates/**/template.yaml`
- `wiki/Home.md`
- `wiki/_Sidebar.md`
- `wiki/docs/vision.md`
- `wiki/docs/demo-story.md`
- `wiki/docs/operating-model.md`
- `wiki/docs/iks-metadata-model.md`
- `wiki/decisions/0001-use-port-for-idp-experiment.md`
- `wiki/decisions/0003-adopt-backstage-for-self-hosted-idp.md`

Avoid unless explicitly justified:
- `port/**` functional changes. `port/` should remain legacy migration reference, not gain new behavior.

## Documentation updates and ADRs

- Main documentation target: `README.md`.
- Wiki documentation may need updates if stale Port-as-target wording remains in landing/navigation/domain docs.
- Backstage migration/reference docs may need minor consistency updates.
- No new ADR is expected. ADR 0003 already records the Backstage target decision; issue #23 implements consistency cleanup for that decision.
- If implementation discovers a new governance decision beyond cleanup, stop and ask before adding an ADR.

## Tests / validation

Required validation:

```bash
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
git diff --check
git status --short
git submodule status
grep -RInE 'validate-port-config|Validate Port configuration' .github/workflows github/workflows || true
```

Required manual validation:
- Read `README.md` and confirm there is only one project-status narrative and it points to Backstage.
- Confirm Port references in active docs are explicitly legacy/migration context.
- Confirm issue #23 acceptance criteria are satisfied.
- If wiki changed, confirm `git -C wiki status --short` is clean after its own commit/push and the parent repo records only the intended submodule pointer.

## Risks, tradeoffs, and open questions

- Risk: Removing all Port wording indiscriminately would erase useful migration context. Mitigation: classify hits; only remove Port-as-target wording.
- Risk: Deleting `.github/workflows/validate-port-config.yml` could remove coverage if `validate-idp-config.yml` is incomplete. Mitigation: verify `validate-idp-config.yml` covers `backstage`, `port`, `examples`, `agents`, and `.github/ISSUE_TEMPLATE`.
- Risk: Wiki edits require a two-repo commit/push sequence. Mitigation: only edit wiki if stale wording exists; commit and push inside `wiki` first.
- Open question: Should issue #17 be closed separately as completed? It appears decision-anchor acceptance criteria are checked, but #23 should not mutate trackers unless explicitly requested outside plan mode.
- Open question: Should `github/issue-templates/*` historical templates be archived more aggressively? Default plan is to keep them as historical references if clearly marked.

## Artifact inventory / traceability

- Plan file: `agents/archive/hermes/plans/2026-05-22_070638-issue-23-repository-consistency-cleanup.md`
  - Status: created by plan mode.
  - Intended to be committed with the issue #23 implementation branch if the user requests execution.
- External issue: #23
  - Status: read-only inspected in plan mode.
  - No comments, edits, labels, assignment, branch creation, commits, pushes, or PRs were performed in plan mode.
- Companion snapshots: none created.
- Deferred actions due to plan mode:
  - Create/check out issue-linked branch.
  - Edit repository docs/workflows.
  - Commit and push changes.
  - Comment on issue #23.
  - Open PR.
