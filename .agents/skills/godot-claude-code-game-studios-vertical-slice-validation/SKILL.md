---
name: godot-claude-code-game-studios-vertical-slice-validation
description: Use when validating a Godot vertical slice, pre-production demo, core-loop build, production feasibility, representative quality, or PROCEED/PIVOT/KILL decision.
---

# Godot Vertical Slice Validation

## Overview

A vertical slice proves both player experience and production feasibility. It
should be short, representative, and built at the intended quality level for the
systems it includes.

## When To Use

- A Godot project is deciding whether to move from pre-production into production.
- The team has GDDs and architecture but needs a representative playable slice.
- A slice needs a clear report covering core loop, feel, art/audio, performance, and velocity.

## Scope Rules

- Target 3-5 minutes of continuous gameplay.
- Include one complete loop: start -> challenge -> resolution.
- Cut content before cutting quality.
- Include representative art/audio where they are part of the promise.
- Stop expanding the slice when it tries to prove too many things at once.

## Godot Slice Plan

```markdown
## Vertical Slice Plan
- Core loop exercised:
- Included Godot scenes:
- Included systems:
- Art/audio quality level: placeholder / representative / near-shipping
- Success criteria:
- Hard time limit:
- Cut list:
```

## Validation Report

```markdown
## Vertical Slice Report
### Verdict
PROCEED / PIVOT / KILL

### Core Loop Validation
What passed, failed, or remained unclear.

### Feel Assessment
Controls, animation, camera, feedback, audio, VFX.

### Technical Findings
Godot performance, engine issues, scene architecture, asset pipeline risks.

### Velocity Log
Day-by-day progress; this feeds sprint planning.

### Recommended Next Steps
```

## Playtest Questions

- How long until the first meaningful action?
- What moment made the intended fantasy land, if any?
- What confused you or pulled you out?
- Did controls, camera, animation, and feedback feel coherent?
- As the developer, does this quality level feel feasible for the full game?

## Special Technique: Wizard Of Oz

For AI, NPC, economy, or complex systemic behavior, one person may secretly
simulate the system while the player tests normally. Use this to validate desired
behavior before investing in full implementation.

## Common Mistakes

- Making a long demo instead of a slice.
- Cutting quality so far that the slice cannot validate the intended game.
- Skipping the velocity log.
- Treating a local multiplayer slice as proof of network feel without latency tests.
- Advancing to production after a broken or unfun slice without a deliberate pivot.

