# Backstage Catalog Map

## Target files

- Root location: `backstage/catalog/locations.yaml`
- Groups: `backstage/catalog/groups.yaml`
- Systems: `backstage/catalog/systems.yaml`
- Central demo components: `backstage/catalog/components.yaml`
- Service-local descriptors: `examples/services/*/catalog-info.yaml`
- Templates: `backstage/templates/*/template.yaml`
- Scorecard/check mapping: `backstage/scorecards/README.md`
- Active issue forms: `.github/ISSUE_TEMPLATE/*.yml`

## Relation rules

- Component `spec.owner` should reference an existing Group, usually `group:default/platform-team`.
- Component `spec.system` should reference an existing System by name.
- IKS metadata should use `metadata.annotations.iks.dev/*`.
- Repository source should use `metadata.annotations.backstage.io/source-location`.
- TechDocs should use `metadata.annotations.backstage.io/techdocs-ref` when docs are available.

## Validation reminders

Run `yamllint backstage port examples agents .github/ISSUE_TEMPLATE` when available. If unavailable, parse touched YAML and manually inspect owner/system refs.
