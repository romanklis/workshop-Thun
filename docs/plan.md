# Cycle 2 Reference Solution Plan

## Goal

Deliver a working cold-chain cockpit that turns Stage 2 CSV sources into a
prepared fleet snapshot and prioritized risk alerts with evidence.

## Data sources

The app loads every file in `datasources/` through `repository.py`. The scenario
clock comes from `dataset_metadata.csv`, so demos are deterministic.

Stage 2 adds driver shifts, sensor events, tunnel outages, maintenance logs,
weather, border queues, and fuel/charging telemetry to the Stage 1 data.

## Architecture

See `docs/architecture.md`.

- `repository.py` loads CSV tables and optional feeds.
- `prep.py` validates telemetry, rejects corrupt rows, groups by truck, selects
  the latest reading, and joins cargo, customer SLA, and truck context.
- `engine.py` combines thermal rules with driver, fuel, maintenance, sensor,
  outage, weather, and border evidence.
- `ui.py` renders the cockpit; `app.py` is the entry point.

## Demo checklist

- `streamlit run app.py` launches without exception.
- The snapshot contains 14 prepared trucks and excludes corrupt packets.
- Risk alerts are prioritized by risk, cargo value, priority, and SLA penalty.
- `TRUCK-44` and `TRUCK-58` are critical.
- The evidence column explains which sources contributed.
- Dispatch is intentionally out of scope on this branch.

## Demo answers

- The highest-risk truck combines thermal exposure with cargo value and SLA.
- Evidence distinguishes telemetry from sensor, maintenance, outage, weather,
  driver, fuel, and border signals.
- The dispatcher receives a ranked, explainable incident list.
