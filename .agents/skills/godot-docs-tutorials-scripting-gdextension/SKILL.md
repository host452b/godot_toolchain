---
name: godot-docs-tutorials-scripting-gdextension
description: "Use when working with the local godot-docs Manual module for The GDExtension system: work with the The GDExtension system documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/scripting/gdextension/index.rst."
---

# Godot Docs The GDExtension system

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/scripting/gdextension/index.rst`
- Purpose: work with the The GDExtension system documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `what_is_gdextension` - What is GDExtension?
- `gdextension_file` - The .gdextension file
- `gdextension_interface_json_file` - The C interface JSON file
- `gdextension_c_example` - GDExtension C example

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
