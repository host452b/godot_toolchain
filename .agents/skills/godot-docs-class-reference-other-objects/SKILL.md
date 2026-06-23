---
name: godot-docs-class-reference-other-objects
description: "Use when working with the local godot-docs Class reference module for Class reference: Other objects: navigate non-Node, non-Resource object API pages. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/classes/index.rst."
---

# Godot Docs Class reference: Other objects

## Source

- Area: Class reference
- Start file: `godot-docs/classes/index.rst`
- Purpose: navigate non-Node, non-Resource object API pages.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `class_object` - Object
- `class_aescontext` - AESContext
- `class_astar2d` - AStar2D
- `class_astar3d` - AStar3D
- `class_astargrid2d` - AStarGrid2D
- `class_audioeffectinstance` - AudioEffectInstance
- `class_audioeffectspectrumanalyzerinstance` - AudioEffectSpectrumAnalyzerInstance
- `class_audiosample` - AudioSample
- `class_audiosampleplayback` - AudioSamplePlayback
- `class_audioserver` - AudioServer
- `class_audiostreamgeneratorplayback` - AudioStreamGeneratorPlayback
- `class_audiostreamplayback` - AudioStreamPlayback
- `class_audiostreamplaybackinteractive` - AudioStreamPlaybackInteractive
- `class_audiostreamplaybackoggvorbis` - AudioStreamPlaybackOggVorbis
- `class_audiostreamplaybackplaylist` - AudioStreamPlaybackPlaylist
- `class_audiostreamplaybackpolyphonic` - AudioStreamPlaybackPolyphonic
- `class_audiostreamplaybackresampled` - AudioStreamPlaybackResampled
- `class_audiostreamplaybacksynchronized` - AudioStreamPlaybackSynchronized
- `class_callbacktweener` - CallbackTweener
- `class_camerafeed` - CameraFeed
- `class_cameraserver` - CameraServer
- `class_charfxtransform` - CharFXTransform
- `class_classdb` - ClassDB
- `class_configfile` - ConfigFile
- `class_crypto` - Crypto
- `class_diraccess` - DirAccess
- `class_displayserver` - DisplayServer
- `class_dtlsserver` - DTLSServer
- `class_editorcontextmenuplugin` - EditorContextMenuPlugin
- `class_editordebuggerplugin` - EditorDebuggerPlugin
- ... 299 more entries in the local `toctree`

## Guardrails

- Use the matching section heading in classes/index.rst, then open the target class_*.rst page.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
