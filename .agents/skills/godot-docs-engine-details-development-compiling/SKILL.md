---
name: godot-docs-engine-details-development-compiling
description: "Use when working with the local godot-docs Engine details module for Building from source: work with the Building from source documentation module and its child pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/engine_details/development/compiling/index.rst."
---

# Godot Docs Building from source

## Source

- Area: Engine details
- Start file: `godot-docs/engine_details/development/compiling/index.rst`
- Purpose: work with the Building from source documentation module and its child pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `getting_source` - Getting the source
- `introduction_to_the_buildsystem` - Introduction to the buildsystem
- `compiling_for_windows` - Compiling for Windows
- `compiling_for_linuxbsd` - Compiling for Linux, \*BSD
- `compiling_for_macos` - Compiling for macOS
- `compiling_for_android` - Compiling for Android
- `compiling_for_ios` - Compiling for iOS
- `compiling_for_visionos` - Compiling for visionOS
- `compiling_for_web` - Compiling for the Web
- `cross-compiling_for_ios_on_linux` - Cross-compiling for iOS on Linux
- `compiling_with_dotnet` - Compiling with .NET
- `compiling_with_script_encryption_key` - Compiling with PCK encryption key
- `optimizing_for_size` - Optimizing a build for size

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
