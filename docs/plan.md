# Cycle 1 Reference Solution Plan

## Goal

Deliver a working fleet-visibility cockpit that turns Stage 1 CSV sources into
a cleaned, latest-state snapshot with cargo and customer-SLA exposure.

## Data sources

The app loads every file in `datasources/` through `repository.py`. The scenario
clock comes from `dataset_metadata.csv`, so demos are deterministic.

Stage 1 contains hubs, routes, trucks, telemetry, cargo manifest, and customer
SLAs.

## Architecture

See `docs/architecture.md`.

- `repository.py` loads the CSV tables and scenario clock.
- `prep.py` validates telemetry, rejects corrupt rows, groups by truck, selects
  the latest reading, and joins cargo, customer SLA, and truck context.
- `ui.py` renders the cockpit; `app.py` is the entry point.

## Demo checklist

- `streamlit run app.py` launches without exception.
- The snapshot contains 10 prepared trucks and excludes corrupt packets.
- `TRUCK-44` shows 7.4 °C, 15% battery, and offline signal.
- Cargo value, priority, customer SLA, and silent minutes are visible.
- The risk engine and dispatch operator are intentionally out of scope.

## Demo answers

- The raw feed is noisy; the prepared snapshot is the trusted state.
- Corrupt packets are rejected before display.
- Business exposure is visible through cargo value and SLA context.
