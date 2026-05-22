# Code Review Pyramid Checklist

Use this checklist when reviewing repository changes, pull requests, agent outputs, or catalog/configuration edits.

The review priority is adapted from Gunnar Morling's "Code Review Pyramid". The intent is to spend human review effort on the parts that are hardest to change later, and to automate low-level checks wherever possible.

## Review Priority

### 1. API and Contract Semantics

Focus here first. In this repository, "API" includes Backstage entity names and refs, catalog metadata shape, annotations, issue form fields, workflow behavior, example config surfaces, docs navigation, and any user-facing conventions.

Ask:

- Does the change preserve stable entity names, refs, relations, annotations, and file paths unless migration is explicit?
- Is the exposed catalog/configuration/docs interface as small as possible and as large as needed?
- Is there one clear way to do the task, rather than competing paths?
- Is the behavior consistent with the Backstage target path and GitHub-as-source-of-truth model?
- Are there no unintended breaking changes to user-facing configuration, examples, templates, issue forms, validation workflows, metrics/log conventions, or docs entry points?

### 2. Implementation Semantics

Ask:

- Does the change satisfy the requested requirement and repository mission?
- Is the logic correct, complete, and robust for edge cases?
- Does it avoid unnecessary complexity or scope expansion?
- Does it preserve MVP boundaries: no Kubernetes automation, production infrastructure changes, or autonomous compliance enforcement unless explicitly approved?
- Does it avoid secrets, real credentials, production endpoints, unsafe automation, and external side effects?
- Are newly introduced dependencies, workflows, or generated artifacts justified?

### 3. Documentation

Ask:

- Are docs updated where metadata shape, workflow behavior, demo flow, or governance changed?
- Are Backstage descriptors, examples, wiki docs, issue templates, and validation references kept in sync?
- Is an ADR added only for meaningful architectural or governance decisions, not routine catalog edits?
- Is legacy Port material clearly framed as migration reference when touched?

### 4. Tests and Validation

Ask:

- Did the change run the lightest relevant validation from `agents/validation.md`?
- Are YAML files parsed/linted when touched?
- Are Backstage relations and identifiers manually checked when catalog files change?
- Are Codex skills validated with `quick_validate.py` when available?
- Are validator gaps stated clearly with a targeted manual read-through?

### 5. Code Style and Formatting

Spend the least human review energy here. Prefer automation.

Ask:

- Is formatting consistent with nearby files?
- Are names and language consistent with existing repository conventions?
- Is wording concise and readable?
- Are style-only comments avoided unless they affect clarity or maintainability?

## Automation Boundary

Automate or mechanically check:

- YAML syntax and linting.
- Markdown link/path sanity where tooling is available.
- Codex skill frontmatter and prompt consistency.
- Static secret-pattern scans and obvious generated-file mistakes.
- Formatting and simple style checks.

Use human judgment for:

- API/contract compatibility.
- Backstage/IKS metadata semantics.
- Scope and governance fit.
- Whether docs and examples explain the right behavior.
- Whether validation proves the intended behavior, not just syntax.

## Reporting Format

Lead review comments with concrete risks and file references:

1. API/contract risks.
2. Implementation or scope risks.
3. Documentation drift.
4. Validation gaps.
5. Style/readability suggestions.

Keep style nits out of the critical path unless they make the change misleading or hard to maintain.

Attribution: adapted from Gunnar Morling, "The Code Review Pyramid", https://www.morling.dev/blog/the-code-review-pyramid/.
