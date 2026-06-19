# Backstage IDP MVP — Validation & Demo Dry-Run

This document records the validation pass and demo dry-run for the Backstage IDP
MVP, tracking issue #15. It captures what was checked, the results, the dry-run
approach taken, and the known limitations and residual risks for stakeholders.

Last validated: 2026-06-19.

## Scope of validation

- `backstage/`
- `examples/services/*/catalog-info.yaml`
- `agents/`
- `.github/ISSUE_TEMPLATE/`
- `wiki/docs/demo-story.md`, `wiki/docs/iks-metadata-model.md`
- `port/` only as legacy migration reference (not actively validated)

## AC1 — YAML validation

Command (mirrors the CI `validate-yaml` job config, which disables
`document-start` and `line-length`):

```bash
yamllint -d "{extends: default, rules: {document-start: disable, line-length: disable}}" \
  backstage port examples agents .github/ISSUE_TEMPLATE
```

Result: **PASS** (exit 0). CI `validate-yaml` and CodeQL also pass on `main`.

## AC2 — Manual consistency pass

All three demo services carry the required IKS metadata fields documented in
`wiki/docs/iks-metadata-model.md` (technical owner, business owner, system,
repository, lifecycle, criticality, protection need, data class, documentation,
IKS scope), and each field is covered by an advisory scorecard check.

Advisory scorecard report
(`python3 backstage/scorecards/check_catalog_scorecards.py`):

| Service          | Result | Notes                                         |
|------------------|--------|-----------------------------------------------|
| `customer-portal`| 11/11  | Complete reference service                    |
| `reporting-api`  | 10/11  | Fails only `catalog-quality/has-runbook` (intentional) |
| `mycrefo`        | 10/11  | Fails only `catalog-quality/has-runbook` (intentionally deferred) |

`--assert-demo-fixtures` passes (customer-portal all-pass, reporting-api fails
only the runbook check).

### Finding (resolved)

`wiki/docs/demo-story.md` still described the demo as using two services and
omitted `mycrefo`, while every other artifact (catalog descriptors,
`backstage/catalog/demo-views.md`, `backstage/runtime/DEMO_CHECKLIST.md`,
`backstage/scorecards/README.md`, `backstage/runtime/README.md`) already
included it. The demo story was updated to describe three services and note
mycrefo's intentional runbook gap, per `agents/validation.md` (demo-flow changes
must be reflected in `wiki/docs/demo-story.md`).

## AC3 — Demo dry-run

Approach: **documented static fallback**, the path sanctioned by
`backstage/runtime/README.md` ("If a contributor does not run a generated
Backstage app during review, record that as a validation fallback"). A live
Backstage run requires Docker, network access, and first-time
`npx @backstage/create-app` generation, which is out of band for this pass.

Statically verified against the versioned catalog source
(`backstage/catalog/locations.yaml` → `examples/services/*/catalog-info.yaml`):

- The catalog imports the expected entities — 4 Groups (`platform-team`,
  `iks-review-board`, `ecreditreform`, `customer-success`), 2 Systems
  (`customer-experience`, `management-reporting`), 3 Components
  (`customer-portal`, `mycrefo`, `reporting-api`), and 3 Templates.
- Component owners resolve to existing `Group` entities and systems to existing
  `System` entities.
- Demo-view filters in `backstage/catalog/demo-views.md` map to present
  annotations/tags (IKS-relevant via `iks.dev/compliance-scope`, critical via
  `iks.dev/criticality`).
- The scorecard report reproduces the demo story's quality signals
  (customer-portal complete; reporting-api and mycrefo show the runbook gap).
- The GitHub issue workflow exists as issue forms under
  `.github/ISSUE_TEMPLATE/` (catalog-metadata-fix, iks-review, backstage-migration).

Live-runtime smoke test (frontend on :3000, backend on :7007, TechDocs
rendering) is **not** executed in this pass and is recorded as the fallback per
the runtime guide. Use `backstage/runtime/DEMO_CHECKLIST.md` to complete it when
a live runtime is available.

## AC4 — Known limitations & residual risks

Known limitations:

- Live Backstage runtime and TechDocs rendering were not smoke-tested in this
  pass (documented fallback). The end-to-end UI walkthrough still needs a one-off
  live run via `backstage/runtime/DEMO_CHECKLIST.md`.
- `mycrefo` and `reporting-api` intentionally lack a runbook link; both surface as
  advisory `catalog-quality/has-runbook` failures by design.
- The runnable Backstage app is generated outside this repository; generator
  output can vary by version (see runtime README troubleshooting).
- The wiki lives in a git submodule; GitHub UI edits can advance it independently
  and stale submodule pointers can hide newer wiki content
  (`agents/validation.md`).

Residual risks for stakeholders:

- First live runtime run depends on external network access and Docker/Node
  availability.
- Scorecard checks are advisory only; they create visible follow-up signals but
  do not block teams or gate merges.

## Definition of Done

Status: met for the static validation scope. The live end-to-end demo walkthrough
is the one remaining item and is intentionally a documented fallback (see AC3 and
Known limitations), not a closed validation gate.

- **No production systems changed** — ✅ validation and dry-run operate only on
  versioned repository artifacts; no production calls.
- **End-to-end demo walkthrough** — ⏳ not executed in this pass. The catalog UI /
  TechDocs path still requires a one-off live run via
  `backstage/runtime/DEMO_CHECKLIST.md`; until then it remains a documented
  fallback / remaining risk rather than a verified, closed gate.
- **Remaining risks documented** — ✅ see above.
- **MVP scope unchanged** — ✅ still excludes Kubernetes, runtime health,
  provisioning, and autonomous compliance enforcement (consistent with
  `wiki/docs/demo-story.md` MVP-Abgrenzung).
