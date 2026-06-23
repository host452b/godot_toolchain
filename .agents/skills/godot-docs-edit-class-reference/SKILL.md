---
name: godot-docs-edit-class-reference
description: "Use when a task targets Godot class reference pages, API descriptions, properties, methods, signals, constants, or files under godot-docs/classes."
---

# Godot Docs Edit Class Reference

## Rule

`godot-docs/classes/` is generated. Do not make normal manual edits there.

## Workflow

1. Open `godot-docs/classes/index.rst` or the target `class_*.rst` to identify the generated output.
2. Use `engine_details/class_reference/index.rst` to understand source XML conventions.
3. Track edits to Godot engine XML sources instead: `doc/classes/*.xml`, `modules/*/doc_classes/*.xml`, or `platform/*/doc_classes/*.xml`.
4. Regenerate with Godot's `doc/tools/make_rst.py` workflow when the engine source is available.
5. If only this docs checkout exists, report that the correct source is outside `godot-docs/classes/`.

## Useful Evidence

- `godot-docs/classes/index.rst` says generated automatically from Godot engine sources.
- `.github/workflows/sync_class_ref.yml` removes old `classes/class_*.rst` and rebuilds from the engine repository.

## Guardrails

- Never hand-edit generated class pages unless the user explicitly asks for a temporary local experiment.
- Class reference content uses BBCode-like XML tags before conversion; do not invent reST-only formatting for XML source changes.
