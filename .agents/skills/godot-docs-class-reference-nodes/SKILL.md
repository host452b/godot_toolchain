---
name: godot-docs-class-reference-nodes
description: "Use when working with the local godot-docs Class reference module for Class reference: Nodes: navigate Node-derived class API pages and node inheritance navigation. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/classes/index.rst."
---

# Godot Docs Class reference: Nodes

## Source

- Area: Class reference
- Start file: `godot-docs/classes/index.rst`
- Purpose: navigate Node-derived class API pages and node inheritance navigation.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `class_node` - Node
- `class_acceptdialog` - AcceptDialog
- `class_aimmodifier3d` - AimModifier3D
- `class_animatablebody2d` - AnimatableBody2D
- `class_animatablebody3d` - AnimatableBody3D
- `class_animatedsprite2d` - AnimatedSprite2D
- `class_animatedsprite3d` - AnimatedSprite3D
- `class_animationmixer` - AnimationMixer
- `class_animationplayer` - AnimationPlayer
- `class_animationtree` - AnimationTree
- `class_area2d` - Area2D
- `class_area3d` - Area3D
- `class_aspectratiocontainer` - AspectRatioContainer
- `class_audiolistener2d` - AudioListener2D
- `class_audiolistener3d` - AudioListener3D
- `class_audiostreamplayer` - AudioStreamPlayer
- `class_audiostreamplayer2d` - AudioStreamPlayer2D
- `class_audiostreamplayer3d` - AudioStreamPlayer3D
- `class_backbuffercopy` - BackBufferCopy
- `class_basebutton` - BaseButton
- `class_bone2d` - Bone2D
- `class_boneattachment3d` - BoneAttachment3D
- `class_boneconstraint3d` - BoneConstraint3D
- `class_bonetwistdisperser3d` - BoneTwistDisperser3D
- `class_boxcontainer` - BoxContainer
- `class_button` - Button
- `class_camera2d` - Camera2D
- `class_camera3d` - Camera3D
- `class_canvasgroup` - CanvasGroup
- `class_canvasitem` - CanvasItem
- ... 252 more entries in the local `toctree`

## Guardrails

- Use the matching section heading in classes/index.rst, then open the target class_*.rst page.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
