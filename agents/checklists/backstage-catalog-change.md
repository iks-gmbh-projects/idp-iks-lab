# Backstage Catalog Change Checklist

- Start reviews with `agents/checklists/code-review-pyramid.md`: treat Backstage entity names, refs, relations, annotations, locations, templates, issue forms, and validation workflow behavior as API/contract surfaces.
- Confirm the target artifact type: catalog entity, location, template, scorecard/check mapping, issue form, or example service catalog.
- Keep entity names, refs, relation targets, and `iks.dev/` annotation names stable unless migration is part of the task.
- Update demo entities when adding required fields.
- Update docs when changing service metadata semantics.
- Check scorecard/check mapping and templates for references to renamed or moved fields.
- Confirm no secrets are introduced into Backstage example config.
- Validate YAML syntax and manually inspect cross-file relations.
