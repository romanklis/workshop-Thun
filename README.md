# TransAlpine Logistics: Cold-Chain Fleet Modernization

### Lean-AI-Dev Workshop | Plan → Architecture → Execute

> **CYCLE 2 STARTER →** `git checkout cycle-2`
>
> If you have not completed Cycle 1, start on `cycle-1`. The completed Cycle 2
> answer is on `cycle-2-solution`.

Welcome to the **TransAlpine Logistics** engineering strike team. Today you are
not a code typist; you are the **system architect and reviewer in chief**. The
workshop teaches organized AI-assisted development: write a plan, draw the
architecture, execute the planned slice, review the running app, then re-plan.

This branch is the **Cycle 2 starter**. Telemetry preparation from Cycle 1 is
already implemented; the risk engine is the current exercise.

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
| `cycle-2` | **Current Cycle 2 starter** | Stage 2 | `app_cycle2.py` |
| `cycle-3` | Next starter — dispatch operator | Stage 3 | `app_cycle3.py` |

### Reference solutions

| Branch | Solved exercise |
|---|---|
| `cycle-1-solution` | Cycle 1 telemetry preparation |
| `cycle-2-solution` | Cycle 2 risk engine |
| `cycle-3-solution` | Cycle 3 dispatch operator |

Use a solution branch only to compare after the matching demo checklist passes.
Do not start the workshop there.

---

## Quickstart — Cycle 2

Run from the repository root.

### Windows PowerShell

```powershell
git checkout cycle-2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle2.py
```

### macOS / Linux

```bash
git checkout cycle-2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
streamlit run app_cycle2.py
```

`init_db.py` is repeatable. Rerun it before each demo to refresh the relative
timestamps; otherwise the seeded trucks will look stale.

To inspect the completed Cycle 1 app on this branch:

```bash
streamlit run app_cycle1.py
```

It runs against the current Stage 2 data and shows 14 prepared trucks.

---

## Plan → Architecture → Execute

Each cycle uses the same loop:

1. **Plan** — read `docs/plans/cycle2.md`.
2. **Architecture** — open `docs/architecture/cycle2.drawio` and trace the flow.
3. **Execute** — supervise the coding agent to implement only the planned slice.
4. **Review** — run the app, complete the demo checklist, and inspect drift.
5. **Re-plan** — record gaps before moving to the next cycle.

`AGENTS.md` contains the operating rules for the coding agent.

---

## Data Stages

| Stage | Routes | Valid trucks | Readings per truck | Corrupt packets | Total packets |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 10 | 4 | 2 | 42 |
| 2 | 8 | 14 | 8 | 3 | 115 |

Stage 1 is the completed Cycle 1 baseline. Stage 2 is the current branch data.
Stage 3 is introduced on `cycle-3`.

---

## Cycle 1 — Completed

`prep.build_fleet_snapshot()` is implemented in `prep.py`. It validates raw
packets, rejects corrupt rows, groups by truck, selects the latest reading,
counts readings, and computes silent minutes.

The Cycle 1 reference answer is on `cycle-1-solution`. If you have not completed
the Cycle 1 exercise, start on `cycle-1`.

---

## Cycle 2 — Current Exercise: Risk Layer

**Goal:** Turn the prepared fleet snapshot into an operational risk view.

**Execution target:** Implement `engine.assess_fleet_risk()` in `engine.py`.
Use `prep.build_fleet_snapshot()` and return one `TriageAlert` per valid truck,
including LOW alerts.

| Cargo | Condition | Risk | Recommended action |
|---|---|---|---|
| PHARMA | `temp_c > 7.0` or (`minutes_silent > 20` and `temp_c > 5.0`) | `CRITICAL` | `DIVERT_TO_NEAREST_DEPOT` |
| PHARMA | `temp_c > 6.0` or `minutes_silent > 20` | `MEDIUM` | `NOTIFY_DRIVER` |
| PHARMA | otherwise | `LOW` | `MONITOR` |
| FRESH_FOOD | `temp_c > 6.0` | `CRITICAL` | `DIVERT_TO_NEAREST_DEPOT` |
| FRESH_FOOD | `temp_c > 4.0` | `MEDIUM` | `NOTIFY_DRIVER` |
| FRESH_FOOD | otherwise | `LOW` | `MONITOR` |
| STANDARD | any valid reading | `LOW` | `MONITOR` |

