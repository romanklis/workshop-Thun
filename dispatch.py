"""Cycle 3 execution target: deterministic dispatch operator.

This module turns critical risk alerts into verified dispatch orders. It is the
current exercise on the Cycle 3 starter. The reference answer is on branch
``cycle-3-solution``.
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
        "Cycle 3: implement build_dispatch_order using docs/plans/cycle3.md. "
        "The reference answer is on branch cycle-3-solution."
    )


def evaluate_incident(
    alert: TriageAlert,
    latest: FleetSnapshotRow,
    history: list[dict],
    assignment: TruckAssignment | None,
) -> tuple[DispatchOrder, dict]:
    """Return the dispatch order and its decision trail."""

    raise NotImplementedError(
        "Cycle 3: implement evaluate_incident using docs/plans/cycle3.md. "
        "The reference answer is on branch cycle-3-solution."
    )
