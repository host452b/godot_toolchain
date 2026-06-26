---
name: godot-claude-code-game-studios-combat-feedback
description: Use when designing or implementing Godot combat features with hit detection, damage rules, enemy reactions, VFX, SFX, tuning knobs, or combat feel.
---

# Godot Combat Feedback

## Overview

Combat quality depends on rule clarity, hit reliability, readable reactions, and
layered feedback. Treat damage math, hit events, animation timing, VFX, SFX, AI
reaction, and tests as one contract.

## When To Use

- A combat feature needs hit impact, weapon feel, enemy reaction, parry, dodge, or damage feedback.
- Combat works mechanically but players cannot read what happened.
- Formulas, tuning knobs, VFX, and SFX need to stay data-driven and testable.

## Combat Contract

Define one event shape before implementation:

```markdown
Combat event: [hit|block|parry|dodge|crit|death]
Source: [node/resource]
Target: [node/resource]
Damage/effect: [formula or resource id]
Timing: [startup/active/recovery frames]
Feedback: [animation, VFX, SFX, camera, UI]
Tuning knobs: [exported vars/resources with safe ranges]
Tests: [unit/integration/manual feel checks]
```

## Godot Implementation Map

| Combat need | Godot tools | Notes |
|---|---|---|
| 2D hitboxes | `Area2D`, `CollisionShape2D`, physics layers | Keep hitbox/hurtbox layers explicit. |
| 3D hitboxes | `Area3D`, `ShapeCast3D`, `RayCast3D` | Prefer deterministic checks for melee arcs. |
| Character motion | `CharacterBody2D/3D` | Do not hide movement rules inside animation callbacks only. |
| Timing | `AnimationPlayer`, `AnimationTree`, signals | Emit active-frame events from animation or state machine. |
| Tuning | `Resource` files, exported variables | Put damage, stun, knockback, cooldown, costs in data. |
| Feedback | particles, shaders, camera, audio bus | Feedback should subscribe to combat events, not duplicate damage logic. |

## Feedback Stack

| Moment | Required layers |
|---|---|
| Windup | pose change, telegraph, optional charge sound |
| Active hit | contact VFX, SFX, hit-stop, damage number or state change |
| Block/parry | distinct visual/audio language, no ambiguity with hit |
| Miss | whiff sound or animation recovery, clear commitment |
| Death | state transition, reward cue, cleanup timing |

## Validation

- Unit-test formulas and state transitions.
- Integration-test event emission and receiver wiring.
- Manual-test readability: players can distinguish hit, block, parry, miss, crit.
- Playtest feel: no repeated "floaty", "slippery", "laggy", or "unfair" reports.

## Common Mistakes

- Tying VFX/SFX directly to damage code instead of a combat event.
- Letting animation timing and physics timing disagree.
- Using one impact sound for hit, block, crit, and death.
- Adding knockback or hit-stop without preserving player control rules.
- Failing to expose safe tuning ranges.

