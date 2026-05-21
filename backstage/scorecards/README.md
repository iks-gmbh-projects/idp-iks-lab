# Backstage Scorecard Mapping

The previous Port experiment used two scorecards: Catalog Quality and IKS Baseline. Backstage does not consume those Port scorecard YAML files directly, so this directory documents the target checks until a concrete Backstage scorecard mechanism is selected.

Preferred options, in order:

1. Backstage Tech Insights checks, if the selected Backstage distribution supports the required checks with acceptable effort.
2. A maintained Backstage scorecard plugin, if it fits the MVP without introducing heavy custom development.
3. A lightweight GitHub validation/report for the first demo, rendered or linked from Backstage.

The MVP behavior remains advisory. Checks may create visibility and follow-up issues, but they must not block teams, provision infrastructure, or make compliance decisions.

## Catalog Quality mapping

| Rule | Backstage field |
|---|---|
| Technical owner is assigned | `spec.owner` |
| System is assigned | `spec.system` |
| Repository is linked | `metadata.annotations.backstage.io/source-location` |
| Lifecycle is classified | `spec.lifecycle` |
| Documentation link is present | `metadata.annotations.backstage.io/techdocs-ref` or documentation link |
| Runbook link is present | `metadata.annotations.iks.dev/runbook-url` or runbook link |

## IKS Baseline mapping

| Rule | Backstage field |
|---|---|
| Business owner is assigned | `metadata.annotations.iks.dev/business-owner` |
| Criticality is classified | `metadata.annotations.iks.dev/criticality` |
| Protection need is classified | `metadata.annotations.iks.dev/protection-need` |
| Data class is classified | `metadata.annotations.iks.dev/data-class` |
| IKS scope is declared | `metadata.annotations.iks.dev/compliance-scope` contains `iks` |

`customer-portal` is the complete example. `reporting-api` intentionally omits the runbook annotation to demonstrate a catalog-quality gap.
