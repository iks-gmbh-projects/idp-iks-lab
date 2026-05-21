# Agent Validation Guide

Use these checks after changing agent artifacts, Backstage catalog/configuration, issue forms, legacy Port references, or example catalog data.

## YAML

- Preferred local command: `yamllint backstage port examples agents .github/ISSUE_TEMPLATE`
- GitHub workflow template: `github/workflows/validate-idp-config.yml`
- If `yamllint` is unavailable, parse the touched YAML with an available YAML parser and manually inspect identifiers, refs, relations, and required metadata.

## Backstage Catalog Consistency

- Entity `kind`, `metadata.name`, `spec.owner`, and `spec.system` values should remain stable unless the change explicitly migrates them.
- Component owners must point to existing `Group` entities.
- Component systems must point to existing `System` entities.
- Service-local `examples/services/*/catalog-info.yaml` files should stay consistent with central demo descriptors in `backstage/catalog/`.
- IKS annotations should use the `iks.dev/` namespace documented in `wiki/docs/iks-metadata-model.md`.
- Example app config must not include secrets, real OAuth credentials, or production-only endpoints.

## Legacy Port Consistency

- `port/` is a migration reference. Avoid adding new Port-only behavior unless explicitly requested.
- When legacy Port files are touched, preserve identifiers and relations unless the task is a migration cleanup.

## Codex Skills

Validate each changed skill with the local Codex `quick_validate.py` script when available.

Check that:

- `SKILL.md` has only `name` and `description` in frontmatter.
- `agents/openai.yaml` default prompts mention the exact `$skill-name`.
- References are loaded only when useful for the task.

## Documentation Consistency

- Schema or annotation changes should be reflected in `wiki/docs/iks-metadata-model.md` when they affect service metadata.
- Governance or scope decisions should be captured in `wiki/decisions/` when they change the MVP boundary.
- Demo flow changes should be reflected in `wiki/docs/demo-story.md`.

## Wiki Submodule

- Initialize docs with `git submodule update --init --remote --merge wiki`.
- Before editing wiki docs, run `git -C wiki switch master` and `git -C wiki pull --ff-only`.
- Commit and push wiki changes inside `wiki`, then commit the updated `wiki` submodule pointer in the main repository.
- Remaining risks: GitHub UI edits can advance the wiki independently, stale submodule pointers can hide new wiki content, and CI or agents must initialize submodules explicitly.
