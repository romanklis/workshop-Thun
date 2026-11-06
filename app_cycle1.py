"""Cycle 1 cockpit: baseline data access and telemetry preparation."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from prep import build_fleet_snapshot
from repository import FleetRepository
from ui import (
    render_header,
    render_kpis,
    render_map,
    render_next_cycle,
    render_raw_feed,
    render_snapshot,
)

st.set_page_config(
    page_title="TransAlpine Cycle 1 Cockpit",
    layout="wide",
)


def main() -> None:
    render_header(
        "Cycle 1 — Baseline & Data Preparation",
        3,
        "docs/architecture/cycle1.drawio",
    )

    repo = FleetRepository()
    try:
        hubs = repo.get_all_hubs()
        routes = repo.get_all_routes()
        raw_readings = repo.get_all_telemetry()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    raw_truck_ids = {row["truck_id"] for row in raw_readings}

    render_kpis(
        [
            ("Raw Packets", len(raw_readings)),
            ("Raw Truck IDs", len(raw_truck_ids)),
            ("Hubs", len(hubs)),
            ("Routes", len(routes)),
        ]
    )

    st.subheader("Raw Telemetry Map")
    render_map(hubs, raw_readings)

    st.subheader("Raw Telemetry Feed")
    render_raw_feed(raw_readings, limit=20)

    st.subheader("Prepared Fleet Snapshot")
    try:
        snapshot = build_fleet_snapshot(raw_readings, now)
    except NotImplementedError as exc:
        st.info(f"Cycle 1 execution target: {exc}")
        st.markdown(
            "Implement `prep.build_fleet_snapshot()` by following "
            "`docs/plans/cycle1.md`. Group the raw packets by truck, keep the "
            "latest timestamp, skip corrupt rows, and compute silent minutes."
        )
    else:
        render_snapshot(snapshot)

    render_next_cycle(
        "Next: branch `cycle-2` adds the risk engine and `app_cycle2.py`."
    )


if __name__ == "__main__":
    main()
