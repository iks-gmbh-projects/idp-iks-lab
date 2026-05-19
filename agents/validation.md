# Agent Validation Guide

Use these checks after changing agent artifacts, Port configuration, or example catalog data.

## YAML

- Preferred local command: `yamllint port examples agents`
- GitHub workflow template: `github/workflows/validate-port-config.yml`
- If `yamllint` is unavailable, parse the touched YAML with an available YAML parser and manually inspect identifiers, relations, and required properties.

## Port Catalog Consistency

- Blueprint identifiers must remain stable unless the change explicitly migrates entities.
- Entity `blueprint` values must match files under `port/blueprints/`.
- Entity relations must point to existing identifiers in the target entity file.
- Scorecards and actions should use field names that exist in the relevant blueprint schema or relations.

## Codex Skills

Validate each skill:

`C:\Users\wla_dev\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe C:\Users\wla_dev\.codex\skills\.system\skill-creator\scripts\quick_validate.py agents\skills\<skill-name>`

Check that:

- `SKILL.md` has only `name` and `description` in frontmatter.
- `agents/openai.yaml` default prompts mention the exact `$skill-name`.
- References are loaded only when useful for the task.

## Documentation Consistency

- Schema changes should be reflected in `docs/iks-metadata-model.md` when they affect service metadata.
- Governance or scope decisions should be captured in `decisions/` when they change the MVP boundary.
- Demo flow changes should be reflected in `docs/demo-story.md`.
