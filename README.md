# TransAlpine Logistics — Cycle 3 Reference Solution

> **SOLUTION BRANCH — Cycle 3**  
> This branch contains a complete reference implementation. For the exercise,
> return to `cycle-3` and design your own solution from the same datasources.

## Quickstart

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The app reads only `datasources/`; there is no database or seed step.

## What this reference does

1. Loads every CSV source through `repository.py`.
2. Cleans and validates telemetry, rejects corrupt packets, deduplicates, and
   selects the latest reading per truck in `prep.py`.
3. Joins cargo, customer SLA, and truck context.
4. Scores risk with thermal and operational evidence in `engine.py`.
5. Produces dispatch orders with runway, travel, margin, depot capacity, driver,
   and fuel checks in `dispatch.py`.
6. Renders the cockpit in `app.py` and `ui.py`.

## Data sources

Stage 3 contains Stage 1–2 sources plus dispatch context:

| Group | Files |
|---|---|
| Scenario | `dataset_metadata.csv` |
| Network | `hubs.csv`, `routes.csv`, `trucks.csv` |
| Telemetry | `telemetry.csv` |
| Commercial | `cargo_manifest.csv`, `customer_slas.csv` |
| Risk feeds | `driver_shifts.csv`, `sensor_events.csv`, `tunnel_outages.csv`, `maintenance_logs.csv`, `weather.csv`, `border_customs_queue.csv`, `fuel_charging_telemetry.csv` |
| Dispatch feeds | `route_assignments.csv`, `depot_capacity.csv`, `traffic_conditions.csv` |

The data deliberately contains duplicates, corrupt readings, stale records,
missing assignments, capacity conflicts, and inconsistent identifiers.

## Reference design

- `docs/architecture.md` — Mermaid data flow and boundaries.
- `docs/plan.md` — plan and demo checklist.
- `models.py` — core Pydantic contracts.
- `prep.py` — cleaning and enrichment.
- `engine.py` — risk and evidence.
- `dispatch.py` — deterministic operator.
- `ui.py` / `app.py` — Streamlit cockpit.

## Demo answers

- `TRUCK-44` and `TRUCK-58` are critical.
- Risk is prioritized by severity, cargo value, priority, and SLA penalty.
- Dispatch orders show the target depot, runway, travel, margin, driver hours,
  fuel range, and assignment context.
- `TRUCK-58` has no assignment and is explicitly reported as `UNASSIGNED`.

## Branch map

| Branch | Role |
|---|---|
| `cycle-3` | Cycle 3 challenge starter |
| `cycle-3-solution` | **This branch** — reference solution |
| `cycle-1`, `cycle-2` | Earlier challenge starters |
| `cycle-1-solution`, `cycle-2-solution` | Earlier reference solutions |

There are no automated tests; verify with the demo checklist and a manual app
run.
