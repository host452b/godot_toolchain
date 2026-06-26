# Strategy And Management Audio Feedback Examples

Use this reference for non-action games where audio carries confirmation,
reward, warning, ambience, and system-state changes.

## Audio Role By Archetype

| Sample | Audio target | Useful cues |
|---|---|---|
| Taiko Risshiden | Historical atmosphere and social consequence. | Town, tea house, battle, rank, event, negotiation, training success/failure. |
| Kairosoft-style tycoon | Light, positive, short-loop reward feedback. | Coin, build, upgrade, customer happy/unhappy, contest, unlock, research. |
| Plague Inc. | Pressure, global escalation, and crisis. | Bubble pop, infection spread, cure alert, news item, country collapse, global warning. |

## Event Priority

| Priority | Examples | Handling |
|---|---|---|
| Critical | Cure breakthrough, bankruptcy, mission failure, outbreak detected. | Distinct cue, visual fallback, optional pause. |
| High | Unlock, rank up, contest result, new country infected. | Short sting, message, no masking. |
| Medium | Facility income, customer satisfaction, NPC relation change. | Variant cue, cooldown, can be batched. |
| Low | Ambient crowd, map movement, routine ticks. | Quiet loops, duck under important cues. |

## Audio Event Spec Additions

For simulation and management games, include:

```text
Event:
Meaning:
Priority:
Can overlap: yes/no
Cooldown:
Variant count:
Bus:
Visual fallback:
Can be muted without losing gameplay information:
```

## Mix Notes

- Keep routine reward sounds short and varied.
- Batch high-frequency income sounds into rhythmic groups.
- Give warning sounds a different shape from reward sounds, not only a louder volume.
- Use ambience to identify mode or location, but duck it under gameplay-critical cues.
- For map-driven games, let audio distinguish inspection, action, and world event.

## Common Mistakes

- Using the same confirm sound for build, unlock, warning, and failure.
- Letting high-frequency reward sounds fatigue the player.
- Making audio-only warnings for critical state changes.
- Adding music intensity without tying it to visible escalation.
