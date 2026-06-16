# Issue #22 Software Templates GitHub Integration Implementation Plan

## Goal

Replace Port self-service actions with Backstage Software Templates that create auditable GitHub issues, making catalog quality and IKS review workflows actionable from within Backstage.

## Current Context

- **Issue:** #22 "Backstage IDP MVP: Replace Port actions with Software Templates and GitHub issue workflows"
- **Branch:** `22-replace-port-actions-with-software-templates`
- **Base:** `main` at commit `a2d9b1f` (includes merged PR #35 with runtime documentation)

### Already Complete

1. ✅ **Software Template scaffolds:**
   - `backstage/templates/catalog-metadata-fix/template.yaml`
   - `backstage/templates/iks-review-request/template.yaml`
   - `backstage/templates/service-onboarding/template.yaml`

2. ✅ **GitHub Issue Forms:**
   - `.github/ISSUE_TEMPLATE/catalog-metadata-fix.yml`
   - `.github/ISSUE_TEMPLATE/iks-review.yml`
   - `.github/ISSUE_TEMPLATE/backstage-migration.yml`

3. ✅ **Templates are imported** into Backstage catalog via `locations.yaml`

4. ✅ **Advisory-only MVP boundary:** Current templates use `debug:log` action (no mutations)

### Current Gaps

1. ❌ Templates use `debug:log` instead of actual GitHub issue creation
2. ❌ No GitHub integration configured for Backstage
3. ❌ No documentation for required credentials/tokens
4. ❌ Template parameters don't match Issue Form fields perfectly
5. ❌ No testing/verification against demo services

### What Needs to Be Done

Based on issue #22 acceptance criteria:

1. **Update templates** to use `github:issues:create` action
2. **Document GitHub integration** setup (credentials, permissions)
3. **Align template parameters** with GitHub Issue Form structure
4. **Add verification steps** to demo checklist
5. **Keep MVP boundaries** (creates issues only, no other mutations)

---

## Technical Background

### Backstage GitHub Actions

Backstage provides `github:issues:create` action from `@backstage/plugin-scaffolder-backend-module-github`:

**Action ID:** `github:issues:create`

**Required inputs:**
- `repoUrl`: Format `github.com?repo=reponame&owner=owner`
- `title`: Issue title

**Optional inputs:**
- `body`: Issue body (markdown)
- `labels`: Array of labels
- `assignees`: Array of GitHub usernames
- `milestone`: Milestone number or title
- `token`: GitHub token (or use credentials provider)

**Outputs:**
- `issueUrl`: URL of created issue
- `issueNumber`: Issue number

### GitHub Authentication Options

**Option A: GitHub App (Recommended for production)**
- More secure, scoped permissions
- Requires GitHub App creation and installation
- Configuration in `app-config.yaml`

**Option B: Personal Access Token (PAT)**
- Simpler for MVP/demo
- Requires manual token generation
- Can be passed via `token` parameter or environment variable

**Option C: GitHub Actions Bot**
- Uses `GITHUB_TOKEN` in GitHub Actions workflows
- Limited to Actions context only

**MVP Decision:** Document both options, recommend GitHub App for future, accept PAT for demo/dev.

---

## Implementation Tasks

### Task 1: Document GitHub Integration Setup

**New file:** `backstage/runtime/GITHUB_INTEGRATION.md`

**Content:**

```markdown
# GitHub Integration for Backstage Software Templates

This guide documents GitHub authentication setup for Backstage Software Templates to create GitHub issues.

## MVP Approach

The MVP uses **Personal Access Token (PAT)** authentication for simplicity. Production deployments should migrate to GitHub App authentication for better security and scoping.

## Personal Access Token Setup (Dev/Demo)

### 1. Generate PAT

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name: `Backstage IDP MVP - Software Templates`
4. Expiration: Choose appropriate expiration (90 days recommended for dev/demo)
5. Scopes required:
   - `repo` (full control of private repositories)
     - Or just `public_repo` if only targeting public repos
   - `workflow` (if templates will create GitHub Actions workflows)

6. Click "Generate token" and copy the token immediately

### 2. Configure Backstage

**Option A: Environment Variable (Recommended for local dev)**

Add to your shell profile or Backstage startup script:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Restart Backstage to pick up the environment variable.

**Option B: app-config.local.yaml (Alternative)**

⚠️ **WARNING:** Never commit real tokens to git. Use this only in local-only config files.

```yaml
integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}  # Reads from environment variable
```

### 3. Verify Integration

1. Start Backstage: `./scripts/start-backstage.sh`
2. Navigate to "Create..." → "Catalog Metadata Fix"
3. Fill in template parameters
4. Execute template
5. Verify issue is created in GitHub repository

## Template Token Usage

Templates can specify token in two ways:

**Method 1: Use integration credentials (recommended)**

```yaml
steps:
  - id: create-issue
    action: github:issues:create
    input:
      repoUrl: github.com?repo=idp-iks-lab&owner=iks-gmbh-projects
      title: ${{ parameters.title }}
      # token parameter omitted - uses integration credentials
