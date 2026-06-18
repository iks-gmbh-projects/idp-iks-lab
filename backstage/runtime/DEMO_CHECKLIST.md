# Backstage MVP Demo Verification Checklist

Use this checklist to verify the local Backstage demo path works end-to-end.

## Prerequisites

- [ ] Node.js LTS installed
- [ ] Yarn installed
- [ ] Python 3 with PyYAML installed
- [ ] Repository cloned with wiki submodule: `git clone --recurse-submodules`

## Local Runtime Setup

- [ ] Run `./scripts/start-backstage-docker.sh` or follow `backstage/runtime/README.md` manual steps
- [ ] Backstage frontend accessible at `http://localhost:3000`
- [ ] Backstage backend accessible at `http://localhost:7007`

## Catalog Import Verification

- [ ] Software Catalog shows 4 Groups: `platform-team`, `iks-review-board`, `ecreditreform`, `customer-success`
- [ ] Software Catalog shows 2 Systems: `customer-experience`, `management-reporting`
- [ ] Software Catalog shows 3 Components (services): `customer-portal`, `mycrefo`, `reporting-api`
- [ ] Software Catalog shows 3 Templates: `catalog-metadata-fix`, `iks-review-request`, `service-onboarding`
- [ ] No generated Backstage sample entities are mixed in

## Catalog Views (backstage/catalog/demo-views.md)

- [ ] All services view shows `customer-portal`, `mycrefo`, and `reporting-api`
- [ ] IKS-relevant services: filter by tag `iks` or inspect `iks.dev/compliance-scope` annotation
- [ ] Critical services: filter by tag `criticality-high` shows `customer-portal` and `mycrefo`

## Service Detail: customer-portal

- [ ] Technical owner: `group:default/platform-team`
- [ ] Business owner annotation: `iks.dev/business-owner: customer-success`
- [ ] System: `customer-experience`
- [ ] Repository: `backstage.io/source-location` present
- [ ] Lifecycle: `experimental`
- [ ] Documentation link or `backstage.io/techdocs-ref` present
- [ ] Runbook annotation `iks.dev/runbook-url` present
- [ ] Criticality: `iks.dev/criticality: high`
- [ ] Protection need: `iks.dev/protection-need: high`
- [ ] Data class: `iks.dev/data-class: personal-data`
- [ ] Compliance scope: `iks.dev/compliance-scope: iks,gdpr`

## Service Detail: reporting-api

- [ ] Technical owner: `group:default/platform-team`
- [ ] Business owner annotation: `iks.dev/business-owner: customer-success`
- [ ] System: `management-reporting`
- [ ] Repository: `backstage.io/source-location` present
- [ ] Lifecycle: `experimental`
- [ ] Documentation link or `backstage.io/techdocs-ref` present
- [ ] **Runbook MISSING** (intentional gap for scorecard demo)
- [ ] Criticality: `iks.dev/criticality: medium`
- [ ] Protection need: `iks.dev/protection-need: normal`
- [ ] Data class: `iks.dev/data-class: confidential`
- [ ] Compliance scope: `iks.dev/compliance-scope: iks`

## Service Detail: mycrefo

- [ ] Technical owner: `group:default/ecreditreform`
- [ ] Business owner annotation: `iks.dev/business-owner: customer-success`
- [ ] System: `customer-experience`
- [ ] Repository: `backstage.io/source-location` points to `iks-gmbh-projects/mycrefo`
- [ ] Lifecycle: `experimental`
- [ ] Documentation link or `backstage.io/techdocs-ref` present
- [ ] Runbook annotation intentionally not set until a concrete runbook exists
- [ ] Criticality: `iks.dev/criticality: high`
- [ ] Protection need: `iks.dev/protection-need: high`
- [ ] Data class: `iks.dev/data-class: personal-data`
- [ ] Compliance scope: `iks.dev/compliance-scope: iks,gdpr`

## Advisory Scorecard Checks (backstage/scorecards/)

