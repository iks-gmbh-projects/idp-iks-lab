# Backstage Catalog Schema

This directory defines the catalog shape for the IKS IDP MVP. Backstage is the target portal, but this repository remains a docs-and-configuration source of truth rather than a production Backstage runtime.

## Source-of-truth rule

GitHub is the versioned source of truth for catalog descriptors. For service `Component` entities, the authoritative files are service-local:

- `examples/services/customer-portal/catalog-info.yaml`
- `examples/services/reporting-api/catalog-info.yaml`

`backstage/catalog/components.yaml` is retained only as a migration/reference copy while the repo moves away from the original Port experiment. Do not import it through `locations.yaml` while the service-local `catalog-info.yaml` files are imported, because that would create duplicate `Component` entity refs.

## Active catalog imports

`backstage/catalog/locations.yaml` is the root demo catalog location. It imports:

- `./groups.yaml`
- `./systems.yaml`
- Software Templates under `backstage/templates/`
- service-local `examples/services/*/catalog-info.yaml` files

It intentionally does not import `./components.yaml`.

The local runtime guide in `../runtime/README.md` shows how a generated Backstage app can load this root location.

## Entity shapes

### Location

Source file: `backstage/catalog/locations.yaml`

Required MVP fields:

- `apiVersion: backstage.io/v1alpha1`
- `kind: Location`
- `metadata.name`
- `metadata.description`
- `spec.targets`

Rules:

- Import shared `Group` and `System` files from this directory.
- Import service `Component` entities from service-local `catalog-info.yaml` files.
- Do not import a central component reference file and service-local component files for the same entities at the same time.

### Group

Source file: `backstage/catalog/groups.yaml`

Required MVP fields:

- `apiVersion: backstage.io/v1alpha1`
- `kind: Group`
- `metadata.name`
- `metadata.title`
- `spec.type`
- `spec.profile.displayName`

Recommended fields:

- `metadata.description`
- `spec.profile.email`
- `metadata.annotations.iks.dev/area`

Current demo groups:

- `platform-team` for technical ownership
- `iks-review-board` for IKS review workflows
- `customer-success` for business ownership

### System

Source file: `backstage/catalog/systems.yaml`

Required MVP fields:

- `apiVersion: backstage.io/v1alpha1`
- `kind: System`
- `metadata.name`
- `metadata.title`
- `spec.owner`

Recommended IKS field:

- `metadata.annotations.iks.dev/domain`

Current demo systems:

- `customer-experience`
- `management-reporting`

### Component

Authoritative import source: `examples/services/*/catalog-info.yaml`

Required MVP fields:

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

Optional/advisory MVP field:

- `metadata.annotations.iks.dev/runbook-url`

Link guidance:

- Add a documentation link for demo readability when documentation exists.
- Add a runbook link when `iks.dev/runbook-url` exists.
- A missing runbook is schema-compatible but should appear as a catalog-quality gap.

`customer-portal` is the complete demo service. `reporting-api` intentionally omits `iks.dev/runbook-url` and a runbook link to demonstrate advisory quality checks.

## Port-to-Backstage migration mapping

| Legacy Port artifact or concept | Backstage target | Notes |
|---|---|---|
| `port/blueprints/team.yaml` / `port/entities/teams.yaml` | `kind: Group` in `backstage/catalog/groups.yaml` | Keep owner refs stable. |
| `port/blueprints/system.yaml` / `port/entities/systems.yaml` | `kind: System` in `backstage/catalog/systems.yaml` | Preserve domain via `iks.dev/domain`. |
| `port/blueprints/service.yaml` / `port/entities/services.yaml` | Service-local `kind: Component` in `examples/services/*/catalog-info.yaml` | Components are imported from service-local files. |
| `port/blueprints/repository.yaml` / `port/entities/repositories.yaml` | `backstage.io/source-location` annotation | Do not add `Resource` entities unless a later issue needs them. |
| `port/blueprints/workflow.yaml` / `port/actions/*.yaml` | Backstage Software Templates and GitHub Issue Forms | Advisory workflows only. |
| `port/scorecards/*.yaml` | `backstage/scorecards/README.md` | Concrete check mechanism is issue #21 scope. |
| `examples/services/*/catalog.yaml` | Legacy service-local Port reference | Backstage source is `catalog-info.yaml`. |

## Validation expectations

For this repository, catalog validation currently means YAML and reference consistency rather than a full Backstage ingestion test. Run the lightest checks that prove the touched surface:

```bash
git diff --check
yamllint backstage port examples agents .github/ISSUE_TEMPLATE
```

If `yamllint` is unavailable, parse the changed YAML with another local YAML parser and perform a targeted manual read-through.

Reference consistency checks:

- `locations.yaml` imports service Components from service-local `catalog-info.yaml` files and not from `components.yaml`.
- Imported entity refs are unique by `kind`, namespace, and name.
- Each service `spec.owner` resolves to an existing `Group`.
- Each service `spec.system` resolves to an existing `System`.
- Each service `iks.dev/business-owner` should resolve to an existing `Group` unless explicitly documented otherwise.
- Required IKS annotations are present on service Components except for intentionally advisory gaps such as the `reporting-api` runbook.
