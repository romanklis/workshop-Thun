# TransAlpine Logistics — Cycle 2 Reference Solution

> **SOLUTION BRANCH — Cycle 2**  
> This branch contains the completed risk layer. For the exercise, return to
> `cycle-2` and design your own solution from the same datasources.

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
5. Renders the cockpit in `app.py` and `ui.py`.

The dispatch operator is intentionally absent on this branch; it is introduced
on `cycle-3` and implemented on `cycle-3-solution`.

## Data sources

Stage 2 contains Stage 1 sources plus risk and commercial feeds:

| Group | Files |
|---|---|
| Scenario | `dataset_metadata.csv` |
| Network | `hubs.csv`, `routes.csv`, `trucks.csv` |
| Telemetry | `telemetry.csv` |
| Commercial | `cargo_manifest.csv`, `customer_slas.csv` |
| Risk feeds | `driver_shifts.csv`, `sensor_events.csv`, `tunnel_outages.csv`, `maintenance_logs.csv`, `weather.csv`, `border_customs_queue.csv`, `fuel_charging_telemetry.csv` |

The data deliberately contains duplicates, corrupt readings, stale records,
missing values, and inconsistent identifiers.

## Reference design

- `docs/architecture.md` — Mermaid data flow and boundaries.
- `docs/plan.md` — plan and demo checklist.
- `models.py` — core Pydantic contracts.
- `prep.py` — cleaning and enrichment.
- `engine.py` — risk and evidence.
- `ui.py` / `app.py` — Streamlit cockpit.

## Demo answers

- The risk table ranks incidents by severity, cargo value, priority, and SLA
  penalty.
- Evidence distinguishes telemetry from sensor, maintenance, outage, weather,
  driver, fuel, and border signals.
- `TRUCK-44` and `TRUCK-58` are critical.
- The dispatch operator is the next cycle.

## Branch map

| Branch | Role |
|---|---|
| `cycle-2` | Cycle 2 challenge starter |
| `cycle-2-solution` | **This branch** — reference risk solution |
| `cycle-1`, `cycle-3` | Other challenge starters |
| `cycle-1-solution`, `cycle-3-solution` | Other reference solutions |

There are no automated tests; verify with the demo checklist and a manual app
run.
