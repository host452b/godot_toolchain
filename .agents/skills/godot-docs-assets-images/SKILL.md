---
name: godot-docs-assets-images
description: "Use when adding, moving, auditing, or explaining images, videos, GIFs, WebP assets, static files, or localized image behavior in Godot documentation."
---

# Godot Docs Assets Images

## Workflow

1. Place page-specific images near the page in an `img/` subdirectory when surrounding pages do that.
2. Use existing reST image style from nearby files: `.. image::`, `.. figure::`, substitutions like `|image0|`, or `.. video::`.
3. Keep asset paths relative to the `.rst` file.
4. Check for unused images with `_tools/list-unused-images.sh` when removing or moving assets.
5. For global CSS/JS/theme assets, use `_static/`, not page-local `img/`.

## Localized Images

`conf.py` rewrites localized image lookup to point at the parallel `godot-docs-l10n` image tree. Be careful with filenames and path stability if a page is translated.

## Guardrails

- Do not use external image URLs for normal docs content unless nearby docs already use that pattern.
- If adding WebP, remember offline ePub workflow converts WebP to PNG.
- Keep alt text meaningful when the directive supports it.
