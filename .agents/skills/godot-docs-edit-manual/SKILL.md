---
name: godot-docs-edit-manual
description: "Use when editing hand-written Godot documentation under tutorials, getting_started, about, community, or engine_details, including reST pages, toctrees, anchors, images, and narrative examples."
---

# Godot Docs Edit Manual

## Scope

Use for hand-written docs under:

- `godot-docs/tutorials/`
- `godot-docs/getting_started/`
- `godot-docs/about/`
- `godot-docs/community/`
- `godot-docs/engine_details/`

## Workflow

1. Read the nearest `index.rst` and the target page before editing.
2. Preserve existing section style, heading levels, anchors, and `:allow_comments:` metadata.
3. If adding a page, add it to the nearest relevant `.. toctree::` and keep order conventions from nearby entries.
4. Prefer existing roles: `:ref:`, `:doc:`, `:button:`, `:menu:`, `:ui:`, `:inspector:`.
5. Run targeted checks: `bash ./_tools/check-rst.sh` and, when dependencies exist, `make SPHINXOPTS='--color -j 4 -W' dummy`.

## Guardrails

- Do not edit `godot-docs/classes/` for manual changes.
- Do not introduce shorthand code block syntax ending in bare `::`; `_tools/check-rst.sh` rejects it.
- Keep examples consistent with nearby Godot version wording and branch `4.6`.
