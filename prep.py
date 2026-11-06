"""Cycle 1 execution target: prepare raw telemetry for the cockpit.

The cockpit receives interleaved raw packets, including corrupt rows. This
module must turn that feed into one latest-state row per truck.

Implementation contract
-----------------------
1. Validate each raw dictionary with ``TelemetryReading`` and skip rows that
   raise ``ValidationError``.
2. Group valid packets by ``truck_id``.
3. Keep the latest packet by parsed timestamp.
4. Count the valid packets per truck.
5. Compute silence with ``calculate_minutes_silent`` and the supplied clock.
6. Return rows sorted by ``truck_id``.

See ``docs/plans/cycle1.md`` for the execution steps and demo checklist.
"""

from __future__ import annotations

from models import FleetSnapshotRow


def build_fleet_snapshot(
    readings: list[dict],
    current_time_iso: str,
) -> list[FleetSnapshotRow]:
    """Return one prepared latest-state row per valid truck."""

    raise NotImplementedError(
        "Cycle 1: implement build_fleet_snapshot using docs/plans/cycle1.md."
    )
