# Issue #21 Advisory Catalog Quality and IKS Checks Implementation Plan

## Goal

Implement issue #21 by replacing the legacy Port scorecards with Backstage-compatible advisory checks that run against this repository's Backstage catalog data.

The implementation should stay inside the repository's MVP boundary:

- no generated Backstage app committed to this repository,
- no Kubernetes, infrastructure, runtime health, or production automation,
- no autonomous compliance enforcement,
- advisory report output only.

## Current context

- Issue: #21 `Backstage IDP MVP: Implement advisory catalog quality and IKS checks`.
- Branch: `21-advisory-catalog-quality-iks-checks`.
- Backstage catalog import root: `backstage/catalog/locations.yaml`.
- Authoritative service descriptors:
  - `examples/services/customer-portal/catalog-info.yaml`
  - `examples/services/reporting-api/catalog-info.yaml`
- Legacy scorecard references:
  - `port/scorecards/catalog-quality.yaml`
  - `port/scorecards/iks-baseline.yaml`
- Current mapping doc: `backstage/scorecards/README.md`.
- `customer-portal` is the complete demo service and should pass all checks.
- `reporting-api` intentionally omits the runbook annotation/link and should fail only the runbook check.
- The repository has no committed app runtime, no package manifest, and no existing validation script tree.
- The active workflow currently runs YAML validation only in `.github/workflows/validate-idp-config.yml`.

## Decision

Use a lightweight repository-owned Python checker plus a generated Markdown report as the MVP implementation path.

Do not implement Backstage Tech Insights or a scorecard plugin in this issue. Those remain future runtime/app choices because this repository currently stores catalog descriptors and config examples, not a generated Backstage application.

The checker is advisory:

- check failures are reported as `FAIL`,
- report generation itself exits successfully when advisory checks fail,
- the command exits nonzero only for execution problems such as unreadable files, invalid YAML, unresolved expected inputs, or internal errors,
- documentation must state that results are signals for follow-up, not compliance decisions or deployment gates.

## Implementation tasks

### 1. Add executable check definitions

Create `backstage/scorecards/checks.yaml` as the executable mapping from legacy scorecards to Backstage catalog fields.

Use two groups:

- `catalog-quality`
- `iks-baseline`

Define exactly these checks for the first MVP iteration:

| Group | Check id | Title | Evaluation |
|---|---|---|---|
| `catalog-quality` | `has-technical-owner` | Technical owner is assigned | `spec.owner` is present and non-empty |
| `catalog-quality` | `has-system` | System is assigned | `spec.system` is present and non-empty |
| `catalog-quality` | `has-repository` | Repository is linked | `metadata.annotations.backstage.io/source-location` is present and non-empty |
| `catalog-quality` | `has-lifecycle` | Lifecycle is classified | `spec.lifecycle` is present and non-empty |
| `catalog-quality` | `has-documentation` | Documentation link is present | `metadata.annotations.backstage.io/techdocs-ref` is present, or `metadata.links[]` contains a documentation/docs link |
| `catalog-quality` | `has-runbook` | Runbook link is present | `metadata.annotations.iks.dev/runbook-url` is present, or `metadata.links[]` contains a runbook link |
| `iks-baseline` | `has-business-owner` | Business owner is assigned | `metadata.annotations.iks.dev/business-owner` is present and non-empty |
| `iks-baseline` | `has-criticality` | Criticality is classified | `metadata.annotations.iks.dev/criticality` is present and non-empty |
| `iks-baseline` | `has-protection-need` | Protection need is classified | `metadata.annotations.iks.dev/protection-need` is present and non-empty |
| `iks-baseline` | `has-data-class` | Data class is classified | `metadata.annotations.iks.dev/data-class` is present and non-empty |
| `iks-baseline` | `has-iks-scope` | IKS scope is declared | `metadata.annotations.iks.dev/compliance-scope` contains token `iks`, splitting comma-separated values and trimming whitespace |

Keep enum validation out of scope for this issue. The first MVP checks presence/classification and IKS-scope membership only, matching the legacy scorecard semantics and the current catalog schema docs.

### 2. Add the local report generator

Create `backstage/scorecards/check_catalog_scorecards.py`.

Behavior:

- Use Python 3 and PyYAML.
- Inputs:
  - `--catalog-root`, default `backstage/catalog/locations.yaml`.
  - `--checks`, default `backstage/scorecards/checks.yaml`.
  - `--output`, optional Markdown report path; if omitted, print Markdown to stdout.
  - `--assert-demo-fixtures`, optional validation mode for the current demo data.
- Resolve `spec.targets` from the catalog root relative to the directory containing `locations.yaml`.
- Load YAML documents from imported targets.
- Evaluate only `kind: Component` entities where `spec.type: service`.
- Ignore the reference-only `backstage/catalog/components.yaml` because it is not imported by `locations.yaml`.
- For each service/check pair, produce a result with:
  - service name,
  - group id,
  - check id,
  - check title,
  - status `PASS` or `FAIL`,
  - field/source used,
  - short remediation hint for failures.
- Generate a Markdown report with:
  - heading `# Catalog Quality and IKS Checks Report`,
  - generation source paths,
  - summary table by service with pass/fail counts,
  - detailed result table grouped by service,
  - note that the report is advisory and does not enforce compliance.
- Default exit behavior:
  - exit `0` if the report was generated, even when advisory checks fail,
  - exit nonzero only if inputs cannot be loaded or parsed.
