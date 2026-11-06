"""Cycle 3 cockpit: risk alerts plus deterministic emergency dispatch."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from engine import assess_fleet_risk
from models import TruckAssignment
from dispatch import evaluate_incident
from prep import build_fleet_snapshot
from repository import FleetRepository
from ui import (
    render_alerts,
    render_dispatch,
    render_header,
    render_kpis,
    render_map,
    render_snapshot,
)

st.set_page_config(
    page_title="TransAlpine Cycle 3 Cockpit",
    layout="wide",
)


def main() -> None:
    render_header(
        "Cycle 3 — Autonomous Operator",
        3,
        "docs/architecture/cycle3.drawio",
    )

    repo = FleetRepository()
    try:
        hubs = repo.get_all_hubs()
        routes = repo.get_all_routes()
        raw_readings = repo.get_all_telemetry()
        assignment_rows = repo.get_all_assignments()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    snapshot = build_fleet_snapshot(raw_readings, now)
    alerts = assess_fleet_risk(raw_readings, now)
    high_risk = sum(1 for alert in alerts if alert.risk_level == "CRITICAL")

    render_kpis(
        [
            ("Active Trucks", len(snapshot)),
            ("Monitored Routes", len(routes)),
            ("High-Risk Incidents", high_risk),
            ("Data Stage", 3),
        ]
    )

    st.subheader("Fleet Snapshot")
    render_snapshot(snapshot)

    st.subheader("Latest Truck Positions")
    render_map(hubs, [row.model_dump() for row in snapshot])

    st.subheader("Agentic Triage")
    render_alerts(alerts)

    st.subheader("Emergency Operator")
    st.caption(
        "Execution target: dispatch.evaluate_incident(). "
        "Reference answer: branch `cycle-3-solution`."
    )
    if st.button("Execute Emergency Triage"):
        try:
            latest_by_truck = {row.truck_id: row for row in snapshot}
            assignments = {
                row["truck_id"]: TruckAssignment.model_validate(row)
                for row in assignment_rows
            }
            orders = []
            trail = []
            for alert in alerts:
                if alert.risk_level != "CRITICAL":
                    continue
                latest = latest_by_truck[alert.truck_id]
                history = repo.get_telemetry_for_truck(alert.truck_id)
                order, decision = evaluate_incident(
                    alert,
                    latest,
                    history,
                    assignments.get(alert.truck_id),
                )
                orders.append(order)
                trail.append(decision)
        except NotImplementedError:
            st.info(
                "Cycle 3 execution target: implement "
                "`dispatch.evaluate_incident()`."
            )
            st.markdown(
                "Use `docs/plans/cycle3.md` and compare with branch "
                "`cycle-3-solution` after the demo checklist passes."
            )
        else:
            render_dispatch(orders, trail)


if __name__ == "__main__":
    main()
