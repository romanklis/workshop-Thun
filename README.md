# TransAlpine Logistics — Cycle 1 Reference Solution

> **SOLUTION BRANCH — Cycle 1**  
> This branch contains the completed baseline cockpit. For the exercise, return
> to `cycle-1` and design your own solution from the same datasources.

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

1. Loads the Stage 1 CSV sources through `repository.py`.
2. Cleans and validates telemetry, rejects corrupt packets, deduplicates, and
   selects the latest reading per truck in `prep.py`.
3. Joins cargo, customer SLA, and truck context.
4. Renders the fleet snapshot, map, and business exposure in `app.py` and
   `ui.py`.

The risk engine and dispatch operator are intentionally absent; they are
introduced on later cycles.

## Data sources

| File | Purpose |
|---|---|
| `dataset_metadata.csv` | Fixed scenario clock and stage |
| `hubs.csv` | Hubs, coordinates, capacity |
| `routes.csv` | Route network |
| `trucks.csv` | Truck and trailer master |
| `telemetry.csv` | Raw sensor readings with corrupt rows and duplicates |
| `cargo_manifest.csv` | Shipment, cargo value, temperature limits, priority |
| `customer_slas.csv` | Customer temperature limit, deadline, penalty |

## Reference design

- `docs/architecture.md` — Mermaid data flow and boundaries.
- `docs/plan.md` — plan and demo checklist.
- `models.py` — core Pydantic contracts.
- `prep.py` — cleaning, validation, grouping, and enrichment.
- `ui.py` / `app.py` — Streamlit cockpit.

## Demo answers

- Ten valid trucks appear after corrupt rows are rejected.
- The latest reading, silence, shipment, customer, value, and SLA are visible
  per truck.
- `TRUCK-44` is the highest-exposure PHARMA shipment.
- Risk scoring and dispatch deliberately arrive in later cycles.

## Branch map

| Branch | Role |
|---|---|
| `cycle-1` | Cycle 1 challenge starter |
| `cycle-1-solution` | **This branch** — reference baseline solution |
| `cycle-2`, `cycle-3` | Later challenge starters |
| `cycle-2-solution`, `cycle-3-solution` | Later reference solutions |

There are no automated tests; verify with the demo checklist and a manual app
run.
