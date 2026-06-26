# Interface-Driven Game Feel And Juice Examples

Use this reference for strategy, management, and simulation games where feel comes
from UI response, animation rhythm, audio, numbers, and system visualization.

## Feel Sources By Archetype

| Sample | Feel target | Feedback sources |
|---|---|---|
| Taiko Risshiden | Immersive life-in-world feel. | Map travel cadence, dialog speed, event frequency, minigame response, rank/relationship feedback. |
| Kairosoft-style tycoon | Busy, cheerful, constantly rewarding feel. | Tiny agents moving, coin ticks, satisfaction bubbles, upgrade flashes, unlock popups. |
| Plague Inc. | Macro control and system collapse feel. | Bubble pops, map color spread, infection counters, news ticker, cure alerts, world state changes. |

## Strategy Game Feel Checklist

- The first response to a click or decision appears immediately.
- Numeric changes are visible without requiring a menu dive.
- The player can feel a system accelerating or slowing down.
- Important warnings have a distinct rhythm, color-independent cue, and sound.
- Fast-forward, pause, and tick speed changes preserve readability.
- Popups do not interrupt the loop more often than they reward it.

## Juice Event Matrix

| Event | Visual | Audio | Timing | Risk |
|---|---|---|---|---|
| Facility earns money | Floating number, short bounce, small sparkle. | Soft coin tick with variation. | Immediate or batched rhythmically. | Too noisy when many facilities fire. |
| New combo discovered | Highlight involved objects, line or pulse between them. | Bright confirm cue. | After player action, before next decision. | Hiding the mechanical reason. |
| Infection reaches new country | Map color bloom, country flash, counter jump. | Low alert or spread cue. | Synchronized with message. | Too much alarm for routine growth. |
| Rank or identity change | Badge animation, title card, new menu affordance. | Promotion sting. | Short ceremony, then control returns. | Blocking frequent play. |

## Feel Acceptance Criteria Examples

- Players notice income sources without opening a finance panel.
- Players can identify the next useful action after an unlock.
- Players describe the world as "busy" or "alive" without being overwhelmed.
- Players can distinguish reward, warning, and failure cues by sound or motion.
- Players do not miss critical system changes while using fast-forward.

## Common Mistakes

- Adding particles to every event instead of giving events hierarchy.
- Showing numbers without explaining what caused them.
- Making macro simulations feel passive because the map changes too slowly.
- Using long modal rewards that break the "one more action" cadence.
