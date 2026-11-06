# Cycle 1 Plan — Baseline Cockpit & Telemetry Preparation

> **Status:** Completed in Cycle 1. This branch stages Stage 2 data, so
> `app_cycle1.py` shows 14 trucks. Reference solution: `cycle-1-solution`.

## Goal

Build a runnable Streamlit cockpit that reads the raw Swiss fleet database and
prepares interleaved sensor packets for display. The starter branch `cycle-1`
begins with the preparation layer unimplemented; `prep.py` is implemented on
this branch.

## Data stage 1

- 4 hubs, 4 routes.
- 10 valid trucks with 4 readings each.
- 2 deliberately corrupt packets.
- 42 raw telemetry rows, interleaved in arrival order so grouping is required.

Key storylines:

- `TRUCK-44` is the high-value PHARMA exception: latest `7.4 °C`, battery `15%`,
  `OFFLINE_LOST_SIGNAL`, about 35 minutes silent.
- `TRUCK-58` is a second PHARMA warning: latest about `6.9 °C`, about 25 minutes
  silent.
- `TRUCK-21` is FRESH_FOOD warming toward `4.9 °C`.
- `TRUCK-99` is STANDARD at `19.5 °C`; warm is normal for dry goods.
- `TRUCK-X1` and `TRUCK-X2` contain impossible temperature/battery values.

## Architecture

Open `docs/architecture/cycle1.drawio`.

Flow: SQLite → `FleetRepository` → `prep.py` → `app_cycle1.py` → `ui.py`.
`engine.py` and `dispatch.py` are shown as dashed future layers; they are not
connected in this cycle.

## Connection points

- `repository.get_all_telemetry()` returns raw rows in arrival order.
- `prep.build_fleet_snapshot(readings, current_time_iso)` must return
  `list[FleetSnapshotRow]`.
- `app_cycle1.py` calls the preparation function and displays the result.
- Do not call `engine.py` or `dispatch.py` in Cycle 1.

## Execute

1. Read this plan and open the Cycle 1 architecture layout.
2. Implement `prep.build_fleet_snapshot()`:
   - validate every raw row with `TelemetryReading`;
   - skip `ValidationError` rows;
   - group valid packets by `truck_id`;
   - keep the latest timestamp per truck;
   - count valid packets per truck;
   - compute `minutes_silent` with `calculate_minutes_silent`;
   - return rows sorted by `truck_id`.
3. Wire the prepared table into `app_cycle1.py` if needed.
4. Run `python init_db.py`, then `streamlit run app_cycle1.py`.
5. Review the architecture and update the plan if reality differs.

## Review checklist

- App launches without an exception.
- Raw feed shows multiple readings per truck, not one row per truck.
- Raw map shows all raw points and looks noisy.
- Prepared panel shows exactly 10 truck rows after implementation.
- Every prepared row has `readings_count == 4`.
- `TRUCK-44` is `7.4 °C`, `15%`, `OFFLINE_LOST_SIGNAL`, about 35 minutes silent.
- `TRUCK-99` is `19.5 °C` and `STANDARD`.
- `TRUCK-X1` and `TRUCK-X2` are absent from the prepared snapshot.
- No duplicate truck rows.

## Out of scope

- Risk levels and alerts (Cycle 2).
- Dispatch orders and route assignments (Cycle 3).
- Automated tests.
