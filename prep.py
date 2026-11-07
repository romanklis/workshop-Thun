"""Clean, validate, group, and enrich the fleet snapshot."""

from __future__ import annotations

import pandas as pd
from pydantic import ValidationError

from models import FleetSnapshot, TelemetryReading

CARGO_MAP = {
    "PHARMA": "PHARMA",
    "FRESH": "FRESH_FOOD",
    "FRESH_FOOD": "FRESH_FOOD",
    "STANDARD": "STANDARD",
}


def _cargo(value: object) -> str:
    return CARGO_MAP.get(str(value).strip().upper(), "STANDARD")


def _number(value: object, default: float = 0.0) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return default if pd.isna(result) else result


def _text(value: object) -> str:
    return "" if value is None or pd.isna(value) else str(value)


def build_snapshot(bundle: dict[str, pd.DataFrame], scenario: pd.Timestamp) -> list[FleetSnapshot]:
    """Return one cleaned, latest-state row per valid truck."""

    telemetry = bundle["telemetry"].copy()
    telemetry["timestamp"] = pd.to_datetime(telemetry["timestamp"], utc=True, errors="coerce")
    telemetry = telemetry.dropna(subset=["truck_id", "timestamp", "lat", "lon", "temp_c", "battery_pct"])
    telemetry["cargo_type"] = telemetry["cargo_type"].map(_cargo)

    valid: list[dict] = []
    for row in telemetry.to_dict("records"):
        row["timestamp"] = row["timestamp"].isoformat()
        try:
            valid.append(TelemetryReading.model_validate(row).model_dump())
        except ValidationError:
            continue
    if not valid:
        return []

    frame = pd.DataFrame(valid)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.drop_duplicates(subset=["truck_id", "timestamp", "temp_c", "battery_pct", "signal_status"])
    counts = frame.groupby("truck_id").size().rename("readings_count")
    latest = frame.sort_values("timestamp").groupby("truck_id", as_index=False).tail(1).merge(counts, on="truck_id")

    cargo = bundle["cargo"].copy()
    cargo["cargo_type"] = cargo["cargo_type"].map(_cargo)
    cargo = cargo.drop_duplicates(subset=["truck_id"], keep="last")
    cargo = cargo[["truck_id", "shipment_id", "customer_id", "cargo_type", "cargo_value_chf", "temp_max_c", "priority"]]

    slas = bundle["slas"].copy()
    slas = slas[["customer_id", "max_temp_c", "delivery_deadline", "penalty_chf_per_hour"]]
    trucks = bundle["trucks"][["truck_id", "home_hub"]]

    merged = latest.merge(cargo, on="truck_id", how="left", suffixes=("", "_cargo"))
    merged = merged.merge(slas, on="customer_id", how="left")
    merged = merged.merge(trucks, on="truck_id", how="left")

    rows: list[FleetSnapshot] = []
    for row in merged.to_dict("records"):
        cargo_type = _cargo(row.get("cargo_type_cargo", row.get("cargo_type")))
        temp_max = _number(row.get("temp_max_c"))
        if not temp_max:
            temp_max = _number(row.get("max_temp_c"), 8.0 if cargo_type == "PHARMA" else 6.0 if cargo_type == "FRESH_FOOD" else 30.0)
        silent = max(0.0, (scenario - row["timestamp"]).total_seconds() / 60)
        rows.append(
            FleetSnapshot(
                truck_id=_text(row["truck_id"]),
                cargo_type=cargo_type,
                timestamp=row["timestamp"].isoformat(),
                lat=_number(row["lat"]),
                lon=_number(row["lon"]),
                temp_c=_number(row["temp_c"]),
                battery_pct=_number(row["battery_pct"]),
                signal_status=_text(row.get("signal_status")),
                readings_count=int(row["readings_count"]),
                minutes_silent=round(silent, 1),
                home_hub=_text(row.get("home_hub")),
                shipment_id=_text(row.get("shipment_id")),
                customer_id=_text(row.get("customer_id")),
                cargo_value_chf=_number(row.get("cargo_value_chf")),
                priority=_text(row.get("priority")) or "STANDARD",
                temp_max_c=temp_max,
                sla_deadline=_text(row.get("delivery_deadline")),
                sla_penalty_chf=_number(row.get("penalty_chf_per_hour")),
            )
        )
    return sorted(rows, key=lambda item: item.truck_id)
