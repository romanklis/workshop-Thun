"""Cycle 1 data stage: seeded hubs, routes, and raw pilot telemetry."""

from __future__ import annotations

from datetime import datetime, timedelta

HUBS = [
    ("HUB-BASEL", "Basel EuroAirport", 47.5596, 7.5886, 120),
    ("HUB-OLTEN", "Olten Central Depot", 47.3499, 7.9033, 80),
    ("HUB-ZURICH", "Zurich North", 47.3769, 8.5417, 150),
    ("HUB-BERN", "Bern Wankdorf", 46.9480, 7.4474, 90),
]

ROUTES = [
    ("R-001", "HUB-BASEL", "HUB-OLTEN", "A2/A1", 55),
    ("R-002", "HUB-OLTEN", "HUB-BERN", "A1", 45),
    ("R-003", "HUB-ZURICH", "HUB-BASEL", "A1/A3", 70),
    ("R-004", "HUB-BERN", "HUB-ZURICH", "A1", 80),
]


def _p(
    truck_id: str,
    cargo_type: str,
    readings: int,
    interval: int,
    last_min: int,
    temp_start: float,
    temp_end: float,
    battery_start: float,
    battery_end: float,
    lat_start: float,
    lon_start: float,
    lat_end: float,
    lon_end: float,
    last_signal: str = "OK",
) -> dict:
    return {
        "truck_id": truck_id,
        "cargo_type": cargo_type,
        "readings": readings,
        "interval_min": interval,
        "last_min": last_min,
        "temp_start": temp_start,
        "temp_end": temp_end,
        "battery_start": battery_start,
        "battery_end": battery_end,
        "lat_start": lat_start,
        "lon_start": lon_start,
        "lat_end": lat_end,
        "lon_end": lon_end,
        "last_signal": last_signal,
    }


TRUCK_PROFILES = [
    _p("TRUCK-12", "FRESH_FOOD", 4, 8, 2, 3.2, 3.2, 92, 88,
       47.48, 7.66, 47.41, 7.74),
    _p("TRUCK-44", "PHARMA", 4, 13, 35, 5.1, 7.4, 45, 15,
       47.36, 7.82, 47.322, 7.795, "OFFLINE_LOST_SIGNAL"),
    _p("TRUCK-99", "STANDARD", 4, 6, 3, 19.5, 19.5, 78, 76,
       46.96, 7.52, 46.95, 7.49),
    _p("TRUCK-07", "PHARMA", 4, 7, 4, 2.0, 2.5, 80, 76,
       47.38, 8.54, 47.56, 7.59),
    _p("TRUCK-21", "FRESH_FOOD", 4, 9, 5, 3.8, 4.9, 65, 60,
       47.56, 7.59, 46.95, 7.45),
    _p("TRUCK-33", "STANDARD", 4, 10, 6, 21.0, 21.2, 70, 68,
       47.35, 7.90, 46.95, 7.45),
    _p("TRUCK-58", "PHARMA", 4, 10, 25, 4.0, 6.9, 40, 18,
       47.35, 7.90, 47.38, 8.54, "OFFLINE_LOST_SIGNAL"),
    _p("TRUCK-66", "FRESH_FOOD", 4, 8, 2, 2.8, 2.9, 95, 92,
       46.95, 7.45, 47.56, 7.59),
    _p("TRUCK-71", "PHARMA", 4, 7, 3, 3.0, 3.1, 55, 52,
       47.38, 8.54, 47.35, 7.90),
    _p("TRUCK-88", "STANDARD", 4, 9, 4, 18.0, 18.2, 42, 40,
       47.56, 7.59, 47.38, 8.54),
]

CORRUPT_PACKETS = [
    (5, "TRUCK-X1", "PHARMA", 1, 47.0, 7.0, -999.0, -10.0),
    (23, "TRUCK-X2", "FRESH_FOOD", 3, 47.1, 7.2, 75.0, 140.0),
]


def _signal(index: int, count: int, last_signal: str) -> str:
    if index == count - 1:
        return last_signal
    if last_signal != "OK" and index == count - 2:
        return "DEGRADED"
    return "OK"


def _row(profile: dict, index: int, now: datetime) -> tuple:
    count = profile["readings"]
    fraction = index / (count - 1) if count > 1 else 0.0
    minutes_ago = profile["last_min"] + (count - 1 - index) * profile["interval_min"]
    return (
        profile["truck_id"],
        profile["cargo_type"],
        (now - timedelta(minutes=minutes_ago)).isoformat(timespec="seconds"),
        round(profile["lat_start"] + (profile["lat_end"] - profile["lat_start"]) * fraction, 4),
        round(profile["lon_start"] + (profile["lon_end"] - profile["lon_start"]) * fraction, 4),
        round(profile["temp_start"] + (profile["temp_end"] - profile["temp_start"]) * fraction, 1),
        round(profile["battery_start"] + (profile["battery_end"] - profile["battery_start"]) * fraction, 1),
        _signal(index, count, profile["last_signal"]),
    )


def build_rows(profiles: list[dict], corrupt: list[tuple], now: datetime) -> list[tuple]:
    """Build interleaved arrival-order rows so grouping is required."""

    max_count = max(profile["readings"] for profile in profiles)
    rows: list[tuple] = []
    for index in reversed(range(max_count)):
        for profile in profiles:
            if index < profile["readings"]:
                rows.append(_row(profile, index, now))

    for position, truck_id, cargo, minutes_ago, lat, lon, temp, battery in corrupt:
        row = (
            truck_id,
            cargo,
            (now - timedelta(minutes=minutes_ago)).isoformat(timespec="seconds"),
            lat,
            lon,
            temp,
            battery,
            "OK",
        )
        rows.insert(min(position, len(rows)), row)
    return rows


def generate(now: datetime) -> list[tuple]:
    """Return the Cycle 1 stage rows."""

    return build_rows(TRUCK_PROFILES, CORRUPT_PACKETS, now)
