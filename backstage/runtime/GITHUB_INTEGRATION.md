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

Export the token before starting the Docker runtime:

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

1. Start Backstage: `./scripts/start-backstage-docker.sh`
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
