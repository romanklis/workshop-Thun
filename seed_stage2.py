"""Cycle 2 data stage: adds telemetry history, routes, and corrupt packets."""

from __future__ import annotations

from datetime import datetime

from seed_stage1 import (
    CORRUPT_PACKETS as BASE_CORRUPT,
    HUBS,
    ROUTES as BASE_ROUTES,
    TRUCK_PROFILES as BASE_PROFILES,
    _p,
    build_rows,
)

TRUCK_PROFILES = [
    {**profile, "readings": 8} for profile in BASE_PROFILES
] + [
    _p("TRUCK-81", "PHARMA", 8, 7, 3, 2.5, 2.7, 88, 84,
       47.38, 8.54, 47.56, 7.59),
    _p("TRUCK-90", "FRESH_FOOD", 8, 9, 4, 4.2, 5.2, 72, 66,
       47.56, 7.59, 46.95, 7.45, "DEGRADED"),
    _p("TRUCK-101", "STANDARD", 8, 8, 5, 20.0, 20.3, 60, 56,
       47.35, 7.90, 46.95, 7.45),
    _p("TRUCK-111", "PHARMA", 8, 10, 6, 3.5, 3.6, 25, 12,
       47.38, 8.54, 47.35, 7.90, "DEGRADED"),
]

ROUTES = BASE_ROUTES + [
    ("R-005", "HUB-BASEL", "HUB-ZURICH", "A3", 75),
    ("R-006", "HUB-OLTEN", "HUB-BASEL", "A2", 55),
    ("R-007", "HUB-BERN", "HUB-OLTEN", "A1", 45),
    ("R-008", "HUB-ZURICH", "HUB-BERN", "A1", 80),
]

CORRUPT_PACKETS = BASE_CORRUPT + [
    (57, "TRUCK-X3", "PHARMA", 2, 47.2, 7.3, -999.0, 50.0),
]


def generate(now: datetime) -> list[tuple]:
    """Return the Cycle 2 stage rows."""

    return build_rows(TRUCK_PROFILES, CORRUPT_PACKETS, now)
