# Clean Backstage Follow-up Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task after explicit approval for any GitHub issue mutations.

**Goal:** Cleanly finish the project steering from the Port experiment to the Backstage target by aligning open issues, removing ambiguity in the repository structure, and leaving a clear next execution queue.

**Architecture:** GitHub remains the versioned source of truth. Backstage is the target self-hosted IDP structure, while `port/` remains legacy migration reference until a later explicit cleanup decision. External GitHub issue changes are side effects and must be performed only after the user approves execution.

**Tech Stack:** Markdown docs, GitHub Issues via `gh`, Backstage catalog YAML, GitHub Issue Forms, wiki submodule docs, `yamllint` validation.

---

## Current Context / Assumptions

- Recent committed direction change already exists:
  - Wiki commit: `14d3828 docs: adopt Backstage as self-hosted IDP target`
  - Main repo commit: `b0a9582 docs: steer IDP lab to Backstage`
  - Branch: `7-mvp-publish-github-source-of-truth-and-activate-validation`
- The repository currently includes Backstage target artifacts:
  - `backstage/README.md`
  - `backstage/catalog/locations.yaml`
  - `backstage/migration-issues.md`
  - `backstage/templates/*/template.yaml`
  - `backstage/scorecards/README.md`
  - `.github/ISSUE_TEMPLATE/backstage-migration.yml`
