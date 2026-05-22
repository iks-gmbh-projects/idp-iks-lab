# Backstage Target Structure

Backstage is the target portal for the self-hosted IKS IDP MVP. This repository stores catalog descriptors, example configuration, template definitions, scorecard mapping, and validation guidance. It does not commit a full generated Backstage application runtime, but it documents a local external runtime path under `runtime/`.

GitHub remains the versioned source of truth. Backstage should read catalog locations and service descriptors from this repository.

## Contents

- `app-config.example.yaml`: non-secret example configuration for a Backstage instance.
- `app-config.local.example.yaml`: local runtime config example for a generated Backstage app in a sibling directory.
- `catalog/`: Backstage catalog locations, shared demo entities, and the catalog schema/source-of-truth rules. Service `Component` entities are imported from `examples/services/*/catalog-info.yaml`; `catalog/components.yaml` is retained only as a reference copy during migration and is not imported by `catalog/locations.yaml`.
- `runtime/`: instructions for generating a local Backstage app outside this repository and pointing it at this repository's catalog data.
- `templates/`: advisory Software Template definitions for GitHub-tracked workflows.
- `techdocs/`: example TechDocs configuration.
- `scorecards/`: mapping from the previous scorecard concepts to a Backstage-compatible approach.

The `port/` directory is retained only as migration reference from the initial experiment.
