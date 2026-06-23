---
name: godot-docs-tutorials-assets-pipeline
description: "Use when working with the local godot-docs Manual module for Assets pipeline: answer, inspect, or update Godot documentation for Assets pipeline. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/assets_pipeline/index.rst."
---

# Godot Docs Assets pipeline

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/assets_pipeline/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Assets pipeline.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `import_process` - Import process
- `importing_images` - Importing images
- `importing_audio_samples` - Importing audio samples
- `importing_translations` - Importing translations
- `importing_3d_scenes/index` - Importing 3D scenes
- `retargeting_3d_skeletons` - Retargeting 3D Skeletons
- `exporting_3d_scenes` - Exporting 3D scenes
- `escn_exporter/index` - Blender ESCN exporter

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
