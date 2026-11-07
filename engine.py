"""Reference risk engine using telemetry plus the expanded datasources."""

from __future__ import annotations

import pandas as pd

from models import FleetSnapshot, TriageAlert

WEIGHT = {"LOW": 1, "MEDIUM": 2, "CRITICAL": 3}
PRIORITY = {"STANDARD": 0, "HIGH": 1, "CRITICAL": 2}


def _num(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return default if pd.isna(result) else result


def _latest_for(df: pd.DataFrame | None, truck: str, time_column: str) -> dict | None:
    if df is None or df.empty or "truck_id" not in df.columns:
        return None
    subset = df[df["truck_id"] == truck].copy()
    if subset.empty:
        return None
    if time_column in subset.columns:
        subset["_ts"] = pd.to_datetime(subset[time_column], utc=True, errors="coerce")
        subset = subset.sort_values("_ts")
    return subset.iloc[-1].to_dict()


def _thermal(row: FleetSnapshot) -> str:
    if row.cargo_type == "PHARMA":
        if row.temp_c > 7.0 or (row.minutes_silent > 20 and row.temp_c > 5.0):
            return "CRITICAL"
        return "MEDIUM" if row.temp_c > 6.0 or row.minutes_silent > 20 else "LOW"
    if row.cargo_type == "FRESH_FOOD":
        return "CRITICAL" if row.temp_c > 6.0 else "MEDIUM" if row.temp_c > 4.0 else "LOW"
    return "LOW"


def assess_risk(bundle: dict, snapshot: list[FleetSnapshot]) -> list[TriageAlert]:
    """Return prioritized alerts with evidence from every available source."""

    alerts: list[TriageAlert] = []
    events = bundle.get("sensor_events")
    maintenance = bundle.get("maintenance_logs")
    outages = bundle.get("tunnel_outages")
    weather = bundle.get("weather")
    shifts = bundle.get("driver_shifts")
    fuel = bundle.get("fuel")
    border = bundle.get("border_queues")

    for row in snapshot:
        evidence: list[str] = []
        severe = False

        if events is not None and not events.empty:
            truck_events = events[events["truck_id"] == row.truck_id]
            high = truck_events[truck_events["severity"].astype(str).str.upper() == "HIGH"]
            if not high.empty:
                evidence.append(f"{len(high)} high-severity sensor events")
                severe = True

        if maintenance is not None and not maintenance.empty:
            mine = maintenance[maintenance["truck_id"] == row.truck_id]
            open_jobs = mine[mine["status"].astype(str).str.upper() == "OPEN"]
            if not open_jobs.empty:
                evidence.append(f"{len(open_jobs)} open maintenance work orders")
                severe = True

        if outages is not None and not outages.empty:
            open_outages = outages[outages["status"].astype(str).str.upper() == "OPEN"]
            if not open_outages.empty:
                evidence.append(f"{len(open_outages)} open tunnel outages")

        if weather is not None and not weather.empty:
            hub_weather = weather[weather["hub_id"] == row.home_hub].copy()
            if not hub_weather.empty:
                hub_weather["_ts"] = pd.to_datetime(hub_weather["timestamp"], utc=True, errors="coerce")
                ambient = _num(hub_weather.sort_values("_ts").iloc[-1].get("ambient_temp_c"), 10)
                if ambient > 30 or ambient < -20:
                    evidence.append(f"extreme ambient temperature {ambient:.1f} C")

        latest_shift = _latest_for(shifts, row.truck_id, "shift_start")
        if latest_shift:
            hours = _num(latest_shift.get("hours_remaining"), 99)
            if hours < 2:
                evidence.append(f"driver hours remaining {hours:.1f}")
                severe = True

        latest_fuel = _latest_for(fuel, row.truck_id, "timestamp")
        if latest_fuel:
            fuel_range = _num(latest_fuel.get("range_km"), 999)
            if fuel_range < 100 or fuel_range < 0:
                evidence.append(f"fuel/charge range {fuel_range:.0f} km")
                severe = True

        if border is not None and not border.empty:
            max_wait = border["wait_min"].apply(_num).max()
            if max_wait > 60:
                evidence.append(f"border queue up to {max_wait:.0f} min")

        risk = _thermal(row)
        if severe and risk == "LOW":
            risk = "MEDIUM"
        elif severe and risk == "MEDIUM":
            risk = "CRITICAL"

        score = WEIGHT[risk] * 1_000_000
        score += row.cargo_value_chf + row.sla_penalty_chf * 100
        score += PRIORITY.get(row.priority.upper(), 0) * 10_000
        reason = f"{row.cargo_type} at {row.temp_c} C after {row.minutes_silent:.1f} min"
        alerts.append(
            TriageAlert(
                truck_id=row.truck_id,
                risk_level=risk,
                reason=reason,
                evidence=evidence,
                minutes_silent=row.minutes_silent,
                cargo_value_chf=row.cargo_value_chf,
                priority=row.priority,
                score=round(score, 1),
            )
        )
    return sorted(alerts, key=lambda alert: alert.score, reverse=True)
