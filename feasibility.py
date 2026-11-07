"""Deterministic feasibility helpers for the dispatch reference."""

from __future__ import annotations

import math

import pandas as pd

from models import FleetSnapshot


def number(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return default if pd.isna(result) else result


def latest(df: pd.DataFrame | None, truck: str, time_column: str) -> dict | None:
    if df is None or df.empty or "truck_id" not in df.columns:
        return None
    subset = df[df["truck_id"] == truck].copy()
    if subset.empty:
        return None
    subset["_ts"] = pd.to_datetime(subset[time_column], utc=True, errors="coerce")
    return subset.sort_values("_ts").iloc[-1].to_dict()


def rate_of_rise(bundle: dict, truck: str) -> float:
    telemetry = bundle.get("telemetry")
    if telemetry is None or telemetry.empty:
        return 0.0
    subset = telemetry[telemetry["truck_id"] == truck].copy()
    subset["_ts"] = pd.to_datetime(subset["timestamp"], utc=True, errors="coerce")
    subset["temp_c"] = subset["temp_c"].apply(number)
    subset = subset[(subset["temp_c"] >= -50) & (subset["temp_c"] <= 60)].dropna(subset=["_ts"])
    subset = subset.sort_values("_ts")
    if len(subset) < 2:
        return 0.0
    first, last = subset.iloc[-2], subset.iloc[-1]
    minutes = (last["_ts"] - first["_ts"]).total_seconds() / 60
    return 0.0 if minutes <= 0 else (last["temp_c"] - first["temp_c"]) / minutes


def nearest_depot(bundle: dict, row: FleetSnapshot) -> tuple[dict | None, float]:
    depots = bundle.get("depots")
    hubs = bundle.get("hubs")
    if depots is None or hubs is None:
        return None, 0.0
    available = depots[depots["available_reefer_slots"].apply(number) > 0]
    merged = available.merge(hubs[["hub_id", "name", "lat", "lon"]], on="hub_id", how="left")
    if merged.empty:
        return None, 0.0
    merged["distance_km"] = merged.apply(
        lambda item: math.hypot(number(item["lat"]) - row.lat, number(item["lon"]) - row.lon) * 111,
        axis=1,
    )
    nearest = merged.sort_values("distance_km").iloc[0].to_dict()
    return nearest, number(nearest["distance_km"])


def operating_context(bundle: dict, row: FleetSnapshot) -> tuple[float, float, float, str]:
    traffic = bundle.get("traffic")
    speed = 70.0
    if traffic is not None and not traffic.empty:
        speeds = traffic["avg_speed_kmh"].apply(number)
        positive = speeds[speeds > 0]
        if not positive.empty:
            speed = float(positive.mean())
    shift = latest(bundle.get("driver_shifts"), row.truck_id, "shift_start")
    hours = number(shift.get("hours_remaining"), 99) if shift else 99
    fuel = latest(bundle.get("fuel"), row.truck_id, "timestamp")
    fuel_range = number(fuel.get("range_km"), 999) if fuel else 999
    assignment = latest(bundle.get("assignments"), row.truck_id, "planned_arrival")
    label = "UNASSIGNED"
    if assignment:
        label = f"{assignment.get('route_id')} to {assignment.get('destination_hub')}"
    return hours, fuel_range, speed, label
