---
name: godot-docs-tutorials-2d
description: "Use when working with the local godot-docs Manual module for 2D: answer, inspect, or update Godot documentation for 2D. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/2d/index.rst."
---

# Godot Docs 2D

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/2d/index.rst`
- Purpose: answer, inspect, or update Godot documentation for 2D.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `introduction_to_2d` - Introduction to 2D
- `canvas_layers` - Canvas layers
- `2d_transforms` - Viewport and canvas transforms
- `2d_lights_and_shadows` - 2D lights and shadows
- `2d_meshes` - 2D meshes
- `2d_sprite_animation` - 2D sprite animation
- `particle_systems_2d` - 2D particle systems
- `particle_process_material_2d` - ParticleProcessMaterial 2D Usage
- `2d_antialiasing` - 2D antialiasing
- `custom_drawing_in_2d` - Custom drawing in 2D
- `2d_parallax` - 2D Parallax
- `2d_movement` - 2D movement overview
- `using_tilesets` - Using TileSets
- `using_tilemaps` - Using TileMaps

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
