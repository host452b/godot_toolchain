---
name: godot-claude-code-game-studios-balance-check
description: Use when checking Godot gameplay numbers, combat DPS, time-to-kill, economy loops, progression curves, loot tables, cooldowns, spawn rates, difficulty tuning, or degenerate strategies.
---

# Godot Balance Check

## Overview

Balance checks compare gameplay numbers against design intent. The goal is not
to make every option equal; it is to catch outliers, broken loops, dead zones,
dominant strategies, and values that contradict the player experience target.

## When to Use

- Combat damage, cooldowns, enemy health, or time-to-kill changed.
- Economy faucets, sinks, prices, crafting, or rewards changed.
- Progression, XP, unlocks, loot, spawn rates, or difficulty curves changed.
- A playtest reports grinding, trivial choices, unfair spikes, or dominant builds.
- A Godot project has exported tuning values with no checked safe range.

## Required Inputs

List every source used in the report:

- Design target: GDD, mechanic spec, loop spec, or balance note.
- Data source: Resources, exported variables, config files, tables, scripts.
- Runtime context: player power tier, difficulty, enemy tier, expected session length.
- Current evidence: tests, playtest notes, telemetry, or manual measurements.

## Domain Checks

| Domain | Checks |
|---|---|
| Combat | DPS, burst damage, TTK, stun lock, invulnerability loops, dominant options. |
| Economy | Faucets, sinks, resource accumulation, infinite loops, useless purchases. |
| Progression | XP curve, power curve, dead zones, spikes, skip or grind strategies. |
| Loot | Drop rates, expected time to item, pity timer math, inventory pressure. |
| Spawning | Encounter density, safe recovery windows, runaway difficulty, repetition. |
| Cooldowns | Uptime, rotation pressure, ability overlap, exploit timing. |

## Godot Implementation Map

Before relying on exact class, method, property, or project-setting names,
cross-check local `godot-docs/classes/class_*.rst` and the relevant manual page.

| Need | Godot tools | Notes |
|---|---|---|
| Tuning storage | `Resource`, exported variables, config data | Prefer one source of truth per system. |
| Curves | `Curve`, arrays, lookup tables | Name axes and units; document interpolation. |
| Simulation | headless scene, script runner, deterministic seed | Use fixed scenarios before playtest tuning. |
| Runtime sampling | signals, counters, lightweight telemetry | Capture actual TTK, damage taken, resource flow. |
| Presentation | table, CSV, chart, report | Show expected range, actual value, and issue. |

## Report Shape

```text
Balance Check: [system]
Sources: [files and notes read]
Verdict: HEALTHY | CONCERNS | CRITICAL

Outliers:
| Value | Expected | Actual | Impact | Suggested action |

Degenerate strategies:
- [strategy] -> [why it dominates] -> [possible fix]

Open questions:
- [missing design target or data source]
```

## References

- `references/strategy-management-economy-loops.md` - threshold, reinvestment,
  and escalation economy loops from sandbox, tycoon, and systemic strategy games.

## Common Mistakes

- Tuning by feel before computing basic ranges.
- Declaring imbalance without a design target.
- Averaging away burst damage, downtime, or failure cost.
- Fixing symptoms by changing many values at once.
- Ignoring how audio, VFX, UI, and readability affect perceived balance.
