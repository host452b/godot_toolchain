---
name: godot-docs-class-reference
description: "Use when working with the local godot-docs Class reference module for Class reference: route Class reference section questions across its local toctree entries. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/classes/index.rst."
---

# Godot Docs Class reference

## Source

- Area: Class reference
- Start file: `godot-docs/classes/index.rst`
- Purpose: route Class reference section questions across its local toctree entries.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `$godot-docs-class-reference-all-classes` - Class reference: All classes
- `$godot-docs-class-reference-globals` - Class reference: Globals
- `$godot-docs-class-reference-nodes` - Class reference: Nodes
- `$godot-docs-class-reference-resources` - Class reference: Resources
- `$godot-docs-class-reference-other-objects` - Class reference: Other objects
- `$godot-docs-class-reference-editor-only` - Class reference: Editor-only
- `$godot-docs-class-reference-variant-types` - Class reference: Variant types

## Guardrails

- Root sidebar caption: Class reference.
- Use child module skills for narrower tasks when possible.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
