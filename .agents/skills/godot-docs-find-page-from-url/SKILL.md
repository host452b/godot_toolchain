---
name: godot-docs-find-page-from-url
description: "Use when converting a docs.godotengine.org URL, HTML page path, or sidebar route into the matching local godot-docs reStructuredText source file."
---

# Godot Docs Find Page From URL

## Mapping

1. Strip domain and language/version prefix: `/en/4.6/`, `/en/stable/`, `/en/latest/`.
2. Convert `.html` to `.rst`.
3. Convert trailing `/index.html` or directory URL to `index.rst`.
4. Preserve anchors after `#` and search for matching labels if needed.

## Examples

- `/en/4.6/tutorials/3d/lights_and_shadows.html` -> `godot-docs/tutorials/3d/lights_and_shadows.rst`
- `/en/4.6/classes/class_node.html#class-node-method-add-child` -> `godot-docs/classes/class_node.rst`, then search the anchor.
- `/en/4.6/tutorials/scripting/gdscript/` -> `godot-docs/tutorials/scripting/gdscript/index.rst`

## Commands

- `test -f godot-docs/<path>.rst`
- `rg -n "anchor|label|heading" godot-docs/<path>.rst`
- `rg -n "Title text" godot-docs --glob '*.rst'` when the URL is stale or redirected.

## Guardrails

- Version labels in URL may not match local checkout branch. This repo currently tracks `4.6`; verify with `.gitmodules` or `git -C godot-docs branch --show-current`.
- Some landing pages are linked by raw HTML and may be `:orphan:`.