```

**Method 2: Explicit token from secrets**

```yaml
steps:
  - id: create-issue
    action: github:issues:create
    input:
      repoUrl: github.com?repo=idp-iks-lab&owner=iks-gmbh-projects
      title: ${{ parameters.title }}
      token: ${{ secrets.GITHUB_TOKEN }}  # Explicit token
```

MVP templates use **Method 1** (integration credentials) for simplicity.

## GitHub App Setup (Future Production Path)

For production deployments, migrate to GitHub App authentication:

1. Create GitHub App in organization settings
2. Grant permissions: `issues: write`, `contents: read`
3. Install app to target repositories
4. Configure app credentials in `app-config.yaml`
5. Update templates to use app-based authentication

See [Backstage GitHub Integration docs](https://backstage.io/docs/integrations/github/locations) for detailed setup.

## Security Considerations

- **Never commit tokens to git**
- Use environment variables or secure secret management
- Rotate tokens regularly (every 90 days minimum)
- Limit token scope to minimum required permissions
- For demo/dev: Use PAT with repo scope only
- For production: Migrate to GitHub App with granular permissions

## Troubleshooting

### "Resource not accessible by integration"

- Verify token has `repo` or `public_repo` scope
- Check token hasn't expired
- Ensure repository owner/name are correct in `repoUrl`

### "Bad credentials"

- Verify `GITHUB_TOKEN` environment variable is set
- Check token is correctly copied (no extra spaces/newlines)
- Regenerate token if needed

### Template execution succeeds but no issue appears

- Check GitHub repository permissions
- Verify repository exists and is accessible
- Check Backstage logs for API errors

---

_MVP documentation for issue #22_
_For production deployment, migrate to GitHub App authentication_
```

**Rationale:** Provides clear setup instructions without committing secrets, documents both MVP and future paths.

---

### Task 2: Update catalog-metadata-fix template

**File:** `backstage/templates/catalog-metadata-fix/template.yaml`

**Changes:**

Replace `debug:log` step with actual GitHub issue creation:

```yaml
  steps:
    - id: create-github-issue
      name: Create GitHub Issue for Catalog Metadata
      action: github:issues:create
      input:
        repoUrl: github.com?repo=idp-iks-lab&owner=iks-gmbh-projects
        title: "Catalog metadata: ${{ parameters.componentRef }}"
        body: |
          ## Backstage Component Reference
          ${{ parameters.componentRef }}

          ## Missing or Incorrect Metadata
          ${{ parameters.reason }}

          ## Details and Context
          ${{ parameters.details }}

          ---
          *This issue was created via Backstage Software Template*
          *Template: `catalog-metadata-fix`*
        labels:
          - catalog
          - metadata

  output:
    links:
      - title: View GitHub Issue
        url: ${{ steps['create-github-issue'].output.issueUrl }}
    text:
      - title: Issue Created
        content: |
          GitHub issue created successfully!

          **Issue URL:** ${{ steps['create-github-issue'].output.issueUrl }}
          **Issue Number:** #${{ steps['create-github-issue'].output.issueNumber }}

          The issue has been tracked in the repository for follow-up.
```

Update parameters to better match GitHub Issue Form:

