# Issue 7 Implementation Plan: Publish GitHub Source of Truth and Activate Validation

> Issue: [#7 MVP: Publish GitHub source of truth and activate validation](https://github.com/iks-gmbh-projects/idp-iks-lab/issues/7)

## Goal

Make GitHub the stable, versioned source of truth for the IDP IKS Lab MVP and ensure changes to Port, example, and agent artifacts are validated before merge.

## Current Context / Assumptions

- Repository: `iks-gmbh-projects/idp-iks-lab`
- Issue #7 is open and labeled `enhancement`.
- The repository currently treats GitHub as the versioned source of truth for Port configuration, demo entities, decisions, and docs.
- Existing relevant files:
  - `README.md`
  - `AGENTS.md`
  - `github/workflows/validate-port-config.yml`
- `AGENTS.md` states that `.github` is not used in this repo and workflow templates live under `github/workflows/`.
- Issue #7 requires deciding whether YAML validation should be active as a real GitHub Action or explicitly documented as template-only.
- MVP boundary remains unchanged:
  - No production infrastructure changes.
  - No Kubernetes or runtime-health integration.
  - No automatic infrastructure provisioning.
  - No autonomous compliance enforcement.

## Proposed Approach

Implement the smallest reviewable change that makes the validation path explicit and usable:

1. Confirm whether the MVP needs an active GitHub Action now.
2. If yes, copy the existing workflow template from `github/workflows/validate-port-config.yml` to `.github/workflows/validate-port-config.yml` and keep the template file only if it remains useful as source documentation.
3. Update documentation so users know which workflow is authoritative.
4. Validate YAML locally where tooling is available, and rely on GitHub Actions parity for final proof.
5. Open a PR that proves the validation path by running the workflow.

Recommended decision for the MVP: enable the real GitHub Action under `.github/workflows/` because issue #7 explicitly asks for validation before merge and the existing file under `github/workflows/` is only a template location.

## Step-by-Step Plan

### Step 1: Inspect current repository state

Commands:

```bash
git status --short
git branch --show-current
git remote get-url origin
```

Expected result:

- Working tree state is known before editing.
- Current branch is known.
- Remote points to `https://github.com/iks-gmbh-projects/idp-iks-lab.git` or an equivalent GitHub remote.

### Step 2: Create a feature branch

Command:

```bash
git switch -c issue-7-activate-github-validation
```

Expected result:

- Work is isolated from the current branch.

### Step 3: Activate the validation workflow

Create the active workflow path:

```bash
mkdir -p .github/workflows
cp github/workflows/validate-port-config.yml .github/workflows/validate-port-config.yml
```

Likely file to create:

- `.github/workflows/validate-port-config.yml`

Expected workflow content should validate YAML for:

```yaml
file_or_dir: port examples agents
```

Keep the workflow focused on the current MVP artifacts. Do not add Kubernetes, deployment, runtime health, or infrastructure checks.

### Step 4: Decide what to do with the template workflow

Choose one of these options:

#### Option A: Keep the template file

Keep:

- `github/workflows/validate-port-config.yml`

Update docs to explain that:

- `.github/workflows/validate-port-config.yml` is the active GitHub Actions workflow.
- `github/workflows/validate-port-config.yml` is a repository template/copy retained for documentation parity.

#### Option B: Remove the template file

Remove:

- `github/workflows/validate-port-config.yml`

Only choose this if the team agrees the template convention is no longer needed. This may conflict with existing `AGENTS.md` guidance, so Option A is safer for the MVP.

Recommended: Option A, because it is less disruptive and respects current repository guidance.

### Step 5: Update README documentation

Modify:

- `README.md`

Add or adjust a short validation section near the existing structure / next-steps content.

Suggested content:

```markdown
## Validierung

Die aktive GitHub-Actions-Validierung liegt unter `.github/workflows/validate-port-config.yml` und prueft YAML-Dateien in `port`, `examples` und `agents`.

Die Datei `github/workflows/validate-port-config.yml` bleibt als Vorlage/Referenz fuer die Workflow-Konfiguration erhalten.
```

Keep README language consistent with the existing German text and ASCII transliteration style (`Validierung`, `prueft`, etc.).

### Step 6: Update AGENTS.md if workflow convention changes

Modify only if the active workflow is added:

- `AGENTS.md`

Current guidance says:

```markdown
- GitHub Actions parity:
  `.github` is not used in this repo; workflow templates live under `github/workflows/`.
```

Update it to avoid stale instructions. Suggested replacement:

```markdown
- GitHub Actions parity:
  The active validation workflow lives under `.github/workflows/`. Template/reference workflow files may also exist under `github/workflows/`; keep them in sync when changing validation behavior.
```

This is a repository guidance change, but it is directly related to issue #7 and avoids future agent confusion.

### Step 7: Run local validation

Preferred command if `yamllint` is available:

```bash
yamllint port examples agents .github/workflows github/workflows
```

If `yamllint` is unavailable locally, document that explicitly and run a fallback parser if dependencies are available:

```bash
python3 - <<'PY'
from pathlib import Path
import sys
try:
    import yaml
except ImportError:
    print('PyYAML unavailable; use GitHub Actions or install yamllint for full validation')
    sys.exit(2)

paths = []
for root in ['port', 'examples', 'agents', '.github/workflows', 'github/workflows']:
    paths.extend(Path(root).rglob('*.yaml'))
    paths.extend(Path(root).rglob('*.yml'))

for path in paths:
    with path.open(encoding='utf-8') as f:
        yaml.safe_load(f)
print(f'Parsed {len(paths)} YAML files')
PY
```

Expected result:

- `yamllint` passes, or unavailable tooling is documented clearly.
- No syntax errors are introduced.

### Step 8: Review the diff

Commands:

```bash
git diff -- .github/workflows/validate-port-config.yml github/workflows/validate-port-config.yml README.md AGENTS.md
git status --short
```

Expected result:

- Diff is limited to validation workflow activation and docs/guidance updates.
- No Port identifiers, demo entities, scorecards, or MVP boundaries are changed.

### Step 9: Commit the implementation

Command:

```bash
git add .github/workflows/validate-port-config.yml README.md AGENTS.md
git commit -m "ci: activate port configuration validation"
```

If keeping template workflow in sync and it changes, include it in the commit:

```bash
git add github/workflows/validate-port-config.yml
```

Expected result:

- One focused commit exists for issue #7.

### Step 10: Push and open PR

Commands:

```bash
git push -u origin issue-7-activate-github-validation
gh pr create \
  --title "Activate Port configuration validation" \
  --body "Closes #7"
```

Expected result:

- PR is open.
- PR references `Closes #7`.
- GitHub Actions validation runs on the PR.

### Step 11: Verify GitHub Actions result

Commands:

```bash
gh pr checks --watch
```

Expected result:

- Validation workflow completes successfully.
- If it fails due to YAML style issues, fix the files rather than weakening validation unless the rule is clearly inappropriate for the repo.

## Files Likely to Change

Required if activating validation:

- `.github/workflows/validate-port-config.yml` — new active GitHub Actions workflow.

Likely documentation updates:

- `README.md` — document active validation behavior.
- `AGENTS.md` — update repository guidance about active `.github/workflows/` usage.

Possibly unchanged but relevant:

- `github/workflows/validate-port-config.yml` — existing template/reference workflow. Keep in sync if the active workflow differs.

## Documentation Updates

- Update `README.md` to describe active validation.
- Update `AGENTS.md` if the repository now uses `.github/workflows/`.
- No wiki documentation update is required unless the team wants operating-model documentation to mention CI validation explicitly.
- No ADR is expected for this issue. Activating CI validation is an implementation/operational step, not a meaningful architecture or governance decision.

## Tests / Validation

Minimum validation:

```bash
yamllint port examples agents .github/workflows github/workflows
```

Repository-state validation:

```bash
git status --short
git diff --check
```

GitHub validation:

```bash
gh pr checks --watch
```

Manual checks:

- Confirm workflow path is `.github/workflows/validate-port-config.yml`.
- Confirm the workflow validates `port`, `examples`, and `agents`.
- Confirm README and AGENTS.md do not contradict each other.
- Confirm no MVP out-of-scope capabilities were introduced.

## Risks, Tradeoffs, and Open Questions

### Risks

- Enabling `.github/workflows/` changes the previous repository convention documented in `AGENTS.md`.
- Duplicating the workflow under both `.github/workflows/` and `github/workflows/` creates drift risk.
- `yamllint` may fail on existing style issues that were previously unvalidated.

### Tradeoffs

- Keeping both workflow files preserves the existing template convention but requires future sync discipline.
- Removing `github/workflows/validate-port-config.yml` reduces duplication but changes repository structure more aggressively.

### Open Questions

- Should `github/workflows/` remain as a template/reference directory after activating real GitHub Actions?
- Should local development instructions include installing `yamllint`?
- Should future validation include JSON schema checks for Port artifacts, or is YAML syntax enough for the MVP?

## Recommended MVP Outcome

For issue #7, implement only:

- Active GitHub Actions YAML validation under `.github/workflows/`.
- Small documentation updates in `README.md` and `AGENTS.md`.
- No schema validation, Port API checks, or external system mutations yet.

This satisfies the issue while keeping the MVP boundary small and reviewable.
