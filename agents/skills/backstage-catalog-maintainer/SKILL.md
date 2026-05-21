---
name: backstage-catalog-maintainer
description: Maintain and review Backstage catalog artifacts in the IDP IKS lab repository, including catalog entities, locations, templates, issue forms, scorecard/check mappings, and example service catalog files.
---

# Backstage Catalog Maintainer

## Workflow

1. Read `AGENTS.md` and the relevant files under `backstage/`, `examples/services/`, `.github/ISSUE_TEMPLATE/`, and `wiki/docs/`.
2. Identify the catalog surface: entity, location, template, scorecard/check mapping, issue form, or service-local `catalog-info.yaml` file.
3. Preserve stable entity names, refs, annotation names, and relation targets unless the user explicitly asks for a migration.
4. When changing schema, annotations, or required metadata, update demo entities and affected docs in the same change.
5. Keep MVP scope intact: no Kubernetes, runtime health, infrastructure provisioning, or autonomous production actions.
6. Validate YAML and manually inspect cross-file relations before reporting completion.

## Reference Loading

- Read `references/backstage-catalog-map.md` when you need the repo-specific Backstage artifact map, relation rules, or validation reminders.

## Output Expectations

- State the catalog behavior changed.
- List validation performed.
- Call out any ingestion, identifier, relation, Backstage template, or migration follow-up risk.
