# TransAlpine Logistics — Cycle 3 Challenge

### Autonomous Dispatch Operator | Plan → Architecture → Execute

> **CYCLE 3 STARTER →** `git checkout cycle-3`
>
> If you have not completed the earlier cycles, start on `cycle-1`. The
> completed Cycle 3 reference answer is on `cycle-3-solution`.

## Your Challenge

The risk view tells the dispatcher what is going wrong. Now they need a decision:
**can the cargo still reach a safe destination, and where should it go?**

New dispatch feeds have arrived: route assignments, depot capacity, traffic
conditions, and expanded driver/fuel context. Build an autonomous operator that
turns a critical alert into an auditable recommendation. Decide whether cargo can
reach a destination before spoiling, account for depot capacity, traffic, border
delays, driver hours, fuel range, customer SLA, and cargo value.

You decide the architecture, data contracts, tool boundaries, and UI. Use AI to
plan and build, but every number in the recommendation must be traceable to data
and deterministic code.

## What You Must Deliver

- A runnable application that reads directly from `datasources/`.
- A prioritized risk view plus an operator that produces dispatch recommendations.
- A decision trail showing runway, travel, margin, capacity, driver, and fuel.
- A one-page plan and an architecture diagram created during the workshop.
- Answers to the demo questions below, backed by data.

## The Business Case

TransAlpine moves pharmaceuticals, fresh food, and dry goods across the Swiss
A1/A2 network. Pharma cargo must stay below **+8.0 °C**. Tunnels, congestion,
border queues, driver limits, and depot capacity can turn a safe reroute into a
failed one. The dispatcher needs a recommendation with evidence, not a chatbot
guess.

## Data Sources

All files are CSV. Timestamps are ISO 8601. The scenario clock is fixed in
`dataset_metadata.csv`; do not use the wall clock for silence or runway.

| File | Rows | What it contains | Known issues |
|---|---:|---|---|
| `dataset_metadata.csv` | 1 | Scenario time and stage | Use this as “now” |
| `hubs.csv` | 4 | Hub coordinates and capacity | — |
| `routes.csv` | 10 | Corridor, duration, distance | — |
| `trucks.csv` | 16 | Truck, cargo, carrier, trailer, home hub | — |
| `telemetry.csv` | 163 | Raw sensor packets | Duplicate IDs, out-of-order timestamps, corrupt values |
| `cargo_manifest.csv` | 17 | Shipment, product, value, temperature limits, priority | Inconsistent cargo codes, missing batch ID, duplicate shipment |
| `customer_slas.csv` | 10 | Customer max temperature, deadline, penalty | Missing penalty and max temperature |
| `driver_shifts.csv` | 19 | Driver hours and contact status | Overlapping shifts, missing end time, negative hours |
| `sensor_events.csv` | 45 | Door, compressor, battery, signal events | Duplicate IDs, unknown event type |
| `tunnel_outages.csv` | 15 | Outage windows and signal loss | Overlapping outages, stale open record |
| `maintenance_logs.csv` | 20 | Work orders, components, findings | Inconsistent component names |
| `weather.csv` | 60 | Hub/road temperature and conditions | Missing station, extreme outlier |
| `border_customs_queue.csv` | 20 | Border waits and queues | Negative wait, unknown crossing |
| `fuel_charging_telemetry.csv` | 60 | Fuel/charge level, range, consumption | Negative range, missing fuel, duplicate |
| `route_assignments.csv` | 15 | Truck, route, destination, planned arrival, progress | Missing assignment, invalid route, past arrival |
| `depot_capacity.csv` | 4 | Dock/reefer capacity and occupancy | Zero availability, stale capacity |
| `traffic_conditions.csv` | 20 | Segment speed, delay, incident | Duplicate segment, negative speed/delay |

Key storylines:

- `TRUCK-44` is critical near the Olten corridor with a high-value pharma load.
- `TRUCK-58` is critical and intentionally has **no route assignment**.
- `HUB-ZURICH` has no available reefer slots.
- Border delays and a tunnel outage complicate travel-time assumptions.
- Some driver and fuel records conflict.

## Constraints

- Pharma limit: **+8.0 °C**.
- A feasible reroute needs runway > travel, depot reefer capacity, driver time,
  and sufficient fuel range.
- Customer deadlines and penalties differ; rank by business impact.
- The scenario clock is frozen; reports must be reproducible.
- Do not let an LLM do arithmetic in prose; use deterministic tools.
- Keep the solution runnable with the provided Python stack.

## Demo Questions

1. Where should the critical truck go, and can it arrive before spoilage?
2. Is the target depot feasible for this cargo and capacity?
3. What are the runway, travel time, and margin assumptions?
4. Why is the recommendation safe and auditable?
5. What happens when the assignment is missing or a depot is full?

## Open Design Questions

- Which calculations belong in deterministic tools?
- How do you model travel time with traffic, border, and tunnel data?
- How do you handle missing or conflicting assignments?
- How do you rank a long reroute against staying on plan?
- What does the dispatcher need to see to trust the recommendation?

## Branch Map

### Challenge starters

| Branch | Focus | Data stage |
|---|---|---|
| `cycle-1` | Baseline challenge | Stage 1 |
| `main` | Default mirror of `cycle-1` | Stage 1 |
| `cycle-2` | Risk-layer challenge | Stage 2 |
| `cycle-3` | **Current dispatch-operator challenge** | Stage 3 |

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

1. **Plan** — define the decision questions, data contracts, and demo checklist.
2. **Architecture** — draw the data flow, evidence boundaries, and tool boundaries.
3. **Execute** — build the smallest vertical slice that produces an auditable order.
4. **Review** — challenge every number and assumption, then re-plan.

Create your own plan and architecture; do not copy a prewritten module list.
