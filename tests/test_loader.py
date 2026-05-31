"""Tests for the Loader module."""

from pathlib import Path

import pytest

from langgraph_declarative.errors import ConfigLoadError
from langgraph_declarative.loader import load_yaml

FIXTURES = Path(__file__).parent / "fixtures"


class TestLoadYaml:
    def test_loads_valid_yaml(self):
        data = load_yaml(FIXTURES / "simple.yaml")
        assert isinstance(data, dict)
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) == 2

    def test_accepts_str_path(self):
        data = load_yaml(str(FIXTURES / "simple.yaml"))
        assert isinstance(data, dict)

    def test_missing_file_raises(self):
        with pytest.raises(ConfigLoadError, match="not found"):
            load_yaml(FIXTURES / "nonexistent.yaml")

    def test_malformed_yaml_raises(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text(":\n  - :\n  bad: [unterminated", encoding="utf-8")
        with pytest.raises(ConfigLoadError, match="Invalid YAML"):
            load_yaml(bad)

    def test_non_dict_yaml_raises(self, tmp_path):
        scalar = tmp_path / "scalar.yaml"
        scalar.write_text("just a string", encoding="utf-8")
        with pytest.raises(ConfigLoadError, match="Expected a YAML mapping"):
            load_yaml(scalar)

    def test_list_yaml_raises(self, tmp_path):
        lst = tmp_path / "list.yaml"
        lst.write_text("- item1\n- item2\n", encoding="utf-8")
        with pytest.raises(ConfigLoadError, match="Expected a YAML mapping"):
            load_yaml(lst)
