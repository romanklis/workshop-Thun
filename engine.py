"""Cycle 2 execution target: assess fleet risk from prepared telemetry.

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

Implementation contract
-----------------------
Validate every raw dictionary with ``TelemetryReading``, skip corrupt rows,
select the latest reading per truck, and return exactly one ``TriageAlert`` per
valid truck, including LOW alerts.

See ``docs/plans/cycle2.md`` for the execution steps and demo checklist.
The reference answer is on branch ``cycle-2-solution``.
"""

from __future__ import annotations

from models import TriageAlert


def assess_fleet_risk(
    readings: list[dict],
    current_time_iso: str,
) -> list[TriageAlert]:
    """Return one triage alert per valid truck using the documented rules."""

    raise NotImplementedError(
        "Cycle 2: implement assess_fleet_risk using docs/plans/cycle2.md. "
        "The reference answer is on branch cycle-2-solution."
    )
