---
name: godot-claude-code-game-studios-game-feel
description: Use when designing or reviewing Godot mechanics where responsiveness, weight, hit impact, camera motion, input latency, animation timing, or player control feel matters.
---

# Godot Game Feel

## Overview

Game feel is the "how it operates" layer: responsiveness, weight, snap,
commitment, impact, and failure texture. Keep it separate from visual/audio
requirements, which only describe what feedback events exist.

## When To Use

- A Godot mechanic feels floaty, mushy, slippery, laggy, weak, or unfair.
- A player-facing system needs input, animation, camera, VFX, SFX, or haptics.
- A design says "feels good" but has no measurable target.
- A prototype needs to prove feel, not just rules.

Do not use this for pure economy, save/load, backend, or data-only changes.

## Core Pattern

1. State a falsifiable feel hypothesis:
   `"If the player does X, they should feel Y; we know it works if Z happens."`
2. Name a reference and an anti-reference:
   `Feels like [specific mechanic] because [quality]; not like [bad quality].`
3. Define input-to-response budgets in milliseconds and frames.
4. Define animation frame data: startup, active, recovery.
5. Define impact moments: hit-stop, screen shake, camera kick, rumble, SFX, VFX.
6. Define playtest acceptance criteria that a human can judge consistently.

## Godot Implementation Map

Before relying on exact class, method, property, or project-setting names,
cross-check local `godot-docs/classes/class_*.rst` and the relevant manual page.

| Target | Godot tools | Notes |
|---|---|---|
| Input response | `InputMap`, `_unhandled_input`, `_physics_process` | Use events for discrete actions and physics ticks for continuous movement. |
| Commitment | `AnimationPlayer`, `AnimationTree` | Make startup/active/recovery frames explicit. |
| Hit impact | Signals, hit-stop, SFX/VFX event | Prefer per-actor freeze before global pause. |
| Camera impact | `Camera2D/3D`, trauma decay | Clamp amplitude and support reduced motion. |
| Visual juice | particles, shaders, `Tween` | Budget particles and shader cost. |
| Audio snap | `AudioStreamPlayer`, buses | Use cooldowns and variants. |

## Feel Spec Template

```markdown
## Game Feel

### Reference
- Target: [specific mechanic + exact quality]
- Anti-reference: [what this must not feel like]

### Input Responsiveness
| Action | Max latency | Frame budget at 60fps | Notes |
|---|---:|---:|---|
| Primary action | 50ms | 3 frames | visible or audible response |

### Animation
| Animation | Startup | Active | Recovery | Feel goal |
|---|---:|---:|---:|---|
| Light attack | 4f | 3f | 8f | snappy, low commitment |

### Impact
| Event | Hit-stop | Camera | VFX | SFX | Configurable |
|---|---:|---|---|---|---|
| Heavy hit | 80ms | directional shake | spark burst | impact thud | yes |

### Acceptance Criteria
- [ ] Players use [target words] without prompting.
- [ ] No tester repeats [anti-reference words].
- [ ] Misses read as fair because [failure cue].
```

## References

- `references/interface-driven-juice-examples.md` - non-action game feel and
  juice examples for sandbox, tycoon, and macro strategy games.

## Common Mistakes

- Writing "make it juicy" without duration and intensity targets.
- Adding screen shake before fixing input delay.
- Using global `Engine.time_scale` for every hit-stop.
- Letting VFX hide gameplay readability.
- Testing action feel in a browser when Godot timing is the target.
