"""Assess fleet risk from prepared telemetry.

Rule table
----------
PHARMA
    CRITICAL: temp_c > 7.0 OR (minutes_silent > 20 AND temp_c > 5.0)
    MEDIUM:   temp_c > 6.0 OR minutes_silent > 20
    LOW:      otherwise
FRESH_FOOD
    CRITICAL: temp_c > 6.0
    MEDIUM:   temp_c > 4.0
    LOW:      otherwise
STANDARD
    LOW:      always, for any valid reading
"""

from __future__ import annotations

from models import FleetSnapshotRow, TriageAlert
from prep import build_fleet_snapshot


def _classify(row: FleetSnapshotRow) -> tuple[str, str]:
    if row.cargo_type == "PHARMA":
        if row.temp_c > 7.0 or (
            row.minutes_silent > 20 and row.temp_c > 5.0
        ):
            return "CRITICAL", "DIVERT_TO_NEAREST_DEPOT"
        if row.temp_c > 6.0 or row.minutes_silent > 20:
            return "MEDIUM", "NOTIFY_DRIVER"
        return "LOW", "MONITOR"

    if row.cargo_type == "FRESH_FOOD":
        if row.temp_c > 6.0:
            return "CRITICAL", "DIVERT_TO_NEAREST_DEPOT"
        if row.temp_c > 4.0:
            return "MEDIUM", "NOTIFY_DRIVER"
        return "LOW", "MONITOR"

    return "LOW", "MONITOR"


def assess_fleet_risk(
    readings: list[dict],
    current_time_iso: str,
) -> list[TriageAlert]:
    """Return one triage alert per valid truck using the documented rules."""

    alerts: list[TriageAlert] = []
    for row in build_fleet_snapshot(readings, current_time_iso):
        risk_level, action = _classify(row)
        alerts.append(
            TriageAlert(
                truck_id=row.truck_id,
                cargo_type=row.cargo_type,
                risk_level=risk_level,
                reason=(
                    f"{row.cargo_type} at {row.temp_c} C after "
                    f"{row.minutes_silent:.1f} min "
                    f"({row.signal_status})"
                ),
                minutes_silent=row.minutes_silent,
                recommended_action=action,
            )
        )
    return alerts
