# IKS Metadata Review Prompt

Use this prompt when reviewing service metadata.

Inspect the target service against the MVP IKS metadata model. Check owner, lifecycle, repository, documentation, criticality, protection need, data class, runbook, compliance scope, and relations. Report missing or inconsistent fields first, then propose the smallest catalog/doc changes needed.

Use the Code Review Pyramid in `agents/checklists/code-review-pyramid.md`: treat catalog metadata shape, entity refs, and relation semantics as review-critical contract concerns; leave wording/style suggestions as lower-priority follow-up.
