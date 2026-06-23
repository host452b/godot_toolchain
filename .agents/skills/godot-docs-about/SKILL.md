---
name: godot-docs-about
description: "Use when working with the local godot-docs About module for About: route About section questions across its local toctree entries. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/index.rst."
---

# Godot Docs About

## Source

- Area: About
- Start file: `godot-docs/index.rst`
- Purpose: route About section questions across its local toctree entries.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `about/introduction` - Introduction
- `about/list_of_features` - List of features
- `about/system_requirements` - System requirements
- `about/faq` - Frequently asked questions
- `about/complying_with_licenses` - Complying with licenses
- `about/release_policy` - Godot release policy
- `about/docs_changelog` - Documentation changelog

## Guardrails

- Root sidebar caption: About.
- Use child module skills for narrower tasks when possible.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
