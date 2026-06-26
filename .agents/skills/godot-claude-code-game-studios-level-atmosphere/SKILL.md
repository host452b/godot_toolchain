---
name: godot-claude-code-game-studios-level-atmosphere
description: Use when designing or reviewing a Godot level, area, biome, encounter space, atmosphere pass, wayfinding, landmarks, pacing, lighting, ambience, or signposting.
---

# Godot Level Atmosphere

## Overview

Level atmosphere is spatial design plus emotional arc. Layout, lighting, landmarks,
encounters, ambience, VFX, and accessibility must agree before production art is made.

## When To Use

- A Godot level or area needs mood, pacing, encounter placement, or navigation clarity.
- A level looks good but players get lost, miss objectives, or feel the wrong emotion.
- Lighting, ambience, VFX, worldbuilding, and gameplay layout need one shared spec.

## Level Brief

```markdown
## Area Brief
- Purpose:
- Emotional arc entering / during / leaving:
- Critical path:
- Optional paths:
- Landmarks:
- Pacing curve:
- Encounter beats:
- Lighting mood:
- Ambience and audio cues:
- VFX/weather:
- Accessibility risks:
```

## Godot Implementation Map

| Need | Godot tools | Notes |
|---|---|---|
| 2D layout | `Node2D`, `TileMapLayer`, `Area2D` triggers | Use collision and camera bounds early. |
| 3D layout | `Node3D`, `GridMap`, `CSG`, blockout meshes | Validate sightlines before decoration. |
| Navigation | `NavigationRegion2D/3D`, `NavigationAgent*` | Check critical path and AI movement separately. |
| Mood | `WorldEnvironment`, lights, color, fog, canvas effects | Lighting must support readability. |
| Landmarks | geometry, silhouettes, color, animation, sound cues | Do not rely on color alone. |
| Ambience | `AudioStreamPlayer2D/3D`, buses, area triggers | Layer base ambience, details, and one-shots. |
| VFX | particles, shaders, weather volumes | Keep readability and performance budgets explicit. |

## Pacing Pass

| Beat | Player state | Space type | Threat | Reward | Cue |
|---|---|---|---|---|---|
| Entrance | curiosity | wide reveal | low | landmark | lighting + ambience |
| First fight | tension | constrained arena | medium | skill check | enemy telegraph |
| Recovery | relief | safe pocket | none | resource | warm light + quiet mix |

## Accessibility Checks

- Critical path uses shape, icon, sound, motion, or landmark cues, not color only.
- Important silhouettes read at gameplay camera distance.
- Puzzle areas do not require holding too many simultaneous facts in memory.
- Combat spaces preserve contrast between enemy, hazard, reward, and background.
- Weather, particles, and post-processing do not hide hazards.

## Common Mistakes

- Letting art direction happen after layout, causing landmark and sightline conflicts.
- Filling the level with atmosphere that obscures gameplay information.
- Using one mood for the whole area instead of an emotional arc.
- Adding adjacent area references without documenting the connection.
- Shipping beautiful spaces with no tested critical path.

