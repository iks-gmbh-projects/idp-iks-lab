# Catalog Maintenance Prompt

Use this prompt when changing Backstage catalog descriptors, locations, templates, scorecard/check mappings, active issue forms, or example service catalog files.

Review the requested catalog change against the existing Backstage target model. Keep entity names and refs stable, update related examples and docs when metadata semantics change, and run the lightest YAML validation available. Summarize changed catalog behavior, validation, and any Backstage ingestion, relation, or migration risks.

Use the Code Review Pyramid in `agents/checklists/code-review-pyramid.md`: prioritize API/contract semantics and implementation behavior before documentation, validation, and style.

If the task touches `port/`, treat it as legacy migration reference unless the user explicitly asks for Port-specific work.
