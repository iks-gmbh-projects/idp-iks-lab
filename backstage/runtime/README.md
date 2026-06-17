# Local Backstage Runtime

## Scope

This guide describes the minimal local runtime path for the IKS IDP MVP. The main `idp-iks-lab` repository remains the Backstage catalog, configuration, documentation, and demo-data source of truth.

For this MVP path, the runnable Backstage application is generated locally outside this repository. Do not commit the generated Backstage app tree into `idp-iks-lab` unless a later decision explicitly changes the repository boundary.

This guide does not add production deployment, Kubernetes automation, production secrets, or authentication/authorization hardening. It is only a local catalog-rendering path for MVP validation.

## Prerequisites

- A local clone of this repository.
- Docker with Docker Compose V2, or `docker-compose`.
- Node.js/npm with `npx` available for the first Backstage app generation.
- Network access for the first Backstage app generation, image build, and dependency installation.

The examples below assume this sibling-directory layout:

```text
<workspace>/idp-iks-lab
<workspace>/iks-backstage-runtime
```

## Start the local runtime

The repository-supported startup path is the Docker wrapper. It creates the
sibling Backstage runtime on first use, writes the Docker-local catalog config,
and starts Backstage through Docker Compose:

```bash
./scripts/start-backstage-docker.sh
```

IntelliJ users can run the shared `Start Backstage` run configuration, which
calls the same script from the repository root.

The first run requires network access for `npx @backstage/create-app@latest`,
the local Docker image build, and dependency installation in the container. The
script prefers the sibling runtime `../iks-backstage-runtime`; if the parent
directory is not writable, it falls back to
`${XDG_CACHE_HOME:-$HOME/.cache}/idp-iks-lab/iks-backstage-runtime`. Set
`IKS_BACKSTAGE_RUNTIME_DIR` to choose another writable runtime directory.

The script answers the Backstage app-name prompt with `iks-idp` by default. Set `IKS_BACKSTAGE_APP_NAME` before running the script if you need a different generated app name.

To start the same wrapper in the background:

```bash
IKS_BACKSTAGE_DETACH=1 ./scripts/start-backstage-docker.sh
```

Stop the Docker runtime with:

```bash
./scripts/start-backstage-docker.sh down
```

The wrapper keeps the repository boundary clear:

- The generated Backstage app stays outside this repository, normally at
  `../iks-backstage-runtime`.
- This repository is mounted read-only into the container so Backstage imports
  `backstage/catalog/locations.yaml` from the versioned repo.
- A generated `app-config.docker.local.yaml` is written into the local runtime
  directory with container paths. Do not commit that generated file.

Set `GITHUB_TOKEN` in your shell before starting the wrapper if you want
GitHub-backed template actions to use a token; basic catalog viewing does not
require one.

### Manual setup

The Docker wrapper normally handles app generation. To pre-create the generated
app yourself, run this from the parent directory of this repository:

```bash
cd ..
npx @backstage/create-app@latest --path iks-backstage-runtime
```

Keep the generated app outside `idp-iks-lab` for this MVP path. The generated app is local runtime scaffolding; this repository remains the versioned source of truth for catalog descriptors and example configuration.

## Point the app at this repository catalog

The Docker wrapper writes a local-only `app-config.docker.local.yaml` into the
generated runtime and mounts this repository at `/workspace/idp-iks-lab` inside
the container.

This repository also provides a non-secret local runtime config example at:

```text
idp-iks-lab/backstage/app-config.local.example.yaml
```

The example config loads the root catalog location from:

```text
../idp-iks-lab/backstage/catalog/locations.yaml
```

Use this example only for manual local experiments outside the Docker wrapper:

```bash
cp ../idp-iks-lab/backstage/app-config.local.example.yaml app-config.local.yaml
```

If your local directory layout differs, change the `catalog.locations[].target`
path in your local-only config copy. The Docker wrapper writes a container path
into its generated Docker config so cache-based runtimes still point back to
this repository. Do not commit machine-specific absolute paths.

Generated Backstage apps may include scaffolded `catalog.locations` in their own `app-config.yaml`. For this MVP smoke path, inspect the generated app config and remove or comment any scaffolded sample catalog locations if sample entities appear. The intended catalog source for this repository is only `../idp-iks-lab/backstage/catalog/locations.yaml`.

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

Backstage generator output can vary by version. The Docker wrapper detects
whether the generated app exposes `dev` or `start` in `package.json` and passes
the repository catalog config to that script. If your generated app needs a
different script, set `IKS_BACKSTAGE_START_SCRIPT` before running the wrapper
while preserving the same catalog target: this repository's
`backstage/catalog/locations.yaml`.

## Follow-up stories

Catalog view/filter guidance from #20 is complete under `backstage/catalog/demo-views.md`. Remaining follow-up stories are:

- #21: Implement advisory catalog quality and IKS checks.
- #22: Replace legacy Port actions with Software Templates and GitHub issue workflows.
- #24: Package and document the local/demo runtime path.