Follow `docs/plans/cycle2.md` and open `docs/architecture/cycle2.drawio`.

**Demo checklist:**

- App launches with `streamlit run app_cycle2.py`.
- Prepared snapshot shows exactly 14 valid trucks.
- One alert per valid truck after implementation.
- `TRUCK-44` is `CRITICAL`.
- `TRUCK-58` is `CRITICAL` (about `6.9 °C`, about 25 minutes silent).
- `TRUCK-21` is `MEDIUM` (FRESH_FOOD above `4.0 °C`).
- `TRUCK-99` is `LOW`.
- High-risk KPI matches the number of `CRITICAL` alerts.

**Reference solution:** branch `cycle-2-solution`.

**Next starter:** `cycle-3` for route assignments and the dispatch operator.
Its answer is on `cycle-3-solution`.

---

## Future Scaffolds on This Branch

These files exist as connection points for Cycle 3 and are not implemented here:

- `dispatch.py` — future dispatch-operator scaffold; both functions raise.
- `TruckAssignment` — future Cycle 3 contract in `models.py`.
- Dashed `dispatch` layer in `docs/architecture/cycle2.drawio`.

Do not implement or call them during Cycle 2.

---

## Repository Map

```text
workshop-Thun/
├── app_cycle1.py             # Completed Cycle 1 cockpit
├── app_cycle2.py             # CURRENT: Cycle 2 cockpit
├── prep.py                   # COMPLETE: telemetry preparation
├── engine.py                 # CURRENT TARGET: assess_fleet_risk()
├── dispatch.py               # Future scaffold: Cycle 3 dispatch operator
├── repository.py             # SQLite access layer
├── models.py                 # Contracts + future TruckAssignment
├── tools.py                  # Deterministic calculations
├── ui.py                     # Shared Streamlit rendering
├── seed_stage1.py            # Stage 1 seed history
├── seed_stage2.py            # Stage 2 seed data
├── init_db.py                # Rebuilds the Stage 2 database
├── docs/plans/README.md      # Plan-execute workflow
├── docs/plans/cycle1.md      # Completed Cycle 1 plan
├── docs/plans/cycle2.md      # Current Cycle 2 plan
├── docs/architecture/        # Cycle 1 and Cycle 2 Draw.io layouts
├── docs/slides.md            # Current workshop deck
├── AGENTS.md                 # Agent operating rules
└── data/logistics.db         # Committed Stage 2 snapshot
```

---

## Guardrails

- **Architecture first:** Read the Cycle 2 plan and layout before prompting.
- **Implement only Cycle 2:** Do not jump ahead to dispatch.
- **Contracts before syntax:** Reference `models.py` when asking for changes.
- **150-line cap:** Split seed data, UI helpers, or domain logic instead of
  growing monolithic files.
- **Compare by branch:** After the checklist passes, compare with
  `cycle-2-solution`. Do not import code from another branch.
- **No automated tests:** Verify with the manual demo checklist and architecture
  review. Do not add pytest or CI.

---

## Demo Data Notes

- **TRUCK-44** (`PHARMA`): rises to `7.4 °C`, battery `15%`, last signal
  `OFFLINE_LOST_SIGNAL` about 35 minutes ago near Egerkingen.
- **TRUCK-58** (`PHARMA`): about `6.9 °C`, about 25 minutes silent.
- **TRUCK-21** (`FRESH_FOOD`): warming to about `4.9 °C`.
- **TRUCK-99** (`STANDARD`): `19.5 °C`; warm is normal for dry goods.
- **TRUCK-X1 / TRUCK-X2 / TRUCK-X3**: corrupt packets rejected by Pydantic.
- Stage 2 adds `TRUCK-81`, `TRUCK-90`, `TRUCK-101`, and `TRUCK-111`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Database not found` | Run `python init_db.py` from the repository root. |
| PowerShell blocks activation | Run `Set-ExecutionPolicy -Scope Process Bypass`, then activate again. |
| Dashboard shows stale times | Rerun `python init_db.py` and refresh the page. |
| Streamlit command not found | Activate the virtual environment or run `python -m streamlit run app_cycle2.py`. |
| Triage panel shows the target placeholder | Implement `engine.assess_fleet_risk()`; compare with `cycle-2-solution` afterward. |

The slide-by-slide workshop outline is in `docs/slides.md`. Render it with Marp
for 16:9 output, or read it as plain Markdown.
