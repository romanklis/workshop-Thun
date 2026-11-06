"""Cycle 2 cockpit: prepared fleet snapshot plus risk alerts."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from engine import assess_fleet_risk
from prep import build_fleet_snapshot
from repository import FleetRepository
from ui import (
    render_alerts,
    render_header,
    render_kpis,
    render_map,
    render_next_cycle,
    render_snapshot,
)

st.set_page_config(
    page_title="TransAlpine Cycle 2 Cockpit",
    layout="wide",
)


def main() -> None:
    render_header(
        "Cycle 2 — Risk Layer",
        2,
        "docs/architecture/cycle2.drawio",
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
    snapshot = build_fleet_snapshot(raw_readings, now)
    engine_ready = True
    try:
        alerts = assess_fleet_risk(raw_readings, now)
    except NotImplementedError:
        alerts = []
        engine_ready = False
    high_risk = sum(1 for alert in alerts if alert.risk_level == "CRITICAL")

    render_kpis(
        [
            ("Active Trucks", len(snapshot)),
            ("Monitored Routes", len(routes)),
            ("High-Risk Incidents", high_risk),
            ("Data Stage", 2),
        ]
    )

    st.subheader("Fleet Snapshot")
    render_snapshot(snapshot)

    st.subheader("Latest Truck Positions")
    render_map(hubs, [row.model_dump() for row in snapshot])

    st.subheader("Agentic Triage")
    if engine_ready:
        render_alerts(alerts)
    else:
        st.info(
            "Cycle 2 execution target: implement `engine.assess_fleet_risk()`."
        )
        st.markdown(
            "Use the rule table in `docs/plans/cycle2.md` and compare with "
            "branch `cycle-2-solution` after the demo checklist passes."
        )

    st.button(
        "Execute Emergency Triage",
        disabled=True,
        help="Unlocked in cycle-3.",
    )

    render_next_cycle(
        "Next starter: `cycle-3` for the dispatch operator. "
        "Reference answer: `cycle-2-solution`."
    )


if __name__ == "__main__":
    main()