```yaml
  parameters:
    - title: Catalog Metadata Fix Request
      required:
        - componentRef
        - reason
      properties:
        componentRef:
          title: Backstage component reference
          type: string
          description: "Example: component:default/customer-portal"
          ui:placeholder: "component:default/customer-portal"
        
        reason:
          title: Missing or incorrect metadata
          type: string
          enum:
            - Technical owner
            - Business owner
            - System
            - Repository
            - Lifecycle
            - Documentation
            - Runbook
            - Criticality
            - Protection need
            - Data class
            - Compliance scope
          ui:widget: select
        
        details:
          title: Details and context
          type: string
          ui:widget: textarea
          ui:options:
            rows: 5
          description: Add scorecard/check evidence, expected value, and validation steps.
```

**Rationale:** Creates real GitHub issues, provides clickable output, matches Issue Form structure.

---

### Task 3: Update iks-review-request template

**File:** `backstage/templates/iks-review-request/template.yaml`

**Changes:**

Replace `debug:log` with GitHub issue creation:

```yaml
  parameters:
    - title: IKS Review Request
      required:
        - componentRef
        - reason
      properties:
        componentRef:
          title: Backstage component reference
          type: string
          description: "Example: component:default/customer-portal"
          ui:placeholder: "component:default/customer-portal"
        
        reason:
          title: Review reason
          type: string
          ui:widget: textarea
          ui:options:
            rows: 3
          description: Why is the IKS review required?
        
        fieldsToReview:
          title: Zu pruefende Angaben
          type: array
          items:
            type: string
            enum:
              - Fachlicher Owner
              - Technischer Owner
              - Kritikalitaet
              - Schutzbedarf
              - Datenklasse
              - Dokumentation
              - Runbook
          uniqueItems: true
          ui:widget: checkboxes
        
        requestedDecision:
          title: Gewuenschte Entscheidung
          type: string
          enum:
            - Freigegeben
            - Freigegeben mit Auflagen
            - Nacharbeit erforderlich
          ui:widget: select

  steps:
    - id: create-github-issue
      name: Create IKS Review Request Issue
      action: github:issues:create
      input:
        repoUrl: github.com?repo=idp-iks-lab&owner=iks-gmbh-projects
        title: "IKS review: ${{ parameters.componentRef }}"
        body: |
          ## Backstage Component Reference
          ${{ parameters.componentRef }}

          ## Review Reason
          ${{ parameters.reason }}

          ## Zu pruefende Angaben
          ${{ parameters.fieldsToReview | dump }}

          ## Gewuenschte Entscheidung
          ${{ parameters.requestedDecision }}

          ---
          *This issue was created via Backstage Software Template*
          *Template: `iks-review-request`*
        labels:
          - iks
          - review

  output:
    links:
      - title: View GitHub Issue
        url: ${{ steps['create-github-issue'].output.issueUrl }}
    text:
      - title: Issue Created
        content: |
          IKS review request created successfully!

          **Issue URL:** ${{ steps['create-github-issue'].output.issueUrl }}
          **Issue Number:** #${{ steps['create-github-issue'].output.issueNumber }}
```

**Rationale:** Matches IKS review issue form structure, provides German field labels.

---

### Task 4: Update service-onboarding template

**File:** `backstage/templates/service-onboarding/template.yaml`

**Note:** No matching GitHub Issue Form exists for this template. Two options:

**Option A:** Create matching issue form (adds scope)
**Option B:** Keep as-is or make advisory-only (defer to future)

**MVP Decision:** Keep `service-onboarding` as advisory-only with `debug:log` for now. Focus on `catalog-metadata-fix` and `iks-review-request` which have matching issue forms.

Add note to template description:

```yaml
metadata:
  name: service-onboarding
  title: Service Onboarding Checklist
  description: |
    Create an advisory checklist for completing Backstage catalog, TechDocs, and IKS metadata.
    
    NOTE: This template is advisory-only in the MVP. Use the GitHub Issue Forms directly
    or create a matching issue form for automation (tracked separately).
```

**Rationale:** Keeps scope manageable, focuses on templates with existing issue forms.

---

### Task 5: Update demo checklist with template testing steps

**File:** `backstage/runtime/DEMO_CHECKLIST.md`

**Add new section after "GitHub Issue Workflow (Fallback for MVP)":**

