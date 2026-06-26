# Strategy And Management Vertical Slice Checkpoints

Use this reference when validating a slice for sandbox, tycoon, or systemic
strategy games.

## Slice Targets By Archetype

| Archetype | Minimum representative slice |
|---|---|
| Historical sandbox | One role, one town/region loop, several NPCs, one mission chain, one emergent world change. |
| Tycoon management | One facility category, one customer/staff loop, one upgrade path, one combo or contest, one expansion decision. |
| Systemic strategy | One complete escalation loop: spread/growth, resource gain, player tuning, opposition response, outcome. |

## Required Evidence

- Core loop can be completed without developer guidance.
- UI shows state, cause, cost, and next action.
- Numeric loop does not obviously stall or explode during the slice.
- Feedback makes rewards, warnings, and failures distinct.
- The slice demonstrates why this game is not just a menu or spreadsheet.
- Art/audio quality is representative where mood or readability is part of the promise.

## Report Additions

Add these sections to the normal vertical-slice report:

```text
Loop readability:
Economy stability:
Dominant strategy observed:
Information gaps:
One-more-turn hooks:
Systemic surprise or emergent moment:
Production content multiplier:
```

## PROCEED / PIVOT / KILL Signals

Proceed when:
- The loop is understandable and produces repeated voluntary decisions.
- Feedback and UI make the system legible.
- Content production scale looks feasible.

Pivot when:
- The fantasy works but the loop, economy, or UI does not support it yet.
- Players like a secondary interaction more than the intended core loop.
- The slice only works with developer explanation.

Kill when:
- The core loop remains passive after scope reduction.
- The best strategy is obvious and boring.
- The required content or simulation complexity is far beyond project scope.
