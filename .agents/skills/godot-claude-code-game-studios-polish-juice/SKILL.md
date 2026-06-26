---
name: godot-claude-code-game-studios-polish-juice
description: Use when a playable Godot feature needs release-quality polish, juice, VFX, audio polish, camera effects, performance cleanup, or regression hardening.
---

# Godot Polish And Juice

## Overview

Polish starts after a feature works. The goal is not "add effects"; it is to make
the feature clear, satisfying, performant, accessible, and stable.

## When To Use

- A Godot feature is functional but feels flat, weak, unclear, noisy, or unfinished.
- VFX, audio, camera, animation, and performance need to be tuned together.
- A feature is approaching a milestone, vertical slice, demo, polish, or release gate.

Do not use before the core interaction is playable. Use a prototype or game-feel
spec first if the mechanic itself is still uncertain.

## Polish Pass

1. Baseline the feature: current FPS, frame spikes, memory, input response, obvious bugs.
2. Improve visual feedback: particles, shader effects, animation accents, camera effects.
3. Improve audio feedback: missing events, mix balance, variants, ambience, spatialization.
4. Improve readability: silhouettes, timing, contrast, telegraphs, reduced-motion mode.
5. Harden edge cases: rapid input, unusual sequences, maximum entities, minimum hardware.
6. Re-test against before/after metrics and player-facing acceptance criteria.

## Godot Checklist

Before relying on exact class, method, property, or project-setting names,
cross-check local `godot-docs/classes/class_*.rst` and the relevant manual page.

| Area | Checks |
|---|---|
| Camera | `Camera2D/3D` shake is directional, decays, clamps, and respects reduced motion. |
| VFX | `GPUParticles2D/3D` or shader effects have particle limits and visibility culling. |
| Animation | `AnimationPlayer`, `AnimationTree`, and `Tween` accents do not block input incorrectly. |
| Audio | `AudioStreamPlayer*` events cover all important actions; buses and volumes are balanced. |
| Performance | Use Godot profiler; watch draw calls, overdraw, shader cost, allocations, and physics load. |
| Accessibility | No critical information is conveyed by color, audio, or motion alone. |
| Regression | Polish changes do not change gameplay rules unless explicitly approved. |

## Juice Event Matrix

```markdown
| Event | Visual | Camera | Audio | Timing | Accessibility fallback |
|---|---|---|---|---|---|
| Player hit enemy | spark burst | 80ms shake | impact variant | on active frame | damage number + enemy flash |
| Player low health | vignette pulse | none | low HP loop ducked | after threshold | HUD icon + color-independent warning |
```

## References

- `references/strategy-management-polish-juice-examples.md` - polish and juice
  examples for sandbox, tycoon, and macro strategy games.

## Common Mistakes

- Adding juice to hide a design problem.
- Increasing particle count without a budget.
- Making every event loud, shaky, or flashy so nothing has hierarchy.
- Treating polish as visual only; audio, feel, accessibility, and QA are part of it.
- Shipping camera shake without reduced-motion handling.
