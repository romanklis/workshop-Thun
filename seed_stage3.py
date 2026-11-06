"""Cycle 3 data stage: adds long telemetry history and route assignments."""

from __future__ import annotations

from datetime import datetime, timedelta

from seed_stage1 import HUBS, _p, build_rows
from seed_stage2 import (
    CORRUPT_PACKETS,
    ROUTES as BASE_ROUTES,
    TRUCK_PROFILES as BASE_PROFILES,
)

TRUCK_PROFILES = [
    {**profile, "readings": 10} for profile in BASE_PROFILES
] + [
    _p("TRUCK-121", "PHARMA", 10, 6, 4, 2.2, 2.4, 90, 86,
       47.38, 8.54, 47.56, 7.59),
    _p("TRUCK-131", "FRESH_FOOD", 10, 8, 5, 3.0, 3.4, 82, 78,
       46.95, 7.45, 47.56, 7.59),
]

ROUTES = BASE_ROUTES + [
    ("R-009", "HUB-BASEL", "HUB-BERN", "A2/A1", 95),
    ("R-010", "HUB-ZURICH", "HUB-OLTEN", "A1/A2", 65),
]

ASSIGNMENT_SPECS = [
    ("TRUCK-12", "R-001", "HUB-OLTEN", 45, 180000, "HIGH"),
    ("TRUCK-44", "R-001", "HUB-OLTEN", 50, 850000, "CRITICAL"),
    ("TRUCK-99", "R-004", "HUB-ZURICH", 80, 95000, "STANDARD"),
    ("TRUCK-07", "R-003", "HUB-BASEL", 70, 420000, "HIGH"),
    ("TRUCK-21", "R-009", "HUB-BERN", 95, 160000, "HIGH"),
    ("TRUCK-33", "R-002", "HUB-BERN", 45, 70000, "STANDARD"),
    ("TRUCK-66", "R-005", "HUB-ZURICH", 75, 190000, "HIGH"),
    ("TRUCK-71", "R-010", "HUB-OLTEN", 65, 300000, "HIGH"),
    ("TRUCK-88", "R-008", "HUB-BERN", 80, 65000, "STANDARD"),
    ("TRUCK-81", "R-003", "HUB-BASEL", 70, 500000, "HIGH"),
    ("TRUCK-90", "R-009", "HUB-BERN", 95, 140000, "HIGH"),
    ("TRUCK-101", "R-007", "HUB-OLTEN", 45, 60000, "STANDARD"),
    ("TRUCK-111", "R-010", "HUB-OLTEN", 65, 720000, "CRITICAL"),
    ("TRUCK-121", "R-003", "HUB-BASEL", 70, 900000, "CRITICAL"),
    ("TRUCK-131", "R-005", "HUB-ZURICH", 75, 150000, "HIGH"),
]


def generate(now: datetime) -> list[tuple]:
    """Return the Cycle 3 stage telemetry rows."""

    return build_rows(TRUCK_PROFILES, CORRUPT_PACKETS, now)


def generate_assignments(now: datetime) -> list[tuple]:
    """Return route assignments for every truck except TRUCK-58."""

    return [
        (
            truck_id,
            route_id,
            destination,
            (now + timedelta(minutes=plus_minutes)).isoformat(
                timespec="seconds"
            ),
            cargo_value,
            priority,
        )
        for (
            truck_id,
            route_id,
            destination,
            plus_minutes,
            cargo_value,
            priority,
        ) in ASSIGNMENT_SPECS
    ]