- `--assert-demo-fixtures` behavior:
  - assert `customer-portal` has zero failed checks,
  - assert `reporting-api` has exactly one failed check: `catalog-quality/has-runbook`,
  - exit nonzero if those expectations are not met.

### 3. Document the advisory check workflow

Update `backstage/scorecards/README.md` so it becomes the primary user documentation for #21.

Required content:

- State that the MVP implementation is the local/CI Markdown report path.
- Explain that Tech Insights or a Backstage scorecard plugin remains a future runtime/app integration option.
- Point to `checks.yaml` as the executable check mapping.
- Document local commands:

```bash
python3 -m pip install PyYAML
python3 backstage/scorecards/check_catalog_scorecards.py \
  --catalog-root backstage/catalog/locations.yaml \
  --checks backstage/scorecards/checks.yaml \
  --output /tmp/catalog-scorecard-report.md
python3 backstage/scorecards/check_catalog_scorecards.py --assert-demo-fixtures
```

- Explain expected demo results:
  - `customer-portal`: all checks pass,
  - `reporting-api`: fails `catalog-quality/has-runbook` intentionally.
- Explain interpretation:
  - `PASS` means the mapped Backstage metadata is present,
  - `FAIL` means the service needs follow-up metadata work,
  - failures are advisory and should lead to GitHub issue workflows in #22, not enforcement.

Optionally update `README.md` and `backstage/README.md` only if the current references to scorecards still say the approach is undecided after this implementation. Keep German root README language intact.

### 4. Add CI report generation without enforcement

Update `.github/workflows/validate-idp-config.yml` to add an advisory report step after YAML validation.

Implementation details:

- Use the existing workflow instead of adding a new workflow file.
- Add Python setup and PyYAML installation only for this report step.
- Run the checker against `backstage/catalog/locations.yaml` and `backstage/scorecards/checks.yaml`.
- Write the Markdown report to a workspace file such as `catalog-scorecard-report.md`.
- Append the report to `$GITHUB_STEP_SUMMARY` so PR reviewers can see the advisory results in GitHub Actions.
- Do not fail the workflow because `reporting-api` has an advisory runbook failure.
- The workflow may still fail if the script cannot parse inputs or cannot generate the report.

Keep any reference/template workflow in sync only if a corresponding `github/workflows/validate-idp-config.yml` file exists in the working tree. If it does not exist, do not create that legacy template path for this issue.

### 5. Validation before PR

Run these checks locally:

```bash
git diff --check
```

Run YAML validation if available:

```bash
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
```

If `yamllint` is unavailable locally, record the caveat and rely on the active GitHub Actions YAML validation.

Run checker validation:

```bash
python3 -m pip install PyYAML
python3 backstage/scorecards/check_catalog_scorecards.py \
  --catalog-root backstage/catalog/locations.yaml \
  --checks backstage/scorecards/checks.yaml \
  --output /tmp/catalog-scorecard-report.md
python3 backstage/scorecards/check_catalog_scorecards.py --assert-demo-fixtures
```

If local network restrictions prevent installing PyYAML, request escalation for the install. If it still cannot be installed locally, document the limitation in the PR and rely on CI for the checker run.

Manual consistency pass:

- Confirm `checks.yaml` and `backstage/scorecards/README.md` list the same 11 checks.
- Confirm `customer-portal` remains the complete passing service.
- Confirm `reporting-api` still intentionally lacks `iks.dev/runbook-url` and a runbook link.
- Confirm no generated Backstage app files, lockfiles, production runtime config, Kubernetes automation, or infrastructure provisioning are introduced.

### 6. PR and tracker updates

Commit implementation on `21-advisory-catalog-quality-iks-checks`.

PR title:

```text
docs: add advisory catalog scorecard report
```

PR body summary:

```markdown
## Summary
- Adds executable advisory catalog quality and IKS check definitions for Backstage catalog data.
- Adds a local/CI Markdown report generator for the demo service scorecards.
- Documents expected demo results: `customer-portal` passes and `reporting-api` intentionally fails the runbook check.

Closes #21

## Validation
- [ ] git diff --check
- [ ] yamllint backstage port examples agents .github/ISSUE_TEMPLATE, or local unavailable + CI validation
- [ ] python3 backstage/scorecards/check_catalog_scorecards.py --assert-demo-fixtures
- [ ] GitHub Actions advisory report generated successfully
```

After opening the PR, check CI. The advisory report should show one intentional `reporting-api` failure for `has-runbook` while the workflow itself succeeds if report generation works.

## Files expected to change

Expected implementation files:

- `backstage/scorecards/checks.yaml`
- `backstage/scorecards/check_catalog_scorecards.py`
- `backstage/scorecards/README.md`
- `.github/workflows/validate-idp-config.yml`
- this plan file under `.hermes/plans/`

Possible documentation-only updates if stale wording remains:

- `README.md`
- `backstage/README.md`
- `backstage/migration-issues.md`

Do not edit the wiki submodule for this issue unless a reviewer explicitly asks for demo-story packaging changes.

## Risks and tradeoffs

- PyYAML is a small validation dependency, but this repo currently has no Python dependency file. Keep it as a CI/local command dependency rather than introducing a broader package management setup.
- A Markdown report is less polished than Backstage Tech Insights, but it fits the MVP boundary and can be linked or pasted into the demo while plugin selection remains open.
- Advisory checks duplicate some catalog schema requirements. The value is visibility and per-service reporting, not hard enforcement.
- If future services are added, the report will include them automatically when they are imported by `backstage/catalog/locations.yaml` as `Component` services.
