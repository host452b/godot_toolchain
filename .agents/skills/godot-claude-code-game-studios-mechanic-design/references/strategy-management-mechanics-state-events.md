# Strategy And Management Mechanics, States, And Events

Use this reference when specifying simulation-heavy Godot mechanics with NPCs,
customers, countries, factions, events, or user-generated content.

## Gameplay Structures

| Sample | Mechanic structure | Key design risk |
|---|---|---|
| Taiko Risshiden | Multi-system sandbox: map travel, relationship, mission, skills, combat, jobs, events. | Many systems can obscure the player's next useful goal. |
| Kairosoft-style tycoon | Lightweight decisions with automated agents and facility interactions. | Repetition if new facilities only increase numbers. |
| Plague Inc. | Macro strategy parameter tuning over a simulated world model. | One dominant build can collapse the strategy space. |

## State Machine Examples

### Customer Or Worker FSM

```text
Idle -> Enter -> ChooseTarget -> Walk -> UseFacility -> PayOrRate -> Leave
```

State contract:
- Entry condition.
- Per-tick behavior.
- Exit condition.
- Output event, such as `customer_paid`, `customer_unhappy`, or `facility_used`.

### Historical NPC / Faction FSM

```text
Idle -> Travel -> Train -> ExecuteMission -> Socialize -> Return
Peace -> PrepareWar -> March -> Siege -> Occupy -> Recover
Wanderer -> Retainer -> CastleLord -> Daimyo
```

Design notes:
- Separate personal state, faction state, and identity/state progression.
- Let simple independent rules create emergent stories.
- Do not make the player the only actor changing the world.

### Country / Global Response FSM

```text
Uninfected -> EarlyInfection -> Widespread -> BorderControls -> CureFocus -> Collapse
Undetected -> Detected -> Researching -> AcceleratedResearch -> CureComplete
```

Design notes:
- Each country can share the same FSM but use different parameters.
- Response triggers should come from thresholds: severity, deaths, region count,
  medical capacity, climate, wealth, or travel links.

## Event System Patterns

| Trigger type | Example |
|---|---|
| Time | Year, season, day count, management cycle, evaluation period. |
| Threshold | Popularity > 300, skill level reached, infection count passed. |
| Location | Player enters city, facility, country, or encounter area. |
| Relationship | NPC affinity, faction trust, reputation, rivalry. |
| World state | Castle captured, route closed, country infected, cure progress. |
| Random weighted event | Migration, scandal, contest invite, market shift, mutation. |

Event contract:

```text
Event id:
Trigger:
Preconditions:
Payload:
Player-facing feedback:
State changes:
Cooldown / one-shot rule:
Failure or fallback:
```

## Mod / Data-Driven Extension

Good mod targets:
- Characters, professions, facilities, customers, countries, diseases, traits.
- Event scripts and trigger conditions.
- Tuning tables, rewards, unlocks, maps, scenarios.
- Icons, portraits, UI skin, localized text.

Guardrails:
- Use stable IDs, not display names, for references.
- Keep event conditions inspectable.
- Separate authored content from runtime save data.
- Version data schemas before exposing them to players.

## Common Mistakes

- Encoding one-off story logic inside generic state machines.
- Letting events change many systems without an audit trail.
- Adding random events without weighting, cooldowns, or player-readable causes.
- Calling a system "emergent" when only scripted events can create change.
