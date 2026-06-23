---
name: godot-docs-class-reference-resources
description: "Use when working with the local godot-docs Class reference module for Class reference: Resources: navigate Resource-derived class API pages and asset/resource APIs. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/classes/index.rst."
---

# Godot Docs Class reference: Resources

## Source

- Area: Class reference
- Start file: `godot-docs/classes/index.rst`
- Purpose: navigate Resource-derived class API pages and asset/resource APIs.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `class_resource` - Resource
- `class_animatedtexture` - AnimatedTexture
- `class_animation` - Animation
- `class_animationlibrary` - AnimationLibrary
- `class_animationnode` - AnimationNode
- `class_animationnodeadd2` - AnimationNodeAdd2
- `class_animationnodeadd3` - AnimationNodeAdd3
- `class_animationnodeanimation` - AnimationNodeAnimation
- `class_animationnodeblend2` - AnimationNodeBlend2
- `class_animationnodeblend3` - AnimationNodeBlend3
- `class_animationnodeblendspace1d` - AnimationNodeBlendSpace1D
- `class_animationnodeblendspace2d` - AnimationNodeBlendSpace2D
- `class_animationnodeblendtree` - AnimationNodeBlendTree
- `class_animationnodeextension` - AnimationNodeExtension
- `class_animationnodeoneshot` - AnimationNodeOneShot
- `class_animationnodeoutput` - AnimationNodeOutput
- `class_animationnodestatemachine` - AnimationNodeStateMachine
- `class_animationnodestatemachineplayback` - AnimationNodeStateMachinePlayback
- `class_animationnodestatemachinetransition` - AnimationNodeStateMachineTransition
- `class_animationnodesub2` - AnimationNodeSub2
- `class_animationnodesync` - AnimationNodeSync
- `class_animationnodetimescale` - AnimationNodeTimeScale
- `class_animationnodetimeseek` - AnimationNodeTimeSeek
- `class_animationnodetransition` - AnimationNodeTransition
- `class_animationrootnode` - AnimationRootNode
- `class_arraymesh` - ArrayMesh
- `class_arrayoccluder3d` - ArrayOccluder3D
- `class_atlastexture` - AtlasTexture
- `class_audiobuslayout` - AudioBusLayout
- `class_audioeffect` - AudioEffect
- ... 386 more entries in the local `toctree`

## Guardrails

- Use the matching section heading in classes/index.rst, then open the target class_*.rst page.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
