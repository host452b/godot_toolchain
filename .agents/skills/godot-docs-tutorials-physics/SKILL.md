---
name: godot-docs-tutorials-physics
description: "Use when working with the local godot-docs Manual module for Physics: answer, inspect, or update Godot documentation for Physics. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/physics/index.rst."
---

# Godot Docs Physics

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/physics/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Physics.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `physics_introduction` - Physics introduction
- `using_jolt_physics` - Using Jolt Physics
- `rigid_body` - Using RigidBody
- `using_area_2d` - Using Area2D
- `using_character_body_2d` - Using CharacterBody2D/3D
- `ray-casting` - Ray-casting
- `ragdoll_system` - Ragdoll system
- `kinematic_character_2d` - Kinematic character (2D)
- `soft_body` - Using SoftBody3D
- `collision_shapes_2d` - Collision shapes (2D)
- `collision_shapes_3d` - Collision shapes (3D)
- `large_world_coordinates` - Large world coordinates
- `interpolation/index` - Physics Interpolation
- `troubleshooting_physics_issues` - Troubleshooting physics issues

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
