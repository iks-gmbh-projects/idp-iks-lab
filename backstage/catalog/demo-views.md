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

- Filter or search by tag `iks` if the generated Backstage app exposes tag filtering/search.
- Fallback: open each service and inspect `metadata.annotations.iks.dev/compliance-scope`; it must contain `iks`.

Expected services:

- `customer-portal` (`iks.dev/compliance-scope: iks,gdpr`)
- `reporting-api` (`iks.dev/compliance-scope: iks`)

## View: critical services

Default UI path:

- Filter or search by tag `criticality-high` or `criticality-critical` if available.
- Fallback: inspect `metadata.annotations.iks.dev/criticality` on service details.

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

## Tag convention

The MVP mirrors selected IKS annotations into `metadata.tags` so the default Catalog UI can support simple filtering or search without app customization:

- `iks`: service has `iks` in `iks.dev/compliance-scope`.
- `criticality-high` / `criticality-critical`: service belongs in the critical-services demo view.
- `criticality-medium` / `criticality-low`: service remains visible for comparison but should not appear in the critical-services view.
- `data-personal` / `data-confidential`: optional data-class context for demo filtering.

The authoritative IKS metadata remains in `metadata.annotations.iks.dev/*`. Keep tags synchronized with the corresponding annotations when service metadata changes.

## Optional generated-app customization

If default Backstage filtering is not clear enough for the stakeholder demo, a future runtime/app issue can add custom Catalog table columns or annotation filters in the generated app. Keep that outside this repository unless a decision explicitly changes the repository boundary.
