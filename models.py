"""Core contracts for the reference TransAlpine solution."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TelemetryReading(BaseModel):
    truck_id: str
    cargo_type: str
    timestamp: str
    lat: float
    lon: float
    temp_c: float = Field(ge=-50, le=60)
    battery_pct: float = Field(ge=0, le=100)
    signal_status: str


class FleetSnapshot(BaseModel):
    truck_id: str
    cargo_type: str
    timestamp: str
    lat: float
    lon: float
    temp_c: float
    battery_pct: float
    signal_status: str
    readings_count: int
    minutes_silent: float
    home_hub: str
    shipment_id: str
    customer_id: str
    cargo_value_chf: float
    priority: str
    temp_max_c: float
    sla_deadline: str
    sla_penalty_chf: float


class TriageAlert(BaseModel):
    truck_id: str
    risk_level: str
    reason: str
    evidence: list[str]
    minutes_silent: float
    cargo_value_chf: float
    priority: str
    score: float


class DispatchOrder(BaseModel):
    truck_id: str
    action: str
    target_hub: str
    runway_min: float
    travel_min: float
    margin_min: float
    executive_summary: str
