"""Reference Streamlit cockpit for the TransAlpine workshop."""

from __future__ import annotations

import streamlit as st

from prep import build_snapshot
from repository import load_bundle
from ui import render_alerts, render_header, render_kpis, render_map, render_orders, render_snapshot

try:
    from engine import assess_risk
except ImportError:
    assess_risk = None

try:
    from dispatch import build_orders
except ImportError:
    build_orders = None

st.set_page_config(page_title="TransAlpine Cold-Chain Command", layout="wide")


def main() -> None:
    stage = 3 if build_orders else 2 if assess_risk else 1
    render_header("Reference cockpit", stage, f"cycle-{stage}-solution")
    bundle, scenario = load_bundle()
    snapshot = build_snapshot(bundle, scenario)

    render_kpis(
        [
            ("Prepared Trucks", len(snapshot)),
            ("Raw Packets", len(bundle["telemetry"])),
            ("Hubs", len(bundle["hubs"])),
            ("Routes", len(bundle["routes"])),
        ]
    )
    st.caption(f"Scenario clock: {scenario.isoformat()}")

    st.subheader("Fleet Snapshot")
    render_snapshot(snapshot)
    st.subheader("Live Map")
    render_map(bundle["hubs"], snapshot)

    if assess_risk is None:
        st.info("The risk layer is introduced on the Cycle 2 branch.")
        return

    alerts = assess_risk(bundle, snapshot)
    high_risk = sum(1 for alert in alerts if alert.risk_level == "CRITICAL")
    st.subheader("Risk Alerts")
    st.metric("Critical Incidents", high_risk)
    render_alerts(alerts)

    if build_orders is None:
        st.info("The dispatch operator is introduced on the Cycle 3 branch.")
        return

    st.subheader("Emergency Operator")
    if st.button("Execute Emergency Triage"):
        orders, trail = build_orders(bundle, snapshot, alerts)
        render_orders(orders, trail)


if __name__ == "__main__":
    main()
