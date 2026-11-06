"""Pure, deterministic calculations used by the fleet application."""

from __future__ import annotations

import math
from datetime import datetime, timezone

HUBS: list[dict] = [
    {
        "hub_id": "HUB-BASEL",
        "name": "Basel EuroAirport",
        "lat": 47.5596,
        "lon": 7.5886,
    },
    {
        "hub_id": "HUB-OLTEN",
        "name": "Olten Central Depot",
        "lat": 47.3499,
        "lon": 7.9033,
    },
    {
        "hub_id": "HUB-ZURICH",
        "name": "Zurich North",
        "lat": 47.3769,
        "lon": 8.5417,
    },
    {
        "hub_id": "HUB-BERN",
        "name": "Bern Wankdorf",
        "lat": 46.9480,
        "lon": 7.4474,
    },
]


def parse_iso(value: str) -> datetime:
    """Parse an ISO 8601 timestamp and normalize it to UTC."""

    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def calculate_minutes_silent(
    last_timestamp_iso: str,
    current_time_iso: str,
) -> float:
    """Return elapsed minutes between two timestamps, never negative."""

    elapsed = parse_iso(current_time_iso) - parse_iso(last_timestamp_iso)
    return max(0.0, elapsed.total_seconds() / 60.0)


def estimate_thermal_runaway_minutes(
    last_temp: float,
    rate_of_rise_per_min: float,
    critical_limit: float = 8.0,
) -> float:
    """Estimate minutes until cargo reaches the critical thermal limit.

    Returns zero when the limit is already reached, infinity when the cargo is
    not warming, and a deterministic linear projection otherwise.
    """

    if last_temp >= critical_limit:
        return 0.0
    if rate_of_rise_per_min <= 0:
        return math.inf
    return (critical_limit - last_temp) / rate_of_rise_per_min


def find_emergency_depots(
    current_lat: float,
    current_lon: float,
) -> list[dict]:
    """Rank Swiss hubs by rough Euclidean distance to a truck position."""

    scored = [
        (
            math.hypot(current_lat - hub["lat"], current_lon - hub["lon"]),
            hub,
        )
        for hub in HUBS
    ]
    scored.sort(key=lambda item: item[0])
    return [
        {**hub, "distance_deg": round(distance, 4)}
        for distance, hub in scored
    ]
