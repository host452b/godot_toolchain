---
name: godot-docs-tutorials-shaders-your-first-shader
description: "Use when working with the local godot-docs Manual module for Your first shader: work with the Your first shader documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/shaders/your_first_shader/index.rst."
---

# Godot Docs Your first shader

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/shaders/your_first_shader/index.rst`
- Purpose: work with the Your first shader documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `your_first_2d_shader` - Your first 2D shader
- `your_first_3d_shader` - Your first 3D shader
- `your_second_3d_shader` - Your second 3D shader

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