- Open GitHub issues still include old Port-specific work (#8-#15) and newer self-hosted/Backstage-shaped work (#17-#24).
- Plan mode forbids external tracker mutation, commits, pushes, and implementation. This plan therefore only prepares the cleanup sequence.

## Proposed Approach

1. Treat issues #17-#24 as the new Backstage migration queue, with targeted edits to remove generic “self-hosted portal” language where Backstage is now selected.
2. Treat old Port runtime issues #8-#15 as superseded or migrated, not as active execution work.
3. Keep `port/` in the repo as a legacy reference for now; do not delete it in the cleanup unless a new explicit decision approves archival/removal.
4. Make the repository navigation point contributors to Backstage artifacts first and to Port artifacts only as migration history.
5. Validate that docs, issue templates, Backstage descriptors, and workflows remain consistent.

## Step-by-Step Plan

### Task 1: Snapshot open issue state before mutation

**Objective:** Capture the exact current issue state so edits/closures can be reviewed and reversed if needed.

**Files:**
- Read: GitHub issues #8-#24 via `gh issue view`
- Optional local note during execution: `.hermes/tmp/backstage-issue-cleanup-before.json` (do not commit unless requested)

**Steps:**
1. Run a read-only issue export:
   - `gh issue list --state open --limit 50 --json number,title,labels,body,url > .hermes/tmp/backstage-issue-cleanup-before.json`
2. Review issue numbers #8-#24 and classify them as:
   - `keep/edit`: still relevant after Backstage decision.
   - `close/superseded`: Port runtime task replaced by Backstage task.
   - `optional/defer`: useful but not part of the immediate Backstage MVP.
3. Do not mutate issues until the user approves execution.

**Acceptance Criteria:**
- A reviewed issue mapping exists before any external mutation.
- No GitHub issue has been edited or closed during this snapshot step.

### Task 2: Edit issue #17 into the completed architecture-decision anchor

**Objective:** Make #17 reflect that the target architecture has been decided: Backstage OSS.

**External GitHub Issue:**
- Modify: `#17 Self-hosted IDP MVP: Decide target architecture and record ADR`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Architecture decision and migration anchor`
- Update body to say:
  - ADR 0003 selected Backstage OSS.
  - ADR 0001 is superseded for target-platform direction.
  - Remaining follow-up issues are #18-#24.
  - Port artifacts are retained only as migration reference.
- Check off acceptance items that are already satisfied by the committed docs.
- Add a comment with links/refs to:
  - `wiki/decisions/0003-adopt-backstage-for-self-hosted-idp.md`
  - `backstage/migration-issues.md`
  - `backstage/README.md`

**Acceptance Criteria:**
- Issue #17 no longer reads like an undecided product-selection task.
- It becomes the canonical issue anchor for the Backstage migration decision.

### Task 3: Edit issue #18 to target Backstage catalog schema explicitly

**Objective:** Convert the generic self-hosted catalog schema issue into a Backstage catalog/schema completion issue.

**External GitHub Issue:**
- Modify: `#18 Self-hosted IDP MVP: Define catalog schema and GitHub source-of-truth format`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Finalize catalog schema and GitHub source-of-truth format`
- Replace generic “self-hosted catalog schema” wording with Backstage-specific entities:
  - `Component`
  - `System`
  - `Group`
  - `Location`
  - Backstage annotations for repository, TechDocs, and IKS metadata.
- Add acceptance criteria for duplicate-source-of-truth prevention:
  - `examples/services/*/catalog-info.yaml` are the service Component import source.
  - `backstage/catalog/components.yaml` remains reference-only unless explicitly selected as import source.
  - `backstage/catalog/locations.yaml` imports only one source per entity ref.

**Acceptance Criteria:**
- Issue #18 clearly tells implementers to complete Backstage entity modeling, not invent a new catalog schema.
- Duplicate entity import risk is explicitly tracked.

### Task 4: Edit issue #19 to scaffold a Backstage app/runtime, not an unspecified portal

**Objective:** Align the runtime issue with the chosen target platform.

**External GitHub Issue:**
- Modify: `#19 Self-hosted IDP MVP: Scaffold portal application/runtime`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Scaffold local Backstage app/runtime`
- Scope should include:
  - Backstage app scaffold or a documented pointer to the intended app directory.
  - Local run path without Kubernetes as a requirement.
  - Example `app-config.local.yaml` or documented local config path.
  - Catalog ingestion from `backstage/catalog/locations.yaml`.
- Scope should exclude:
  - Production deployment.
  - Kubernetes automation.
  - Hardening SSO/RBAC beyond documented placeholders.

**Acceptance Criteria:**
- Issue #19 can be picked up without re-deciding the platform.
- Local runtime work starts from Backstage conventions.

### Task 5: Edit issue #20 to map service catalog views to Backstage pages/plugins

**Objective:** Make catalog-view work implementable in Backstage terms.

**External GitHub Issue:**
- Modify: `#20 Self-hosted IDP MVP: Implement service catalog views`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Configure service catalog views and filters`
- Replace “self-hosted portal UI” with Backstage Catalog UI.
- Add implementation notes:
  - MVP can start with default Backstage catalog table filters plus documented demo navigation.
  - Custom IKS filters are optional unless needed for demo clarity.
  - Service detail page must surface annotations/metadata for owner, business owner, system, repository, lifecycle, documentation, runbook, criticality, protection need, data class, and compliance scope.

**Acceptance Criteria:**
- The issue distinguishes default Backstage capability from optional custom plugin/UI work.
- Demo navigation remains achievable without overbuilding.

### Task 6: Edit issue #21 to map scorecards to Backstage-compatible checks

**Objective:** Replace generic scorecard language with the Backstage scorecard path selected in docs.

**External GitHub Issue:**
- Modify: `#21 Self-hosted IDP MVP: Recreate catalog quality and IKS scorecards`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Implement advisory catalog quality and IKS checks`
- Update body to reflect acceptable MVP options:
  - Backstage Tech Insights if adopted.
  - A Backstage-compatible scorecard plugin if selected.
  - A GitHub Actions/local report if lower-risk for the MVP.
- Keep checks advisory-only.
- Require mapping to `backstage/scorecards/README.md`.

**Acceptance Criteria:**
- Issue #21 does not imply Port scorecards remain the target.
- It supports a pragmatic MVP path even before a scorecard plugin is finalized.

### Task 7: Edit issue #22 to use Backstage Software Templates plus GitHub Issue Forms

**Objective:** Align self-service workflow work with the Backstage target artifacts already added.

**External GitHub Issue:**
- Modify: `#22 Self-hosted IDP MVP: Replace Port self-service actions with GitHub issue workflows`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Replace Port actions with Software Templates and GitHub issue workflows`
- Scope should reference:
  - `backstage/templates/catalog-metadata-fix/template.yaml`
  - `backstage/templates/iks-review-request/template.yaml`
  - `.github/ISSUE_TEMPLATE/catalog-metadata-fix.yml`
  - `.github/ISSUE_TEMPLATE/iks-review.yml`
  - `.github/ISSUE_TEMPLATE/backstage-migration.yml`
- Add acceptance criteria that generated work remains advisory and GitHub-tracked only.

**Acceptance Criteria:**
- Issue #22 points implementers to Backstage template files and active GitHub Issue Forms.
- It no longer centers Port action definitions except as migration inputs.

### Task 8: Edit issue #23 into a repository consistency/cleanup issue

**Objective:** Convert #23 from a broad direction-change task into a targeted consistency cleanup after the Backstage commit.

**External GitHub Issue:**
- Modify: `#23 Self-hosted IDP MVP: Update repository structure, docs, and validation away from Port runtime assumptions`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Finish repository consistency cleanup`
- Scope should include:
  - `README.md`
  - `AGENTS.md`
  - `wiki/Home.md`
  - `wiki/_Sidebar.md`
  - `wiki/docs/*.md`
  - `.github/workflows/*`
  - `github/workflows/*` if reference workflows exist
  - `.github/ISSUE_TEMPLATE/*`
  - `backstage/*`
- Add stale-language search acceptance:
  - Search for `Port`, `port/`, `self-hosted portal`, `workspace`, `blueprint`, and `action`.
  - Confirm each remaining occurrence is either legacy/migration context or intentionally retained.

**Acceptance Criteria:**
- #23 becomes the cleanup umbrella for stale wording and navigation, not a duplicate of the already completed ADR work.

### Task 9: Edit issue #24 to package the Backstage local/demo path

**Objective:** Make the demo-packaging task explicitly Backstage-based.

**External GitHub Issue:**
- Modify: `#24 Self-hosted IDP MVP: Package and document local/demo deployment`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Package and document local/demo runtime`
- Scope should include:
  - Local Backstage start command.
  - Catalog import from this repository.
  - Demo data load path for `customer-portal` and `reporting-api`.
  - Documented fallback if the runtime is not yet scaffolded.
- Retain the boundary:
  - No production Kubernetes automation.
  - No production infrastructure promises.

**Acceptance Criteria:**
- #24 gives a concrete end-to-end demo packaging target for Backstage.

### Task 10: Close or supersede old Port runtime issues #8-#13

**Objective:** Remove stale active work that would steer contributors back to Port.

**External GitHub Issues:**
- Close/supersede: `#8 MVP: Create Port workspace for the IDP catalog demo`
- Close/supersede: `#9 MVP: Import Port blueprints`
- Close/supersede: `#10 MVP: Import demo catalog entities`
- Close/supersede: `#11 MVP: Configure catalog quality and IKS baseline scorecards`
- Close/supersede: `#12 MVP: Configure Port catalog demo views`
- Close/supersede: `#13 MVP: Wire low-risk GitHub issue self-service actions`

**Proposed closure comments:**
- #8 superseded by #17/#19/#24.
- #9 superseded by #18 and Backstage catalog descriptors.
- #10 superseded by #18 and service-local `catalog-info.yaml` imports.
- #11 superseded by #21 and `backstage/scorecards/README.md`.
- #12 superseded by #20.
- #13 superseded by #22.

**Acceptance Criteria:**
- Old Port workspace/import/action issues are no longer open execution targets.
- Each closure points to a Backstage replacement issue.

### Task 11: Reclassify issue #14 as deferred legacy/future work or close it

**Objective:** Decide how to handle the old metadata-drift automation issue without accidentally reviving Port automation.

**External GitHub Issue:**
- Modify or close: `#14 MVP: Decide whether metadata drift automation stays draft or enters demo`

**Recommended action:**
- Close as superseded/deferred unless the user wants a future Backstage advisory automation issue.
- If kept open, retitle to: `Backstage IDP future: Decide advisory metadata drift notification path`
- Explicitly remove Port automation from MVP scope.

**Acceptance Criteria:**
- No open issue asks implementers to configure Port automation for the MVP.

### Task 12: Reframe issue #15 as Backstage demo validation

**Objective:** Keep the useful dry-run/validation intent while aligning the validation targets.

**External GitHub Issue:**
- Modify: `#15 MVP: Run validation and complete demo dry-run`

**Proposed changes:**
- Update title to: `Backstage IDP MVP: Run validation and complete demo dry-run`
- Replace validation targets with:
  - `backstage/`
  - `examples/services/*/catalog-info.yaml`
  - `agents/`
  - `.github/ISSUE_TEMPLATE/`
  - `wiki/docs/demo-story.md`
  - `wiki/docs/iks-metadata-model.md`
  - `port/` only as legacy migration reference
- Acceptance should mention `yamllint backstage port examples agents .github/ISSUE_TEMPLATE`.

**Acceptance Criteria:**
- #15 remains useful as the final demo-dry-run gate.
- Validation no longer treats Port as the target runtime.

### Task 13: Update repository issue mapping after external issue cleanup

**Objective:** Keep the in-repo migration issue breakdown aligned with actual GitHub issues.

**Files:**
- Modify: `backstage/migration-issues.md`

**Proposed changes:**
- Add GitHub issue numbers once external mutations are complete:
  - Architecture decision: #17
  - Catalog schema: #18
  - Runtime scaffold: #19
  - Catalog views: #20
  - Scorecards/checks: #21
  - Workflows/templates: #22
  - Repo consistency cleanup: #23
  - Local/demo packaging: #24
  - Demo validation: #15
- Add a short “Superseded Port issues” section for #8-#14.
- Keep the note that issue mutation requires human approval.

**Acceptance Criteria:**
- `backstage/migration-issues.md` mirrors the current issue tracker state.
- A future reader can move from repo docs to the right active issues.

### Task 14: Repository stale-language and structure cleanup pass

**Objective:** Remove or mark leftover stale Port/runtime assumptions after issue cleanup.

**Files likely to inspect/modify:**
- `README.md`
- `AGENTS.md`
- `wiki/Home.md`
- `wiki/_Sidebar.md`
- `wiki/docs/vision.md`
- `wiki/docs/demo-story.md`
- `wiki/docs/operating-model.md`
- `wiki/docs/iks-metadata-model.md`
- `.github/ISSUE_TEMPLATE/*.yml`
- `.github/workflows/*.yml`
- `github/workflows/*.yml` if present
- `backstage/README.md`
- `backstage/migration-issues.md`
- `port/README.md` if present or create only if needed to mark legacy status

**Steps:**
1. Search for stale target-language terms:
   - `Port`
   - `Port workspace`
   - `blueprint`
   - `Port action`
   - `self-hosted portal` where Backstage should now be named
2. For each occurrence, classify it as:
   - keep as legacy/migration context,
   - rewrite to Backstage target language,
   - delete if obsolete.
3. Confirm navigation pages point to Backstage docs and ADR 0003.

**Acceptance Criteria:**
- Remaining Port references are intentional legacy/migration references.
- Landing pages and navigation no longer send contributors to Port as the active target.

### Task 15: Validate after cleanup

**Objective:** Prove that the cleanup did not break YAML or documentation consistency.

**Commands:**
- `yamllint backstage port examples agents .github/ISSUE_TEMPLATE`
- `git status --short`
- `git -C wiki status --short`
- Targeted stale-language search using `rg` or repository search tooling.

**Manual checks:**
- Read `README.md`, `backstage/README.md`, `wiki/Home.md`, and `wiki/_Sidebar.md`.
- Confirm Backstage is the active target.
- Confirm Port is legacy/migration reference only.
- Confirm no new Kubernetes automation, production infrastructure change, or autonomous compliance enforcement was introduced.

**Acceptance Criteria:**
- YAML validation passes, or any missing local validator is clearly documented.
- Main repo and wiki changes are intentional and reviewable.
- Cleanup is ready for commit and PR after user approval.

## Files Likely to Change

Repository files:
- `backstage/migration-issues.md`
- `README.md`
- `AGENTS.md`
- `backstage/README.md`
- `.github/ISSUE_TEMPLATE/backstage-migration.yml`
- Possibly `.github/ISSUE_TEMPLATE/catalog-metadata-fix.yml`
- Possibly `.github/ISSUE_TEMPLATE/iks-review.yml`
- Possibly workflow files under `.github/workflows/`
- Possibly reference workflow files under `github/workflows/` if present
- Possibly a legacy marker under `port/`, only if current docs are insufficient

Wiki submodule files:
- `wiki/Home.md`
- `wiki/_Sidebar.md`
- `wiki/docs/vision.md`
- `wiki/docs/demo-story.md`
- `wiki/docs/operating-model.md`
- `wiki/docs/iks-metadata-model.md`
- No new ADR expected for issue cleanup itself.

External tracker items, after explicit approval only:
- GitHub issues #8-#15
- GitHub issues #17-#24

## Documentation / ADR Expectations

- No new ADR is expected for the clean follow-up because ADR 0003 already records the meaningful architecture decision to adopt Backstage.
- A new ADR would be appropriate only if the cleanup changes a governance or architecture decision, for example:
  - removing `port/` entirely rather than keeping it as legacy reference,
  - selecting Red Hat Developer Hub instead of Backstage OSS,
  - adding Kubernetes/production deployment to the MVP,
  - making scorecards blocking/enforcing instead of advisory.
- Documentation updates should focus on navigation, issue mapping, and stale-language cleanup.

## Tests / Validation

Primary validation:
- `yamllint backstage port examples agents .github/ISSUE_TEMPLATE`

Issue validation:
- `gh issue view <number>` for all modified issues.
- Confirm closed issues have replacement links.
- Confirm edited issues no longer contain stale Port-as-target language.

Manual consistency validation:
- Landing pages: `README.md`, `wiki/Home.md`, `wiki/_Sidebar.md`.
- Backstage structure: `backstage/README.md`, `backstage/migration-issues.md`.
- Demo path: `wiki/docs/demo-story.md` and issue #24.

## Risks, Tradeoffs, and Open Questions

- **External side effects:** Editing/closing GitHub issues is an external mutation and needs explicit user approval before execution.
- **Issue churn:** Large issue rewrites may hide original history; mitigate with comments that explain supersession and link replacement issues.
- **Port deletion risk:** Removing `port/` now may lose useful migration examples. Recommended: keep it until Backstage import and demo validation are proven.
- **Backstage runtime scope:** The repo currently states it does not yet contain a runnable Backstage app. Issue #19 must define whether to scaffold an app in-repo or document how a separate Backstage app consumes this repo.
- **Scorecard plugin choice:** Backstage scorecards may be implemented through Tech Insights, another plugin, or CI/local reports. Keep #21 flexible until the MVP runtime exists.
- **Labels/milestones:** The current issues have generic labels. Consider adding `backstage`, `migration`, and `legacy-port` labels only if the user approves label mutation.

## Deferred Actions Because This Was Plan Mode

- No GitHub issues were edited, commented on, closed, labeled, or created.
- No repository files were changed except this plan file.
- No commits, pushes, or PRs were made.
