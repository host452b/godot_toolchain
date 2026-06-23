---
name: godot-docs-tutorials-animation
description: "Use when working with the local godot-docs Manual module for Animation: answer, inspect, or update Godot documentation for Animation. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/animation/index.rst."
---

# Godot Docs Animation

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/animation/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Animation.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `introduction` - Introduction to the animation features
- `animation_track_types` - Animation Track types
- `cutout_animation` - Cutout animation
- `2d_skeletons` - 2D skeletons
- `animation_tree` - Using AnimationTree
- `playing_videos` - Playing videos
- `creating_movies` - Creating movies

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
