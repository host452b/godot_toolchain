---
name: godot-docs-router
description: "Use when working with the local godot-docs Root module for Router: route broad Godot documentation questions to the right local module skill and source file. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/index.rst."
---

# Godot Docs Router

## Source

- Area: Root
- Start file: `godot-docs/index.rst`
- Purpose: route broad Godot documentation questions to the right local module skill and source file.

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
- `getting_started/introduction/index` - Introduction
- `getting_started/step_by_step/index` - Step by step
- `getting_started/first_2d_game/index` - Your first 2D game
- `getting_started/first_3d_game/index` - Your first 3D game
- `tutorials/best_practices/index` - Best practices
- `tutorials/troubleshooting` - Troubleshooting
- `tutorials/editor/index` - Editor introduction
- `tutorials/migrating/index` - Migrating to a new version
- `tutorials/2d/index` - 2D
- `tutorials/3d/index` - 3D
- `tutorials/animation/index` - Animation
- `tutorials/assets_pipeline/index` - Assets pipeline
- `tutorials/audio/index` - Audio
- `tutorials/export/index` - Export
- `tutorials/io/index` - File and data I/O
- `tutorials/i18n/index` - Internationalization
- `tutorials/inputs/index` - Input handling
- `tutorials/math/index` - Math
- `tutorials/navigation/index` - Navigation
- `tutorials/networking/index` - Networking
- `tutorials/performance/index` - Performance
- `tutorials/physics/index` - Physics
- `tutorials/platform/index` - Platform-specific
- ... 16 more entries in the local `toctree`

## Guardrails

- Use this first when the user asks about Godot docs structure, navigation, or an unclear documentation topic.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
