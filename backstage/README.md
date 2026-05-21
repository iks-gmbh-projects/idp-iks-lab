# Backstage Target Structure

Backstage is the target portal for the self-hosted IKS IDP MVP. This repository stores catalog descriptors, example configuration, template definitions, scorecard mapping, and validation guidance. It does not yet contain a runnable Backstage application runtime.

GitHub remains the versioned source of truth. Backstage should read catalog locations and service descriptors from this repository.

## Contents

- `app-config.example.yaml`: non-secret example configuration for a Backstage instance.
- `catalog/`: Backstage catalog locations and shared demo entities. Service `Component` entities are imported from `examples/services/*/catalog-info.yaml`; `catalog/components.yaml` is retained as a central reference copy during migration.
- `templates/`: advisory Software Template definitions for GitHub-tracked workflows.
- `techdocs/`: example TechDocs configuration.
- `scorecards/`: mapping from the previous scorecard concepts to a Backstage-compatible approach.

The `port/` directory is retained only as migration reference from the initial experiment.