```markdown
## Software Template GitHub Integration (issue #22)

Prerequisites:
- [ ] GitHub Personal Access Token created with `repo` scope
- [ ] `GITHUB_TOKEN` environment variable set
- [ ] Backstage restarted to pick up token

Testing catalog-metadata-fix template:
- [ ] Navigate to "Create..." in Backstage
- [ ] Select "Catalog Metadata Fix" template
- [ ] Fill in parameters:
  - Component ref: `component:default/reporting-api`
  - Reason: `Runbook`
  - Details: `Missing runbook annotation - detected by scorecard check`
- [ ] Execute template
- [ ] Verify success message with issue URL
- [ ] Click issue URL and verify GitHub issue created
- [ ] Verify issue title: "Catalog metadata: component:default/reporting-api"
- [ ] Verify issue labels: `catalog`, `metadata`
- [ ] Verify issue body includes component ref, reason, details

Testing iks-review-request template:
- [ ] Navigate to "Create..." in Backstage
- [ ] Select "IKS Review Request" template
- [ ] Fill in parameters:
  - Component ref: `component:default/customer-portal`
  - Reason: `Pre-production IKS compliance review`
  - Fields to review: (check relevant items)
  - Requested decision: (select one)
- [ ] Execute template
- [ ] Verify success message with issue URL
- [ ] Click issue URL and verify GitHub issue created
- [ ] Verify issue title: "IKS review: component:default/customer-portal"
- [ ] Verify issue labels: `iks`, `review`
- [ ] Verify issue body includes all parameters

Fallback testing (without GitHub token):
- [ ] Templates still load in Backstage catalog
- [ ] Template execution shows clear error about missing credentials
- [ ] Error message points to `backstage/runtime/GITHUB_INTEGRATION.md`
```

**Rationale:** Makes template testing actionable, provides concrete verification steps.

---

### Task 6: Update app-config examples

**File:** `backstage/app-config.local.example.yaml`

**Add GitHub integration section:**

```yaml
# GitHub integration for Software Templates
# See backstage/runtime/GITHUB_INTEGRATION.md for setup instructions
integrations:
  github:
    - host: github.com
      # Use environment variable for token (never commit real tokens)
      token: ${GITHUB_TOKEN}
```

**Rationale:** Shows where to configure GitHub integration without committing secrets.

---

### Task 7: Add template testing note to README

**File:** `README.md`

**Update "Naechste Schritte" section:**

After step 5 ("Templates oder GitHub Issue Forms..."), add specific template testing note:

```markdown
5. Templates oder GitHub Issue Forms fuer Review- und Katalogpflege-Workflows testen:
   - GitHub-Token gemaess `backstage/runtime/GITHUB_INTEGRATION.md` konfigurieren
   - Software Templates im Backstage "Create..."-Menü ausfuehren
   - GitHub-Issues aus Backstage heraus erzeugen und verifizieren
   - Tracking von #22
```

**Rationale:** Points users to integration documentation, clarifies token requirement.

---

## Validation Before Commit

### Repository Consistency

- [ ] Run `git diff --check` to verify no trailing whitespace
- [ ] Verify YAML files parse correctly: `yamllint backstage`
- [ ] Manual read-through: verify all template YAML is valid
- [ ] Check that no real tokens are committed anywhere
- [ ] Verify German language consistency (IKS review template)

### Template YAML Validation

```bash
# Verify templates are valid YAML
python3 -c "import yaml; yaml.safe_load(open('backstage/templates/catalog-metadata-fix/template.yaml'))"
python3 -c "import yaml; yaml.safe_load(open('backstage/templates/iks-review-request/template.yaml'))"
python3 -c "import yaml; yaml.safe_load(open('backstage/templates/service-onboarding/template.yaml'))"
```

### Documentation Consistency

- [ ] Integration documentation doesn't reveal secrets
- [ ] Demo checklist steps reference correct template names
- [ ] app-config examples use environment variable syntax
- [ ] README updates point to correct documentation files

---

## Files Expected to Change

**New files:**
- `backstage/runtime/GITHUB_INTEGRATION.md` - GitHub auth setup documentation

**Updated files:**
- `backstage/templates/catalog-metadata-fix/template.yaml` - GitHub issue creation
- `backstage/templates/iks-review-request/template.yaml` - GitHub issue creation
- `backstage/templates/service-onboarding/template.yaml` - Advisory note added
- `backstage/app-config.local.example.yaml` - GitHub integration section
- `backstage/runtime/DEMO_CHECKLIST.md` - Template testing steps
- `README.md` - Updated next steps with token setup reference

