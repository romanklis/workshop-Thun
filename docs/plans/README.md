# Plan → Architecture → Execute

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

## Branch map

| Branch | Apps | Data stage | What it demonstrates |
|---|---|---|---|
| `cycle-1` | `app_cycle1.py` | Stage 1 | **Start here** — baseline cockpit and telemetry preparation |
| `main` | `app_cycle1.py` | Stage 1 | Default landing branch; mirrors `cycle-1` |
| `cycle-2` | `app_cycle1.py`, `app_cycle2.py` | Stage 2 | Reference solution — prepared snapshot plus the risk engine |
| `cycle-3` | all three apps | Stage 3 | Reference solution — deterministic operator and dispatch trail |

All branches are published. Start on `cycle-1`; `main` mirrors it. Compare the
later branches only after completing the current cycle.

## Data stages

| Stage | Routes | Valid trucks | Readings per truck | Corrupt packets | Total packets | Assignments |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 10 | 4 | 2 | 42 | 0 |
| 2 | 8 | 14 | 8 | 3 | 115 | 0 |
| 3 | 10 | 16 | 10 | 3 | 163 | 15 |

The data grows with the application because each cycle needs more context:
raw snapshots, then telemetry history, then route assignments.

## Plans

- `cycle1.md` — baseline cockpit and data preparation.
- `cycle2.md` — risk engine (available on `cycle-2`).
- `cycle3.md` — autonomous operator (available on `cycle-3`).

Before coding, read `AGENTS.md` and the current cycle plan. Keep every Python
file under 150 lines. Do not add automated tests; finish with the demo checklist.
