---
name: godot-claude-code-game-studios-mechanic-design
description: Use when defining or reviewing a specific Godot gameplay mechanic, rules, states, transitions, edge cases, tuning knobs, dependencies, acceptance criteria, or implementation contract.
---

# Godot Mechanic Design

## Overview

A mechanic spec should let a programmer implement the behavior without guessing.
It must describe player intent, system rules, state transitions, dependencies,
feedback, and testable acceptance criteria.

## When to Use

- A mechanic needs rules before Godot implementation.
- Existing gameplay code works but nobody can state the intended behavior.
- A feature has unclear edge cases, tuning knobs, or ownership boundaries.
- Designers and programmers disagree about what the mechanic should do.
- A story or task says "make it feel good" without measurable criteria.

## Mechanic Contract

```text
Name: [mechanic]
Player fantasy: [what this should make the player feel]
Owner: [scene/node/system that owns truth]
Inputs: [player, AI, physics, timers, external systems]
Outputs: [state changes, events, feedback, rewards, penalties]
Rules: [numbered, unambiguous]
States: [state list]
Transitions: [from -> trigger -> to]
Tuning knobs: [value, range, reason]
Edge cases: [what must not break]
Acceptance criteria: [Given/When/Then]
```

## State And Rule Tables

| State | Allowed inputs | Exits | Feedback |
|---|---|---|---|
| [state] | [actions/events] | [transition triggers] | [animation/audio/UI/VFX] |

| Rule | Reason | Test |
|---|---|---|
| [specific rule] | [design intent] | [unit/integration/manual check] |

## Godot Implementation Map

Before relying on exact class, method, property, or project-setting names,
cross-check local `godot-docs/classes/class_*.rst` and the relevant manual page.

| Need | Godot tools | Notes |
|---|---|---|
| Mechanic owner | scene root `Node`, component node, or system node | One place owns truth; others subscribe. |
| Tunable data | `Resource`, exported variables, data files | Prefer inspectable values with safe ranges. |
| State machine | enums, child state nodes, or Resource-driven states | Pick the simplest model that exposes transitions. |
| Input binding | `InputMap`, input events, action polling | Do not hardcode device-specific buttons into rules. |
| Collision/query | `Area2D/3D`, `CollisionShape2D/3D`, ray or shape casts | Document layers, masks, and timing. |
| Feedback wiring | signals, animation, audio, particles, UI events | Feedback must not duplicate rule logic. |
| Tests | scripted checks plus manual feel checks | Automate rules; manually validate subjective feel. |

## Acceptance Criteria

Use concrete Given/When/Then statements:

```text
Given [initial state]
When [player action or system event]
Then [specific state/output changes]
And [observable feedback]
```

Subjective criteria need observable anchors:

- Bad: "Jump feels responsive."
- Better: "Jump starts within [N] frames, reaches [height], and supports [coyote/buffer] window."

## References

- `references/strategy-management-mechanics-state-events.md` - simulation
  mechanics, state machines, event triggers, AI, and mod extension examples.

## Common Mistakes

- Hiding rules inside animation callbacks without documenting ownership.
- Letting VFX or audio trigger gameplay state directly.
- Writing formulas without variable definitions and safe ranges.
- Omitting "what the player cannot do."
- Treating manual feel checks as a replacement for rule tests.
