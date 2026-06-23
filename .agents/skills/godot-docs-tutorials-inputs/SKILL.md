---
name: godot-docs-tutorials-inputs
description: "Use when working with the local godot-docs Manual module for Input handling: answer, inspect, or update Godot documentation for Input handling. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/inputs/index.rst."
---

# Godot Docs Input handling

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/inputs/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Input handling.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `inputevent` - Using InputEvent
- `input_examples` - Input examples
- `mouse_and_input_coordinates` - Mouse and input coordinates
- `custom_mouse_cursor` - Customizing the mouse cursor
- `controllers_gamepads_joysticks` - Controllers, gamepads, and joysticks
- `controller_features` - Controller features
- `handling_quit_requests` - Handling quit requests

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
