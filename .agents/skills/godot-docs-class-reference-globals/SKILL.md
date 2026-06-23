---
name: godot-docs-class-reference-globals
description: "Use when working with the local godot-docs Class reference module for Class reference: Globals: navigate the Globals section, @GDScript, and @GlobalScope API pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/classes/index.rst."
---

# Godot Docs Class reference: Globals

## Source

- Area: Class reference
- Start file: `godot-docs/classes/index.rst`
- Purpose: navigate the Globals section, @GDScript, and @GlobalScope API pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `class_@gdscript` - @GDScript
- `class_@globalscope` - @GlobalScope

## Guardrails

- Use the matching section heading in classes/index.rst, then open the target class_*.rst page.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
