---
name: godot-docs-engine-details-development-profiling
description: "Use when working with the local godot-docs Engine details module for Using C++ profilers: work with the Using C++ profilers documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/engine_details/development/profiling/index.rst."
---

# Godot Docs Using C++ profilers

## Source

- Area: Engine details
- Start file: `godot-docs/engine_details/development/profiling/index.rst`
- Purpose: work with the Using C++ profilers documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `hotspot` - Hotspot
- `instruments` - Instruments
- `perfetto` - Perfetto
- `tracy` - Tracy
- `very_sleepy` - VerySleepy

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
