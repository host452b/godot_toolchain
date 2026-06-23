---
name: godot-docs-tutorials-shaders
description: "Use when working with the local godot-docs Manual module for Shaders: answer, inspect, or update Godot documentation for Shaders. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/shaders/index.rst."
---

# Godot Docs Shaders

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/shaders/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Shaders.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `introduction_to_shaders` - Introduction to shaders
- `shader_reference/index` - Shading reference
- `your_first_shader/index` - Your first shader
- `visual_shaders` - Using VisualShaders
- `compute_shaders` - Using compute shaders
- `screen-reading_shaders` - Screen-reading shaders
- `converting_glsl_to_godot_shaders` - Converting GLSL to Godot shaders
- `shaders_style_guide` - Shaders style guide
- `using_viewport_as_texture` - Using a SubViewport as a texture
- `custom_postprocessing` - Custom post-processing
- `advanced_postprocessing` - Advanced post-processing
- `making_trees` - Making trees

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
