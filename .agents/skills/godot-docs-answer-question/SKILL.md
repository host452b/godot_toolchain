---
name: godot-docs-answer-question
description: "Use when answering user questions from the local godot-docs checkout, especially when the answer may require combining manual tutorials, engine details, and generated class reference pages."
---

# Godot Docs Answer Question

## Workflow

1. Start with `$godot-docs-router` if the module is unclear.
2. Read the relevant manual or engine-details page first; use `classes/class_*.rst` only for API surface, signatures, constants, properties, and signals.
3. If a page mentions an API, open the matching class reference page and cite both layers when behavior depends on the API.
4. Separate "docs say how to use it" from "engine implementation behaves this way"; inspect engine source only when the user asks about implementation.
5. Answer with local file paths and line numbers for non-obvious claims.

## Search Patterns

- `rg -n "keyword" godot-docs/tutorials godot-docs/getting_started godot-docs/engine_details`
- `rg -n "^ClassName$|_class_ClassName" godot-docs/classes`
- `rg -n "\.\. _doc_|:ref:|:doc:" godot-docs --glob '*.rst'`

## Guardrails

- Do not browse unless the user asks for current online docs or upstream state.
- Do not treat `classes/` as the source of narrative guidance; it is generated API reference.
- If manual and class reference appear inconsistent, call that out and cite both files.