**Planning artifacts:**
- `.hermes/plans/2026-06-16_150000-issue-22-software-templates-github-integration.md` - This plan

---

## Acceptance Criteria Verification

After implementation, verify issue #22 acceptance criteria:

1. ✅ **Backstage offers a template/action to create a metadata-fix issue**
   - Verified by: `catalog-metadata-fix` template with `github:issues:create`

2. ✅ **Backstage offers a template/action to request an IKS review**
   - Verified by: `iks-review-request` template with `github:issues:create`

3. ✅ **Created issues include service identifier, missing field/reason, catalog links**
   - Verified by: Template parameters map to issue body fields

4. ✅ **Workflow is auditable and low-risk: creates GitHub issues only**
   - Verified by: Only `github:issues:create` action used, no other mutations

5. ✅ **Credentials/secrets documented and not committed**
   - Verified by: `GITHUB_INTEGRATION.md` documents setup, uses env vars

6. ✅ **Generated issue content matches active GitHub Issue Forms**
   - Verified by: Template parameters align with `.github/ISSUE_TEMPLATE/*.yml` fields

---

## Definition of Done Checklist

- [ ] Integration documentation created (`GITHUB_INTEGRATION.md`)
- [ ] Templates updated with `github:issues:create` action
- [ ] Demo checklist includes template testing steps
- [ ] app-config example includes GitHub integration
- [ ] No secrets committed anywhere
- [ ] Manual template testing completed (with local GitHub token)
- [ ] Created issues verified in GitHub
- [ ] All files committed on branch `22-replace-port-actions-with-software-templates`
- [ ] Plan file included in branch for traceability
- [ ] PR created with summary and testing instructions

---

## Commit Strategy

### Commit 1: Add GitHub integration documentation

```
docs: add GitHub integration setup for Software Templates

- Create backstage/runtime/GITHUB_INTEGRATION.md
- Document PAT and GitHub App authentication options
- Provide troubleshooting guidance
- Emphasize never committing tokens

Part of #22
```

Files: `backstage/runtime/GITHUB_INTEGRATION.md`

### Commit 2: Update Software Templates with GitHub issue creation

```
feat: enable GitHub issue creation in Software Templates

- Update catalog-metadata-fix template with github:issues:create action
- Update iks-review-request template with github:issues:create action
- Add advisory note to service-onboarding template (deferred to future)
- Align template parameters with GitHub Issue Form fields
- Add clickable output links to created issues

Part of #22
```

Files:
- `backstage/templates/catalog-metadata-fix/template.yaml`
- `backstage/templates/iks-review-request/template.yaml`
- `backstage/templates/service-onboarding/template.yaml`

### Commit 3: Update documentation and examples

```
docs: document template testing and GitHub integration

- Add template testing section to DEMO_CHECKLIST.md
- Add GitHub integration to app-config.local.example.yaml
- Update README next steps with token setup reference

Part of #22
```

Files:
- `backstage/runtime/DEMO_CHECKLIST.md`
- `backstage/app-config.local.example.yaml`
- `README.md`

### Commit 4: Add implementation plan

```
docs: add implementation plan for issue #22

Part of #22
```

Files: `.hermes/plans/2026-06-16_150000-issue-22-software-templates-github-integration.md`

---

## Risks and Considerations

### GitHub Token Security

**Risk:** Developers might accidentally commit GitHub tokens.

**Mitigation:**
- Clear documentation warns against committing tokens
- Example configs use `${GITHUB_TOKEN}` environment variable syntax
- `.gitignore` should catch common token file patterns
- Plan emphasizes using environment variables

### Token Scope and Permissions

**Risk:** Token might have too broad permissions (security) or too narrow (functionality).

**Mitigation:**
- Documentation specifies minimum required scopes (`repo` or `public_repo`)
- Recommends GitHub App for production (better scoping)
- MVP accepts broader PAT for simplicity

### Template Execution Without Token

**Risk:** Users might try templates without configuring GitHub token, get cryptic errors.

