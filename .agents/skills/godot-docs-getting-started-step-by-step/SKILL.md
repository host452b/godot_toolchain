---
name: godot-docs-getting-started-step-by-step
description: "Use when working with the local godot-docs Getting started module for Step by step: answer, inspect, or update Godot documentation for Step by step. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/getting_started/step_by_step/index.rst."
---

# Godot Docs Step by step

## Source

- Area: Getting started
- Start file: `godot-docs/getting_started/step_by_step/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Step by step.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `nodes_and_scenes` - Nodes and Scenes
- `instancing` - Creating instances
- `scripting_languages` - Scripting languages
- `scripting_first_script` - Creating your first script
- `scripting_player_input` - Listening to player input
- `signals` - Using signals

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
