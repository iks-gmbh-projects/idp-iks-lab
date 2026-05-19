# IKS Metadata Review Rules

## Required For MVP Catalog Readiness

- `relations.owner`
- `properties.businessOwner`
- `properties.lifecycle`
- `relations.repository`
- `properties.documentation`
- `properties.criticality`
- `properties.protectionNeed`
- `properties.dataClass`

## Expected Hygiene

- `properties.runbook` should be a useful URL for operational services.
- `properties.complianceScope` should include `iks` for IKS-relevant services.
- `relations.system` should point to an existing system entity.
- URLs should not be empty strings unless the demo intentionally shows a gap.

## Reporting Format

- Start with service identifier and readiness result.
- Then list missing or inconsistent fields.
- End with a minimal fix proposal and validation recommendation.
