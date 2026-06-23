---
name: godot-docs-tutorials-assets-pipeline-importing-3d-scenes
description: "Use when working with the local godot-docs Manual module for Importing 3D scenes: work with the Importing 3D scenes documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/assets_pipeline/importing_3d_scenes/index.rst."
---

# Godot Docs Importing 3D scenes

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/assets_pipeline/importing_3d_scenes/index.rst`
- Purpose: work with the Importing 3D scenes documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `available_formats` - Available 3D formats
- `model_export_considerations` - Model export considerations
- `node_type_customization` - Node type customization using name suffixes
- `import_configuration` - Import configuration
- `advanced_import_settings` - Advanced Import Settings

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
