# Cycle 2 Plan — Risk Layer

> **Status:** Completed on `cycle-2-solution`. The reference implementation is
> `engine.py`; the exercise starts on `cycle-2`.

## Goal

Turn the prepared fleet snapshot into an operational risk view. The preparation
layer from Cycle 1 is implemented, and this solution branch contains the
completed risk engine.

## Data stage 2

- 4 hubs, 8 routes.
- 14 valid trucks with 8 readings each.
- 3 deliberately corrupt packets.
- 115 raw telemetry rows.

Additions over Stage 1:

- `TRUCK-81` — PHARMA nominal.
- `TRUCK-90` — FRESH_FOOD warming.
- `TRUCK-101` — STANDARD nominal.
- `TRUCK-111` — PHARMA with a low-battery alarm.
- Routes `R-005` through `R-008`.

## Architecture

Open `docs/architecture/cycle2.drawio`.

Flow: SQLite → `FleetRepository` → `prep.py` → `engine.py` → `app_cycle2.py`
→ `ui.py`. `dispatch.py` remains a dashed future layer.

## Connection points

- `prep.build_fleet_snapshot()` is implemented on this branch.
- `engine.assess_fleet_risk(readings, current_time_iso)` returns one
  `TriageAlert` per valid truck.
- `app_cycle2.py` renders the prepared snapshot and the alert table.
- Do not call `dispatch.py` in Cycle 2.

## Risk rule table

| Cargo | Condition | Risk | Recommended action |
|---|---|---|---|
| PHARMA | `temp_c > 7.0` or (`minutes_silent > 20` and `temp_c > 5.0`) | `CRITICAL` | `DIVERT_TO_NEAREST_DEPOT` |
| PHARMA | `temp_c > 6.0` or `minutes_silent > 20` | `MEDIUM` | `NOTIFY_DRIVER` |
| PHARMA | otherwise | `LOW` | `MONITOR` |
| FRESH_FOOD | `temp_c > 6.0` | `CRITICAL` | `DIVERT_TO_NEAREST_DEPOT` |
| FRESH_FOOD | `temp_c > 4.0` | `MEDIUM` | `NOTIFY_DRIVER` |
| FRESH_FOOD | otherwise | `LOW` | `MONITOR` |
| STANDARD | any valid reading | `LOW` | `MONITOR` |

## Execute

1. Read this plan and open the Cycle 2 architecture layout.
2. Verify the completed `prep.build_fleet_snapshot()` from Cycle 1.
3. Implement `engine.assess_fleet_risk()` using the rule table on `cycle-2`.
4. Use `app_cycle2.py` to review the prepared snapshot and alerts.
5. Run `python init_db.py`, then `streamlit run app_cycle2.py`.
6. Review the architecture and update the plan if reality differs.

This solution branch contains the completed engine.

## Review checklist

- App launches without an exception.
- Exactly 14 valid trucks appear in the prepared snapshot.
- One alert per valid truck, including `LOW`.
- `TRUCK-44` is `CRITICAL`.
- `TRUCK-58` is `CRITICAL` (about `6.9 °C`, about 25 minutes silent).
- `TRUCK-21` is `MEDIUM` (FRESH_FOOD above `4.0 °C`).
- `TRUCK-99` is `LOW`.
- High-risk KPI matches the number of `CRITICAL` alerts.

## Out of scope

- Dispatch orders and route assignments (Cycle 3).
- Automated tests.
