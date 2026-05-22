---
name: iks-metadata-reviewer
description: Review service catalog metadata for IKS readiness in the IDP IKS lab repository. Use when Codex needs to inspect services for required owner, lifecycle, repository, documentation, criticality, protection need, data class, runbook, compliance scope, and relation completeness, then propose minimal catalog fixes.
---

# IKS Metadata Reviewer

## Workflow

1. Read `wiki/docs/iks-metadata-model.md`, the target service entity, and any service-local Backstage `catalog-info.yaml`; use `catalog.yaml` only as a legacy Port reference if needed.
2. Compare the service against MVP catalog readiness: owner, business owner, lifecycle, repository, documentation, criticality, protection need, and data class.
3. Also report operational gaps such as empty runbook links, missing `iks` compliance scope for IKS-relevant services, or broken relations.
4. Apply `agents/checklists/code-review-pyramid.md`: treat metadata shape, entity refs, relation targets, and required IKS fields as API/contract and semantic readiness concerns.
5. Prefer concrete YAML edits or issue text over broad policy language.
6. Keep findings ordered by impact: missing required metadata, inconsistent relations, documentation/validation gaps, then hygiene or wording improvements.

## Reference Loading

- Read `references/review-rules.md` for the concise field checklist and reporting format.

## Output Expectations

- Give a pass/fail readiness result for each reviewed service.
- Name missing or inconsistent fields exactly as they appear in the catalog.
- Suggest the smallest safe fix.
- Avoid style-only findings unless they affect catalog understanding or maintainability.
