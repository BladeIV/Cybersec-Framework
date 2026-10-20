"""Tests for the catalog loader, models and triage workspace."""
from pathlib import Path

import pytest

from netguardian.loader import CatalogError, load_catalog
from netguardian.models import CSF_FUNCTIONS, VALID_TEAMS
from netguardian.triage import Case


def test_catalog_loads_all_functions():
    catalog = load_catalog()
    codes = [fn.code for fn in catalog.functions]
    # Every function present and in canonical order.
    assert codes == [c for c in CSF_FUNCTIONS if c in codes]
    assert set(codes) == set(CSF_FUNCTIONS)


def test_every_tool_is_valid():
    catalog = load_catalog()
    tools = list(catalog.iter_tools())
    assert len(tools) >= 40
    for tool in tools:
        assert tool.name and tool.url.startswith("http")
        assert tool.description
        assert set(tool.teams) <= VALID_TEAMS and tool.teams
        assert tool.license and tool.cost
        assert tool.function in CSF_FUNCTIONS


def test_team_filter():
    catalog = load_catalog()
    red = catalog.filter(team="red")
    assert all("red" in t.teams for t in red.iter_tools())
    assert list(red.iter_tools()), "expected some red-team tools"


def test_search_filter():
    catalog = load_catalog()
    hits = [t.name for t in catalog.filter(query="nmap").iter_tools()]
    assert "Nmap" in hits


def test_free_only_filter():
    catalog = load_catalog()
    free = catalog.filter(free_only=True)
    assert all(t.cost == "free" for t in free.iter_tools())


def test_empty_functions_dropped():
    catalog = load_catalog()
    narrow = catalog.filter(query="this-string-matches-nothing-xyz")
    assert list(narrow.iter_tools()) == []
    assert narrow.functions == []


def test_bad_team_rejected(tmp_path: Path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "function: ID\nname: Identify\ncategories:\n"
        "  - name: X\n    tools:\n"
        "      - name: T\n        url: http://x\n        description: d\n"
        "        teams: [purple]\n        license: MIT\n        cost: free\n"
    )
    with pytest.raises(CatalogError):
        load_catalog(tmp_path)


def test_case_checklist_and_markdown():
    case = Case.new("Test incident", "incident")
    done, total = case.progress
    assert done == 0 and total > 0
    case.checklist[0].done = True
    case.add_note("Isolated host web01")
    md = case.to_markdown()
    assert "# Test incident" in md
    assert "[x]" in md and "Isolated host web01" in md


def test_case_roundtrip(tmp_path: Path):
    case = Case.new("Engagement A", "pentest")
    case.add_note("ROE signed")
    path = case.save(tmp_path)
    loaded = Case.load(path)
    assert loaded.name == case.name
    assert loaded.kind == "pentest"
    assert loaded.notes[0].text == "ROE signed"


def test_unknown_case_kind():
    with pytest.raises(ValueError):
        Case.new("x", "nonsense")
