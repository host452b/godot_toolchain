---
name: godot-docs-getting-started-first-2d-game
description: "Use when working with the local godot-docs Getting started module for Your first 2D game: answer, inspect, or update Godot documentation for Your first 2D game. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/getting_started/first_2d_game/index.rst."
---

# Godot Docs Your first 2D game

## Source

- Area: Getting started
- Start file: `godot-docs/getting_started/first_2d_game/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Your first 2D game.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `01.project_setup` - missing in local checkout
- `02.player_scene` - missing in local checkout
- `03.coding_the_player` - missing in local checkout
- `04.creating_the_enemy` - missing in local checkout
- `05.the_main_game_scene` - missing in local checkout
- `06.heads_up_display` - missing in local checkout
- `07.finishing-up` - missing in local checkout

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
