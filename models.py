"""Pydantic contracts shared by the TransAlpine fleet platform."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

CargoType = Literal["PHARMA", "FRESH_FOOD", "STANDARD"]
RiskLevel = Literal["LOW", "MEDIUM", "CRITICAL"]


class Hub(BaseModel):
    """A fixed logistics hub in the Swiss network."""

    hub_id: str
    name: str
    lat: float
    lon: float


class TelemetryReading(BaseModel):
    """A single validated IoT sensor packet."""

    truck_id: str
    cargo_type: CargoType
    timestamp: str
    lat: float
    lon: float
    temp_c: float = Field(ge=-50, le=60)
    battery_pct: float = Field(ge=0, le=100)
    signal_status: str


class FleetSnapshotRow(BaseModel):
    """One prepared, latest-state row per truck for the cockpit."""

    truck_id: str
    cargo_type: CargoType
    latest_timestamp: str
    lat: float
    lon: float
    temp_c: float
    battery_pct: float
    signal_status: str
    readings_count: int
    minutes_silent: float


class TriageAlert(BaseModel):
    """Risk assessment produced for one truck."""

    truck_id: str
    cargo_type: CargoType
    risk_level: RiskLevel
    reason: str
    minutes_silent: float
    recommended_action: str


class DispatchOrder(BaseModel):
    """A verified remediation order produced by the autonomous operator."""

    truck_id: str
    action: str
    target_hub: str
    estimated_margin_min: float
    executive_summary: str
