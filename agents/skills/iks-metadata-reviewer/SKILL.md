---
name: iks-metadata-reviewer
description: Review service catalog metadata for IKS readiness in the IDP IKS lab repository. Use when Codex needs to inspect services for required owner, lifecycle, repository, documentation, criticality, protection need, data class, runbook, compliance scope, and relation completeness, then propose minimal catalog fixes.
---

# IKS Metadata Reviewer

## Workflow

1. Read `docs/iks-metadata-model.md`, the target service entity, and any service-local `catalog.yaml`.
2. Compare the service against MVP catalog readiness: owner, business owner, lifecycle, repository, documentation, criticality, protection need, and data class.
3. Also report operational gaps such as empty runbook links, missing `iks` compliance scope for IKS-relevant services, or broken relations.
4. Prefer concrete YAML edits or issue text over broad policy language.
5. Keep findings ordered by impact: missing required metadata, inconsistent relations, then hygiene improvements.

## Reference Loading

- Read `references/review-rules.md` for the concise field checklist and reporting format.

## Output Expectations

- Give a pass/fail readiness result for each reviewed service.
- Name missing or inconsistent fields exactly as they appear in the catalog.
- Suggest the smallest safe fix.
