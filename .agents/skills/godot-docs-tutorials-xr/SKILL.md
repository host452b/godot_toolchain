---
name: godot-docs-tutorials-xr
description: "Use when working with the local godot-docs Manual module for XR: answer, inspect, or update Godot documentation for XR. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/xr/index.rst."
---

# Godot Docs XR

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/xr/index.rst`
- Purpose: answer, inspect, or update Godot documentation for XR.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `setting_up_xr` - Setting up XR
- `deploying_to_android` - Deploying to Android
- `a_better_xr_start_script` - A better XR start script
- `ar_passthrough` - AR / Passthrough
- `xr_next_steps` - Where to go from here
- `openxr_settings` - OpenXR Settings
- `xr_action_map` - The XR action map
- `xr_room_scale` - Room scale in XR
- `xr_full_screen_effects` - XR full screen effects
- `openxr_composition_layers` - OpenXR composition layers
- `openxr_hand_tracking` - OpenXR hand tracking
- `openxr_body_tracking` - OpenXR body tracking
- `openxr_render_models` - OpenXR Render Models
- `openxr_spatial_entities` - OpenXR spatial entities
- `introducing_xr_tools` - Introducing XR tools
- `basic_xr_locomotion` - Basic XR Locomotion

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
