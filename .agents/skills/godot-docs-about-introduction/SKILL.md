---
name: godot-docs-about-introduction
description: "Use when working with the local godot-docs About module for Introduction: answer, inspect, or update Godot documentation for Introduction. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/about/introduction.rst."
---

# Godot Docs Introduction

## Source

- Area: About
- Start file: `godot-docs/about/introduction.rst`
- Purpose: answer, inspect, or update Godot documentation for Introduction.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- No child `toctree` entries; treat this as a leaf page.

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
