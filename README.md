# TransAlpine Logistics: Cold-Chain Fleet Modernization

### Lean-AI-Dev Workshop | Plan → Architecture → Execute

Welcome to the **TransAlpine Logistics** engineering strike team. Today you are
not a code typist; you are the **system architect and reviewer in chief**. The
workshop teaches organized AI-assisted development: write a plan, draw the
architecture, execute the planned slice, review the running app, then re-plan.

The repository is deliberately split into three cumulative branches and three
growing data stages. Verification is by manual demo checklist, not an automated
test suite.

---

## The Business Context

TransAlpine Logistics manages cold-chain pharmaceutical and food transport
across the Swiss A1/A2 motorway network (Basel, Olten, Bern, Zurich).

- **The problem:** Pharma clients require certified real-time temperature
  tracking for sensitive medications and vaccines, with a maximum allowed limit
  of **+8.0 °C**.
- **The complication:** Swiss tunnels and topography create cellular blind
  spots. A silent truck with a failing compressor can spoil high-value cargo
  before anyone notices.
- **The mission:** Move from spreadsheets to a digital command cockpit with a
  risk layer and a deterministic dispatch operator.

---

## Branch Map

| Branch | Apps | Data stage | What works |
|---|---|---|---|
| `main` | `app_cycle1.py` | Stage 1 | Raw data access, noisy feed, architecture scaffold; `prep.py` is the execution target |
| `cycle-2` | `app_cycle1.py`, `app_cycle2.py` | Stage 2 | Prepared fleet snapshot and risk alerts |
| `cycle-3` | all three apps | Stage 3 | Deterministic operator, dispatch orders, decision trail |

All branches are published. Fork `main`, implement Cycle 1, then switch branches
to compare the later stages.

> **Current branch:** `cycle-3` — the full Cycle 3 reference solution. Run
> `streamlit run app_cycle3.py` after seeding the database.

---

## Quickstart — Cycle 1

