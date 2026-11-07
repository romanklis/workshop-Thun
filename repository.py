"""Load the workshop CSV datasources into one data bundle."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "datasources"
OPTIONAL = {
    "driver_shifts": "driver_shifts.csv",
    "sensor_events": "sensor_events.csv",
    "tunnel_outages": "tunnel_outages.csv",
    "maintenance_logs": "maintenance_logs.csv",
    "weather": "weather.csv",
    "border_queues": "border_customs_queue.csv",
    "fuel": "fuel_charging_telemetry.csv",
    "assignments": "route_assignments.csv",
    "depots": "depot_capacity.csv",
    "traffic": "traffic_conditions.csv",
}


def _read(name: str) -> pd.DataFrame | None:
    path = DATA_DIR / name
    if not path.exists():
        return None
    return pd.read_csv(path)


def load_bundle() -> tuple[dict[str, pd.DataFrame], pd.Timestamp]:
    """Return all available source tables and the scenario clock."""

    meta = _read("dataset_metadata.csv")
    if meta is None or meta.empty:
        raise FileNotFoundError("datasources/dataset_metadata.csv is required")
    scenario = pd.to_datetime(meta.iloc[0]["scenario_now"], utc=True)

    bundle: dict[str, pd.DataFrame | None] = {
        "hubs": _read("hubs.csv"),
        "routes": _read("routes.csv"),
        "trucks": _read("trucks.csv"),
        "telemetry": _read("telemetry.csv"),
        "cargo": _read("cargo_manifest.csv"),
        "slas": _read("customer_slas.csv"),
    }
    for key, filename in OPTIONAL.items():
        bundle[key] = _read(filename)

    required = ("hubs", "routes", "trucks", "telemetry", "cargo", "slas")
    missing = [name for name in required if bundle[name] is None]
    if missing:
        raise FileNotFoundError(f"Missing required datasources: {missing}")

    return {key: value for key, value in bundle.items() if value is not None}, scenario
