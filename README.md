# TransAlpine Logistics — Cycle 1 Challenge

### Cold-Chain Fleet Modernization | Plan → Architecture → Execute

> **START HERE →** `git checkout cycle-1`
>
> `main` mirrors this branch. The completed reference answer is on
> `cycle-1-solution`; use it only after your own demo checklist passes.

## Your Challenge

You are the engineering team for **TransAlpine Logistics**. Build a fleet
visibility cockpit from raw operational and commercial data.

The dispatcher cannot see which truck state is current, which sensor packets are
trustworthy, which shipments are exposed, or which customer SLAs are at risk.
You must turn the raw files in `datasources/` into a defensible, visual answer.

You decide the architecture, data contracts, cleaning strategy, and UI. Use AI to
plan and build, but you own the boundaries and the evidence.

## What You Must Deliver

- A runnable application that reads directly from `datasources/`.
- A cleaned, latest-state view per truck that rejects corrupt records.
- A map, fleet table, and business-exposure view for the dispatcher.
- A one-page plan and an architecture diagram created during the workshop.
- Answers to the demo questions below, backed by data.

## The Business Case

TransAlpine moves pharmaceuticals, fresh food, and dry goods across the Swiss
A1/A2 network. Pharma cargo must stay below **+8.0 °C**. Tunnels and congestion
create signal blind spots. A silent truck with a failing compressor can spoil
hundreds of thousands of Swiss francs of cargo before anyone notices.

Your cockpit is the first step: make the current fleet state and commercial
exposure visible before adding predictions or automation.

## Data Sources

All files are CSV. Timestamps are ISO 8601. The scenario clock is fixed in
`dataset_metadata.csv`; do not use the wall clock for silence calculations.

| File | Rows | What it contains | Known issues |
|---|---:|---|---|
| `dataset_metadata.csv` | 1 | Scenario time and stage | Use this as “now” |
| `hubs.csv` | 4 | Hub coordinates and capacity | — |
| `routes.csv` | 4 | Corridor, duration, distance | — |
| `trucks.csv` | 10 | Truck, cargo, carrier, trailer, home hub | — |
| `telemetry.csv` | 42 | Raw sensor packets | Duplicate IDs, out-of-order timestamps, corrupt temperature/battery, missing signal |
| `cargo_manifest.csv` | 10 | Shipment, product, value, temperature limits, priority | Inconsistent cargo codes, missing batch ID |
| `customer_slas.csv` | 6 | Customer max temperature, deadline, penalty | Missing penalty value |

Storylines to investigate:

- `TRUCK-44` (PHARMA) rises to 7.4 °C, battery drops to 15%, and the last packet
  is `OFFLINE_LOST_SIGNAL`.
- `TRUCK-58` (PHARMA) is around 6.9 °C and about 25 minutes silent.
- `TRUCK-21` (FRESH_FOOD) is warming toward 4.9 °C.
- `TRUCK-99` (STANDARD) is at 19.5 °C, which is normal for dry goods.
- Two packets contain impossible values.

## Constraints

- Pharma limit: **+8.0 °C**.
- Customer deadlines and penalties matter; not every warm truck has equal value.
- The scenario clock is frozen; reports must be reproducible.
- Do not invent data to make a case look clean.
- Keep the solution runnable with the provided Python stack.

## Demo Questions

1. Which truck is the highest business risk right now, and why?
2. Which telemetry records did you trust, and which did you reject?
3. Which shipment and customer SLA are exposed?
4. How does your app answer these questions without manual spreadsheet work?

## Open Design Questions

- What is the contract for a valid telemetry packet?
- How do you select the current state per truck?
- How do you handle duplicate or conflicting records?
- How do you join commercial context without double-counting shipments?
- What does the dispatcher need to see first?
- Where should data cleaning stop and UI formatting begin?

## Branch Map

### Challenge starters

| Branch | Focus | Data stage |
|---|---|---|
| `cycle-1` | **Current baseline challenge** | Stage 1 |
| `main` | Default mirror of `cycle-1` | Stage 1 |
| `cycle-2` | Risk layer challenge | Stage 2 |
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

Suggested stack: Python, pandas, Pydantic, Streamlit. You may add dependencies if
you justify them.

## How to Work with AI

1. **Plan** — define the problem, data contracts, and demo checklist.
2. **Architecture** — draw the data flow and component boundaries.
3. **Execute** — build the smallest vertical slice that answers the demo questions.
4. **Review** — inspect the data evidence, reject weak assumptions, and re-plan.

Create your own plan and architecture; do not copy a prewritten module list.

## Next Cycle

When the Cycle 1 checklist passes, check out `cycle-2` for the risk-layer
challenge. New datasources arrive there.
