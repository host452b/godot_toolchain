---
name: godot-claude-code-game-studios-gameplay-loop
description: Use when designing or reviewing a Godot game's core verb, core loop, player fantasy, gameplay pillars, moment-to-moment loop, session loop, or fun hypothesis before implementation.
---

# Godot Gameplay Loop

## Overview

A gameplay loop is the repeatable cycle of intent, action, feedback, reward,
and reset. In Godot, define the loop before architecture so scenes, signals,
Resources, UI, audio, and tests all support the same player experience.

## When to Use

- A game idea needs a concrete core verb and core loop.
- A feature seems fun in prose but has no player action cycle.
- A prototype or vertical slice needs a loop target.
- Multiple systems exist but do not reinforce the same player fantasy.
- A Godot implementation is starting before the gameplay question is clear.

Do not use this for pure polish of an already-proven mechanic. Use
`godot-claude-code-game-studios-polish-juice` for that.

## Core Loop Contract

Write the loop as a falsifiable contract:

```text
Player fantasy: [what the player should feel]
Core verb: [the most repeated player action]
Primary decision: [what the player evaluates before acting]
Risk: [what can go wrong]
Reward: [what changes after success]
Reset: [what invites the next cycle]
Failure texture: [what failure teaches or costs]
```

## Loop Scales

| Scale | Purpose | Questions |
|---|---|---|
| 5-second action | Immediate verb feel | Is the action readable, responsive, and worth repeating? |
| 30-second loop | Moment-to-moment play | What creates choice, risk, feedback, and reward? |
| 5-minute loop | Short-term goal | What goal structures repeated actions into progress? |
| Session loop | Return motivation | What persists, escalates, unlocks, or changes next time? |

## Godot Implementation Map

Before relying on exact class, method, property, or project-setting names,
cross-check local `godot-docs/classes/class_*.rst` and the relevant manual page.

| Need | Godot tools | Notes |
|---|---|---|
| Player input | `InputMap`, `_unhandled_input`, `_physics_process` | Separate discrete events from continuous movement. |
| Loop owner | `Node`, scene composition, autoload only if needed | Keep ownership explicit; avoid global state by default. |
| Tunable data | `Resource`, exported variables, config data | Keep tuning values out of hidden code paths. |
| State changes | signals, state machine, groups | Feedback listens to events; rules own state. |
| Spatial trigger | `Area2D/3D`, collision layers, ray/shape casts | Make interactable and hazard boundaries inspectable. |
| Feedback | animation, particles, audio, camera, UI | Every gameplay-critical event needs readable feedback. |
| Persistence | save data, progression Resources | Persist rewards only when the loop needs long-term stakes. |

## Validation

- Can a fresh player describe the goal after one cycle?
- Does the player make a meaningful decision, not just execute a script?
- Does failure explain what to try next?
- Does the reward change the next cycle or the player's plan?
- Does every supporting system reinforce the same player fantasy?

## References

- `references/strategy-management-loop-archetypes.md` - Taiko Risshiden,
  Kairosoft-style tycoon, and Plague Inc. loop archetypes.

## Common Mistakes

- Starting with content count before proving the core verb.
- Describing genre instead of the actual repeated player action.
- Treating reward as only score, loot, or UI fireworks.
- Letting UI, audio, and VFX communicate different priorities.
- Building a full architecture before the loop hypothesis is testable.
