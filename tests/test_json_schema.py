"""Tests for JSON Schema export (task-016)."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest
import yaml

from langgraph_declarative import export_json_schema

FIXTURES = Path(__file__).parent / "fixtures"
REPO_ROOT = Path(__file__).parent.parent

GOOD_FIXTURES = [
    "simple.yaml",
    "conditional.yaml",
    "fan_out.yaml",
    "full_featured.yaml",
    "state_declaration.yaml",
    "match_routing.yaml",
    "llm_workflow.yaml",
]


class TestExportJsonSchema:
    def test_returns_dict_with_metadata(self):
        schema = export_json_schema()
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert "nodes" in schema["properties"]
        assert "edges" in schema["properties"]

    def test_covers_v11_state_section(self):
        schema = export_json_schema()
        assert "state" in schema["properties"]
        defs = schema.get("$defs", {})
        assert "StateFieldConfig" in defs
        assert set(defs["StateFieldConfig"]["properties"]) >= {
            "name",
            "type",
            "default",
            "reducer",
        }

    def test_writes_to_file(self, tmp_path):
        out = tmp_path / "workflow.schema.json"
        schema = export_json_schema(output_path=out)
        assert json.loads(out.read_text(encoding="utf-8")) == schema

    @pytest.mark.parametrize("fixture", GOOD_FIXTURES)
    def test_validates_known_good_fixtures(self, fixture):
        schema = export_json_schema()
        data = yaml.safe_load((FIXTURES / fixture).read_text(encoding="utf-8"))
        jsonschema.validate(data, schema)  # raises on failure

    def test_rejects_known_bad_yaml(self):
        schema = export_json_schema()
        bad = {"nodes": "not-a-list", "edges": []}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(bad, schema)

    def test_rejects_missing_nodes(self):
        schema = export_json_schema()
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate({"edges": []}, schema)

    def test_committed_artifact_is_current(self):
        """schema/workflow.schema.json must match the generated schema."""
        artifact = REPO_ROOT / "schema" / "workflow.schema.json"
        assert artifact.exists(), "run export_json_schema('schema/workflow.schema.json')"
        committed = json.loads(artifact.read_text(encoding="utf-8"))
        assert committed == export_json_schema()
