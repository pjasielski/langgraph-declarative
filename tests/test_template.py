"""Tests for the LangGraph template packaging (task-022)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml

from langgraph_declarative import build_graph

TEMPLATE = Path(__file__).parent.parent / "template"


class TestTemplateStructure:
    def test_required_files_present(self):
        for rel in (
            "langgraph.json",
            "pyproject.toml",
            "README.md",
            "src/agent/workflow.yaml",
            "src/agent/nodes.py",
            "src/agent/graph.py",
        ):
            assert (TEMPLATE / rel).exists(), f"missing template file: {rel}"

    def test_langgraph_json_points_at_graph(self):
        config = json.loads((TEMPLATE / "langgraph.json").read_text(encoding="utf-8"))
        assert config["graphs"]["agent"] == "./src/agent/graph.py:graph"

    def test_workflow_yaml_is_valid_config(self):
        from langgraph_declarative.schema import validate_config

        raw = yaml.safe_load(
            (TEMPLATE / "src/agent/workflow.yaml").read_text(encoding="utf-8")
        )
        config = validate_config(raw)
        assert len(config.nodes) == 3


class TestTemplateRuns:
    def _load_nodes_module(self):
        spec = importlib.util.spec_from_file_location(
            "template_nodes", TEMPLATE / "src/agent/nodes.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules["template_nodes"] = module
        spec.loader.exec_module(module)
        return module

    def test_scaffolded_workflow_builds_and_runs(self):
        nodes = self._load_nodes_module()
        graph = build_graph(TEMPLATE / "src/agent/workflow.yaml", nodes.registry)
        result = graph.invoke({"messages": [{"role": "user", "content": "Hello!"}]})
        contents = [m.content for m in result["messages"]]
        assert contents[-1] == "Done."
        assert len(contents) == 4  # user + 3 nodes
