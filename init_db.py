"""Create and seed the local SQLite database for the workshop."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

import seed_stage3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "logistics.db"

SCHEMA = """
DROP TABLE IF EXISTS truck_assignments;
DROP TABLE IF EXISTS sensor_telemetry;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS hubs;

CREATE TABLE hubs (
    hub_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE routes (
    route_id TEXT PRIMARY KEY,
    origin_hub TEXT NOT NULL,
    dest_hub TEXT NOT NULL,
    corridor TEXT NOT NULL,
    standard_duration_min INTEGER NOT NULL
);

CREATE TABLE sensor_telemetry (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    truck_id TEXT NOT NULL,
    cargo_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    temp_c REAL NOT NULL,
    battery_pct REAL NOT NULL,
    signal_status TEXT NOT NULL
);

CREATE TABLE truck_assignments (
    truck_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    destination_hub TEXT NOT NULL,
    planned_arrival TEXT NOT NULL,
    cargo_value_chf REAL NOT NULL,
    priority TEXT NOT NULL
);
"""


def init_db() -> None:
    """Rebuild the database with the current cycle's data stage."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    telemetry_rows = seed_stage3.generate(now)
    assignment_rows = seed_stage3.generate_assignments(now)

    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.executescript(SCHEMA)
        connection.executemany(
            "INSERT INTO hubs VALUES (?, ?, ?, ?, ?)",
            seed_stage3.HUBS,
        )
        connection.executemany(
            "INSERT INTO routes VALUES (?, ?, ?, ?, ?)",
            seed_stage3.ROUTES,
        )
        connection.executemany(
            """
            INSERT INTO sensor_telemetry
                (truck_id, cargo_type, timestamp, lat, lon,
                 temp_c, battery_pct, signal_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            telemetry_rows,
        )
        connection.executemany(
            """
            INSERT INTO truck_assignments
                (truck_id, route_id, destination_hub, planned_arrival,
                 cargo_value_chf, priority)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            assignment_rows,
        )
        connection.commit()

    print(
        f"Seeded {DB_PATH} with {len(seed_stage3.HUBS)} hubs, "
        f"{len(seed_stage3.ROUTES)} routes, "
        f"{len(telemetry_rows)} telemetry rows, "
        f"{len(assignment_rows)} assignments."
    )


if __name__ == "__main__":
    init_db()
