"""Reference dispatch operator using capacity, traffic, driver, and fuel data."""

from __future__ import annotations

from feasibility import nearest_depot, number, operating_context, rate_of_rise
from models import DispatchOrder, FleetSnapshot, TriageAlert


def build_orders(
    bundle: dict,
    snapshot: list[FleetSnapshot],
    alerts: list[TriageAlert],
) -> tuple[list[DispatchOrder], list[dict]]:
    """Build dispatch orders and decision trails for critical alerts."""

    by_truck = {row.truck_id: row for row in snapshot}
    orders: list[DispatchOrder] = []
    trail: list[dict] = []
    border = bundle.get("border_queues")
    border_wait = border["wait_min"].apply(number).max() if border is not None and not border.empty else 0

    for alert in alerts:
        if alert.risk_level != "CRITICAL":
            continue
        row = by_truck[alert.truck_id]
        rate = rate_of_rise(bundle, row.truck_id)
        if row.temp_c >= row.temp_max_c:
            runway = 0.0
        elif rate <= 0:
            runway = float("inf")
        else:
            runway = (row.temp_max_c - row.temp_c) / rate
        depot, distance = nearest_depot(bundle, row)
        hours, fuel_range, speed, assignment = operating_context(bundle, row)

        if depot is None:
            orders.append(
                DispatchOrder(
                    truck_id=row.truck_id,
                    action="ESCALATE",
                    target_hub="NONE",
                    runway_min=round(runway, 1),
                    travel_min=0.0,
                    margin_min=0.0,
                    executive_summary=f"{row.truck_id} critical; no depot has reefer capacity.",
                )
            )
            trail.append(
                {
                    "Truck": row.truck_id,
                    "Action": "ESCALATE",
                    "Assignment": assignment,
                    "Evidence": "; ".join(alert.evidence),
                }
            )
            continue

        travel = distance / speed * 60 + max(0.0, border_wait) * 0.1
        margin = runway - travel
        feasible = margin > 0 and hours >= 1 and fuel_range >= distance
        action = "DIVERT_TO_NEAREST_DEPOT" if feasible else "EMERGENCY_DIVERT"
        summary = (
            f"{row.truck_id} {row.cargo_type} at {row.temp_c} C; "
            f"limit {row.temp_max_c} C; rate {rate:.3f} C/min; "
            f"runway {runway:.1f} min; nearest {depot['name']} "
            f"{distance:.1f} km; travel {travel:.1f} min; margin {margin:.1f} min; "
            f"driver {hours:.1f} h; fuel range {fuel_range:.0f} km; "
            f"assignment {assignment}; cargo value {row.cargo_value_chf:.0f} CHF."
        )
        orders.append(
            DispatchOrder(
                truck_id=row.truck_id,
                action=action,
                target_hub=str(depot["hub_id"]),
                runway_min=round(runway, 1),
                travel_min=round(travel, 1),
                margin_min=round(margin, 1),
                executive_summary=summary,
            )
        )
        trail.append(
            {
                "Truck": row.truck_id,
                "Temp °C": row.temp_c,
                "Temp limit °C": row.temp_max_c,
                "Rate °C/min": round(rate, 3),
                "Runway (min)": round(runway, 1),
                "Nearest Depot": depot["name"],
                "Distance (km)": round(distance, 1),
                "Travel (min)": round(travel, 1),
                "Margin (min)": round(margin, 1),
                "Driver h": round(hours, 1),
                "Fuel range km": round(fuel_range, 0),
                "Assignment": assignment,
                "Action": action,
                "Evidence": "; ".join(alert.evidence),
            }
        )
    return orders, trail
