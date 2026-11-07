# Cycle 3 Reference Solution Plan

## Goal

Deliver a working cold-chain command cockpit that turns Stage 3 CSV sources
into a prepared fleet snapshot, prioritized risk alerts, and auditable dispatch
recommendations.

## Data sources

The app loads every file in `datasources/` through `repository.py`. The scenario
clock comes from `dataset_metadata.csv`, so demos are deterministic.

Stage 3 adds `route_assignments.csv`, `depot_capacity.csv`, and
`traffic_conditions.csv` to the Stage 1–2 sources.

## Architecture

See `docs/architecture.md`.

- `repository.py` loads CSV tables and optional feeds.
- `prep.py` validates telemetry, rejects corrupt rows, groups by truck, selects
  the latest reading, and joins cargo, customer SLA, and truck context.
- `engine.py` combines thermal rules with driver, fuel, maintenance, sensor,
  outage, weather, and border evidence.
- `dispatch.py` evaluates critical alerts against depot capacity, traffic,
  driver hours, fuel range, and cargo/SLA context.
- `ui.py` renders the cockpit; `app.py` is the entry point.

## Demo checklist

- `streamlit run app.py` launches without exception.
- The snapshot contains 16 prepared trucks and excludes corrupt packets.
- Risk alerts are prioritized by risk, cargo value, priority, and SLA penalty.
- `TRUCK-44` and `TRUCK-58` are critical.
- Execute Emergency Triage produces dispatch orders and a decision trail.
- `TRUCK-58` is unassigned and is still handled.
- Every number in the decision trail comes from deterministic Python.

## Demo answers

- The highest-risk truck combines thermal exposure with cargo value and SLA.
- Evidence distinguishes telemetry from sensor, maintenance, outage, weather,
  driver, fuel, and border signals.
- Dispatch decisions show runway, travel, margin, capacity, driver, and fuel
  assumptions.
