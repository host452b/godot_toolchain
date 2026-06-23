---
name: godot-docs-class-reference-variant-types
description: "Use when working with the local godot-docs Class reference module for Class reference: Variant types: navigate Variant, built-in value types, containers, math types, and packed arrays. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/classes/index.rst."
---

# Godot Docs Class reference: Variant types

## Source

- Area: Class reference
- Start file: `godot-docs/classes/index.rst`
- Purpose: navigate Variant, built-in value types, containers, math types, and packed arrays.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `class_variant` - Variant
- `class_aabb` - AABB
- `class_array` - Array
- `class_basis` - Basis
- `class_bool` - bool
- `class_callable` - Callable
- `class_color` - Color
- `class_dictionary` - Dictionary
- `class_float` - float
- `class_int` - int
- `class_nodepath` - NodePath
- `class_object` - Object
- `class_packedbytearray` - PackedByteArray
- `class_packedcolorarray` - PackedColorArray
- `class_packedfloat32array` - PackedFloat32Array
- `class_packedfloat64array` - PackedFloat64Array
- `class_packedint32array` - PackedInt32Array
- `class_packedint64array` - PackedInt64Array
- `class_packedstringarray` - PackedStringArray
- `class_packedvector2array` - PackedVector2Array
- `class_packedvector3array` - PackedVector3Array
- `class_packedvector4array` - PackedVector4Array
- `class_plane` - Plane
- `class_projection` - Projection
- `class_quaternion` - Quaternion
- `class_rect2` - Rect2
- `class_rect2i` - Rect2i
- `class_rid` - RID
- `class_signal` - Signal
- `class_string` - String
- ... 9 more entries in the local `toctree`

## Guardrails

- Use the matching section heading in classes/index.rst, then open the target class_*.rst page.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
