# Plan → Architecture → Execute

> **Solution branch:** Cycle 3 is complete. Return to `cycle-3` for the exercise,
> then compare the implementations.

This workshop is organized as repeated, reviewable cycles. Each cycle starts
with a written plan and an architecture layout, then executes only that slice.
Verification is a manual demo checklist; the repository intentionally contains
no automated test suite.

## The loop

1. **Plan** — read the cycle plan: goal, data stage, interfaces, and demo list.
2. **Architecture** — open the cycle Draw.io layout and trace the changed flow.
3. **Execute** — supervise the coding agent to implement only the planned slice.
4. **Review** — run the app, complete the demo checklist, and compare the branch.
5. **Re-plan** — record gaps before starting the next cycle.

## Cycle starters

| Branch | Role | Data stage | What it demonstrates |
|---|---|---|---|
| `cycle-1` | Cycle 1 starter | Stage 1 | Telemetry-preparation exercise |
| `main` | Default landing mirror | Stage 1 | Mirrors `cycle-1` |
| `cycle-2` | Cycle 2 starter | Stage 2 | Risk-engine exercise |
| `cycle-3` | **Current Cycle 3 starter** | Stage 3 | Dispatch-operator exercise |

## Reference solutions

| Branch | Solved exercise |
|---|---|
| `cycle-1-solution` | Cycle 1 telemetry preparation |
| `cycle-2-solution` | Cycle 2 risk engine |
| `cycle-3-solution` | **This branch** — Cycle 3 dispatch operator |

Start on `cycle-1`; `main` mirrors it. Compare with a solution branch only after
the matching demo checklist passes.

## Data stages

| Stage | Routes | Valid trucks | Readings per truck | Corrupt packets | Total packets | Assignments |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 10 | 4 | 2 | 42 | 0 |
| 2 | 8 | 14 | 8 | 3 | 115 | 0 |
| 3 | 10 | 16 | 10 | 3 | 163 | 15 |

Stages 1 and 2 are completed history. Stage 3 is current.

## Plans

- `cycle1.md` — completed baseline cockpit and data-preparation plan.
- `cycle2.md` — completed risk-engine plan.
- `cycle3.md` — completed dispatch-operator plan.

Before coding, read `AGENTS.md` and the current cycle plan. Keep every Python
file under 150 lines. Do not add automated tests; finish with the demo checklist.
