---
name: godot-docs-tutorials-io
description: "Use when working with the local godot-docs Manual module for File and data I/O: answer, inspect, or update Godot documentation for File and data I/O. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/io/index.rst."
---

# Godot Docs File and data I/O

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/io/index.rst`
- Purpose: answer, inspect, or update Godot documentation for File and data I/O.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `background_loading` - Background loading
- `data_paths` - File paths in Godot projects
- `saving_games` - Saving games
- `runtime_file_loading_and_saving` - Runtime file loading and saving
- `binary_serialization_api` - Binary serialization API

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
