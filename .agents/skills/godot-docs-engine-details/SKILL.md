---
name: godot-docs-engine-details
description: "Use when working with the local godot-docs Engine details module for Engine details: route Engine details section questions across its local toctree entries. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/index.rst."
---

# Godot Docs Engine details

## Source

- Area: Engine details
- Start file: `godot-docs/index.rst`
- Purpose: route Engine details section questions across its local toctree entries.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `engine_details/architecture/index` - Engine architecture
- `engine_details/engine_api/index` - Engine extension APIs
- `engine_details/development/index` - Engine development
- `engine_details/editor/index` - Editor development
- `engine_details/class_reference/index` - Class reference primer
- `engine_details/file_formats/index` - Godot file formats

## Guardrails

- Root sidebar caption: Engine details.
- Use child module skills for narrower tasks when possible.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
