"""Prepare raw telemetry for the fleet cockpit."""

from __future__ import annotations

from collections import defaultdict

from pydantic import ValidationError

from models import FleetSnapshotRow, TelemetryReading
from tools import calculate_minutes_silent, parse_iso


def build_fleet_snapshot(
    readings: list[dict],
    current_time_iso: str,
) -> list[FleetSnapshotRow]:
    """Return one prepared latest-state row per valid truck.

    Corrupt packets are rejected by the Pydantic boundary and never reach the
    grouped snapshot. Rows are sorted by truck ID for stable display.
    """

    grouped: dict[str, list[TelemetryReading]] = defaultdict(list)
    for raw in readings:
        try:
            reading = TelemetryReading.model_validate(raw)
        except ValidationError:
            continue
        grouped[reading.truck_id].append(reading)

    snapshot: list[FleetSnapshotRow] = []
    for truck_id in sorted(grouped):
        truck_readings = grouped[truck_id]
        latest = max(
            truck_readings,
            key=lambda reading: parse_iso(reading.timestamp),
        )
        snapshot.append(
            FleetSnapshotRow(
                truck_id=latest.truck_id,
                cargo_type=latest.cargo_type,
                latest_timestamp=latest.timestamp,
                lat=latest.lat,
                lon=latest.lon,
                temp_c=latest.temp_c,
                battery_pct=latest.battery_pct,
                signal_status=latest.signal_status,
                readings_count=len(truck_readings),
                minutes_silent=calculate_minutes_silent(
                    latest.timestamp,
                    current_time_iso,
                ),
            )
        )
    return snapshot
