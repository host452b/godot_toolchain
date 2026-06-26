# Strategy And Management Economy Loop Examples

Use this reference when checking numbers for sandbox RPG strategy, tycoon
management, or macro simulation games.

## Economy Types

| Sample | Economy model | Core pressure |
|---|---|---|
| Taiko Risshiden | Matrix of personal stats, skills, money, merit, rank, relationships, faction resources. | Thresholds unlock new social and strategic power. |
| Kairosoft-style tycoon | Compact reinvestment economy with income, cost, popularity, staff, research, combos. | Frequent positive feedback and layout optimization. |
| Plague Inc. | Dynamic opposing variables: spread, severity, lethality, DNA, cure progress, country parameters. | Expansion produces resources while detection produces resistance. |

## Loop Patterns

### Threshold Unlock Loop

```text
Complete action -> gain skill/merit/relation -> pass threshold
-> unlock mission, role, negotiation, route, or event
```

Check:
- Are thresholds visible or learnable?
- Does crossing a threshold create new decisions, not just a title?
- Can low-stat routes still remain viable through different resources?

### Reinvestment Loop

```text
Money -> facility/staff/research -> throughput or appeal
-> more customers -> more money -> larger layout
```

Check:
- Payback time for each purchase.
- Marginal value of upgrade vs new build vs staff.
- Facility combo value and whether it dominates all alternatives.
- Late-game inflation and whether sinks keep money meaningful.

### Escalation / Opposition Loop

```text
Spread -> resource gain -> stronger traits
-> more visible threat -> opponent response
-> player adapts to delay, overwhelm, or redirect response
```

Check:
- Positive feedback: does early success snowball too hard?
- Negative feedback: does response create strategy or just punishment?
- Is stealth vs power a real tradeoff?
- Does each region or opponent parameter matter?

## Useful Metrics

| Metric | Use |
|---|---|
| Payback time | How long until a purchase returns its cost. |
| Resource faucet/sink ratio | Whether the economy inflates or starves. |
| Time to unlock | Whether progression pacing matches session length. |
| Dominance check | Whether one option is strictly better across all contexts. |
| Dead-zone duration | Time with no meaningful decision or reward. |
| Snowball rate | How quickly early advantage compounds. |
| Counter-pressure delay | Time between player success and system response. |

## Balance Report Additions

For these genres, add:

```text
Loop type: threshold | reinvestment | escalation | hybrid
Primary resource:
Primary sink:
Secondary resource:
Dominant strategy candidates:
Dead-zone risk:
One-more-turn hooks:
```

## Common Mistakes

- Tuning only the first 10 minutes and ignoring late-game inflation.
- Treating every unlock as equal even when some unlock new decision types.
- Giving combos multiplicative power without layout, time, or upkeep costs.
- Letting a cure/opposition meter be a timer instead of an interactive pressure.
