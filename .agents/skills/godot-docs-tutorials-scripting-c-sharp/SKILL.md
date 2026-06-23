---
name: godot-docs-tutorials-scripting-c-sharp
description: "Use when working with the local godot-docs Manual module for C#/.NET: work with the C#/.NET documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/scripting/c_sharp/index.rst."
---

# Godot Docs C#/.NET

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/scripting/c_sharp/index.rst`
- Purpose: work with the C#/.NET documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `c_sharp_basics` - C# basics
- `c_sharp_features` - C# language features
- `c_sharp_style_guide` - C# style guide
- `diagnostics/index` - C# diagnostics
- `c_sharp_differences` - C# API differences to GDScript
- `c_sharp_collections` - C# collections
- `c_sharp_variant` - C# Variant
- `c_sharp_signals` - C# signals
- `c_sharp_exports` - C# exported properties
- `c_sharp_global_classes` - C# global classes

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
