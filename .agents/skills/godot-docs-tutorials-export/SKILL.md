---
name: godot-docs-tutorials-export
description: "Use when working with the local godot-docs Manual module for Export: answer, inspect, or update Godot documentation for Export. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/export/index.rst."
---

# Godot Docs Export

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/export/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Export.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `exporting_projects` - Exporting projects
- `exporting_pcks` - Exporting packs, patches, and mods
- `feature_tags` - Feature tags
- `exporting_for_windows` - Exporting for Windows
- `exporting_for_linux` - Exporting for Linux
- `exporting_for_macos` - Exporting for macOS
- `exporting_for_android` - Exporting for Android
- `exporting_for_ios` - Exporting for iOS
- `exporting_for_visionos` - Exporting for visionOS
- `exporting_for_web` - Exporting for the Web
- `changing_application_icon_for_windows` - Manually changing application icon for Windows
- `running_on_macos` - Running Godot apps on macOS
- `android_gradle_build` - Gradle builds for Android
- `one-click_deploy` - One-click deploy
- `exporting_for_dedicated_servers` - Exporting for dedicated servers

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
