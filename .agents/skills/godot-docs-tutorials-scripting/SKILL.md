---
name: godot-docs-tutorials-scripting
description: "Use when working with the local godot-docs Manual module for Scripting: answer, inspect, or update Godot documentation for Scripting. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/scripting/index.rst."
---

# Godot Docs Scripting

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/scripting/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Scripting.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `gdscript/index` - GDScript
- `c_sharp/index` - C#/.NET
- `cpp/index` - C++ (godot-cpp)
- `other_languages` - Other languages
- `gdextension/index` - The GDExtension system
- `how_to_read_the_godot_api` - How to read the Godot API
- `debug/index` - Debug
- `idle_and_physics_processing` - Idle and Physics Processing
- `groups` - Groups
- `nodes_and_scene_instances` - Nodes and scene instances
- `overridable_functions` - Overridable functions
- `cross_language_scripting` - Cross-language scripting
- `creating_script_templates` - Creating script templates
- `evaluating_expressions` - Evaluating expressions
- `change_scenes_manually` - Change scenes manually
- `instancing_with_signals` - Instancing with signals
- `pausing_games` - Pausing games and process mode
- `filesystem` - File system
- `resources` - Resources
- `singletons_autoload` - Singletons (Autoload)
- `scene_tree` - Using SceneTree
- `scene_unique_nodes` - Scene Unique Nodes
- `logging` - Logging

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