**Mitigation:**
- Integration documentation is clear and findable
- Demo checklist includes prerequisites check
- README points to integration docs in next steps
- Consider adding error handling in future (out of #22 scope)

### Issue Form Field Mismatch

**Risk:** Template parameters might not perfectly match Issue Form fields.

**Mitigation:**
- Manually compared template parameters to issue form fields
- Updated parameters to align (dropdowns, checkboxes)
- Testing step in demo checklist verifies field alignment

### Service Onboarding Template

**Risk:** No matching GitHub Issue Form for `service-onboarding`.

**Mitigation:**
- Explicitly defer this template to future work
- Add note that it's advisory-only in MVP
- Focus #22 on templates with existing issue forms
- Can create matching issue form in follow-up if needed

---

## PR Strategy

**Title:** `feat: enable GitHub issue creation in Software Templates`

**Body:**

```markdown
## Summary
- Enables Backstage Software Templates to create real GitHub issues
- Adds GitHub integration documentation with PAT and GitHub App options
- Updates templates to use `github:issues:create` action
- Closes #22

## Changes

### New Documentation
- Created `backstage/runtime/GITHUB_INTEGRATION.md`
  - PAT setup instructions for dev/demo
  - GitHub App migration path for production
  - Security best practices
  - Troubleshooting guide

### Updated Templates
- `catalog-metadata-fix`: Now creates GitHub issues with `catalog`, `metadata` labels
- `iks-review-request`: Now creates GitHub issues with `iks`, `review` labels
- `service-onboarding`: Added advisory note (deferred to future work)
- All templates provide clickable issue URLs in output

### Updated Documentation
- `DEMO_CHECKLIST.md`: Added template testing verification steps
- `app-config.local.example.yaml`: Added GitHub integration section
- `README.md`: Updated next steps to reference token setup

## Prerequisites for Testing

**⚠️ GitHub Token Required**

To test the templates, you must configure a GitHub Personal Access Token:

1. Follow instructions in `backstage/runtime/GITHUB_INTEGRATION.md`
2. Generate PAT with `repo` scope
3. Set environment variable: `export GITHUB_TOKEN=ghp_xxxxx`
4. Restart Backstage to pick up token

## Testing Instructions

### With GitHub Token Configured

1. Start Backstage: `./scripts/start-backstage.sh`
2. Navigate to "Create..." in Backstage UI
3. Select "Catalog Metadata Fix" template
4. Fill parameters:
   - Component ref: `component:default/reporting-api`
   - Reason: `Runbook`
   - Details: `Missing runbook - detected by scorecard`
5. Execute template
6. Verify GitHub issue created at output URL
7. Repeat for "IKS Review Request" template

### Without GitHub Token (Fallback)

1. Templates still appear in catalog
2. Execution will fail with authentication error
3. Error should mention missing GitHub credentials

## Verification

- [x] YAML syntax validation passed
- [x] Manual read-through of all changed files
- [x] No secrets committed (only environment variable examples)
- [x] Template parameters align with GitHub Issue Forms
- [x] German language preserved in IKS review template
- [x] Integration documentation complete

## Acceptance Criteria Met

- ✅ Backstage offers template to create metadata-fix issues
- ✅ Backstage offers template to request IKS reviews
- ✅ Issues include service identifier, reason, details
- ✅ Workflow is auditable (creates GitHub issues only)
- ✅ Credentials documented, not committed
- ✅ Issue content matches GitHub Issue Forms

## MVP Boundaries Preserved

- ✅ Creates GitHub issues only (low-risk, auditable)
- ✅ No production system mutations
- ✅ No automated changes outside GitHub issues
- ✅ Explicit token configuration required (not auto-enabled)

## Follow-up Work (Out of Scope)

- Create GitHub Issue Form for `service-onboarding` template
- Migrate from PAT to GitHub App authentication (production)
- Add error handling for missing token configuration
- Consider custom UI for template execution status

Generated with [Devin](https://cli.devin.ai/docs)
```

---

## Follow-up Work (Out of Scope for #22)

Explicitly deferred to other issues:

- **Create matching issue form for `service-onboarding` template** (new issue if needed)
- **Migrate to GitHub App authentication** (production deployment work)
- **Add custom error handling for missing credentials** (UX enhancement)
- **Template execution status/history UI** (optional enhancement)
- **Auto-populate component ref from catalog context** (future improvement)

---

_Plan created: 2026-06-16_
_Issue: #22 "Backstage IDP MVP: Replace Port actions with Software Templates and GitHub issue workflows"_
_Branch: `22-replace-port-actions-with-software-templates`_
