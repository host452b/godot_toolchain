---
name: godot-docs-getting-started-introduction
description: "Use when working with the local godot-docs Getting started module for Introduction: answer, inspect, or update Godot documentation for Introduction. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/getting_started/introduction/index.rst."
---

# Godot Docs Introduction

## Source

- Area: Getting started
- Start file: `godot-docs/getting_started/introduction/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Introduction.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `introduction_to_godot` - Introduction to Godot
- `learn_to_code_with_gdscript` - Learn to code with GDScript
- `key_concepts_overview` - Overview of Godot's key concepts
- `first_look_at_the_editor` - First look at Godot's interface
- `learning_new_features` - Learning new features
- `godot_design_philosophy` - Godot's design philosophy

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
