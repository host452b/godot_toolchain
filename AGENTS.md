# Repository Agent Instructions

This repository is a lightweight Godot ecosystem toolchain. It collects GitHub
repository metadata, loads it into SQLite, exports analysis artifacts, and also
contains a local `godot-docs` submodule plus repo-local agent skills for working
with that documentation.

## Scope

- These instructions apply to the whole repository.
- Keep shared agent behavior here. Do not duplicate the same guidance in
  `CLAUDE.md`; that file should import this one.
- Prefer local repository evidence over memory or assumptions. When answering
  non-obvious questions, cite file paths and line numbers.

## Project Map

- `collect.sh` collects GitHub search results into `data/raw/*.jsonl`.
- `load.py` loads JSONL into `godot.db`.
- `verify.sh` validates collection and SQLite output.
- `export_csv.py` exports `godot_repos.csv`.
- `build_notebook.py` builds the rendered notebook.
- `tests/` contains Python tests for the data-loading behavior.
- `godot-docs/` is a Git submodule for the local Godot documentation snapshot.
- `.agents/skills/` is the repo-local skill source for Codex-compatible agents.
- `.claude/skills/` contains Claude-visible skill links. Preserve symlinks;
  do not replace linked skill directories with copied directories.

## Working Rules

- Check `git status --short --branch` before editing. The worktree may contain
  user or generated changes; do not revert unrelated changes.
- Keep edits narrow and aligned with existing scripts and data formats.
- Use `rg`/`rg --files` for repository searches.
- Use structured parsing for JSON, CSV, SQLite, and notebooks instead of ad hoc
  text edits when practical.
- Treat `data/raw/*.jsonl`, `godot.db`, `godot_repos.csv`, and
  `godot_repos_matrix.ipynb` as generated or data artifacts. Regenerate them
  intentionally and explain the command used.
- Network-dependent commands such as `gh search repos` can fail because of auth,
  rate limits, or sandboxing. Report the exact failure and do not fabricate data.

## Godot Docs Work

- Work from the local `godot-docs/` checkout unless the user explicitly asks for
  online documentation.
- Start broad Godot documentation questions from `godot-docs/index.rst`, then
  follow relevant Sphinx `toctree` entries.
- Manual/tutorial content lives mainly under `godot-docs/tutorials/`.
- Engine internals and contributor material live under `godot-docs/engine_details/`.
- API reference pages live under `godot-docs/classes/` and are generated from
  Godot engine class data. Do not hand-edit `godot-docs/classes/` for normal
  documentation changes.
- Use the `godot-docs-*` skills in `.agents/skills/` for routing, lookup,
  cross-reference, and validation tasks when they match the request.

## Skill Layout

- Add or edit Codex-facing skills under `.agents/skills/<skill-name>/`.
- Keep each skill focused and give `SKILL.md` a clear `name` and `description`.
- If a skill should also be visible to Claude, add a relative symlink under
  `.claude/skills/` pointing to the `.agents/skills/` directory.
- If a skill includes `agents/openai.yaml`, use it for Codex app metadata and
  invocation policy only; keep workflow instructions in `SKILL.md`.

## Verification

- For loader or data-model changes, run:

```bash
python3 -m pytest tests/ -v
```

- For collection/load pipeline changes, prefer this full check when network and
  GitHub authentication are available:

```bash
./collect.sh && python3 load.py && ./verify.sh
```

- For local-only pipeline checks after data already exists, run:

```bash
python3 load.py && ./verify.sh
```

- For Godot docs skill edits, inspect representative `SKILL.md` files and verify
  the Claude symlink layout when relevant:

```bash
find .agents/skills -maxdepth 2 -name SKILL.md | wc -l
find .claude/skills -maxdepth 1 -type l | wc -l
```

