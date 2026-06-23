---
name: godot-docs-cross-reference
description: "Use when adding, repairing, or explaining Godot documentation cross-references, including reST labels, :ref:, :doc:, class anchors, toctree entries, and generated API links."
---

# Godot Docs Cross Reference

## Reference Types

- Page label: `.. _doc_topic_name:`
- Label link: ``:ref:`Visible text <doc_topic_name>```
- Same-title label link: ``:ref:`doc_topic_name```
- Document link: ``:doc:`Visible text <../relative/page>```
- Class API link: generated labels like `class_Node`, `class_Node_method_add_child`, `class_Node_property_owner`.

## Workflow

1. Search for an existing label before creating a new one: `rg -n "\.\. _doc_name|_class_Name" godot-docs`.
2. Prefer existing stable labels over file-path links when linking conceptual pages.
3. Use `:doc:` for direct page navigation when no stable label exists.
4. For class members, open `classes/class_*.rst` and copy the generated target label pattern exactly.
5. Run Sphinx dummy build when changing anchors or toctrees.

## Guardrails

- Do not create duplicate `.. _doc_*:` labels.
- Do not point manual pages at generated source internals unless the user asked for contributor docs.
- Keep relative paths in `toctree` entries extensionless, matching surrounding style.
