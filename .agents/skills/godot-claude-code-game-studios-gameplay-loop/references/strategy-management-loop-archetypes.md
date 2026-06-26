# Strategy And Management Loop Archetypes

Use this reference when a Godot game concept resembles historical sandbox,
tycoon management, or systemic strategy simulation.

## Sample Archetypes

| Sample | Design archetype | Primary promise |
|---|---|---|
| Taiko Risshiden | Character-driven sandbox RPG + strategy simulation | Live a self-authored role inside a historical world. |
| Kairosoft-style tycoon | Compact garden management with strong numeric feedback | Invest, optimize, expand, and watch numbers rise. |
| Plague Inc. | Abstract macro strategy with asymmetric opposition | Tune a global system while humanity reacts. |

## Core Loops

### Historical Sandbox Loop

```text
Accept mission or self-set goal
-> travel / train / socialize / trigger events
-> resolve minigame, negotiation, combat, or trade
-> gain skill, money, relationship, merit, or identity progress
-> unlock a role, system, event chain, or political leverage
-> reshape the world state
```

Design notes:
- Usually has multiple parallel loops by role: warrior, merchant, ninja, pirate,
  tea master, ruler, wanderer.
- The loop must support player agency and emergent narrative, not just task
  completion.
- The world needs enough independent motion that the player feels they are
  participating in history, not only consuming quests.

### Tycoon Loop

```text
Build or upgrade facility
-> customers or workers use it
-> earn money, popularity, research, or satisfaction
-> unlock new facility, staff, combo, contest, or land
-> expand layout and optimize throughput
```

Design notes:
- Short feedback is essential: visible customers, income ticks, upgrade flashes,
  new unlock prompts.
- "One more turn" comes from overlapping timers: one upgrade is finishing while
  a contest opens and a new expansion becomes affordable.
- The loop works best when each decision has opportunity cost: build, upgrade,
  hire, research, expand, or save.

### Systemic Strategy Loop

```text
System spreads or evolves
-> player gains resource from spread or pressure
-> player tunes traits, actions, or policies
-> opposing system detects and reacts
-> player adapts to keep escalation under control
```

Design notes:
- The player appears to click a skill tree, but the true game is global system
  tuning.
- Positive feedback must be countered by opposing pressure, otherwise the best
  early snowball dominates.
- The map or dashboard must show the system changing at a glance.

## Loop Scale Checklist

| Scale | Sandbox | Tycoon | Systemic strategy |
|---|---|---|---|
| 5 seconds | Choose menu, move, talk, train. | Place, tap, collect, inspect. | Pop event, pick upgrade, inspect map. |
| 30 seconds | Complete one visit/task/action. | Earn, upgrade, unlock, reposition. | Observe spread, react to resistance. |
| 5 minutes | Finish mission, build relationship, raise skill. | Expand layout, pass contest, unlock tier. | Reach new region phase, trigger countermeasure. |
| 1 hour | Change status, faction, profession, or world politics. | Rebuild economy around new combos and late-game goals. | Discover a stable strategy and counter its weaknesses. |

## Red Flags

- A loop has actions and rewards but no meaningful decision.
- Long-term unlocks do not change the next short loop.
- The player can identify the optimal opening and repeat it forever.
- UI feedback does not expose why the system changed.
- The game promises freedom but rewards only one route.
