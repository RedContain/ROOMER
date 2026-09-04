"""
ROOMER — SQLite database schema.

Creates the database structure described in the draw.io ER diagram.
No third-party dependencies are required.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Union


PathLike = Union[str, Path]


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS object_group (
    group_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    code         TEXT NOT NULL UNIQUE,
    description  TEXT,
    icon         TEXT,
    sort_order   INTEGER NOT NULL DEFAULT 0,
    is_system    INTEGER NOT NULL DEFAULT 0 CHECK (is_system IN (0, 1)),
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted   INTEGER NOT NULL DEFAULT 0 CHECK (is_deleted IN (0, 1))
);

CREATE TABLE IF NOT EXISTS attribute_type (
    type_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    code         TEXT NOT NULL UNIQUE,
    description  TEXT,
    is_system    INTEGER NOT NULL DEFAULT 0 CHECK (is_system IN (0, 1))
);

CREATE TABLE IF NOT EXISTS attribute (
    attribute_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id     INTEGER NOT NULL,
    type_id      INTEGER NOT NULL,
    name         TEXT NOT NULL,
    code         TEXT NOT NULL UNIQUE,
    description  TEXT,
    is_required  INTEGER NOT NULL DEFAULT 0 CHECK (is_required IN (0, 1)),
    is_unique    INTEGER NOT NULL DEFAULT 0 CHECK (is_unique IN (0, 1)),
    default_value TEXT,
    sort_order   INTEGER NOT NULL DEFAULT 0,
    is_system    INTEGER NOT NULL DEFAULT 0 CHECK (is_system IN (0, 1)),
    is_deleted   INTEGER NOT NULL DEFAULT 0 CHECK (is_deleted IN (0, 1)),

    FOREIGN KEY (group_id) REFERENCES object_group(group_id),
    FOREIGN KEY (type_id) REFERENCES attribute_type(type_id)
);

CREATE TABLE IF NOT EXISTS status (
    status_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    code         TEXT NOT NULL UNIQUE,
    color        TEXT,
    sort_order   INTEGER NOT NULL DEFAULT 0,
    is_system    INTEGER NOT NULL DEFAULT 0 CHECK (is_system IN (0, 1))
);

CREATE TABLE IF NOT EXISTS users (
    users_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    username     TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name    TEXT NOT NULL,
    role         TEXT NOT NULL,
    is_active    INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS object (
    object_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id     INTEGER NOT NULL,
    name         TEXT NOT NULL,
    code         TEXT NOT NULL UNIQUE,
    description  TEXT,
    status_id    INTEGER,
    created_by   INTEGER,
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted   INTEGER NOT NULL DEFAULT 0 CHECK (is_deleted IN (0, 1)),

    FOREIGN KEY (group_id) REFERENCES object_group(group_id),
    FOREIGN KEY (status_id) REFERENCES status(status_id),
    FOREIGN KEY (created_by) REFERENCES users(users_id)
);

CREATE TABLE IF NOT EXISTS object_value (
    value_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id     INTEGER NOT NULL,
    attribute_id  INTEGER NOT NULL,

    value_string  TEXT,
    value_real    REAL,
    value_boolean INTEGER CHECK (value_boolean IS NULL OR value_boolean IN (0, 1)),
    value_date    TEXT,
    value_text    TEXT,
    value_json    TEXT,
    value_blob    BLOB,
    value_integer INTEGER,

    FOREIGN KEY (object_id) REFERENCES object(object_id) ON DELETE CASCADE,
    FOREIGN KEY (attribute_id) REFERENCES attribute(attribute_id) ON DELETE CASCADE,

    UNIQUE (object_id, attribute_id)
);

CREATE INDEX IF NOT EXISTS idx_attribute_group
    ON attribute(group_id);

CREATE INDEX IF NOT EXISTS idx_attribute_type
    ON attribute(type_id);

CREATE INDEX IF NOT EXISTS idx_object_group
    ON object(group_id);

CREATE INDEX IF NOT EXISTS idx_object_status
    ON object(status_id);

CREATE INDEX IF NOT EXISTS idx_object_created_by
    ON object(created_by);

CREATE INDEX IF NOT EXISTS idx_object_value_object
    ON object_value(object_id);

CREATE INDEX IF NOT EXISTS idx_object_value_attribute
    ON object_value(attribute_id);
"""


def connect(db_path: PathLike = "roomer.db") -> sqlite3.Connection:
    """Open SQLite database with foreign-key enforcement enabled."""
    connection = sqlite3.connect(str(db_path))
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: PathLike = "roomer.db") -> None:
    """Create all ROOMER tables and indexes if they do not exist."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with connect(db_path) as connection:
        connection.executescript(SCHEMA)


def create_database(db_path: PathLike = "roomer.db") -> sqlite3.Connection:
    """
    Create/initialize the database and return an open connection.

    The caller is responsible for closing the returned connection.
    """
    initialize_database(db_path)
    return connect(db_path)


if __name__ == "__main__":
    path = Path("roomer.db")
    initialize_database(path)
    print(f"Database initialized: {path.resolve()}")
