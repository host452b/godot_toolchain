---
name: godot-docs-community-asset-library
description: "Use when working with the local godot-docs Community module for Asset Library: answer, inspect, or update Godot documentation for Asset Library. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/community/asset_library/index.rst."
---

# Godot Docs Asset Library

## Source

- Area: Community
- Start file: `godot-docs/community/asset_library/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Asset Library.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `what_is_assetlib` - About the Asset Library
- `using_assetlib` - Using the Asset Library
- `submitting_to_assetlib` - Submitting to the Asset Library

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
