---
name: godot-claude-code-game-studios-prototype-validation
description: Use when choosing how to prototype a Godot game concept, especially when deciding whether to validate rules, logic, moment-to-moment feel, input timing, or technical risk.
---

# Godot Prototype Validation

## Overview

A prototype answers one risky question. It is not a miniature production game.
Choose the prototype medium based on whether the question is about rules, logic,
feel, atmosphere, or engine feasibility.

## When To Use

- A Godot idea needs validation before full GDD or production work.
- The team is unsure whether to build an HTML, paper, or Godot prototype.
- A mechanic depends on input timing, physics, camera, animation, or tactile feel.
- A prototype is growing menus, save systems, polish, or architecture too early.

## Choose The Path

| Question | Prototype path | Why |
|---|---|---|
| Does this action feel good? | Godot engine | Native timing, physics, input, and camera matter. |
| Are these rules interesting? | Paper or spreadsheet | Fastest iteration for economy, cards, strategy, progression. |
| Is this logic understandable? | HTML or paper | Good for puzzle, menu, turn-based, and simple state machines. |
| Does the atmosphere work? | Godot engine | Rendering, audio, lighting, and camera carry the answer. |
| Can Godot handle this risk? | Godot spike | Test performance/API risk, not fun. |

Rule of thumb: "Does this feel right?" -> Godot. "Are these rules interesting?"
-> paper. "Is the logic clear?" -> HTML or paper.

## Prototype Rules

- Write the hypothesis before building:
  `"If the player does X, they will feel Y; we know it works if Z."`
- Test the riskiest assumption first, not the easiest one.
- Cut menus, save systems, long tutorials, full architecture, and cosmetic polish.
- If a Godot prototype is not playable after a short focused effort, reduce scope.
- Watch fresh players silently for feel tests; think-aloud is better for UI clarity.

## Godot Prototype Scope

Keep only what answers the question:

```markdown
Prototype: [name]
Question: [one risky assumption]
Path: Godot engine
Included: [one room, one enemy, one action, one feedback loop]
Cut: menus, progression, persistence, full art, production architecture
Success signal: [observable behavior or report]
Stop condition: [time limit or failed risk]
```

## References

- `references/strategy-management-prototype-questions.md` - prototype questions
  for sandbox, tycoon, and systemic strategy loops.

## Common Mistakes

- Using browser output to judge platformer or combat feel.
- Adding polish before the core hypothesis is answered.
- Testing yourself only and mistaking familiarity for clarity.
- Treating a throwaway prototype as production architecture.
- Asking "is it fun?" instead of a falsifiable question.
