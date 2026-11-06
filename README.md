# TransAlpine Logistics: Cold-Chain Fleet Modernization

### Lean-AI-Dev Workshop | Plan → Architecture → Execute

> **CYCLE 3 STARTER →** `git checkout cycle-3`
>
> If you have not completed the earlier cycles, start on `cycle-1`. The
> completed Cycle 3 answer is on `cycle-3-solution`.

Welcome to the **TransAlpine Logistics** engineering strike team. Today you are
not a code typist; you are the **system architect and reviewer in chief**. The
workshop teaches organized AI-assisted development: write a plan, draw the
architecture, execute the planned slice, review the running app, then re-plan.

This branch is the **Cycle 3 starter**. Telemetry preparation and the risk
engine are complete; the dispatch operator is the current exercise.

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

### Cycle starters

| Branch | Role | Data stage | App |
|---|---|---|---|
| `cycle-1` | Cycle 1 starter | Stage 1 | `app_cycle1.py` |
| `main` | Default landing branch; mirrors `cycle-1` | Stage 1 | `app_cycle1.py` |
| `cycle-2` | Cycle 2 starter | Stage 2 | `app_cycle2.py` |
| `cycle-3` | **Current Cycle 3 starter** | Stage 3 | `app_cycle3.py` |

### Reference solutions

| Branch | Solved exercise |
|---|---|
| `cycle-1-solution` | Cycle 1 telemetry preparation |
| `cycle-2-solution` | Cycle 2 risk engine |
| `cycle-3-solution` | Cycle 3 dispatch operator |

Use a solution branch only to compare after the matching demo checklist passes.
Do not start the workshop there.

---

## Quickstart — Cycle 3

Run from the repository root.

### Windows PowerShell

```powershell
git checkout cycle-3
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle3.py
```

### macOS / Linux

```bash
git checkout cycle-3
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle3.py
```

`init_db.py` is repeatable. Rerun it before each demo to refresh the relative
timestamps; otherwise the seeded trucks will look stale.

---

## Plan → Architecture → Execute

Each cycle uses the same loop:

1. **Plan** — read `docs/plans/cycle3.md`.
2. **Architecture** — open `docs/architecture/cycle3.drawio` and trace the flow.
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

Stages 1 and 2 are completed history. Stage 3 is the current branch data and
adds route assignments for dispatch.

---

## Cycle 1 — Completed

`prep.build_fleet_snapshot()` validates packets, rejects corrupt rows, groups by
truck, selects the latest reading, counts readings, and computes silent minutes.

Reference solution: `cycle-1-solution`.

---

## Cycle 2 — Completed

`engine.assess_fleet_risk()` applies the PHARMA, FRESH_FOOD, and STANDARD risk
rules and returns one alert per valid truck, including LOW alerts.

Reference solution: `cycle-2-solution`.

---

## Cycle 3 — Current Exercise: Autonomous Operator

**Goal:** Turn critical risk alerts into verified dispatch orders with an
auditable decision trail.

**Execution target:** Implement `dispatch.evaluate_incident()` and
`dispatch.build_dispatch_order()` in `dispatch.py`.

**Operator formula:**

1. Take the latest prepared row and the truck's valid telemetry history.
2. Compute the temperature rate from the last two valid readings.
3. Compute runway minutes to `8.0 °C`.
4. Rank depots with `find_emergency_depots`.
5. Compute travel minutes to the nearest depot.
6. Compute margin = runway − travel.
7. Choose `DIVERT_TO_NEAREST_DEPOT` when margin is positive, otherwise
   `EMERGENCY_DIVERT`.
8. Include the assignment summary; use `UNASSIGNED` when no assignment exists.

Follow `docs/plans/cycle3.md` and open `docs/architecture/cycle3.drawio`.

**Demo checklist:**

