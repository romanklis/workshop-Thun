"""Shared Streamlit rendering for the reference solutions."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from models import DispatchOrder, FleetSnapshot, TriageAlert


def render_header(title: str, stage: int, solution: str) -> None:
    st.title("TransAlpine Logistics — Cold-Chain Command")
    st.caption(f"{title} | Data stage {stage} | Reference solution: `{solution}`")


def render_kpis(items: list[tuple[str, object]]) -> None:
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        column.metric(label, value)


def render_map(hubs: pd.DataFrame, rows: list[FleetSnapshot]) -> None:
    points = [{"lat": item["lat"], "lon": item["lon"]} for item in hubs.to_dict("records")]
    points.extend({"lat": row.lat, "lon": row.lon} for row in rows)
    if points:
        st.map(pd.DataFrame(points), zoom=7)


def render_snapshot(rows: list[FleetSnapshot]) -> None:
    if not rows:
        st.info("No valid telemetry rows.")
        return
    table = pd.DataFrame(
        [
            {
                "Truck": row.truck_id,
                "Cargo": row.cargo_type,
                "Temp °C": row.temp_c,
                "Limit °C": row.temp_max_c,
                "Battery %": row.battery_pct,
                "Signal": row.signal_status,
                "Silent min": row.minutes_silent,
                "Readings": row.readings_count,
                "Shipment": row.shipment_id,
                "Customer": row.customer_id,
                "Value CHF": row.cargo_value_chf,
                "Priority": row.priority,
            }
            for row in rows
        ]
    )
    st.dataframe(table, use_container_width=True, hide_index=True)


def render_alerts(alerts: list[TriageAlert]) -> None:
    if not alerts:
        st.info("No risk alerts.")
        return
    table = pd.DataFrame(
        [
            {
                "Truck": alert.truck_id,
                "Risk": alert.risk_level,
                "Score": alert.score,
                "Reason": alert.reason,
                "Evidence": "; ".join(alert.evidence) or "telemetry only",
                "Value CHF": alert.cargo_value_chf,
                "Priority": alert.priority,
            }
            for alert in alerts
        ]
    )
    st.dataframe(table, use_container_width=True, hide_index=True)


def render_orders(orders: list[DispatchOrder], trail: list[dict]) -> None:
    if not orders:
        st.info("No critical incident requires dispatch.")
        return
    st.dataframe(
        pd.DataFrame([order.model_dump() for order in orders]),
        use_container_width=True,
        hide_index=True,
    )
    if trail:
        st.caption("Decision trail")
        st.dataframe(pd.DataFrame(trail), use_container_width=True, hide_index=True)
