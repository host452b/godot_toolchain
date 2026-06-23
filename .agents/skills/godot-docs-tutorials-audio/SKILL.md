---
name: godot-docs-tutorials-audio
description: "Use when working with the local godot-docs Manual module for Audio: answer, inspect, or update Godot documentation for Audio. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/audio/index.rst."
---

# Godot Docs Audio

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/audio/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Audio.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `audio_buses` - Audio buses
- `audio_effects` - Audio effects
- `audio_streams` - Audio streams
- `sync_with_audio` - Sync the gameplay with audio and music
- `recording_with_microphone` - Recording with microphone
- `text_to_speech` - Text to speech

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