- App launches with `streamlit run app_cycle3.py`.
- Prepared snapshot shows 16 valid trucks.
- Critical alerts are visible before dispatch.
- Clicking **Execute Emergency Triage** produces `DispatchOrder` rows after
  implementation.
- `TRUCK-44` routes to `HUB-OLTEN` with a positive margin.
- `TRUCK-58` is critical but unassigned; its summary shows `UNASSIGNED`.
- Standard cargo does not produce dispatch orders.
- The decision trail shows temperature rate, runway, nearest depot, travel,
  margin, and action.

**Reference solution:** branch `cycle-3-solution`.

---

## Repository Map

```text
workshop-Thun/
├── app_cycle1.py             # Completed Cycle 1 cockpit
├── app_cycle2.py             # Completed Cycle 2 cockpit
├── app_cycle3.py             # CURRENT: Cycle 3 cockpit
├── prep.py                   # COMPLETE: telemetry preparation
├── engine.py                 # COMPLETE: risk engine
├── dispatch.py               # CURRENT TARGET: dispatch operator
├── repository.py             # SQLite access layer
├── models.py                 # Contracts, including TruckAssignment
├── tools.py                  # Deterministic calculations
├── ui.py                     # Shared Streamlit rendering
├── seed_stage1.py            # Stage 1 seed history
├── seed_stage2.py            # Stage 2 seed history
├── seed_stage3.py            # Stage 3 seed data and assignments
├── init_db.py                # Rebuilds the Stage 3 database
├── docs/plans/README.md      # Plan-execute workflow
├── docs/plans/cycle1.md      # Completed Cycle 1 plan
├── docs/plans/cycle2.md      # Completed Cycle 2 plan
├── docs/plans/cycle3.md      # Current Cycle 3 plan
├── docs/architecture/        # All three Draw.io layouts
├── docs/slides.md            # Final workshop deck
├── AGENTS.md                 # Agent operating rules
└── data/logistics.db         # Committed Stage 3 snapshot
```

---

## Guardrails

- **Architecture first:** Read the Cycle 3 plan and layout before prompting.
- **Implement only Cycle 3:** Do not redo preparation or risk logic.
- **Deterministic math:** All numbers come from `tools.py`; no LLM arithmetic.
- **150-line cap:** Split seed data, UI helpers, or domain logic instead of
  growing monolithic files.
- **Compare by branch:** After the checklist passes, compare with
  `cycle-3-solution`. Do not import code from another branch.
- **No automated tests:** Verify with the manual demo checklist and architecture
  review. Do not add pytest or CI.

---

## Demo Data Notes

- **TRUCK-44** (`PHARMA`): rises to `7.4 °C`, battery `15%`, last signal
  `OFFLINE_LOST_SIGNAL` about 35 minutes ago near Egerkingen.
- **TRUCK-58** (`PHARMA`): about `6.9 °C`, about 25 minutes silent, and
  intentionally unassigned.
- **TRUCK-21** (`FRESH_FOOD`): warming to about `4.9 °C`.
- **TRUCK-99** (`STANDARD`): `19.5 °C`; warm is normal for dry goods.
- Stage 3 adds `TRUCK-121`, `TRUCK-131`, and 15 route assignments.
- **TRUCK-X1 / TRUCK-X2 / TRUCK-X3**: corrupt packets rejected by Pydantic.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Database not found` | Run `python init_db.py` from the repository root. |
| PowerShell blocks activation | Run `Set-ExecutionPolicy -Scope Process Bypass`, then activate again. |
| Dashboard shows stale times | Rerun `python init_db.py` and refresh the page. |
| Streamlit command not found | Activate the virtual environment or run `python -m streamlit run app_cycle3.py`. |
| Emergency Operator shows the target placeholder | Implement `dispatch.evaluate_incident()`; compare with `cycle-3-solution` afterward. |

The slide-by-slide workshop outline is in `docs/slides.md`. Render it with Marp
for 16:9 output, or read it as plain Markdown.
