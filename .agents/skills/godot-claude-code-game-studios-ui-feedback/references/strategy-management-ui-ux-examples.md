# Strategy And Management UI/UX Examples

Use this reference for UI-heavy Godot games where the interface is the primary
control surface for simulation, strategy, or management.

## UI Role By Archetype

| Sample | UI role | Main pain |
|---|---|---|
| Taiko Risshiden | Navigates map, people, missions, skills, identity, diplomacy. | Deep information hierarchy and frequent menu/map switching. |
| Kairosoft-style tycoon | Shows facility state, cash flow, workers, customers, upgrades, unlocks. | Dense small-screen readability and too many simultaneous micro-events. |
| Plague Inc. | Makes an abstract global simulation legible. | Map, country detail, skill tree, cure progress, and alerts must stay coherent. |

## Interface-Driven Game Pattern

The player does not directly control a character. They control a system through:

```text
Dashboard -> inspect -> choose intervention -> see system response -> adjust
```

UI must therefore communicate:
- Current system state.
- Why it changed.
- What actions are available.
- What each action costs.
- What the likely consequence is.
- What just became urgent.

## Information Hierarchy

| Tier | Examples |
|---|---|
| Always visible | Money, time, core pressure, active objective, cure/progress meter. |
| Contextual | Facility detail, country stats, NPC relationship, selected action cost. |
| On demand | Full ledger, historical logs, detailed formulas, encyclopedia. |
| Alert only | Crisis events, contest results, disease discovery, major unlocks. |

## UI Concepts Worth Reusing

- Affordance: buttons, facilities, countries, and NPCs must show they can be inspected or acted on.
- Tooltip: explain the effect, cost, and condition without leaving the screen.
- UI flow: common loops need fewer clicks than rare management actions.
- Cognitive load: split large systems into views that answer one decision at a time.
- Feedback UI: after every action, show what changed and why.
- Readability: map overlays and tiny agents must still work at target resolution.

## UX Checks

- Can a new player find the next useful action in three minutes?
- Can players understand failure reasons without external guides?
- Are upgrades compared against current values?
- Are warnings color-independent?
- Can the player pause or slow time before making a high-stakes decision?
- Do modal windows interrupt automation only when the decision is meaningful?
