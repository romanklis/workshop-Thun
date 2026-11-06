"""Shared Streamlit rendering helpers for the cycle snapshots."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from models import FleetSnapshotRow, Hub, TriageAlert


def render_header(cycle: str, stage: int, architecture_path: str) -> None:
    st.title("TransAlpine Logistics — Cold-Chain Fleet Cockpit")
    st.caption(f"{cycle} | Data stage {stage} | Architecture: `{architecture_path}`")


def render_kpis(items: list[tuple[str, object]]) -> None:
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        column.metric(label, value)


def render_map(
    hubs: list[Hub],
    points: list[dict],
    zoom: int = 7,
) -> None:
    rows = [{"lat": hub.lat, "lon": hub.lon} for hub in hubs]
    rows.extend({"lat": point["lat"], "lon": point["lon"]} for point in points)
    if rows:
        st.map(pd.DataFrame(rows), zoom=zoom)
    else:
        st.info("No map points available.")


def render_raw_feed(rows: list[dict], limit: int = 20) -> None:
    if not rows:
        st.info("No raw telemetry packets available.")
        return
    display = rows[:limit]
    table = pd.DataFrame(
        [
            {
                "Reading": row["reading_id"],
                "Truck": row["truck_id"],
                "Cargo": row["cargo_type"],
                "Timestamp": row["timestamp"],
                "Temp °C": row["temp_c"],
                "Battery %": row["battery_pct"],
                "Signal": row["signal_status"],
            }
            for row in display
        ]
    )
    st.dataframe(table, use_container_width=True, hide_index=True)
    if len(rows) > limit:
        st.caption(f"Showing {limit} of {len(rows)} raw packets.")


def render_snapshot(snapshot: list[FleetSnapshotRow]) -> None:
    if not snapshot:
        st.info("No valid telemetry rows available.")
        return
    table = pd.DataFrame([row.model_dump() for row in snapshot])
    st.dataframe(table, use_container_width=True, hide_index=True)


def render_alerts(alerts: list[TriageAlert]) -> None:
    if not alerts:
        st.info("No triage alerts available.")
        return
    table = pd.DataFrame([alert.model_dump() for alert in alerts])
    st.dataframe(table, use_container_width=True, hide_index=True)


def render_next_cycle(message: str) -> None:
    st.info(message)
