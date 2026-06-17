# Plan: Activate Dependabot for this repository

## Goal

Enable GitHub Dependabot for `iks-gmbh-projects/idp-iks-lab` where it is useful and low-risk, without changing the repository's MVP boundary or triggering external systems directly.

## Current context / assumptions

- Repository is a docs-and-configuration MVP, not an application runtime.
- Existing active GitHub workflow files are intentionally not under `.github/workflows/`; workflow templates live under `github/workflows/` per `AGENTS.md`.
- GitHub requires Dependabot configuration at `.github/dependabot.yml`; this is a necessary exception to the repo's `github/workflows/` template convention.
- Current dependency surface appears minimal:
  - `package-lock.json` exists at repo root, but there is no `package.json`; the lockfile currently has no packages.
  - `github/workflows/validate-port-config.yml` is a workflow template and references reusable GitHub Actions, but it is not an active workflow unless copied to `.github/workflows/`.
- A `.github/dependabot.yml` file may already exist as an uncommitted local change from the current work session. Before finalizing implementation, inspect and either keep, adjust, or remove/recreate it intentionally.
- No ADR is expected: this is routine repository hygiene, not a meaningful architecture or governance decision.

## Proposed approach

Add a conservative Dependabot configuration with only feasible ecosystems:

1. `npm` for the repository root, so Dependabot starts working if JavaScript dependencies are added later. With the current empty lockfile/no `package.json`, this may be a no-op until a manifest exists.
2. `github-actions` for the repository root. GitHub Actions updates only apply to workflows under `.github/workflows/`; because this repo keeps workflow templates under `github/workflows/`, this may also be a no-op unless active workflows are later added. Still, it is valid and future-proof.

Keep the schedule weekly and limit open PRs to avoid noise.

## Step-by-step plan

1. Inspect current state
   - Check whether `.github/dependabot.yml` already exists.
   - Confirm dependency manifests with file search for:
     - `package.json`
     - `package-lock.json`
     - requirements files, Dockerfiles, Gradle/Maven files, or other ecosystem manifests.
   - Confirm workflow convention from `AGENTS.md` and existing `github/workflows/` templates.

2. Add or normalize `.github/dependabot.yml`
   - Create `.github/dependabot.yml` if absent.
   - If already present, review it for correctness and adjust if needed.
   - Use this shape:

   ```yaml
   version: 2
   updates:
     - package-ecosystem: "npm"
       directory: "/"
       schedule:
         interval: "weekly"
       open-pull-requests-limit: 5

     - package-ecosystem: "github-actions"
       directory: "/"
       schedule:
         interval: "weekly"
       open-pull-requests-limit: 5
   ```

   - Optionally include short comments explaining that GitHub requires this file under `.github/`, while this repo's workflow templates remain under `github/workflows/`.

3. Validate locally
   - Preferred validation:
     - `yamllint .github/dependabot.yml port examples agents`
   - If `yamllint` is unavailable locally, state that explicitly and perform a targeted YAML parse if a parser is available.
   - If no YAML parser is available, perform a manual indentation and schema read-through and state the validator limitation.

4. Review diff
   - Check `git diff -- .github/dependabot.yml`.
   - Check `git status --short`.
   - Ensure only the intended Dependabot config is changed.

5. Stop before external side effects
   - Do not commit, push, open a PR, or modify GitHub repository settings unless the user explicitly approves.
   - Dependabot activates only after the `.github/dependabot.yml` file is committed and pushed to the default branch on GitHub.

## Files likely to change

- `.github/dependabot.yml`

No wiki files, Port blueprints/entities, examples, or agent skills should change.

## Documentation updates

- No README or wiki update is required for this small repository-hygiene change.
- No ADR is expected because this does not introduce a new architecture or governance decision.

## Tests / validation

- Run YAML validation if available:
  - `yamllint .github/dependabot.yml port examples agents`
- If unavailable, use a targeted parser/read-through and report the limitation.
- Manual consistency checks:
  - Verify `version: 2` is present.
  - Verify each `updates` entry has `package-ecosystem`, `directory`, and `schedule.interval`.
  - Verify ecosystems are feasible for this repo's current/future dependency surface.

## Risks, tradeoffs, and open questions

- `npm` updates may be inactive until a root `package.json` exists; this is acceptable because it future-proofs the repo with minimal noise.
- `github-actions` updates may be inactive while workflows remain templates under `github/workflows/`; GitHub only processes active workflows under `.github/workflows/`.
- Adding `.github/dependabot.yml` creates a real GitHub configuration path, unlike the repo's workflow-template path. This is necessary for Dependabot and should be called out in the change summary.
- Open question for the user/reviewer: should the empty `package-lock.json` remain in the repo? This plan does not remove it because that would be a separate cleanup decision.

## Expected final summary after implementation

- Added `.github/dependabot.yml` with weekly checks for npm and GitHub Actions.
- Noted that both ecosystems are currently low/no-op given the repo's minimal dependency surface and workflow-template convention.
- Validation result, including any unavailable local tools.
- No commits or external GitHub changes performed unless separately approved.
