"""Database-backed graph-definition loader (SQLite, stdlib-only).

Stores workflow definitions as YAML/JSON text with per-source version
tracking, so workflows can be managed at runtime without file deployments.
The DB holds the *topology* only — node functions still come from the
registry.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import yaml

from langgraph_declarative.errors import ConfigLoadError

_SCHEMA = """
CREATE TABLE IF NOT EXISTS graph_definitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    definition TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (source_id, version)
)
"""


class SQLiteLoader:
    """``Loader`` implementation reading graph definitions from SQLite.

    Source syntax: ``"my_workflow"`` loads the latest version,
    ``"my_workflow@2"`` loads version 2 explicitly.
    """

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)
        with self._connect() as conn:
            conn.execute(_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def save(self, source_id: str, definition: dict | str) -> int:
        """Store a definition (dict or YAML/JSON text). Returns the new version."""
        text = (
            yaml.safe_dump(definition, sort_keys=False)
            if isinstance(definition, dict)
            else definition
        )
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(MAX(version), 0) FROM graph_definitions "
                "WHERE source_id = ?",
                (source_id,),
            ).fetchone()
            version = row[0] + 1
            conn.execute(
                "INSERT INTO graph_definitions (source_id, version, definition) "
                "VALUES (?, ?, ?)",
                (source_id, version, text),
            )
        return version

    def versions(self, source_id: str) -> list[int]:
        """Return all stored versions for a source, ascending."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT version FROM graph_definitions WHERE source_id = ? "
                "ORDER BY version",
                (source_id,),
            ).fetchall()
        return [r[0] for r in rows]

    def load(self, source: str) -> dict:
        """Load a definition by ``source_id`` or ``source_id@version``."""
        source_id, _, version_str = source.partition("@")
        if version_str:
            try:
                version = int(version_str)
            except ValueError:
                raise ConfigLoadError(
                    f"Invalid version '{version_str}' in source '{source}' — "
                    "expected an integer (e.g. 'my_workflow@2')"
                ) from None
            query = (
                "SELECT definition FROM graph_definitions "
                "WHERE source_id = ? AND version = ?"
            )
            params: tuple = (source_id, version)
        else:
            query = (
                "SELECT definition FROM graph_definitions WHERE source_id = ? "
                "ORDER BY version DESC LIMIT 1"
            )
            params = (source_id,)

        with self._connect() as conn:
            row = conn.execute(query, params).fetchone()
        if row is None:
            raise ConfigLoadError(
                f"Graph definition '{source}' not found in database {self.db_path}"
            )

        try:
            data = yaml.safe_load(row[0])  # YAML superset also parses JSON
        except yaml.YAMLError as exc:
            raise ConfigLoadError(
                f"Invalid YAML/JSON in stored definition '{source}': {exc}"
            ) from None
        if not isinstance(data, dict):
            raise ConfigLoadError(
                f"Stored definition '{source}' is not a mapping, "
                f"got {type(data).__name__}"
            )
        return data


def build_graph_from_db(
    source_id: str,
    registry: "Registry",  # noqa: F821
    db_path: str | Path,
    state_class: type | None = None,
):
    """One-line graph compilation from a database-stored definition.

    Args:
        source_id: Definition key, optionally versioned (``"flow@2"``).
        registry: Registry containing the node/router functions.
        db_path: Path to the SQLite database file.
        state_class: State annotation override (YAML ``state:`` still wins).
    """
    from langgraph_declarative.builder import GraphBuilder
    from langgraph_declarative.schema import validate_config

    raw = SQLiteLoader(db_path).load(source_id)
    config = validate_config(raw)
    builder = GraphBuilder(registry=registry, state_class=state_class)
    return builder.build(config)
