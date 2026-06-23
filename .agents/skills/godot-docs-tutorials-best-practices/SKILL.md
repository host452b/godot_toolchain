---
name: godot-docs-tutorials-best-practices
description: "Use when working with the local godot-docs Manual module for Best practices: answer, inspect, or update Godot documentation for Best practices. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/best_practices/index.rst."
---

# Godot Docs Best practices

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/best_practices/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Best practices.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `introduction_best_practices` - Introduction
- `what_are_godot_classes` - Applying object-oriented principles in Godot
- `scene_organization` - Scene organization
- `scenes_versus_scripts` - When to use scenes versus scripts
- `autoloads_versus_regular_nodes` - Autoloads versus regular nodes
- `node_alternatives` - When and how to avoid using nodes for everything
- `godot_interfaces` - Godot interfaces
- `godot_notifications` - Godot notifications
- `data_preferences` - Data preferences
- `logic_preferences` - Logic preferences
- `project_organization` - Project organization
- `version_control_systems` - Version control systems

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
