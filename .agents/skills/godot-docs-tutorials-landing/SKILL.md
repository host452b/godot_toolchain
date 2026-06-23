---
name: godot-docs-tutorials-landing
description: "Use when working with the local godot-docs Manual module for Tutorials: work with the Tutorials documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/index.rst."
---

# Godot Docs Tutorials

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/index.rst`
- Purpose: work with the Tutorials documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `best_practices/index` - Best practices
- `editor/index` - Editor introduction
- `migrating/index` - Migrating to a new version
- `troubleshooting` - Troubleshooting
- `2d/index` - 2D
- `3d/index` - 3D
- `animation/index` - Animation
- `assets_pipeline/index` - Assets pipeline
- `audio/index` - Audio
- `export/index` - Export
- `io/index` - File and data I/O
- `i18n/index` - Internationalization
- `inputs/index` - Input handling
- `math/index` - Math
- `navigation/index` - Navigation
- `networking/index` - Networking
- `performance/index` - Performance
- `physics/index` - Physics
- `platform/index` - Platform-specific
- `plugins/index` - Plugins
- `rendering/index` - Rendering
- `scripting/index` - Scripting
- `shaders/index` - Shaders
- `ui/index` - User interface (UI)
- `xr/index` - XR

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
