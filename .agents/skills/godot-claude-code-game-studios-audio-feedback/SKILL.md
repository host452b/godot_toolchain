---
name: godot-claude-code-game-studios-audio-feedback
description: Use when designing or reviewing Godot SFX, audio events, mix hierarchy, adaptive music, ambience, spatial audio, or sound feedback for player actions.
---

# Godot Audio Feedback

## Overview

Audio feedback is both emotional tone and gameplay information. Design the sonic
identity first, then specify events, mix priority, implementation route, and
accessibility fallback.

## When To Use

- A feature needs SFX, UI sounds, ambience, adaptive music, or spatial audio.
- Gameplay-critical information is currently silent or audio-only.
- Audio events are repetitive, too loud, masked, missing, or not wired to gameplay.
- A Godot project needs an audio event list or audio manager design.

## Audio Design Pass

1. Define sonic identity: acoustic/synthetic, clean/distorted, sparse/dense.
2. Define emotional target per state: exploration, combat, danger, success, failure.
3. List every audio event and its trigger condition.
4. Set priority, bus, volume range, pitch variation, cooldown, and concurrency.
5. Decide native Godot audio vs middleware; keep native unless a real need exists.
6. Add visual/text fallback for all gameplay-critical audio.

## Godot Implementation Map

Before relying on exact class, method, property, or project-setting names,
cross-check local `godot-docs/classes/class_*.rst` and the relevant manual page.

| Need | Godot tool | Notes |
|---|---|---|
| One-shot UI/gameplay SFX | `AudioStreamPlayer`, `AudioStreamPlayer2D/3D` | Pool players for frequent sounds. |
| Mix hierarchy | Audio buses, `AudioServer` | Separate music, ambience, UI, gameplay, voice. |
| Adaptive music | Multiple players or synchronized stems | Crossfade by state; document transitions. |
| Spatial cues | `AudioStreamPlayer2D/3D` | Validate attenuation, panning, and max distance. |
| Reverb / area bus effects | `Area2D/3D` bus routing, `Area3D` reverb buses | Treat occlusion as custom raycast/filter logic unless the project uses middleware. |
| Variation | Random stream/pitch within safe ranges | Avoid repetition without changing meaning. |

## Audio Event Spec

```markdown
| Event | Trigger | Priority | Bus | Volume | Pitch | Cooldown | Variants | Fallback |
|---|---|---|---|---:|---:|---:|---:|---|
| enemy_alert | enemy detects player | High | Gameplay | -8 dB | +/-4% | 0.5s | 3 | icon over enemy |
```

## Accessibility Rules

- No required game state can be audio-only.
- Sudden loud sounds need mix limits and, when relevant, player settings.
- Subtitle or caption rules should cover dialogue and critical non-dialogue cues.
- If an audio cue warns the player, add visual, UI, or haptic backup.

## References

- `references/strategy-management-audio-examples.md` - audio event priority,
  mix, ambience, reward, and warning examples for strategy/management games.

## Common Mistakes

- Letting every feature create its own unmanaged `AudioStreamPlayer`.
- Missing cooldowns for spammy sounds like hits, pickups, and UI hover.
- Using pitch randomization so wide that a sound changes meaning.
- Mixing ambience over gameplay-critical cues.
- Creating audio assets before the event list and priority hierarchy are clear.
