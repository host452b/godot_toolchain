---
name: godot-docs-sphinx-validate
description: "Use when verifying Godot documentation edits, checking reST syntax, Sphinx toctrees, anchors, warnings, CI behavior, or local build commands in godot-docs."
---

# Godot Docs Sphinx Validate

## Checks

Run from `godot-docs/`.

1. Cheap custom check:
   ```bash
   bash ./_tools/check-rst.sh
   ```
2. Full warning-as-error structure check when dependencies are installed:
   ```bash
   make SPHINXOPTS='--color -j 4 -W' dummy
   ```
3. HTML build when rendered output matters:
   ```bash
   make SPHINXOPTS='--color -j 4' html
   ```

## CI Mirrors

- `.github/workflows/ci.yml` runs pre-commit, `_tools/check-rst.sh`, installs `requirements.txt`, then `make SPHINXOPTS='--color -j 4 -W' dummy`.
- `.readthedocs.yml` uses `conf.py` and `requirements.txt`.

## Guardrails

- If dependencies are missing, report the exact skipped command and reason.
- Do not claim docs are valid without running at least the available local checks.
- `linkcheck` exists via Sphinx but has network sensitivity; use only when requested or needed.
