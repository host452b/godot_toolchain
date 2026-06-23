---
name: godot-docs-tutorials-networking
description: "Use when working with the local godot-docs Manual module for Networking: answer, inspect, or update Godot documentation for Networking. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/tutorials/networking/index.rst."
---

# Godot Docs Networking

## Source

- Area: Manual
- Start file: `godot-docs/tutorials/networking/index.rst`
- Purpose: answer, inspect, or update Godot documentation for Networking.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `high_level_multiplayer` - High-level multiplayer
- `http_request_class` - Making HTTP requests
- `http_client_class` - HTTP client class
- `ssl_certificates` - TLS/SSL certificates
- `websocket` - Using WebSockets
- `webrtc` - WebRTC

## Guardrails

- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
