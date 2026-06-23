---
name: godot-docs-tutorials-ui
description: "Use when working with the local godot-docs Manual module for User interface (UI): answer, inspect, or update Godot documentation for User interface (UI). Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/ui/index.rst."
---

# Godot Docs User interface (UI)

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/ui/index.rst`
- Purpose: answer, inspect, or update Godot documentation for User interface (UI).

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `size_and_anchors` - Size and anchors
- `gui_containers` - Using Containers
- `custom_gui_controls` - Custom GUI controls
- `gui_navigation` - Keyboard/Controller Navigation and Focus
- `control_node_gallery` - Control node gallery
- `gui_skinning` - Introduction to GUI skinning
- `gui_using_theme_editor` - Using the theme editor
- `gui_theme_type_variations` - Theme type variations
- `gui_using_fonts` - Using Fonts
- `bbcode_in_richtextlabel` - BBCode in RichTextLabel
- `creating_applications` - Creating applications

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
