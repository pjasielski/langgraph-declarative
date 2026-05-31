"""YAML file loader — thin wrapper around PyYAML."""

from __future__ import annotations

from pathlib import Path

import yaml

from langgraph_declarative.errors import ConfigLoadError


def load_yaml(path: str | Path) -> dict:
    """Load and parse a YAML file into a Python dict.

    Raises ``ConfigLoadError`` if the file is missing or contains invalid YAML.
    The returned dict is **not** validated against the graph schema — that is
    the job of :func:`langgraph_declarative.schema.validate_config`.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ConfigLoadError(f"Config file not found: {path}") from None
    except OSError as exc:
        raise ConfigLoadError(f"Cannot read config file {path}: {exc}") from None

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ConfigLoadError(f"Invalid YAML in {path}: {exc}") from None

    if not isinstance(data, dict):
        raise ConfigLoadError(
            f"Expected a YAML mapping at top level in {path}, got {type(data).__name__}"
        )
    return data
