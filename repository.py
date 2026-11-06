"""SQLite access layer for the TransAlpine fleet cockpit."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

from models import Hub

DEFAULT_DB_PATH = Path(__file__).resolve().parent / "data" / "logistics.db"


class FleetRepository:
    """Read fleet data without leaking SQL into the UI or domain layer."""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found at {self.db_path}. "
                "Run `python init_db.py` first."
            )
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _fetch_all(
        self,
        query: str,
        params: tuple = (),
    ) -> list[dict]:
        with closing(self._connect()) as connection:
            rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def get_all_hubs(self) -> list[Hub]:
        """Return every seeded hub as a validated contract."""

        rows = self._fetch_all(
            "SELECT hub_id, name, lat, lon FROM hubs ORDER BY name"
        )
        return [Hub.model_validate(row) for row in rows]

    def get_all_telemetry(self) -> list[dict]:
        """Return raw telemetry in arrival order, including corrupt packets."""

        return self._fetch_all(
            "SELECT * FROM sensor_telemetry ORDER BY reading_id ASC"
        )

    def get_telemetry_for_truck(self, truck_id: str) -> list[dict]:
        """Return a truck's readings in chronological order."""

        return self._fetch_all(
            """
            SELECT *
            FROM sensor_telemetry
            WHERE truck_id = ?
            ORDER BY timestamp ASC, reading_id ASC
            """,
            (truck_id,),
        )

    def get_all_routes(self) -> list[dict]:
        """Return the seeded route network used by the cockpit KPI."""

        return self._fetch_all(
            """
            SELECT route_id, origin_hub, dest_hub, corridor,
                   standard_duration_min
            FROM routes
            ORDER BY route_id
            """
        )