Local test:
```bash
python3 -m pip install PyYAML
python3 backstage/scorecards/check_catalog_scorecards.py --assert-demo-fixtures
```

- [ ] `--assert-demo-fixtures` passes without errors
- [ ] Generate report: `python3 backstage/scorecards/check_catalog_scorecards.py --output /tmp/report.md`
- [ ] Report shows `customer-portal`: 11/11 checks PASS
- [ ] Report shows `reporting-api`: 10/11 checks PASS, 1 FAIL (runbook)

CI verification:
- [ ] GitHub Actions workflow runs scorecard report on PR/push
- [ ] Report appears in GitHub Actions step summary

## Software Template GitHub Integration (issue #22)

Prerequisites:
- [ ] GitHub Personal Access Token created with `repo` scope
- [ ] `GITHUB_TOKEN` environment variable set (see `backstage/runtime/GITHUB_INTEGRATION.md`)
- [ ] Backstage restarted to pick up token

Testing catalog-metadata-fix template:
- [ ] Navigate to "Create..." in Backstage
- [ ] Select "Catalog Metadata Fix" template
- [ ] Fill in parameters:
  - Component ref: `component:default/reporting-api`
  - Reason: `Runbook`
  - Details: `Missing runbook annotation - detected by scorecard check`
- [ ] Execute template
- [ ] Verify success message with issue URL
- [ ] Click issue URL and verify GitHub issue created
- [ ] Verify issue title: "Catalog metadata: component:default/reporting-api"
- [ ] Verify issue labels: `catalog`, `metadata`
- [ ] Verify issue body includes component ref, reason, details

Testing iks-review-request template:
- [ ] Navigate to "Create..." in Backstage
- [ ] Select "IKS Review Request" template
- [ ] Fill in parameters:
  - Component ref: `component:default/customer-portal`
  - Reason: `Pre-production IKS compliance review`
  - Fields to review: (check relevant items)
  - Requested decision: (select one)
- [ ] Execute template
- [ ] Verify success message with issue URL
- [ ] Click issue URL and verify GitHub issue created
- [ ] Verify issue title: "IKS review: component:default/customer-portal"
- [ ] Verify issue labels: `iks`, `review`
- [ ] Verify issue body includes all parameters

Fallback testing (without GitHub token):
- [ ] Templates still load in Backstage catalog
- [ ] Template execution shows clear error about missing credentials
- [ ] Error message points to `backstage/runtime/GITHUB_INTEGRATION.md`

GitHub Issue Forms (alternative workflow):
- [ ] Navigate to `.github/ISSUE_TEMPLATE/catalog-metadata-fix.yml`
- [ ] Verify issue form structure matches template parameters
- [ ] (Optional) Create a test issue manually to verify form fields

## TechDocs (Optional for #24)

TechDocs rendering may require additional local setup depending on Backstage version. Basic verification:

- [ ] `backstage.io/techdocs-ref` annotation present on services
- [ ] TechDocs source files exist: `examples/services/*/docs/index.md`

Full TechDocs rendering verification is optional for #24; defer to #15 if local rendering setup is complex.

## Demo Flow Complete (wiki/docs/demo-story.md)

- [ ] Catalog overview shows teams, systems, services
- [ ] IKS-relevant and critical service filtering works or manual inspection succeeds
- [ ] Service detail pages show all expected metadata
- [ ] Scorecard report demonstrates complete vs incomplete metadata
- [ ] GitHub Issue Forms available for follow-up workflows

## Known Gaps & Deferred Work

Document any gaps discovered:
- TechDocs rendering setup steps if needed
- Service onboarding template GitHub integration (no matching issue form yet)
- Production deployment story (explicitly out of MVP scope)
- Custom Backstage UI columns/filters (optional, tracked separately if needed)

## Notes

Record any local environment specifics, version mismatches, or deviation from documented path:

---

_Last updated: 2026-06-16 (issue #24)_
