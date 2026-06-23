---
name: godot-docs-class-reference-editor-only
description: "Use when working with the local godot-docs Class reference module for Class reference: Editor-only: navigate editor-only API classes and editor plugin API references. Trigger on Godot docs, Sphinx toctree, reST, API reference, or source path godot-docs/classes/index.rst."
---

# Godot Docs Class reference: Editor-only

## Source

- Area: Class reference
- Start file: `godot-docs/classes/index.rst`
- Purpose: navigate editor-only API classes and editor plugin API references.

## Workflow

1. Read the start file first.
2. Follow only the relevant `.. toctree::` entries for the user's task.
3. Preserve the documentation layer: tutorial/manual pages explain usage; `engine_details/` explains internals and contribution workflows; `classes/` is generated API reference.
4. When answering, cite local file paths and line numbers for non-obvious claims.

## Local Child Pages

- `class_editorcommandpalette` - EditorCommandPalette
- `class_editorcontextmenuplugin` - EditorContextMenuPlugin
- `class_editordebuggerplugin` - EditorDebuggerPlugin
- `class_editordebuggersession` - EditorDebuggerSession
- `class_editordock` - EditorDock
- `class_editorexportplatform` - EditorExportPlatform
- `class_editorexportplatformandroid` - EditorExportPlatformAndroid
- `class_editorexportplatformappleembedded` - EditorExportPlatformAppleEmbedded
- `class_editorexportplatformextension` - EditorExportPlatformExtension
- `class_editorexportplatformios` - EditorExportPlatformIOS
- `class_editorexportplatformlinuxbsd` - EditorExportPlatformLinuxBSD
- `class_editorexportplatformmacos` - EditorExportPlatformMacOS
- `class_editorexportplatformpc` - EditorExportPlatformPC
- `class_editorexportplatformvisionos` - EditorExportPlatformVisionOS
- `class_editorexportplatformweb` - EditorExportPlatformWeb
- `class_editorexportplatformwindows` - EditorExportPlatformWindows
- `class_editorexportplugin` - EditorExportPlugin
- `class_editorexportpreset` - EditorExportPreset
- `class_editorfeatureprofile` - EditorFeatureProfile
- `class_editorfiledialog` - EditorFileDialog
- `class_editorfilesystem` - EditorFileSystem
- `class_editorfilesystemdirectory` - EditorFileSystemDirectory
- `class_editorfilesystemimportformatsupportquery` - EditorFileSystemImportFormatSupportQuery
- `class_editorimportplugin` - EditorImportPlugin
- `class_editorinspector` - EditorInspector
- `class_editorinspectorplugin` - EditorInspectorPlugin
- `class_editorinterface` - EditorInterface
- `class_editornode3dgizmo` - EditorNode3DGizmo
- `class_editornode3dgizmoplugin` - EditorNode3DGizmoPlugin
- `class_editorpaths` - EditorPaths
- ... 28 more entries in the local `toctree`

## Guardrails

- Use the matching section heading in classes/index.rst, then open the target class_*.rst page.
- Work from the current local checkout; do not assume online docs are current unless the user asks to browse.
- Use `rg -n` and line-numbered reads to ground answers in exact source files.
- For exact engine API behavior, cross-check `godot-docs/classes/class_*.rst`; for implementation behavior, inspect the Godot engine source if available.
- Do not edit `godot-docs/classes/` for normal documentation changes; it is generated from Godot engine class XML.
