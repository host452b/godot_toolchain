---
name: godot-docs-i18n
description: "Use when working with Godot documentation localization, translated builds, Weblate text, gettext output, language tags, localized images, or i18n class reference behavior."
---

# Godot Docs I18n

## Key Files

- `godot-docs/conf.py`
- `godot-docs/Makefile`
- `godot-docs/index.rst`

## Workflow

1. Check `conf.py` language handling and `supported_languages` before changing language-specific behavior.
2. Use `make gettext` for translation template generation; it passes `-t i18n` and writes outside the docs submodule layout.
3. Treat translated material as living in `godot-docs-l10n`; this repo is the English source checkout.
4. For images, account for the custom `figure_language_filename` override in `conf.py`.
5. For class reference, note that i18n builds may replace `classes` with a symlink to localized class docs.

## Guardrails

- Do not edit translated strings in this English docs repo unless the task is about source text.
- Do not remove `only:: i18n` or `only:: not i18n` blocks without checking both build modes.
- If a local l10n checkout is absent, report that limitation.
