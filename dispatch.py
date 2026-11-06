"""Cycle 3 solution: deterministic dispatch operator."""

from __future__ import annotations

from pydantic import ValidationError

from models import (
    DispatchOrder,
    FleetSnapshotRow,
    TelemetryReading,
    TriageAlert,
    TruckAssignment,
)
from tools import (
    calculate_temp_rate_per_min,
    estimate_thermal_runaway_minutes,
    estimate_travel_minutes,
    find_emergency_depots,
)


def _valid_history(history: list[dict]) -> list[dict]:
    valid: list[dict] = []
    for raw in history:
        try:
            valid.append(TelemetryReading.model_validate(raw).model_dump())
        except ValidationError:
            continue
    return valid


def _assignment_text(assignment: TruckAssignment | None) -> str:
    if assignment is None:
        return "assignment UNASSIGNED"
    return (
        f"assignment {assignment.route_id} to {assignment.destination_hub}, "
        f"planned {assignment.planned_arrival}, "
        f"cargo {assignment.cargo_value_chf:.0f} CHF"
    )


def _evaluate(
    alert: TriageAlert,
    latest: FleetSnapshotRow,
    history: list[dict],
    assignment: TruckAssignment | None,
) -> tuple[DispatchOrder, dict]:
    valid_history = _valid_history(history)
    rate = calculate_temp_rate_per_min(valid_history)
    runway = estimate_thermal_runaway_minutes(latest.temp_c, rate)
    nearest = find_emergency_depots(latest.lat, latest.lon)[0]
    travel = estimate_travel_minutes(nearest["distance_deg"])
    margin = runway - travel
    action = (
        "DIVERT_TO_NEAREST_DEPOT"
        if margin > 0
        else "EMERGENCY_DIVERT"
    )
    summary = (
        f"{alert.truck_id} {alert.cargo_type} at {latest.temp_c} C. "
        f"Rate {rate:.3f} C/min, runway {runway:.1f} min. "
        f"Nearest {nearest['hub_id']} ({nearest['name']}), "
        f"travel {travel:.1f} min, margin {margin:.1f} min. "
        f"{_assignment_text(assignment)}."
    )
    order = DispatchOrder(
        truck_id=latest.truck_id,
        action=action,
        target_hub=nearest["hub_id"],
        estimated_margin_min=margin,
        executive_summary=summary,
    )
    trail = {
        "Truck": latest.truck_id,
        "Temp °C": latest.temp_c,
        "Rate °C/min": round(rate, 3),
        "Runway (min)": round(runway, 1),
        "Nearest Depot": nearest["name"],
        "Travel (min)": round(travel, 1),
        "Margin (min)": round(margin, 1),
        "Action": action,
        "Assignment": (
            "UNASSIGNED"
            if assignment is None
            else assignment.destination_hub
        ),
    }
    return order, trail


def build_dispatch_order(
    alert: TriageAlert,
    latest: FleetSnapshotRow,
    history: list[dict],
    assignment: TruckAssignment | None,
) -> DispatchOrder:
    """Turn a critical alert into a verified dispatch order."""

    return _evaluate(alert, latest, history, assignment)[0]


def evaluate_incident(
    alert: TriageAlert,
    latest: FleetSnapshotRow,
    history: list[dict],
    assignment: TruckAssignment | None,
) -> tuple[DispatchOrder, dict]:
    """Return the dispatch order and its auditable decision trail."""

    return _evaluate(alert, latest, history, assignment)
