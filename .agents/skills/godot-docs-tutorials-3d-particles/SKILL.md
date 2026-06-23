---
name: godot-docs-tutorials-3d-particles
description: "Use when working with the local godot-docs Manual module for Particle systems (3D): work with the Particle systems (3D) documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/3d/particles/index.rst."
---

# Godot Docs Particle systems (3D)

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/3d/particles/index.rst`
- Purpose: work with the Particle systems (3D) documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `creating_a_3d_particle_system` - Creating a 3D particle system
- `properties` - 3D Particle system properties
- `process_material_properties` - Process material properties
- `subemitters` - Particle sub-emitters
- `trails` - 3D Particle trails
- `turbulence` - Particle turbulence
- `attractors` - 3D Particle attractors
- `collision` - 3D Particle collisions
- `complex_shapes` - Complex emission shapes

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
