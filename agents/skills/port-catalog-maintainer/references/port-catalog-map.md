# Port Catalog Map

## Primary Paths

- `port/blueprints/`: Port data model for teams, systems, repositories, services, workflows, and agents.
- `port/entities/`: demo catalog data imported into Port.
- `port/scorecards/`: quality and IKS baseline checks.
- `port/actions/`: low-risk self-service workflows that create tasks or checklists.
- `port/automations/`: notification-style workflow definitions.
- `examples/services/*/catalog.yaml`: service-local metadata examples.

## Relation Expectations

- Service `owner` relation targets `team`.
- Service `system` relation targets `system`.
- Service `repository` relation targets `repository`.
- Agent `owner` relation targets `team`.
- Workflow `owner` relation targets `team`.

## MVP Guardrails

- Keep actions auditable and human-reviewable.
- Do not add direct production mutation.
- Do not introduce Kubernetes or runtime health as MVP behavior.
