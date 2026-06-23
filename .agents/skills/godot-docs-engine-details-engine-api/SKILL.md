---
name: godot-docs-engine-details-engine-api
description: "Use when working with the local godot-docs Engine details module for Engine extension APIs: answer, inspect, or update Godot documentation for Engine extension APIs. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/engine_details/engine_api/index.rst."
---

# Godot Docs Engine extension APIs

## Source

- Area: Engine details
- Start file: `godot-docs/engine_details/engine_api/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Engine extension APIs.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `custom_modules_in_cpp` - Custom modules in C++
- `binding_to_external_libraries` - Binding to external libraries
- `custom_godot_servers` - Custom Godot servers
- `custom_resource_format_loaders` - Custom resource format loaders
- `custom_audiostreams` - Custom AudioStreams
- `custom_platform_ports` - Custom platform ports

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
