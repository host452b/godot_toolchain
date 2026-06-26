---
name: godot-claude-code-game-studios-ui-feedback
description: Use when designing or reviewing Godot UI, HUD, menus, input feedback, screen transitions, haptics, accessibility, or player-facing interface states.
---

# Godot UI Feedback

## Overview

Every UI action should answer three questions immediately: what did I do, what
happened, and what can I do next? Specify feedback per component, not just per
screen.

## When To Use

- A Godot HUD, menu, inventory, dialogue, pause screen, or settings flow is being designed.
- UI feels unresponsive, confusing, noisy, inaccessible, or inconsistent.
- A UI spec needs input, feedback, events, animation, accessibility, and localization checks.

## Interaction Map

For each interactive component:

```markdown
| Component | Input | Immediate feedback | Event fired | Outcome | Failure state |
|---|---|---|---|---|---|
| Start button | click / gamepad A | scale pulse + click SFX | ui_start_pressed | load game | disabled tooltip |
```

## Godot Implementation Map

Before relying on exact class, method, property, or project-setting names,
cross-check local `godot-docs/classes/class_*.rst` and the relevant manual page.

| Need | Godot tools | Notes |
|---|---|---|
| Layout | `Control`, containers, anchors, size flags | Test 16:9, ultrawide, small window, and text scale. |
| HUD layering | `CanvasLayer`, `Control` | Keep gameplay HUD separate from pause/modal layers. |
| Focus navigation | focus neighbors, `InputMap` actions | Gamepad/keyboard path must be explicit. |
| Visual state | `Theme`, styleboxes, modulate, disabled states | Do not rely on color alone. |
| Motion | `Tween`, `AnimationPlayer` | Provide reduced-motion alternatives for pulses, shakes, transitions. |
| Events | signals | UI emits intent; gameplay systems own state changes. |
| Audio | UI audio bus | Use quiet, short, non-fatiguing variants. |

## HUD Information Tiers

| Tier | Meaning |
|---|---|
| Must Show | Always visible; required for core decisions. |
| Contextual | Visible only when relevant, such as combat or near interactable. |
| On Demand | Player requests it with a hold, toggle, menu, or inspect action. |
| Hidden | Communicated through world, animation, audio, or haptics instead of text. |

If "Must Show" grows too large, stop and resolve the conflict with the game's HUD
philosophy before implementing.

## Accessibility Checks

- Keyboard-only and gamepad-only paths work.
- Text is readable at the target minimum size.
- Information is not color-only, sound-only, or motion-only.
- Subtitles/captions exist where needed.
- A project-level reduced-motion option disables non-essential UI motion.
- Localized text has room to expand.

## References

- `references/strategy-management-ui-ux-examples.md` - UI/UX examples for
  interface-driven sandbox, tycoon, and macro strategy games.

## Common Mistakes

- Animating UI transitions so slowly that the interface feels laggy.
- Letting UI code mutate gameplay state directly instead of emitting signals.
- Treating hover feedback as enough when the game targets gamepad or touch.
- Designing a HUD after implementation instead of before story acceptance criteria.