Run from the repository root.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle1.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle1.py
```

`init_db.py` is repeatable. Rerun it before each demo to refresh the relative
timestamps; otherwise the seeded trucks will look stale.

### Cycle 2 quickstart on this branch

```bash
python init_db.py
streamlit run app_cycle2.py
```

`prep.py` and `engine.py` are already implemented here. Read
`docs/plans/cycle2.md` and `docs/architecture/cycle2.drawio` to review what was
executed.

### Cycle 3 quickstart on this branch

```bash
python init_db.py
streamlit run app_cycle3.py
```

`dispatch.py`, `tools.py`, and the route assignments are implemented on this
branch. Read `docs/plans/cycle3.md` and `docs/architecture/cycle3.drawio`.

---

## Plan → Architecture → Execute

Each cycle uses the same loop:

1. **Plan** — read `docs/plans/cycleN.md`: goal, data stage, interfaces, demo list.
2. **Architecture** — open `docs/architecture/cycleN.drawio` and trace the flow.
3. **Execute** — supervise the coding agent to implement only the planned slice.
4. **Review** — run the app, complete the demo checklist, and inspect drift.
5. **Re-plan** — record gaps before moving to the next cycle.

`AGENTS.md` contains the operating rules for the coding agent.

---

## Data Stages

| Stage | Routes | Valid trucks | Readings per truck | Corrupt packets | Total packets | Assignments |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 10 | 4 | 2 | 42 | 0 |
| 2 | 8 | 14 | 8 | 3 | 115 | 0 |
| 3 | 10 | 16 | 10 | 3 | 163 | 15 |

The data grows because the application needs more context each cycle: raw
snapshots for the cockpit, telemetry history for risk, then route assignments
for dispatch.

---

## Cycle 1: Baseline & Data Preparation

**Goal:** Understand the baseline, then prepare interleaved raw packets for
display.

**The trap:** The raw feed mixes multiple readings per truck and includes
corrupt packets. The baseline dispatcher view looks busy but does not tell you
which truck state is current.

**Execution target:** Implement `prep.build_fleet_snapshot()` in `prep.py`:

1. Validate each raw row with `TelemetryReading`.
2. Skip corrupt rows.
3. Group valid packets by `truck_id`.
4. Keep the latest timestamp per truck.
5. Count valid packets per truck.
6. Compute silent minutes with `calculate_minutes_silent`.
7. Return rows sorted by `truck_id`.

Follow `docs/plans/cycle1.md` and open `docs/architecture/cycle1.drawio`.
On this branch the Cycle 1 target is already implemented; use
`app_cycle1.py` to inspect the prepared result.

**Demo checklist:**

- App launches with `streamlit run app_cycle1.py`.
- Raw feed shows multiple readings per truck, not one row per truck.
- Raw map shows all raw points and looks noisy.
- Prepared panel shows exactly 10 trucks after implementation.
- `TRUCK-44` is `7.4 °C`, `15%`, `OFFLINE_LOST_SIGNAL`, about 35 minutes silent.
- `TRUCK-99` is `19.5 °C` and `STANDARD`.
- `TRUCK-X1` and `TRUCK-X2` are excluded from the prepared snapshot.
- No duplicate truck rows.

**Key question:** Everything looks green on the map. Is the fleet actually safe?

---

## Cycle 2: Risk Layer

Check out `cycle-2` and run:

```bash
python init_db.py
streamlit run app_cycle2.py
```

The branch implements `engine.assess_fleet_risk()` and adds the alert table.

| Cargo | Condition | Risk | Recommended action |
|---|---|---|---|
| PHARMA | `temp_c > 7.0` or (`minutes_silent > 20` and `temp_c > 5.0`) | `CRITICAL` | `DIVERT_TO_NEAREST_DEPOT` |
| PHARMA | `temp_c > 6.0` or `minutes_silent > 20` | `MEDIUM` | `NOTIFY_DRIVER` |
| PHARMA | otherwise | `LOW` | `MONITOR` |
| FRESH_FOOD | `temp_c > 6.0` | `CRITICAL` | `DIVERT_TO_NEAREST_DEPOT` |
| FRESH_FOOD | `temp_c > 4.0` | `MEDIUM` | `NOTIFY_DRIVER` |
| FRESH_FOOD | otherwise | `LOW` | `MONITOR` |
| STANDARD | any valid reading | `LOW` | `MONITOR` |

Expected demo: `TRUCK-44` and `TRUCK-58` are `CRITICAL`, `TRUCK-21` is `MEDIUM`,
and `TRUCK-99` remains `LOW`.

---

## Cycle 3: Autonomous Operator

Check out `cycle-3` and run:

```bash
python init_db.py
streamlit run app_cycle3.py
```

The branch adds route assignments, deterministic tools, and `dispatch.py`.
Click **Execute Emergency Triage** to generate `DispatchOrder` rows and inspect
the decision trail: temperature rate, runway, nearest depot, travel time, and
margin.

Expected demo: `TRUCK-44` routes to the Olten depot. `TRUCK-58` is critical but
has no route assignment, so its order summary shows `UNASSIGNED` without
crashing the app.

---

## Repository Map

```text
workshop-Thun/
├── app_cycle1.py             # Cycle 1 entry point (main)
├── app_cycle2.py             # Cycle 2 entry point (cycle-2+)
├── app_cycle3.py             # Cycle 3 entry point (cycle-3)
├── prep.py                   # Cycle 1 preparation target
├── engine.py                 # Cycle 2 risk target
├── dispatch.py               # Cycle 3 dispatch target (cycle-3)
├── repository.py             # SQLite access layer
├── models.py                 # Pydantic data contracts
├── tools.py                  # Deterministic calculations
├── ui.py                     # Shared Streamlit rendering
├── seed_stage1.py            # Stage 1 seed (main)
├── seed_stage2.py            # Stage 2 seed (cycle-2+)
├── seed_stage3.py            # Stage 3 seed (cycle-3)
├── init_db.py                # Rebuilds the current stage database
├── docs/plans/               # Plan-execute documents
├── docs/architecture/        # Per-cycle Draw.io layouts
├── docs/slides.md            # 9-slide workshop deck
├── AGENTS.md                 # Agent operating rules
└── data/logistics.db         # Committed stage snapshot
```

---

## Guardrails

- **Architecture first:** Read the cycle plan and layout before prompting.
- **One slice per execution:** Do not jump ahead to a later cycle.
- **Contracts before syntax:** Reference `models.py` when asking for changes.
- **150-line cap:** Split seed data, UI helpers, or domain logic instead of
  growing monolithic files.
- **No automated tests:** Verify with the plan's manual demo checklist and
  architecture review. Do not add pytest or CI.
- **Review the diff:** The agent writes syntax; you own the boundaries.

---

## Demo Data Notes

- **TRUCK-12** (`FRESH_FOOD`): nominal at approximately `3.2 °C`.
- **TRUCK-44** (`PHARMA`): rises to `7.4 °C`, battery `15%`, last signal
  `OFFLINE_LOST_SIGNAL` about 35 minutes ago near Egerkingen.
- **TRUCK-58** (`PHARMA`): about `6.9 °C`, about 25 minutes silent, unassigned
  in Stage 3.
- **TRUCK-99** (`STANDARD`): `19.5 °C`; warm is normal for dry goods.
- **TRUCK-X1 / TRUCK-X2**: deliberately corrupt packets that must be rejected
  by the Pydantic boundary.
- **TRUCK-21** (`FRESH_FOOD`): warming to about `4.9 °C`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Database not found` | Run `python init_db.py` from the repository root. |
| PowerShell blocks activation | Run `Set-ExecutionPolicy -Scope Process Bypass`, then activate again. |
| Dashboard shows stale times | Rerun `python init_db.py` and refresh the page. |
| Streamlit command not found | Activate the virtual environment or run `python -m streamlit run app_cycle1.py`. |
| App shows a `NotImplementedError` panel | That is the current cycle's execution target; read the matching plan. |

The slide-by-slide workshop outline is in `docs/slides.md`. Render it with Marp
for 16:9 output, or read it as plain Markdown.
