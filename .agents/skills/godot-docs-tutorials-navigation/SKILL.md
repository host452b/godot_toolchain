---
name: godot-docs-tutorials-navigation
description: "Use when working with the local godot-docs Manual module for Navigation: answer, inspect, or update Godot documentation for Navigation. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/navigation/index.rst."
---

# Godot Docs Navigation

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/navigation/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Navigation.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `navigation_introduction_2d` - 2D navigation overview
- `navigation_introduction_3d` - 3D navigation overview
- `navigation_using_navigationservers` - Using NavigationServer
- `navigation_using_navigationmaps` - Using NavigationMaps
- `navigation_using_navigationregions` - Using NavigationRegions
- `navigation_using_navigationmeshes` - Using navigation meshes
- `navigation_using_navigationpaths` - Using NavigationPaths
- `navigation_using_navigationpathqueryobjects` - Using NavigationPathQueryObjects
- `navigation_using_navigationagents` - Using NavigationAgents
- `navigation_using_navigationobstacles` - Using NavigationObstacles
- `navigation_using_navigationlinks` - Using NavigationLinks
- `navigation_using_navigationlayers` - Using NavigationLayers
- `navigation_debug_tools` - Navigation debug tools
- `navigation_connecting_navmesh` - Connecting navigation meshes
- `navigation_different_actor_types` - Support different actor types
- `navigation_different_actor_locomotion` - Support different actor locomotion
- `navigation_different_actor_area_access` - Support different actor area access
- `navigation_optimizing_performance` - Optimizing Navigation Performance

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
