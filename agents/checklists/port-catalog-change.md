# Port Catalog Change Checklist

> Legacy reference only. Backstage is the target catalog structure for new work. Use `agents/checklists/backstage-catalog-change.md` unless a task explicitly changes legacy Port migration artifacts.

- Confirm the target artifact type: blueprint, entity, scorecard, action, automation, or example service catalog.
- Keep identifiers, relation names, and enum values stable unless migration is part of the task.
- Update demo entities when adding required fields.
- Update docs when changing service metadata semantics.
- Check scorecards and actions for references to renamed or moved fields.
- Validate YAML syntax and manually inspect cross-file relations.
