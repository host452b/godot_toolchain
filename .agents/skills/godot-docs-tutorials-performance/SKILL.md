---
name: godot-docs-tutorials-performance
description: "Use when working with the local godot-docs Manual module for Performance: answer, inspect, or update Godot documentation for Performance. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/performance/index.rst."
---

# Godot Docs Performance

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/performance/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Performance.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `general_optimization` - General optimization tips
- `using_servers` - Optimization using Servers
- `cpu_optimization` - CPU optimization
- `gpu_optimization` - GPU optimization
- `using_multimesh` - Optimization using MultiMeshes
- `pipeline_compilations` - Reducing stutter from shader (pipeline) compilations
- `optimizing_3d_performance` - Optimizing 3D performance
- `vertex_animation/index` - Animating thousands of objects
- `using_multiple_threads` - Using multiple threads
- `thread_safe_apis` - Thread-safe APIs

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
