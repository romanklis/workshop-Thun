# TransAlpine Logistics — Cycle 2 Challenge

### Risk Layer | Plan → Architecture → Execute

> **CYCLE 2 STARTER →** `git checkout cycle-2`
>
> If you have not completed Cycle 1, start on `cycle-1`. The completed Cycle 2
> reference answer is on `cycle-2-solution`.

## Your Challenge

The baseline cockpit answered “what is happening now.” New operational and
commercial feeds have arrived: driver shifts, sensor events, tunnel outages,
maintenance logs, weather, border queues, and fuel/charging telemetry.

Build a risk layer that turns this noisy, multi-source dataset into a
prioritized, explainable incident view. Distinguish real thermal or operational
risk from sensor noise and network blind spots. Rank incidents by cargo value,
customer SLA, and urgency.

You decide the architecture, data contracts, evidence model, and UI. Use AI to
plan and build, but you own the boundaries and the reasoning.

## What You Must Deliver

- A runnable application that reads directly from `datasources/`.
- A cleaned fleet snapshot and a prioritized risk feed with evidence.
- A clear explanation of why each alert exists and which sources contributed.
- A one-page plan and an architecture diagram created during the workshop.
- Answers to the demo questions below, backed by data.

## The Business Case

TransAlpine moves pharmaceuticals, fresh food, and dry goods across the Swiss
A1/A2 network. Pharma cargo must stay below **+8.0 °C**. Tunnels and congestion
create signal blind spots. A silent truck with a failing compressor can spoil
hundreds of thousands of Swiss francs of cargo before anyone notices.

The new feeds can clarify a real incident or create false alarms. Your risk
layer must earn the dispatcher's trust.

## Data Sources

All files are CSV. Timestamps are ISO 8601. The scenario clock is fixed in
`dataset_metadata.csv`; do not use the wall clock for silence calculations.

| File | Rows | What it contains | Known issues |
|---|---:|---|---|
| `dataset_metadata.csv` | 1 | Scenario time and stage | Use this as “now” |
| `hubs.csv` | 4 | Hub coordinates and capacity | — |
| `routes.csv` | 8 | Corridor, duration, distance | — |
| `trucks.csv` | 14 | Truck, cargo, carrier, trailer, home hub | — |
| `telemetry.csv` | 115 | Raw sensor packets | Duplicate IDs, out-of-order timestamps, corrupt values, missing signal |
| `cargo_manifest.csv` | 15 | Shipment, product, value, temperature limits, priority | Inconsistent cargo codes, missing batch ID, duplicate shipment |
| `customer_slas.csv` | 8 | Customer max temperature, deadline, penalty | Missing penalty and missing max temperature |
| `driver_shifts.csv` | 17 | Driver, shift window, hours remaining, contact status | Overlapping shifts, missing end time, negative hours |
| `sensor_events.csv` | 30 | Door, compressor, battery, signal events | Duplicate event IDs, unknown event type |
| `tunnel_outages.csv` | 12 | Outage windows and signal loss | Overlapping outages, stale open record |
| `maintenance_logs.csv` | 15 | Work orders, components, findings | Inconsistent component names, open and closed records |
| `weather.csv` | 40 | Hub/road temperature and conditions | Missing station, extreme outlier |
| `border_customs_queue.csv` | 12 | Border waits and queue lengths | Negative wait, unknown crossing |
| `fuel_charging_telemetry.csv` | 40 | Fuel/charge level, range, consumption | Negative range, missing fuel value, duplicate |

Key storylines:

- `TRUCK-44` (PHARMA) is at 7.4 °C, 15% battery, and offline.
- `TRUCK-58` (PHARMA) is around 6.9 °C and 25 minutes silent.
- `TRUCK-21` (FRESH_FOOD) is warming toward 4.9 °C.
- A tunnel outage and compressor event overlap with the pharma incidents.
- Some alerts will be false positives if you trust the wrong source.

## Constraints

- Pharma limit: **+8.0 °C**.
- Customer deadlines and penalties differ; rank incidents by business impact.
- The scenario clock is frozen; reports must be reproducible.
- Do not invent data to make a case look clean.
- Keep the solution runnable with the provided Python stack.

## Demo Questions

1. Which incidents are true risks versus noise?
2. What evidence supports each alert?
3. Which customer and cargo are prioritized first?
4. What would you tell the dispatcher to do next?

## Open Design Questions

- Which sources confirm or contradict a telemetry alert?
- How do you combine thermal and operational signals?
- How do you rank a high-value but medium-temperature shipment?
- How do you make evidence auditable without hiding assumptions?
- Where should risk logic stop and UI formatting begin?

## Branch Map

### Challenge starters

| Branch | Focus | Data stage |
|---|---|---|
| `cycle-1` | Baseline challenge | Stage 1 |
| `main` | Default mirror of `cycle-1` | Stage 1 |
| `cycle-2` | **Current risk challenge** | Stage 2 |
| `cycle-3` | Dispatch operator challenge | Stage 3 |

### Reference solutions

| Branch | Completed answer |
|---|---|
| `cycle-1-solution` | Baseline cockpit |
| `cycle-2-solution` | Risk layer |
| `cycle-3-solution` | Dispatch operator |

Use a solution branch only after your demo checklist passes.

## Setup

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

There is no application yet. You build it.

Suggested stack: Python, pandas, Pydantic, Streamlit.

## How to Work with AI

1. **Plan** — define the risk questions, data contracts, and demo checklist.
2. **Architecture** — draw the data flow and evidence boundaries.
3. **Execute** — build the smallest vertical slice that answers the demo questions.
4. **Review** — challenge every alert against the evidence and re-plan.

Create your own plan and architecture; do not copy a prewritten module list.

## Next Cycle

When the Cycle 2 checklist passes, check out `cycle-3` for the dispatch-operator
challenge. Route assignments, depot capacity, and traffic data arrive there.
