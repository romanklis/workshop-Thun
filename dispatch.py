"""Cycle 3 future scaffold: deterministic dispatch operator.

This module is not used in Cycle 2. It is a connection point for the next
cycle. Implement it only after completing the Cycle 2 risk engine.

The reference Cycle 3 answer is on branch ``cycle-3-solution``.
"""

from __future__ import annotations

from models import (
    DispatchOrder,
    FleetSnapshotRow,
    TriageAlert,
    TruckAssignment,
)


def build_dispatch_order(
    alert: TriageAlert,
    latest: FleetSnapshotRow,
    history: list[dict],
    assignment: TruckAssignment | None,
) -> DispatchOrder:
    """Return a verified dispatch order for a critical incident."""

    raise NotImplementedError(
        "Cycle 3 future scaffold: implement on the cycle-3 branch."
    )


def evaluate_incident(
    alert: TriageAlert,
    latest: FleetSnapshotRow,
    history: list[dict],
    assignment: TruckAssignment | None,
) -> tuple[DispatchOrder, dict]:
    """Return the dispatch order and its decision trail."""

    raise NotImplementedError(
        "Cycle 3 future scaffold: implement on the cycle-3 branch."
    )
