---
name: godot-docs-manual
description: "Use when working with the local godot-docs Manual module for Manual: route Manual section questions across its local toctree entries. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/index.rst."
---

# Godot Docs Manual

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/index.rst`
- Purpose: route Manual section questions across its local toctree entries.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `tutorials/best_practices/index` - Best practices
- `tutorials/troubleshooting` - Troubleshooting
- `tutorials/editor/index` - Editor introduction
- `tutorials/migrating/index` - Migrating to a new version
- `tutorials/2d/index` - 2D
- `tutorials/3d/index` - 3D
- `tutorials/animation/index` - Animation
- `tutorials/assets_pipeline/index` - Assets pipeline
- `tutorials/audio/index` - Audio
- `tutorials/export/index` - Export
- `tutorials/io/index` - File and data I/O
- `tutorials/i18n/index` - Internationalization
- `tutorials/inputs/index` - Input handling
- `tutorials/math/index` - Math
- `tutorials/navigation/index` - Navigation
- `tutorials/networking/index` - Networking
- `tutorials/performance/index` - Performance
- `tutorials/physics/index` - Physics
- `tutorials/platform/index` - Platform-specific
- `tutorials/plugins/index` - Plugins
- `tutorials/rendering/index` - Rendering
- `tutorials/scripting/index` - Scripting
- `tutorials/shaders/index` - Shaders
- `tutorials/ui/index` - User interface (UI)
- `tutorials/xr/index` - XR

## Guardrails

- Root sidebar caption: Manual.
- Use child module skills for narrower tasks when possible.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
