# Cycle 3 Plan — Autonomous Operator

> **Status:** Cycle 3 starter. Implement `dispatch.py`; the reference answer is
> on branch `cycle-3-solution`.

## Goal

Add a deterministic dispatch operator on top of the Cycle 2 risk layer. The
operator turns a critical alert into a verified `DispatchOrder` and exposes the
decision numbers to the dispatcher.

## Data stage 3

- 4 hubs, 10 routes.
- 16 valid trucks with 10 readings each.
- 3 deliberately corrupt packets.
- 163 raw telemetry rows.
- 15 route assignments; `TRUCK-58` is intentionally unassigned.

Additions over Stage 2:

- `TRUCK-121` — PHARMA high-value.
- `TRUCK-131` — FRESH_FOOD.
- Routes `R-009` and `R-010`.
- `truck_assignments` table with route, destination, planned arrival, cargo
  value, and priority.

## Architecture

Open `docs/architecture/cycle3.drawio`.

Flow: SQLite → `FleetRepository` → `prep.py` → `engine.py` → `dispatch.py` →
`tools.py` → `app_cycle3.py` → `ui.py`.

## Connection points

- `repository.get_all_assignments()` returns raw assignment rows.
- `dispatch.build_dispatch_order(alert, latest, history, assignment)` returns a
  `DispatchOrder`.
- `tools.calculate_temp_rate_per_min()` and `estimate_travel_minutes()` keep
  the math deterministic.
- `app_cycle3.py` runs the operator only for `CRITICAL` alerts.

## Operator formula

1. Take the latest prepared row and the truck's valid telemetry history.
2. Compute the temperature rate from the last two valid readings.
3. Compute runway minutes to `8.0 °C`.
4. Rank depots with `find_emergency_depots`.
5. Compute travel minutes to the nearest depot.
6. Compute margin = runway − travel.
7. Choose `DIVERT_TO_NEAREST_DEPOT` when margin is positive, otherwise
   `EMERGENCY_DIVERT`.
8. Include the assignment summary; use `UNASSIGNED` when no assignment exists.

## Execute

1. Read this plan and open the Cycle 3 architecture layout.
2. Add `TruckAssignment`, assignment access, and deterministic tools.
3. Implement `dispatch.build_dispatch_order()` on `cycle-3`.
4. Add `app_cycle3.py` and the dispatch-table helper.
5. Run `python init_db.py`, then `streamlit run app_cycle3.py`.
6. Click **Execute Emergency Triage** and review the decision trail.

## Review checklist

- App launches without an exception.
- 16 valid trucks appear in the prepared snapshot.
- Critical alerts produce `DispatchOrder` rows.
- `TRUCK-44` routes to `HUB-OLTEN` with a positive margin.
- `TRUCK-58` is critical and unassigned; its summary shows `UNASSIGNED`.
- Standard cargo does not produce dispatch orders.
- The decision trail shows temperature rate, runway, nearest depot, travel,
  margin, and action.

## Out of scope

- LLM prompt orchestration and live external systems.
- Automated tests.
