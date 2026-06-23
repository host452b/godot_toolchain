---
name: godot-docs-tutorials-plugins-editor
description: "Use when working with the local godot-docs Manual module for Editor plugins: work with the Editor plugins documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/plugins/editor/index.rst."
---

# Godot Docs Editor plugins

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/plugins/editor/index.rst`
- Purpose: work with the Editor plugins documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `installing_plugins` - Installing plugins
- `making_plugins` - Making plugins
- `making_main_screen_plugins` - Making main screen plugins
- `import_plugins` - Import plugins
- `3d_gizmos` - 3D gizmo plugins
- `inspector_plugins` - Inspector plugins
- `visual_shader_plugins` - Visual Shader plugins

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
