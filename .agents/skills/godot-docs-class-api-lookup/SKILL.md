---
name: godot-docs-class-api-lookup
description: "Use when looking up a Godot class, method, property, signal, constant, annotation, Variant type, Node, Resource, or generated API anchor in the local class reference."
---

# Godot Docs Class API Lookup

## Workflow

1. Normalize the class name to lowercase file form: `Node3D` -> `godot-docs/classes/class_node3d.rst`.
2. If unsure, search:
   ```bash
   rg -n "^ClassName$|\.\. _class_ClassName:" godot-docs/classes
   ```
3. For members, search inside the class file:
   ```bash
   rg -n "method_name|property_name|signal_name|CONSTANT_NAME" godot-docs/classes/class_name.rst
   ```
4. Use the generated anchor labels exactly when linking from manual docs.
5. If conceptual explanation is needed, also search manual pages for the class name.

## Class Groups

- Globals: `$godot-docs-class-reference-globals`
- Nodes: `$godot-docs-class-reference-nodes`
- Resources: `$godot-docs-class-reference-resources`
- Other objects: `$godot-docs-class-reference-other-objects`
- Editor-only: `$godot-docs-class-reference-editor-only`
- Variant types: `$godot-docs-class-reference-variant-types`

## Guardrails

- API pages describe surface and signatures; they are not proof of runtime implementation details.
- Do not edit generated `class_*.rst` for permanent changes; use `$godot-docs-edit-class-reference`.
