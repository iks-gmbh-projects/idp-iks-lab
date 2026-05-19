---
name: port-catalog-maintainer
description: Maintain and review Port catalog artifacts in the IDP IKS lab repository, including blueprints, entities, scorecards, actions, automations, and example service catalog files. Use when Codex needs to edit or inspect Port YAML, preserve catalog identifiers and relations, update related docs, or validate catalog configuration.
---

# Port Catalog Maintainer

## Workflow

1. Read `AGENTS.md` and the relevant files under `port/`, `examples/services/`, and `docs/`.
2. Identify the catalog surface: blueprint, entity, scorecard, action, automation, or service-local catalog file.
3. Preserve stable identifiers, relation names, and enum values unless the user explicitly asks for a migration.
4. When changing schema or required fields, update demo entities and affected docs in the same change.
5. Keep MVP scope intact: no Kubernetes, runtime health, infrastructure provisioning, or autonomous production actions.
6. Validate YAML and manually inspect cross-file relations before reporting completion.

## Reference Loading

- Read `references/port-catalog-map.md` when you need the repo-specific Port artifact map, relation rules, or validation reminders.

## Output Expectations

- State the catalog behavior changed.
- List validation performed.
- Call out any import, identifier, relation, or Port workspace follow-up risk.
