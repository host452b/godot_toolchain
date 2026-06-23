---
name: godot-docs-tutorials-3d
description: "Use when working with the local godot-docs Manual module for 3D: answer, inspect, or update Godot documentation for 3D. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/3d/index.rst."
---

# Godot Docs 3D

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/3d/index.rst`
- Purpose: answer, inspect, or update Godot documentation for 3D.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `introduction_to_3d` - Introduction to 3D
- `using_transforms` - Using 3D transforms
- `procedural_geometry/index` - Procedural geometry
- `3d_text` - 3D text
- `3d_rendering_limitations` - 3D rendering limitations
- `standard_material_3d` - Standard Material 3D and ORM Material 3D
- `lights_and_shadows` - 3D lights and shadows
- `using_decals` - Using decals
- `physical_light_and_camera_units` - Physical light and camera units
- `particles/index` - Particle systems (3D)
- `high_dynamic_range` - High dynamic range lighting
- `global_illumination/index` - Global illumination
- `environment_and_post_processing` - Environment and post-processing
- `volumetric_fog` - Volumetric fog and fog volumes
- `3d_antialiasing` - 3D antialiasing
- `using_multi_mesh_instance` - Using MultiMeshInstance3D
- `mesh_lod` - Mesh level of detail (LOD)
- `visibility_ranges` - Visibility ranges (HLOD)
- `occlusion_culling` - Occlusion culling
- `resolution_scaling` - Resolution scaling
- `variable_rate_shading` - Variable rate shading
- `csg_tools` - Prototyping levels with CSG
- `using_gridmaps` - Using GridMaps
- `spring_arm` - Third-person camera with spring arm

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
