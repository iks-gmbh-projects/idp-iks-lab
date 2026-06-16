# Local Backstage Runtime

## Scope

This guide describes the minimal local runtime path for the IKS IDP MVP. The main `idp-iks-lab` repository remains the Backstage catalog, configuration, documentation, and demo-data source of truth.

For this MVP path, the runnable Backstage application is generated locally outside this repository. Do not commit the generated Backstage app tree into `idp-iks-lab` unless a later decision explicitly changes the repository boundary.

This guide does not add production deployment, Kubernetes automation, production secrets, or authentication/authorization hardening. It is only a local catalog-rendering path for MVP validation.

## Prerequisites

- A local clone of this repository.
- Node.js LTS compatible with the current Backstage `create-app` requirements.
- Yarn as required by the generated Backstage app.
- Network access for the first Backstage app generation and dependency installation.

The examples below assume this sibling-directory layout:

```text
<workspace>/idp-iks-lab
<workspace>/iks-backstage-runtime
```

## Create the local app

The repository includes a convenience startup script that creates the sibling runtime on first use, copies the local catalog config when needed, and starts Backstage:

```bash
./scripts/start-backstage.sh
```

IntelliJ users can run the shared `Start Backstage` run configuration, which calls the same script from the repository root.

The first run requires network access for `npx @backstage/create-app@latest` and dependency installation. The script prefers the sibling runtime `../iks-backstage-runtime`; if the parent directory is not writable, it falls back to `${XDG_CACHE_HOME:-$HOME/.cache}/idp-iks-lab/iks-backstage-runtime`. Set `IKS_BACKSTAGE_RUNTIME_DIR` to choose another writable runtime directory.

The script answers the Backstage app-name prompt with `iks-idp` by default. Set `IKS_BACKSTAGE_APP_NAME` before running the script if you need a different generated app name.

### Manual setup

From the parent directory of this repository, generate a Backstage app as a sibling directory:

```bash
cd ..
npx @backstage/create-app@latest --path iks-backstage-runtime
cd iks-backstage-runtime
```

Keep the generated app outside `idp-iks-lab` for this MVP path. The generated app is local runtime scaffolding; this repository remains the versioned source of truth for catalog descriptors and example configuration.

## Point the app at this repository catalog

This repository provides a non-secret local runtime config example at:

```text
idp-iks-lab/backstage/app-config.local.example.yaml
```

The example config loads the root catalog location from:

```text
../idp-iks-lab/backstage/catalog/locations.yaml
```

Use one of these local options:

1. Copy the example into the generated app as a local config file:

   ```bash
   cp ../idp-iks-lab/backstage/app-config.local.example.yaml app-config.local.yaml
   ```

2. Or pass the repository config file explicitly when starting the generated app, if the generated Backstage command supports your desired config flags:

   ```bash
   yarn dev --config app-config.yaml --config ../idp-iks-lab/backstage/app-config.local.example.yaml
   ```

If your local directory layout differs, change the `catalog.locations[].target` path in your local-only config copy. The startup script writes an absolute target into its generated local config so cache-based runtimes still point back to this repository. Do not commit machine-specific absolute paths.

Generated Backstage apps may include scaffolded `catalog.locations` in their own `app-config.yaml`. For this MVP smoke path, inspect the generated app config and remove or comment any scaffolded sample catalog locations if sample entities appear. The intended catalog source for this repository is only `../idp-iks-lab/backstage/catalog/locations.yaml`.

## Start Backstage

Use the repository startup script:

```bash
./scripts/start-backstage.sh
```

Or, from the generated app directory:

```bash
yarn dev
```

Expected local URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:7007`

## Verify catalog import

Open the Software Catalog and confirm that Backstage reads entities from this repository rather than from hardcoded UI fixtures. Also confirm that generated Backstage sample entities are not mixed into the MVP catalog view. If sample entities appear, revisit the generated app's `catalog.locations` configuration.

Expected demo entities:

- Groups:
  - `platform-team`
  - `iks-review-board`
  - `customer-success`
- Systems:
  - `customer-experience`
  - `management-reporting`
- Components:
  - `customer-portal`
  - `reporting-api`
- Templates:
  - `catalog-metadata-fix`
  - `iks-review-request`
  - `service-onboarding`

`reporting-api` intentionally lacks a runbook annotation/link so later advisory-check work can demonstrate an incomplete metadata case.

This guide documents the local runtime path for #19. If a contributor does not run a generated Backstage app during review, record that as a validation fallback and leave full demo/runtime smoke validation to #24/#15.

The #19 runtime path focuses on catalog import. The example config enables local TechDocs, but rendering TechDocs pages may require additional generated-app or local MkDocs/TechDocs prerequisites depending on the Backstage version. Treat full TechDocs/demo verification as #24/#15 scope unless explicitly smoke-tested here.

## Troubleshooting

### Catalog file path does not resolve

Backstage file locations resolve from the generated app process working directory. With the sibling layout above, the relative target `../idp-iks-lab/backstage/catalog/locations.yaml` should resolve from `<workspace>/iks-backstage-runtime`.

If the app lives elsewhere, copy `app-config.local.example.yaml` to a local-only config file and adjust the target path. Absolute paths are acceptable for local smoke testing, but do not commit machine-specific absolute paths.

### Catalog imports central components instead of service-local files

The intended MVP import root is `backstage/catalog/locations.yaml`. It imports service `Component` entities from `examples/services/*/catalog-info.yaml` and intentionally does not import `backstage/catalog/components.yaml`, which is retained only as a migration/reference copy.

### Generated app command differs

Backstage generator output can vary by version. If `yarn dev` or config flags differ in your generated app, follow that generated app's README while preserving the same catalog target: this repository's `backstage/catalog/locations.yaml`.

## Follow-up stories

Catalog view/filter guidance from #20 is complete under `backstage/catalog/demo-views.md`. Remaining follow-up stories are:

- #21: Implement advisory catalog quality and IKS checks.
- #22: Replace legacy Port actions with Software Templates and GitHub issue workflows.
- #24: Package and document the local/demo runtime path.
