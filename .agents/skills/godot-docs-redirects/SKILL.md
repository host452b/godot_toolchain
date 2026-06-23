---
name: godot-docs-redirects
description: "Use when moving, renaming, deleting, or restructuring Godot documentation pages where old URLs may need redirects or historical route preservation."
---

# Godot Docs Redirects

## Workflow

1. Before moving a page, identify old and new `.rst` paths.
2. Update every relevant `toctree`, `:doc:`, and `:ref:` usage.
3. Inspect `_tools/redirects/README.md` and scripts before changing redirect data.
4. If moving via git, use `git mv` so rename detection can feed redirect generation.
5. Validate with Sphinx dummy build after path or anchor changes.

## Files

- `godot-docs/_tools/redirects/README.md`
- `godot-docs/_tools/redirects/convert_git_renames_to_csv.py`
- `godot-docs/_tools/redirects/create_redirects.py`

## Guardrails

- Do not silently break old docs URLs when renaming files.
- Do not add redirects without checking existing redirect tooling format.
- For simple text-only edits, redirects are not relevant.
