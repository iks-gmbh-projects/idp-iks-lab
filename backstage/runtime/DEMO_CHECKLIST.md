# Backstage MVP Demo Verification Checklist

Use this checklist to verify the local Backstage demo path works end-to-end.

## Prerequisites

- [ ] Node.js LTS installed
- [ ] Yarn installed
- [ ] Python 3 with PyYAML installed
- [ ] Repository cloned with wiki submodule: `git clone --recurse-submodules`

## Local Runtime Setup

- [ ] Run `./scripts/start-backstage.sh` or follow `backstage/runtime/README.md` manual steps
- [ ] Backstage frontend accessible at `http://localhost:3000`
- [ ] Backstage backend accessible at `http://localhost:7007`

## Catalog Import Verification

- [ ] Software Catalog shows 3 Groups: `platform-team`, `iks-review-board`, `customer-success`
- [ ] Software Catalog shows 2 Systems: `customer-experience`, `management-reporting`
- [ ] Software Catalog shows 2 Components (services): `customer-portal`, `reporting-api`
- [ ] Software Catalog shows 3 Templates: `catalog-metadata-fix`, `iks-review-request`, `service-onboarding`
- [ ] No generated Backstage sample entities are mixed in

## Catalog Views (backstage/catalog/demo-views.md)

- [ ] All services view shows both `customer-portal` and `reporting-api`
- [ ] IKS-relevant services: filter by tag `iks` or inspect `iks.dev/compliance-scope` annotation
- [ ] Critical services: filter by tag `criticality-high` shows `customer-portal` only

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

## GitHub Issue Workflow (Fallback for MVP)

The MVP Software Templates are advisory-only and use `debug:log` actions. The active workflow path uses GitHub Issue Forms:

- [ ] Navigate to `.github/ISSUE_TEMPLATE/catalog-metadata-fix.yml`
- [ ] Verify issue form structure matches template parameters
- [ ] (Optional) Create a test issue manually to verify form fields

Full Software Template GitHub integration testing is tracked by issue #22.

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
- Software Template GitHub integration (tracked by #22)
- Production deployment story (explicitly out of MVP scope)
- Custom Backstage UI columns/filters (optional, tracked separately if needed)

## Notes

Record any local environment specifics, version mismatches, or deviation from documented path:

---

_Last updated: 2026-06-16 (issue #24)_
