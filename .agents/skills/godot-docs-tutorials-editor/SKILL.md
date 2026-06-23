---
name: godot-docs-tutorials-editor
description: "Use when working with the local godot-docs Manual module for Editor introduction: answer, inspect, or update Godot documentation for Editor introduction. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/editor/index.rst."
---

# Godot Docs Editor introduction

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/editor/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Editor introduction.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `project_manager` - Using the Project Manager
- `inspector_dock` - Inspector Dock
- `project_settings` - Project Settings
- `script_editor` - Script Editor
- `default_key_mapping` - Default editor shortcuts
- `customizing_editor` - Customizing the interface
- `using_the_xr_editor` - Using the XR editor
- `using_the_android_editor` - Using the Android editor
- `using_the_web_editor` - Using the Web editor
- `command_line_tutorial` - Command line tutorial
- `external_editor` - Using an external text editor
- `using_engine_compilation_configuration_editor` - Using the engine compilation configuration editor
- `managing_editor_features` - Managing editor features

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
